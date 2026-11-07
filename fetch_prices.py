import json
import datetime
import yfinance as yf

# 監視対象銘柄（拡張版：主要日本株・米国株）
SYMBOLS = {
    # 日本株
    "7203.T": "トヨタ自動車",
    "6758.T": "ソニーグループ",
    "8306.T": "三菱UFJフィナンシャルG",
    "7974.T": "任天堂",
    "9984.T": "ソフトバンクG",
    "8035.T": "東京エレクトロン",
    "6857.T": "アドバンテスト",
    "9983.T": "ファーストリテイリング",
    "6501.T": "日立製作所",
    "7011.T": "三菱重工業",
    # 米国株
    "AAPL": "アップル",
    "NVDA": "エヌビディア",
    "MSFT": "マイクロソフト",
    "AMZN": "アマゾン",
    "TSLA": "テスラ"
}

def fetch_stock_data():
    output_data = {
        "updated_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "stocks": {}
    }

    for symbol, name in SYMBOLS.items():
        try:
            ticker = yf.Ticker(symbol)
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

    with open("stock_data.json", "w", encoding="utf-8") as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    fetch_stock_data()