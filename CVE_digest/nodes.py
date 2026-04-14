from dotenv import load_dotenv
load_dotenv()

from langgraph.graph import MessagesState
from langgraph.prebuilt import ToolNode
from react import llm, tools

SYSTEM_MESSAGE = """
You are a cybersecurity threat-intelligence assistant.
Given a CVE ID, search the web and retrieve as much relevant information as possible from reliable sources.
Your primary objective is to extract detailed threat-action knowledge needed for threat-model construction. Focus on how the vulnerability is exploited, what the attacker must do, what preconditions are required, what components or interfaces are manipulated, what sequence of operations is involved, and what effect each action produces.
Threat actions must be described as concrete attacker operations, not generic summaries. Extract operational knowledge that can later be mapped into a formal threat model or attack trace.
Be explicit about what is directly supported by retrieved sources and what is inferred from available evidence. Do not invent unsupported exploit details. If exploitation details are incomplete, say so clearly.
Return the final answer in the following format:
CVE:
Affected Product / Component:
Vulnerability Type:
Attack Surface:
Attacker Prerequisites:
Required Capabilities:
Exploitation Procedure:
Detailed Threat Actions:
Targeted Assets / States:
Security Impact:
Protocol-Relevant Threat Interpretation:
Evidence Strength / Notes:
"""

def run_agent_reasoning(state: MessagesState) -> MessagesState:
    """
    Run the agent reasoning node.
    """
    response = llm.invoke(
        [{"role": "system", "content": SYSTEM_MESSAGE}, *state["messages"]]
    )
    return {"messages": [response]}

tool_node = ToolNode(tools)