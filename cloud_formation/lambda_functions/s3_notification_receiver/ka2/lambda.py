import boto3
import logging
import json
import http.client
import os
from datetime import datetime, timedelta

logging.basicConfig(level=logging.DEBUG,
                    format='%(filename)s: '
                    '%(levelname)s: '
                    '%(funcName)s(): '
                    '%(lineno)d:\t'
                    '%(message)s')
logger = logging.getLogger('readings_update')
logger.setLevel(logging.INFO)

# Function to convert timestamp to SGT (UTC+8) and ISO 8601 format
def convert_sgt_to_iso8601_with_tz(timestamp_str):
    # Assuming the input timestamp_str is in "YYYY-MM-DD HH:MM:SS.sss" format and represents SGT
    datetime_obj = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S.%f")
    # Format into ISO 8601 with explicit timezone offset for SGT
    return datetime_obj.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "+08:00"

def lambda_handler(event, context):
    s3 = boto3.resource('s3')
    rest_api_endpoint = "elgo-backend.vercel.app"  # Assuming HTTPS endpoint

    for rec in event['Records']:
        bucket = rec['s3']['bucket']['name']
        key = rec['s3']['object']['key']
        obj = s3.Object(bucket, key)
        raw_payload = obj.get()['Body'].read().decode('utf-8')

        for line in raw_payload.split('\n'):
            if line:
                deviceLabel, devicePower, timestamp, isofAnomaly = line.split(',')
                # Convert isofAnomaly to boolean based on threshold
                isofAnomaly_bool = float(isofAnomaly) > 0.75  # Example threshold check
                # Convert timestamp
                timestamp_iso = convert_sgt_to_iso8601_with_tz(timestamp)

                # Prepare JSON payload for POST request
                post_body = json.dumps({
                    "device_label": deviceLabel,
                    "power": float(devicePower),
                    "timestamp": timestamp_iso,
                    "isofAnomaly": isofAnomaly_bool,
                    "lstmAnomaly": None  # Keeping lstmAnomaly as false for now
                })

                # Send POST request
                headers = {'Content-type': 'application/json'}
                connection = http.client.HTTPSConnection(rest_api_endpoint)
                connection.request('POST', '/sagemakerAnomalies/create', body=post_body, headers=headers)

                response = connection.getresponse()
                logger.info(f'Response status: {response.status}')
                logger.info(f'Response reason: {response.reason}')

                # Read and log the response body
                response_body = response.read().decode()
                logger.info(f'Response body: {response_body}')
                connection.close()

    return {
        "statusCode": 200,
        "body": json.dumps({"message": "Data sent to REST API successfully"}),
    }
