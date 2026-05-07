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

You can optionally create a `.env` file if you want to provide a fallback OpenAI API key or model name:

```bash
OPENAI_API_KEY=your_api_key_here
OPENAI_MODEL=gpt-5.2
```

If no API key is provided, the app runs in mock mode.

## API Modes

The app currently supports two API modes.

**Mock mode** does not require an API key. It returns fixed demo responses so the interface and persona flow can be tested without calling a live model.

**Live OpenAI mode** requires an OpenAI API key. You can enter the key directly inside the app in the collapsed Settings section, or provide it through `.env` as an optional fallback. Keys entered in the app are stored only in the current Streamlit session and are not saved to disk.

**Web search** is optional. The model does not automatically browse the web. If web search is disabled, the model only uses the prompt, persona cards, user input, and its internal knowledge. Enable web search in Settings if you want the OpenAI Responses API to use the web search tool.

For market data such as prices, short interest, options chains, borrow fees, filings, or other structured financial data, separate financial data APIs are still needed. Those APIs are not connected in this demo yet.
