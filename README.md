# Demo Agent — LinkedIn Job Search

[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![Fetch.ai](https://img.shields.io/badge/Fetch.ai-uAgents-000000)](https://fetch.ai/)

A Fetch.ai uAgent that searches LinkedIn job listings via RapidAPI and returns structured job results through the AI Engine protocol.

## Features

- **LinkedIn Job Search** — Queries LinkedIn's job search API for relevant listings
- **AI Engine Integration** — Works with Fetch.ai's DeltaV and AI Engine
- **Structured Responses** — Returns job title, company, location, and direct links
- **Customizable Queries** — Accepts any job description as search input

## How It Works

1. Receives a `JobRequest` with a job description via the uAgent protocol
2. Queries the LinkedIn Data API through RapidAPI
3. Parses and formats job listings with titles, companies, locations, and URLs
4. Returns formatted results via `UAgentResponse`

## Setup

```bash
pip install uagents requests pydantic
```

### Environment Variables

Set your RapidAPI key in the script or via environment variable:

```python
rapidapi_key = "your-rapidapi-key"
```

## Usage

```bash
python agent.py
```

The agent registers the `job_protocol` and listens for incoming job search requests from DeltaV or other uAgents.

## Example Query

> "Find software engineering jobs in the United States"

## Project Structure

```
demo-agent/
└── agent.py    # Main agent with LinkedIn job search protocol
```

## License

MIT
