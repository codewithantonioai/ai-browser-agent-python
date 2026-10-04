# Lesson 5 · The agent loop

▶ [Watch this lesson](https://youtu.be/1HuYr6E_nsM?t=600) (starts at 10:00)

## Goal

Lesson five. The agent loop.

## Commands and files (as shown in the video)

### `agent.py` · code tools

```python
import json

from openai import OpenAI

from browser import Browser

MODEL = "gpt-6-luna"
MAX_STEPS = 25
PRICE_IN, PRICE_OUT = 0.10, 0.50  # dollars per million tokens
client = OpenAI()

INSTRUCTIONS = (
    "You are webpilot, an agent that uses a real web browser. "
    "After each action you get the page as an accessibility snapshot: "
    'each line is a role and a name, like: link "Travel". '
    "Use them to click or type. "
    "When the task is done, answer in plain text, no Markdown."
)


def tool(name, description, /, **params):
    return {
        "type": "function",
        "name": name,
        "description": description,
        "strict": True,
        "parameters": {
            "type": "object",
            "properties": {k: {"type": "string", "description": v}
                           for k, v in params.items()},
            "required": list(params),
            "additionalProperties": False,
        },
    }


TOOLS = [
    tool("go_to", "Open a URL in the browser.", url="The full URL"),
    tool("click", "Click an element from the snapshot.",
         role="Its role, like link, button or checkbox", name="Its exact name"),
    tool("type_text", "Type into a text field.",
         label="The field's label", text="What to type"),
    tool("choose", "Pick an option in a dropdown.",
         label="The dropdown's label", option="The option's text"),
]


def run_agent(task, browser):
    actions = {"go_to": browser.go_to, "click": browser.click,
               "type_text": browser.type_text, "choose": browser.choose}
    messages = [{"role": "user", "content": task}]
    tokens_in = tokens_out = 0
    for step in range(1, MAX_STEPS + 1):
        response = client.responses.create(
            model=MODEL,
            instructions=INSTRUCTIONS,
            tools=TOOLS,
            input=messages,
        )
        tokens_in += response.usage.input_tokens
        tokens_out += response.usage.output_tokens
        messages += response.output
        calls = [item for item in response.output if item.type == "function_call"]
        if not calls:
            cost = (tokens_in * PRICE_IN + tokens_out * PRICE_OUT) / 1_000_000
            print(f"\033[2m({step} steps · {tokens_in:,} tokens in · "
                  f"{tokens_out:,} out · ${cost:.4f})\033[0m")
            return response.output_text
        for call in calls:
            args = json.loads(call.arguments)
            print(f"\033[36m● {call.name}\033[0m", " · ".join(args.values()))
            try:
                result = actions[call.name](**args)
            except Exception as error:
                result = f"Error: {str(error).splitlines()[0]}"
            messages.append({"type": "function_call_output",
                             "call_id": call.call_id, "output": result})
    return "I stopped: too many steps."


def main():
    print(f"webpilot · {MODEL}")
    task = input("Task: ")
    browser = Browser()
    try:
        print(run_agent(task, browser))
    finally:
        browser.close()


if __name__ == "__main__":
    main()
```

### `agent.py` · code instructions

```python
import json

from openai import OpenAI

from browser import Browser

MODEL = "gpt-6-luna"
MAX_STEPS = 25
PRICE_IN, PRICE_OUT = 0.10, 0.50  # dollars per million tokens
client = OpenAI()

INSTRUCTIONS = (
    "You are webpilot, an agent that uses a real web browser. "
    "After each action you get the page as an accessibility snapshot: "
    'each line is a role and a name, like: link "Travel". '
    "Use them to click or type. "
    "When the task is done, answer in plain text, no Markdown."
)


def tool(name, description, /, **params):
    return {
        "type": "function",
        "name": name,
        "description": description,
        "strict": True,
        "parameters": {
            "type": "object",
            "properties": {k: {"type": "string", "description": v}
                           for k, v in params.items()},
            "required": list(params),
            "additionalProperties": False,
        },
    }


TOOLS = [
    tool("go_to", "Open a URL in the browser.", url="The full URL"),
    tool("click", "Click an element from the snapshot.",
         role="Its role, like link, button or checkbox", name="Its exact name"),
    tool("type_text", "Type into a text field.",
         label="The field's label", text="What to type"),
    tool("choose", "Pick an option in a dropdown.",
         label="The dropdown's label", option="The option's text"),
]


def run_agent(task, browser):
    actions = {"go_to": browser.go_to, "click": browser.click,
               "type_text": browser.type_text, "choose": browser.choose}
    messages = [{"role": "user", "content": task}]
    tokens_in = tokens_out = 0
    for step in range(1, MAX_STEPS + 1):
        response = client.responses.create(
            model=MODEL,
            instructions=INSTRUCTIONS,
            tools=TOOLS,
            input=messages,
        )
        tokens_in += response.usage.input_tokens
        tokens_out += response.usage.output_tokens
        messages += response.output
        calls = [item for item in response.output if item.type == "function_call"]
        if not calls:
            cost = (tokens_in * PRICE_IN + tokens_out * PRICE_OUT) / 1_000_000
            print(f"\033[2m({step} steps · {tokens_in:,} tokens in · "
                  f"{tokens_out:,} out · ${cost:.4f})\033[0m")
            return response.output_text
        for call in calls:
            args = json.loads(call.arguments)
            print(f"\033[36m● {call.name}\033[0m", " · ".join(args.values()))
            try:
                result = actions[call.name](**args)
            except Exception as error:
                result = f"Error: {str(error).splitlines()[0]}"
            messages.append({"type": "function_call_output",
                             "call_id": call.call_id, "output": result})
    return "I stopped: too many steps."


def main():
    print(f"webpilot · {MODEL}")
    task = input("Task: ")
    browser = Browser()
    try:
        print(run_agent(task, browser))
    finally:
        browser.close()


if __name__ == "__main__":
    main()
```

### `agent.py` · code run agent

```python
import json

from openai import OpenAI

from browser import Browser

MODEL = "gpt-6-luna"
MAX_STEPS = 25
PRICE_IN, PRICE_OUT = 0.10, 0.50  # dollars per million tokens
client = OpenAI()

INSTRUCTIONS = (
    "You are webpilot, an agent that uses a real web browser. "
    "After each action you get the page as an accessibility snapshot: "
    'each line is a role and a name, like: link "Travel". '
    "Use them to click or type. "
    "When the task is done, answer in plain text, no Markdown."
)


def tool(name, description, /, **params):
    return {
        "type": "function",
        "name": name,
        "description": description,
        "strict": True,
        "parameters": {
            "type": "object",
            "properties": {k: {"type": "string", "description": v}
                           for k, v in params.items()},
            "required": list(params),
            "additionalProperties": False,
        },
    }


TOOLS = [
    tool("go_to", "Open a URL in the browser.", url="The full URL"),
    tool("click", "Click an element from the snapshot.",
         role="Its role, like link, button or checkbox", name="Its exact name"),
    tool("type_text", "Type into a text field.",
         label="The field's label", text="What to type"),
    tool("choose", "Pick an option in a dropdown.",
         label="The dropdown's label", option="The option's text"),
]


def run_agent(task, browser):
    actions = {"go_to": browser.go_to, "click": browser.click,
               "type_text": browser.type_text, "choose": browser.choose}
    messages = [{"role": "user", "content": task}]
    tokens_in = tokens_out = 0
    for step in range(1, MAX_STEPS + 1):
        response = client.responses.create(
            model=MODEL,
            instructions=INSTRUCTIONS,
            tools=TOOLS,
            input=messages,
        )
        tokens_in += response.usage.input_tokens
        tokens_out += response.usage.output_tokens
        messages += response.output
        calls = [item for item in response.output if item.type == "function_call"]
        if not calls:
            cost = (tokens_in * PRICE_IN + tokens_out * PRICE_OUT) / 1_000_000
            print(f"\033[2m({step} steps · {tokens_in:,} tokens in · "
                  f"{tokens_out:,} out · ${cost:.4f})\033[0m")
            return response.output_text
        for call in calls:
            args = json.loads(call.arguments)
            print(f"\033[36m● {call.name}\033[0m", " · ".join(args.values()))
            try:
                result = actions[call.name](**args)
            except Exception as error:
                result = f"Error: {str(error).splitlines()[0]}"
            messages.append({"type": "function_call_output",
                             "call_id": call.call_id, "output": result})
    return "I stopped: too many steps."


def main():
    print(f"webpilot · {MODEL}")
    task = input("Task: ")
    browser = Browser()
    try:
        print(run_agent(task, browser))
    finally:
        browser.close()


if __name__ == "__main__":
    main()
```

### Terminal · term run

```bash
uv run --env-file .env agent.py
```

## Recap

So: the tools are JSON schemas, the loop runs until the model answers in plain text, and a real task costs less than a cent. Now, something riskier: forms.
