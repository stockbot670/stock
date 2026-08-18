Python
import pandas as pd
import yfinance as yf
import requests

# 1. 최신 S&P 500 종목 가져오기
tickers = get_sp500_tickers()

# 2. 주가 데이터 한 번에 다운로드
data = yf.download(tickers, period="1y", interval="1d", progress=False)['Close']

target_stocks = []

# 3. 200일선 부근(±2%) 종목 필터링
for ticker in tickers:
    try:
        series = data[ticker].dropna()
        if len(series) >= 200:
            sma200 = series.rolling(200).mean().iloc[-1]
            latest_close = series.iloc[-1]
            diff_percent = abs((latest_close - sma200) / sma200) * 100
            
            if diff_percent <= 2.0:  # 2% 이내 접촉
                target_stocks.append(f"• {ticker}: 현재가 ${latest_close:.2f} (200일선 ${sma200:.2f})")
    except Exception:
        continue

# 4. 텔레그램으로 알림 전송하기
bot_token = '8600711544:AAHxHxdGJNdk2X2A8UQZV6jcnYq-k_Ec76U'  # 텔레그램 봇 토큰 입력
chat_id = '7188493977'      # 내 텔레그램 Chat ID 입력

if target_stocks:
    message = "🚨 **[S&P 500 200일선 도달 종목 알림]**\n\n" + "\n".join(target_stocks)
else:
    message = "✅ 오늘 200일선 부근에 위치한 S&P 500 종목이 없습니다."

telegram_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
requests.post(telegram_url, data={'chat_id': chat_id, 'text': message, 'parse_mode': 'Markdown'})
