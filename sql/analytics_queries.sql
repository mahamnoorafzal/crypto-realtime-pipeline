-- Crypto Real-Time Trade Analytics
-- Athena database: crypto_realtime_db

-- 1. Check Silver data by cryptocurrency
SELECT
    symbol,
    COUNT(*) AS trade_count,
    AVG(price) AS average_price,
    SUM(trade_value) AS total_trade_value
FROM crypto_realtime_db.silver_trades
GROUP BY symbol
ORDER BY trade_count DESC;


-- 2. Gold trade summary
SELECT *
FROM crypto_realtime_db.gold_trade_summary
ORDER BY trade_count DESC;


-- 3. Check ML anomaly results
SELECT
    symbol,
    COUNT(*) AS total_trades,
    SUM(anomaly_label) AS anomalies
FROM crypto_realtime_db.crypto_trade_anomalies
GROUP BY symbol
ORDER BY anomalies DESC;


-- 4. Show strongest anomalies
SELECT
    symbol,
    trade_id,
    price,
    quantity,
    trade_value,
    anomaly_score,
    anomaly_label,
    trade_time
FROM crypto_realtime_db.crypto_trade_anomalies
WHERE anomaly_label = 1
ORDER BY anomaly_score ASC
LIMIT 20;


-- 5. Overall anomaly rate
SELECT
    COUNT(*) AS total_trades,
    SUM(anomaly_label) AS total_anomalies,
    ROUND(
        100.0 * SUM(anomaly_label) / COUNT(*),
        2
    ) AS anomaly_rate_percent
FROM crypto_realtime_db.crypto_trade_anomalies;
