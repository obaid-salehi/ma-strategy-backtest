import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

df = yf.download("NVDA",start="2014-12-17",end="2025-10-04",interval="1d")
df = df.drop(["High","Low","Open","Volume"],axis=1)

df["50d_avg"] = df["Close"].rolling(window=50).mean()
df["200d_avg"] = df["Close"].rolling(window=200).mean()
df = df[199:]

df["Diff"] = df["50d_avg"] - df["200d_avg"]
df.loc[df["Diff"] > 0, "Signal"] = 1
df.loc[df["Diff"] < 0, "Signal"] = 0

df["DailyReturn"] = (df["Close"]/df["Close"].shift(1))-1
df["ActualReturn"] = df["DailyReturn"]*df["Signal"].shift(1)
df["TotalReturn"] = (1 + df["ActualReturn"]).cumprod()
df["AssetReturn"] = (1 + df["DailyReturn"]).cumprod()


InitialValue = 1000000
df["CurrentValue"] = InitialValue*df["TotalReturn"]
df["AssetValue"] = InitialValue*df["AssetReturn"]
print(" ")
print("Value of Investment:",df["CurrentValue"].iloc[len(df)-1])
print("Strategy Rate of Return:",df["TotalReturn"].iloc[len(df)-1]*100,"%")
print("Asset Rate of Return:",df["AssetReturn"].iloc[len(df)-1]*100,"%")

print(" ")
CAGR = (df["CurrentValue"].iloc[-1]/InitialValue)**(1/10) - 1
Volatility = df["ActualReturn"].std()*(252**0.5)
StrategySharpe = CAGR/Volatility
AssetSharpe = ((df["AssetValue"].iloc[-1]/InitialValue)**(1/10) - 1)/(df["DailyReturn"].std()*(252**0.5))
print("CAGR:",CAGR*100,"%")
print("Strategy Sharpe Ratio:",StrategySharpe)
print("Asset Sharpe Ratio:",AssetSharpe)
print(" ")
print(df)

plt.plot(df.index,df["AssetReturn"],label="Asset Price",c="r",lw=1)
plt.plot(df.index,df["TotalReturn"],label="Strategy Portfolio",c="b",lw=1)
plt.title("Strategy (Blue) vs. Asset (Red)")
plt.xlabel("Date")
plt.ylabel("Value")
plt.show()
