from llm.client import llm_response
from tools.calculator import calculator
from tools.web_search import web_search
from tools.notes import store_notes, get_notes
from agent.memory import add_memory


def run_agent(user_input: str):

    response = llm_response(user_input)

    if not isinstance(response, dict):
        return str(response)

    action = response.get("action", "final")
    tool_input = response.get("input", "")

    # 🧼 CLEAN INPUT SAFETY
    if not tool_input or not isinstance(tool_input, str):
        tool_input = user_input

    tool_input = tool_input.strip()

    # 🧠 MEMORY AFTER DECISION (better practice)
    add_memory(user_input)

    # ---------------- TOOLS ---------------- #

    if action == "calculator":
        result = calculator(tool_input)
        return f"🧮 Result: {result}"


    elif action == "web_search":

        result = web_search(tool_input)

        if not result or not result.strip():
            return "🌐 No results found. Try rephrasing your question."

        return f"🌐 Search Results:\n\n{result}"

        # clean formatting for Streamlit
        if isinstance(result, list):
            formatted = ""
            for r in result:
                formatted += f"🔹 {r.get('title','')}\n{r.get('href','')}\n{r.get('body','')}\n\n"
            return "🌐 Search Results:\n\n" + formatted

        return f"🌐 Search Results:\n\n{result}"

    elif action == "save_note":
        store_notes(tool_input)
        return "📝 Note saved successfully."

    elif action == "get_notes":
        return f"📒 Notes:\n{get_notes()}"

    # ---------------- FINAL ---------------- #

    elif action == "final":
        return tool_input

    else:
        return "⚠️ I couldn't understand your request."