# CLI Code Agent

A CLI coding assistant—similar in spirit to Claude, Cursor, and other AI dev tools—built in **Python** on top of the **Google Gemini** API.

You give it a natural-language task like:

> "Fix my calculator app, it's not starting correctly"

…and the agent will:

- Inspect files in a project
- Read code
- Run Python files
- Overwrite files with new code

All while staying inside a **defined working directory**.

---

## Tech Stack Used: 

- LLM: **Google Gemini** (`gemini-2.0-flash-001`)
- Tool calling support (Pre-defined python funtions):
  - List files and folders
  - Read file contents
  - Run Python files with args
  - Write/overwrite files
- Defined working directory: `WORKING_DIR`. Currently set to './calculator'. You can configure this in config.py
- Iterative **agent loop** with a configurable `MAX_ITERS`
- Comes with a small example project: a CLI **calculator app** for the agent to debug

---

## Architecture Overview

![flowchart](flowchart.png)

At a high level:

1. **`main.py`** reads your prompt from the command line.
2. It sends your prompt + a **system prompt** + a set of **tool declarations** to Gemini.
3. Gemini either:
   - Returns a **final text answer**, or  
   - Returns **function calls** (tool invocations), e.g. “read this file”, “run that script”.
4. The Python code executes those tools, feeds the results back to Gemini…
5. …and repeats until Gemini produces a final answer.

