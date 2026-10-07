import json
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1] / "producer")
)

import producer


def test_trade_data_is_json_serializable():
    trade = {
        "symbol": "BTCUSDT",
        "trade_id": 12345,
        "price": 100000.50,
        "quantity": 0.01,
        "trade_time_ms": 1750000000000,
        "is_buyer_maker": False,
        "ingested_at_ms": 1750000001000,
    }

    result = json.dumps(trade)

    assert isinstance(result, str)


@patch("producer.kinesis")
def test_send_to_kinesis(mock_kinesis):
    trade = {
        "symbol": "BTCUSDT",
        "trade_id": 12345,
        "price": 100000.50,
        "quantity": 0.01,
        "trade_time_ms": 1750000000000,
        "is_buyer_maker": False,
        "ingested_at_ms": 1750000001000,
    }

    mock_kinesis.put_record.return_value = {
        "SequenceNumber": "test-sequence"
    }

    producer.send_to_kinesis(trade)

    mock_kinesis.put_record.assert_called_once()

    call_args = mock_kinesis.put_record.call_args.kwargs

    assert call_args["StreamName"] == "crypto-trades"
    assert call_args["PartitionKey"] == "BTCUSDT"