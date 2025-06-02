import websocket
import json

API_KEY = "d0u63dhr01qn5fk3d4f0d0u63dhr01qn5fk3d4fg"
symbol = "AAPL"

# Counter to limit how many messages are printed
message_count = 0
MAX_MESSAGES = 2

def on_message(ws, message):
    global message_count
    data = json.loads(message)
    
    # Only show trade data
    if data.get("type") == "trade":
        for trade in data["data"]:
            print(f"🔔 {trade['s']} Price: ${trade['p']} Time: {trade['t']}")

        message_count += 1
        if message_count >= MAX_MESSAGES:
            print("✅ Received required updates. Closing WebSocket...")
            ws.close()

def on_open(ws):
    print("🔌 WebSocket connected.")
    ws.send(json.dumps({
        "type": "subscribe",
        "symbol": symbol
    }))

def on_error(ws, error):
    print("❌ Error:", error)

def on_close(ws):
    print("🔌 WebSocket disconnected.")

socket = f"wss://ws.finnhub.io?token={API_KEY}"
ws = websocket.WebSocketApp(socket,
                            on_open=on_open,
                            on_message=on_message,
                            on_error=on_error,
                            on_close=on_close)

print("📲 Starting real-time price feed...")
ws.run_forever()
