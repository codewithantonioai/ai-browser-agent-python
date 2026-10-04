# Build an AI Browser Agent in Python (Automate the Web)

Companion repository for the **Code with Antonio** video course · [Watch on YouTube](https://youtu.be/1HuYr6E_nsM).

Build an AI browser agent in Python from scratch: Playwright drives a real Chromium, an OpenAI model decides, and it asks you before pressing any button.

## What you'll build

webpilot: a ~150-line terminal agent that drives Chromium with Playwright, reads each page as an aria snapshot and acts through four tools chosen by gpt-6-luna; it finds the cheapest mystery book on a scraping sandbox, fills a local sign-up form asking before it clicks the button, and stays safe against prompt injection and off-limits sites.

## Lessons

| # | Lesson | Video | Folder |
|---|---|---|---|
| 1 | What is a browser agent? | [0:00](https://youtu.be/1HuYr6E_nsM?t=0) | [lessons/01-what-is-a-browser-agent](lessons/01-what-is-a-browser-agent) |
| 2 | Playwright in five minutes | [2:49](https://youtu.be/1HuYr6E_nsM?t=169) | [lessons/02-playwright-in-five-minutes](lessons/02-playwright-in-five-minutes) |
| 3 | The agent's eyes | [5:26](https://youtu.be/1HuYr6E_nsM?t=326) | [lessons/03-the-agent-s-eyes](lessons/03-the-agent-s-eyes) |
| 4 | The agent's hands | [7:47](https://youtu.be/1HuYr6E_nsM?t=467) | [lessons/04-the-agent-s-hands](lessons/04-the-agent-s-hands) |
| 5 | The agent loop | [10:00](https://youtu.be/1HuYr6E_nsM?t=600) | [lessons/05-the-agent-loop](lessons/05-the-agent-loop) |
| 6 | Fill forms, ask first | [13:49](https://youtu.be/1HuYr6E_nsM?t=829) | [lessons/06-fill-forms-ask-first](lessons/06-fill-forms-ask-first) |
| 7 | Stay safe and know the limits | [16:30](https://youtu.be/1HuYr6E_nsM?t=990) | [lessons/07-stay-safe-and-know-the-limits](lessons/07-stay-safe-and-know-the-limits) |

## Requirements

- Playwright for Python 1.63.0 · Chromium headless · openai 3.24.0 (Responses API) · gpt-6-luna · uv 0.12.14 · Python 3.12 · Ubuntu (Linux), headless server
- Python 3.12+ and [uv](https://docs.astral.sh/uv/)

## Run the final project

```bash
cd app
uv sync
uv run playwright install chromium
cp .env.example .env    # then put your OpenAI API key in .env
uv run python -m http.server 8077 --bind 127.0.0.1 --directory site    # second terminal: the local demo pages
uv run --env-file .env agent.py    # type a task, e.g. find the cheapest Mystery book on https://books.toscrape.com
uv run cheapest.py    # the same task without AI
```

## Repository structure

```
README.md          this file
lessons/           one folder per lesson: goal, timestamp, commands and files exactly as in the video
app/               the final working project
assets/            thumbnail
```

## License

MIT — use it for anything, credit appreciated.

---
Generated on 2026-10-04 from the course scripts. Code with Antonio · AI tutor.