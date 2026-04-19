# agent.py
import os
import json
from groq import Groq
from dotenv import load_dotenv
from tools import execute_tool, TOOLS

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

SYSTEM_PROMPT = """You are an expert Incident Response AI Agent.
When given an incident you must:
1. Call analyze_incident to find root cause
2. Call calculate_blast_radius to estimate user impact
3. Call get_remediation_steps to get fix steps
4. Give a clear final summary to the on-call engineer.
Always call all 3 tools before giving your final answer."""


def run_agent(incident_id: str, title: str, description: str, severity: str) -> dict:
    print(f"\n[Agent] Starting analysis for {incident_id}...")

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": f"""
Incident ID: {incident_id}
Title: {title}
Severity: {severity}
Description: {description}

Analyze this incident and provide root cause, blast radius, and remediation steps.
"""}
    ]

    try:
        max_iterations = 10  # safety limit
        iteration = 0

        while iteration < max_iterations:
            iteration += 1
            print(f"[Agent] Iteration {iteration}")

            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                max_tokens=1024,
                messages=messages,
                tools=TOOLS,
                tool_choice="auto"
            )

            choice = response.choices[0]
            print(f"[Agent] Stop reason: {choice.finish_reason}")

            # Claude wants to call tools
            if choice.finish_reason == "tool_calls":
                # add assistant message to history
                messages.append({
                    "role": "assistant",
                    "content": choice.message.content,
                    "tool_calls": [
                        {
                            "id": tc.id,
                            "type": "function",
                            "function": {
                                "name": tc.function.name,
                                "arguments": tc.function.arguments
                            }
                        }
                        for tc in choice.message.tool_calls
                    ]
                })

                # execute each tool
                for tool_call in choice.message.tool_calls:
                    tool_input = json.loads(tool_call.function.arguments)
                    name = tool_call.function.name

                    print(f"[Agent] Calling tool: {name} | args: {tool_input}")
                    result = execute_tool(name, tool_input)
                    print(f"[Agent] Tool result: {result}")

                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": str(result)
                    })

            # Final answer
            elif choice.finish_reason == "stop":
                final_text = choice.message.content
                print("[Agent] Final answer ready.")
                return {
                    "incident_id": incident_id,
                    "analysis": final_text
                }

            else:
                print(f"[Agent] Unknown stop reason: {choice.finish_reason}")
                break

        # If loop exceeded
        return {
            "incident_id": incident_id,
            "analysis": "Agent completed analysis. Please check logs for details."
        }

    except Exception as e:
        print(f"[Agent] ERROR: {type(e).__name__}: {str(e)}")
        raise e