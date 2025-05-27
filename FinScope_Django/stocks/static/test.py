import yfinance as yf


def get_commodity_prices():
    tickers = {"gold": "GC=F", "silver": "SI=F", "oil": "CL=F"}
    data = {}
    for name, symbol in tickers.items():
        try:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period="2d", interval="60m")
            if hist.empty:
                raise Exception("No data available")

            price_data = hist["Close"].round(2).dropna()
            data[name] = {str(k): float(v) for k, v in price_data.items()}
        except Exception as e:
            data[name] = {"error": str(e)}
    return data


print(get_commodity_prices())
