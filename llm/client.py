import openai
import streamlit as st
import os
import json

api_key = None

# 1. Streamlit cloud
if hasattr(st, "secrets") and "GROQ_API_KEY" in st.secrets:
    api_key = st.secrets["GROQ_API_KEY"]

# 2. Local fallback
if not api_key:
    api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY not found in secrets or env variables")

client = openai.OpenAI(
    api_key=api_key,
    base_url="https://api.groq.com/openai/v1"
)
system_prompt = """
You are an AI agent.

You must return ONLY valid JSON.

Available actions:
- calculator
- web_search
- save_note
- get_notes
- final

────────────────────────

DECISION RULES:

1. calculator:
If input contains math symbols like + - * / ( )

2. web_search:
If user asks:
- who is ...
- what is ...
- when ...
- where ...
- why ...
- explain ...
- define ...
- any real-world factual question

3. save_note:
If user says to remember/store something

4. get_notes:
If user asks for saved notes
5. final → use this when NO tool is needed.

Use final for:
- greetings
- casual chat
- how-to explanations (like cooking, tutorials)
- storytelling
- general knowledge that does NOT require real-time facts

IMPORTANT RULES:
- If the question requires up-to-date or factual verification → use web_search
- If math → calculator
- If storing/retrieving info → use notes tools
- NEVER mix tool usage with final

────────────────────────

IMPORTANT:
- NEVER solve math yourself
- NEVER answer factual questions directly
- ALWAYS choose correct action

---------------------------------

RESPONSE QUALITY RULES:

FINAL OUTPUT RULE (CRITICAL):

- When action = final:
  - "input" MUST ALWAYS be a plain string
  - NEVER return JSON objects
  - NEVER return dictionaries
  - NEVER return nested structures
  - ONLY return human-readable text

If you return JSON in final → it is invalid.

Return format:
{
  "action": "...",
  "input": "..."
}
"""
def llm_response(user_input):
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input}
        ]
    )

    content = response.choices[0].message.content

    try:
        return json.loads(content)
    except:
        return {
            "thought": "parse error",
            "action": "final",
            "input": content
        }
