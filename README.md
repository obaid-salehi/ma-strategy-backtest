# Moving-Average Trading Strategy Backtest

A Python implementation and backtest of a 50/200-day moving-average crossover trading strategy, developed to explore the effectiveness of momentum-based signals in equity markets.

---

## Overview
This project simulates a simple trend-following strategy that goes **long** when the 50-day moving average crosses above the 200-day moving average and **exits** when it crosses below.  
It measures returns, risk, and performance metrics over a 10-year period using historical data from the yfinance API.

---

## Tools & Libraries
- **Python**
- **pandas**: data manipulation & rolling averages  
- **yfinance**: historical price data  
- **matplotlib**: performance visualisation  
- **NumPy**: vectorised calculations

---

## Key Features
- Fully vectorised backtest for fast execution  
- Automated signal generation and portfolio tracking  
- Performance metrics: CAGR, volatility, Sharpe ratio  
- Benchmark comparison against underlying assets
- Visual output of comparison over 10yr period

---

## Results
- Achieved a Sharpe ratio of ≈ 0.6 on the S&P 500 test period  
- Outperformed Nvidia stock by **+0.217** in Sharpe ratio  
- Demonstrated clear risk-adjusted improvement during sustained up-trends
