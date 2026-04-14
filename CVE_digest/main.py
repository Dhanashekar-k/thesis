from dotenv import load_dotenv
load_dotenv()

from langchain_core.messages import HumanMessage
from langgraph.constants import START
from langgraph.graph import MessagesState, StateGraph, END

from nodes import tool_node, run_agent_reasoning

AGENT_REASON = "agent_reason"
ACT = "act"

def should_continue(state: MessagesState) -> str:
    last_message = state["messages"][-1]
    if getattr(last_message, "tool_calls", None):
        return ACT
    return END

flow = StateGraph(MessagesState)

flow.add_node(AGENT_REASON, run_agent_reasoning)
flow.add_node(ACT, tool_node)

flow.add_edge(START, AGENT_REASON)
flow.add_conditional_edges(
    AGENT_REASON,
    should_continue,
    {
        ACT: ACT,
        END: END,
    },
)
flow.add_edge(ACT, AGENT_REASON)

app = flow.compile()

if __name__ == "__main__":
    cve_id = "CVE-2025-12357"
    print(f"-------------------{cve_id}-------------------------")
    query = f"""
    Given the CVE ID {cve_id}, search the web for relevant sources and retrieve as much information as possible.
    Focus on detailed threat actions needed to exploit the vulnerability, including attacker steps, required conditions, manipulated components or interfaces, and resulting effects.
    Return a structured analysis suitable for threat-model construction.
    """
    res = app.invoke(
        {"messages": [HumanMessage(content=query)]},
        config={"recursion_limit": 10},
    )
    final_message = res["messages"][-1]
    print(final_message.content)