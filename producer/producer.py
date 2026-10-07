import json
import time

import boto3
import websocket


STREAM = "crypto-trades"
REGION = "ap-south-1"

URL = (
    "wss://stream.binance.com:9443/stream"
    "?streams=btcusdt@trade/ethusdt@trade/solusdt@trade"
)

kinesis = boto3.client(
    "kinesis",
    region_name=REGION,
)


def send_to_kinesis(trade):
    response = kinesis.put_record(
        StreamName=STREAM,
        Data=(json.dumps(trade) + "\n").encode("utf-8"),
        PartitionKey=trade["symbol"],
    )

    print(
        f"Sent to Kinesis: {trade['symbol']} "
        f"| Sequence: {response['SequenceNumber']}"
    )


def on_message(ws, message):
    data = json.loads(message)["data"]

    trade = {
        "symbol": data["s"],
        "trade_id": data["t"],
        "price": float(data["p"]),
        "quantity": float(data["q"]),
        "trade_time_ms": data["T"],
        "is_buyer_maker": data["m"],
        "ingested_at_ms": int(time.time() * 1000),
    }

    print(trade)

    send_to_kinesis(trade)


def on_error(ws, error):
    print("ERROR:", error)


def on_close(ws, close_status_code, close_msg):
    print("Connection closed")


def on_open(ws):
    print("Connected to Binance WebSocket")
    print("Sending live trades to Kinesis...\n")


ws = websocket.WebSocketApp(
    URL,
    on_open=on_open,
    on_message=on_message,
    on_error=on_error,
    on_close=on_close,
)

ws.run_forever()