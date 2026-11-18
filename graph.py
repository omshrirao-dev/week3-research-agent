import os
import re
from dotenv import load_dotenv
from groq import Groq
from tools import web_search, read_url, write_report

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

SYSTEM_PROMPT = """You are a research agent. Follow these steps exactly:

Step 1: Use web_search to find information.
Step 2: Use read_url to read one important page in full.
Step 3: When told to write your report, write a complete markdown report.

To use a tool, output EXACTLY:
TOOL: web_search
INPUT: your search query

OR:
TOOL: read_url
INPUT: https://url-here.com

Do NOT write a report unless specifically asked to. Only output TOOL calls until asked.
"""

def parse_tool_call(text):
    tool_match = re.search(r'TOOL:\s*(web_search|read_url)', text)
    input_match = re.search(r'INPUT:\s*(.+?)(?:\n|$)', text, re.DOTALL)
    if tool_match and input_match:
        return tool_match.group(1).strip(), input_match.group(1).strip()
    return None, None

def call_llm(messages, max_tokens):
    response = client.chat.completions.create(
        model="qwen/qwen3.8-27b",
        messages=messages,
        max_tokens=max_tokens,
        temperature=0
    )
    return response.choices[0].message.content

def run_research(topic: str, callback=None) -> dict:
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": f"Research this topic: {topic}\n\nStart with a web search now."}
    ]

    for i in range(4):
        reply = call_llm(messages, max_tokens=250)
        messages.append({"role": "assistant", "content": reply})

        tool_name, tool_input = parse_tool_call(reply)

        if tool_name == "web_search":
            if callback: callback(f"🔎 Searching: {tool_input}")
            result = web_search.invoke({"query": tool_input})
            messages.append({
                "role": "user",
                "content": f"Search results:\n{result[:600]}"
            })

        elif tool_name == "read_url":
            if callback: callback(f"📄 Reading: {tool_input.strip()[:60]}...")
            result = read_url.invoke({"url": tool_input.strip()})
            messages.append({
                "role": "user",
                "content": f"Page content:\n{result[:500]}"
            })

        else:
            messages.append({
                "role": "user",
                "content": "Use a tool first. Search the web before writing the report."
            })

    if callback: callback("✍️ Writing final report...")
    messages.append({
        "role": "user",
        "content": (
            "You have gathered enough information. "
            "Now write a complete, well-structured markdown report on the topic. "
            "Include: Overview, Key Findings, Sources. "
            "Keep it concise — under 600 words. Do not use any tools."
        )
    })

    report = call_llm(messages, max_tokens=900)

    filename = re.sub(r'[^a-z0-9]+', '_', topic.lower())[:40]
    write_report.invoke({"filename": filename, "content": report})
    return {"topic": topic, "result": report}