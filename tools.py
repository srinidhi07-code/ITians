# tools.py

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "analyze_incident",
            "description": "Analyze an incident description to identify root cause and category",
            "parameters": {
                "type": "object",
                "properties": {
                    "description": {"type": "string"},
                    "severity":    {"type": "string"}
                },
                "required": ["description", "severity"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_remediation_steps",
            "description": "Get remediation steps for a specific incident type",
            "parameters": {
                "type": "object",
                "properties": {
                    "incident_type": {"type": "string"}
                },
                "required": ["incident_type"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculate_blast_radius",
            "description": "Estimate how many users are affected",
            "parameters": {
                "type": "object",
                "properties": {
                    "severity":      {"type": "string"},
                    "incident_type": {"type": "string"}
                },
                "required": ["severity", "incident_type"]
            }
        }
    }
]


def execute_tool(tool_name: str, tool_input: dict) -> str:

    if tool_name == "analyze_incident":
        desc = tool_input["description"].lower()
        if any(w in desc for w in ["database", "db", "sql", "query", "connection pool"]):
            return "incident_type: database | likely_cause: Database overload or connection exhaustion"
        elif any(w in desc for w in ["ssh", "brute force", "unauthorized", "breach", "attack"]):
            return "incident_type: security | likely_cause: Unauthorized access attempt"
        elif any(w in desc for w in ["disk", "cpu", "memory", "ram", "server"]):
            return "incident_type: infrastructure | likely_cause: Resource exhaustion"
        elif any(w in desc for w in ["api", "timeout", "latency", "503", "500"]):
            return "incident_type: application | likely_cause: Application layer failure"
        else:
            return "incident_type: network | likely_cause: Network or connectivity issue"

    elif tool_name == "get_remediation_steps":
        runbooks = {
            "database": [
                "Check and increase connection pool size",
                "Identify and kill long-running queries",
                "Review recent deployments for slow queries",
                "Scale up database instance if needed",
                "Enable slow query logging"
            ],
            "security": [
                "Block attacking IPs at firewall immediately",
                "Rotate all potentially compromised credentials",
                "Enable MFA on all admin accounts",
                "Review access logs for successful breaches",
                "Notify security team and document timeline"
            ],
            "infrastructure": [
                "Free up disk space by removing old logs/archives",
                "Scale up instance or add more nodes",
                "Set up resource usage alerts at 80% threshold",
                "Review and optimize resource-heavy processes",
                "Schedule regular cleanup cron jobs"
            ],
            "application": [
                "Check recent deployments and roll back if needed",
                "Review error logs for stack traces",
                "Scale horizontally by adding more app instances",
                "Add circuit breakers to prevent cascade failures",
                "Increase timeout thresholds temporarily"
            ],
            "network": [
                "Check DNS resolution across regions",
                "Verify load balancer health check configs",
                "Review firewall and security group rules",
                "Test connectivity between services",
                "Check for network saturation or packet loss"
            ]
        }
        return str(runbooks.get(tool_input["incident_type"], ["Investigate and escalate to on-call engineer"]))

    elif tool_name == "calculate_blast_radius":
        matrix = {
            "critical": {"database": "100% users affected", "application": "80-100% users affected", "security": "All data potentially at risk", "infrastructure": "Full service down", "network": "All regions affected"},
            "high":     {"database": "50-80% users affected", "application": "30-60% users affected", "security": "Partial data exposure risk", "infrastructure": "Degraded performance", "network": "Single region affected"},
            "medium":   {"database": "10-30% users affected", "application": "5-15% users affected", "security": "Low exposure risk", "infrastructure": "Minor degradation", "network": "Subset of users affected"},
            "low":      {"database": "<5% users affected", "application": "<5% users affected", "security": "Minimal risk", "infrastructure": "No user impact", "network": "Negligible impact"},
        }
        sev = tool_input["severity"].lower()
        inc_type = tool_input["incident_type"].lower()
        return matrix.get(sev, {}).get(inc_type, "Impact unknown — investigate further")

    return "Tool not found"