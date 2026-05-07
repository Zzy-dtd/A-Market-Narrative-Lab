# Market Narrative Lab

Market Narrative Lab is an early demo for a conversational market-thinking simulator.

The core idea is simple:

> Learn how different investors think.

Instead of giving stock picks, trading signals, or buy/sell recommendations, the project explores how different types of market participants might reason about:

- individual stocks
- broad market conditions
- valuation debates
- investor behavior
- online market narratives
- crowd psychology
- speculative episodes
- trading structure

The current demo includes three experimental personas:

- Long-Term Value Allocator
- Market Structure Trader
- Behavioral Contrarian

## Current Status

This repository is only a working MVP demo.

The current version is useful for testing the product direction, but it is not the final product. The reasoning logic, prompt structure, response format, and frontend design all still need significant iteration.

In particular, the app still needs work on:

- making the conversation feel more natural
- improving the visual chat interface
- refining persona behavior and response quality
- improving roundtable discussion logic
- connecting external information sources such as news or market data APIs
- making the product experience less like a demo and more like a finished learning tool


## Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Environment Variables

Create a `.env` file if you want to use live OpenAI model output:

```bash
OPENAI_API_KEY=your_api_key_here
OPENAI_MODEL=gpt-5.2
```

If no API key is provided, the app runs in mock mode.
