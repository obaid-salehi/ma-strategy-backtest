import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

df = yf.download("NVDA",start="2014-12-17",end="2025-10-04",interval="1d")
df = df.drop(["High","Low","Open","Volume"],axis=1)

df["50d_avg"] = df["Close"].rolling(window=50).mean()
df["200d_avg"] = df["Close"].rolling(window=200).mean()  #creating columns for 50d and 200d averages
df = df[199:]  #ignoring the first 199 lines as they won't have a 200d average to work with

df["Diff"] = df["50d_avg"] - df["200d_avg"]
df.loc[df["Diff"] > 0, "Signal"] = 1
df.loc[df["Diff"] < 0, "Signal"] = 0  #generating a signal if there is a corssover of moving-averages

df["DailyReturn"] = (df["Close"]/df["Close"].shift(1))-1  #daily return is the decimal amount the price has changed fom the day before
df["ActualReturn"] = df["DailyReturn"]*df["Signal"].shift(1)  #actual return is the decimal amount the portfolio value has changed from the day before
df["TotalReturn"] = (1 + df["ActualReturn"]).cumprod()
df["AssetReturn"] = (1 + df["DailyReturn"]).cumprod()


InitialValue = 1000000  #given an arbitray value as the investment size
df["CurrentValue"] = InitialValue*df["TotalReturn"]  #a series of the size of the portfolio on each
df["AssetValue"] = InitialValue*df["AssetReturn"]  #a series of the size of the portfolio without the strategy
print(" ")
print("Value of Investment:",df["CurrentValue"].iloc[len(df)-1])
print("Strategy Rate of Return:",df["TotalReturn"].iloc[len(df)-1]*100,"%")
print("Asset Rate of Return:",df["AssetReturn"].iloc[len(df)-1]*100,"%")

print(" ")
CAGR = (df["CurrentValue"].iloc[-1]/InitialValue)**(1/10) - 1
Volatility = df["ActualReturn"].std()*(252**0.5)
StrategySharpe = CAGR/Volatility
AssetSharpe = ((df["AssetValue"].iloc[-1]/InitialValue)**(1/10) - 1)/(df["DailyReturn"].std()*(252**0.5))  #caclulating the sharpe ratio of the portfolio without the strategy
print("CAGR:",CAGR*100,"%")
print("Strategy Sharpe Ratio:",StrategySharpe)
print("Asset Sharpe Ratio:",AssetSharpe)
print(" ")
print(df)

plt.plot(df.index,df["AssetReturn"],label="Asset Price",c="r",lw=1)
plt.plot(df.index,df["TotalReturn"],label="Strategy Portfolio",c="b",lw=1)  #plotting the strategy's portfolio alongside the underlying asset over the span of 10 years
plt.title("Strategy (Blue) vs. Asset (Red)")
plt.xlabel("Date")
plt.ylabel("Value")
plt.show()

