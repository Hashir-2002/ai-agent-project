from llm.client import llm_response
from tools.calculator import calculator
from tools.web_search import web_search
from tools.notes import store_notes, get_notes
from agent.memory import add_memory


def run_agent(user_input: str):

    add_memory(user_input)

    response = llm_response(user_input)

    action = response.get("action", "final")
    tool_input = response.get("input", "")

    # 🔒 FORCE CLEAN STRING OUTPUT
    if isinstance(tool_input, dict):
        # flatten broken LLM output
        if "story" in tool_input:
            tool_input = tool_input["story"]
        else:
            tool_input = str(tool_input)

    if action == "calculator":
        result = calculator(tool_input)
        return f"🧮 Result: {result}"

    elif action == "web_search":
        result = web_search(tool_input)
        return f"🌐 Search Results:\n\n{result}"

    elif action == "save_note":
        store_notes(tool_input)
        return "📝 Note saved successfully."

    elif action == "get_notes":
        return f"📒 Notes:\n{get_notes()}"

    elif action == "final":
        return tool_input if isinstance(tool_input, str) else str(tool_input)

    else:
        return "⚠️ I couldn't understand your request."