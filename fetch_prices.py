import json
import datetime
import yfinance as yf

# 監視対象銘柄の定義（ティッカーシンボル -> 表示名）
SYMBOLS = {
    "7203.T": "トヨタ自動車",
    "6758.T": "ソニーグループ",
    "8306.T": "三菱UFJフィナンシャルG",
    "7974.T": "任天堂",
    "AAPL": "アップル"
}

def fetch_stock_data():
    output_data = {
        "updated_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "stocks": {}
    }

    for symbol, name in SYMBOLS.items():
        try:
            ticker = yf.Ticker(symbol)
            # fast_info または info から最新データ・前日価格・高安を取得
            info = ticker.fast_info
            
            price = round(float(info.last_price), 2)
            prev_close = round(float(info.previous_close), 2)
            high = round(float(info.day_high if info.day_high is not None else price), 2)
            low = round(float(info.day_low if info.day_low is not None else price), 2)

            change = round(price - prev_close, 2)
            change_percent = round((change / prev_close) * 100, 2) if prev_close else 0.0

            output_data["stocks"][symbol] = {
                "name": name,
                "price": price,
                "change": change,
                "change_percent": change_percent,
                "high": high,
                "low": low
            }
            print(f"Successfully fetched {symbol}: {price}")
        except Exception as e:
            print(f"Error fetching data for {symbol}: {e}")

    # JSONファイルへ保存
    with open("stock_data.json", "w", encoding="utf-8") as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    fetch_stock_data()