# Real-Time Crypto Trade Analytics Pipeline

A cloud-based real-time data engineering and machine learning pipeline that collects cryptocurrency trade data, processes it through AWS data services, performs analytics, and detects anomalous trading activity using machine learning.

## Architecture

```text
Binance WebSocket
       ↓
Python Producer
       ↓
Docker
       ↓
Amazon Kinesis Data Streams
       ↓
Amazon Kinesis Data Firehose
       ↓
Amazon S3 — Bronze
       ↓
AWS Glue Crawler
       ↓
AWS Glue Spark ETL
       ↓
Amazon S3 — Silver
       ↓
Amazon Athena — Gold Analytics
       ↓
Amazon SageMaker
       ↓
Isolation Forest
       ↓
Amazon S3 — Anomaly Results
       ↓
Amazon Athena