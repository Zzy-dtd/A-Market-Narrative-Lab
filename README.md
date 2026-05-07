# Market Narrative Lab

Market Narrative Lab is a Next.js prototype for a conversational market-thinking simulator.

The core idea:

> Learn how different investors think, not copy their trades.

The app lets a user ask open-ended market questions and hear how different market participant personas reason through the same narrative.

## What This Is

- A visual conversation interface for market reasoning
- A one-on-one chat with a selected market participant persona
- A roundtable discussion among several personas
- An educational tool for understanding narratives, incentives, valuation debates, crowd behavior, and risk framing

## What This Is Not

- Not a stock picker
- Not a trading signal generator
- Not personalized investment advice
- Not a tool that tells users what to buy or sell
- Not a replacement for professional financial advice

## Personas

- Long-Term Value Allocator
- Market Structure Trader
- Behavioral Contrarian

## Run Locally

```bash
npm install
npm run dev
```

Then open the local URL printed by Next.js, usually:

```text
http://localhost:3000
```

## API Key

Live responses require an OpenAI API key.

Enter the key inside the app's Settings modal. The key is stored only in browser session state and is not saved to disk.

You can optionally set a default model in `.env.local`:

```bash
NEXT_PUBLIC_DEFAULT_MODEL=gpt-5.2
```

## Web Search And Market Data

Web search is optional and can be enabled from Settings. The model does not automatically browse the web unless web search is enabled.

For structured market data such as prices, short interest, options chains, borrow fees, filings, or fundamentals, separate financial data APIs are still required. Those are not connected yet.

## Safety

This app is for educational market reasoning only. It does not provide personalized investment advice, buy/sell recommendations, or price targets.
