# Market Narrative Lab

A conversational market-thinking simulator that helps users learn how different types of market participants interpret stocks, markets, narratives, and crowd behavior.

## What this is

An educational AI mentor for market reasoning.

## What this is not

- Not a stock picker
- Not a trading signal generator
- Not personalized investment advice
- Not a replacement for professional financial advice

## Core idea

"Learn how different investors think, not copy their trades."

## Personas

- Long-Term Value Allocator
- Market Structure Trader
- Behavioral Contrarian

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Environment variables

Create a `.env` file:

```bash
OPENAI_API_KEY=your_api_key_here
OPENAI_MODEL=gpt-5.2
```

If no API key is provided, the app runs in mock mode.

## Example questions

- Recently the stock market has rallied strongly, but Berkshire has been holding a large cash position. Some people online say Buffett missed the rally and no longer understands the current market. How should I think about this narrative?
- Many investors say AI stocks are expensive, but valuation does not matter because the future growth opportunity is so large. How should I think about this argument?
- A heavily shorted stock suddenly rises sharply, and people online say retail traders can force institutions to cover. What does this narrative reveal about market participants?
- I often notice that after a stock goes up a lot, people suddenly start explaining why the company is great. Before the price move, nobody cared. Why does this happen?
- During strong bull markets, cautious investors are often mocked as outdated or too conservative. What can we learn from this behavior?

## Future improvements

- Add RAG over investor letters, market commentary, and historical case studies
- Add real-time market data
- Add social sentiment input
- Add source citations
- Add user-uploaded article analysis
- Add more personas, such as Macro Regime Trader and Narrative Growth Investor
