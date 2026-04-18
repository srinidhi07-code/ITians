# agent.py
import os
from google import genai
from google.genai import types
from dotenv import load_dotenv
from tools import execute_tool

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

SYSTEM_PROMPT = """You are an expert Incident Response AI Agent.
When given an incident you must:
1. Call analyze_incident to find root cause
2. Call calculate_blast_radius to estimate user impact
3. Call get_remediation_steps to get fix steps
4. Give a clear final summary to the on-call engineer.
Always call all 3 tools before giving your final answer."""

gemini_tools = types.Tool(function_declarations=[
    types.FunctionDeclaration(
        name="analyze_incident",
        description="Analyze an incident description to identify root cause and category",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "description": types.Schema(type=types.Type.STRING),
                "severity":    types.Schema(type=types.Type.STRING),
            },
            required=["description", "severity"]
        )
    ),
    types.FunctionDeclaration(
        name="get_remediation_steps",
        description="Get remediation steps for a specific incident type",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "incident_type": types.Schema(type=types.Type.STRING),
            },
            required=["incident_type"]
        )
    ),
    types.FunctionDeclaration(
        name="calculate_blast_radius",
        description="Estimate how many users are affected based on severity and type",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "severity":      types.Schema(type=types.Type.STRING),
                "incident_type": types.Schema(type=types.Type.STRING),
            },
            required=["severity", "incident_type"]
        )
    ),
])


def run_agent(incident_id: str, title: str, description: str, severity: str) -> dict:
    print(f"\n[Agent] Starting analysis for {incident_id}...")

    user_message = f"""
Incident ID: {incident_id}
Title: {title}
Severity: {severity}
Description: {description}

Analyze this incident and provide root cause, blast radius, and remediation steps.
"""

    contents = [types.Content(role="user", parts=[types.Part(text=user_message)])]

    try:
        while True:
            response = client.models.generate_content(
               model="gemini-2.0-flash-lite",
                contents=contents,
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_PROMPT,
                    tools=[gemini_tools],
                )
            )

            print(f"[Agent] Response received")
            print(f"[Agent] Full response: {response}")

            contents.append(types.Content(
                role="model",
                parts=response.candidates[0].content.parts
            ))

            tool_calls_found = False

            for part in response.candidates[0].content.parts:
                if part.function_call:
                    tool_calls_found = True
                    name = part.function_call.name
                    args = dict(part.function_call.args)

                    print(f"[Agent] Calling tool: {name} | args: {args}")
                    result = execute_tool(name, args)
                    print(f"[Agent] Tool result: {result}")

                    contents.append(types.Content(
                        role="user",
                        parts=[types.Part(
                            function_response=types.FunctionResponse(
                                name=name,
                                response={"result": result}
                            )
                        )]
                    ))
                    break

            if not tool_calls_found:
                print("[Agent] Final answer ready.")
                return {
                    "incident_id": incident_id,
                    "analysis": response.text
                }

    except Exception as e:
        print(f"[Agent] ERROR: {type(e).__name__}: {str(e)}")
        raise e