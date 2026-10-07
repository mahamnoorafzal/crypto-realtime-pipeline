terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.0"
    }
  }

  required_version = ">= 1.6.0"
}

provider "aws" {
  region  = "ap-south-1"
  profile = "AdministratorAccess-246312965173"
}

resource "aws_s3_bucket" "crypto_pipeline" {
  bucket = "maham-crypto-pipeline-2026-246312965173"
}

resource "aws_kinesis_stream" "crypto_trades" {
  name        = "crypto-trades"
  shard_count = 1

  stream_mode_details {
    stream_mode = "PROVISIONED"
  }
}

resource "aws_kinesis_firehose_delivery_stream" "crypto_firehose" {
  name        = "crypto-trades-firehose"
  destination = "extended_s3"

  kinesis_source_configuration {
    kinesis_stream_arn = aws_kinesis_stream.crypto_trades.arn
    role_arn           = "arn:aws:iam::246312965173:role/crypto-firehose-role"
  }

  extended_s3_configuration {
    role_arn   = "arn:aws:iam::246312965173:role/crypto-firehose-role"
    bucket_arn = "arn:aws:s3:::maham-crypto-pipeline-2026-246312965173"

    prefix              = "bronze/trades/"
    error_output_prefix = "bronze_errors/"
  }
}
