# This Script will Receive a Webhook Event from Stripe via Google Cloud Function, then create a new JSON payload and then writes it to a BigQuery Dataset

import json
import logging
import datetime as datetime
import stripe
import os
from google.cloud import bigquery

stripe.api_key = os.environ.get("STRIPE_API_KEY_YOU_CREATED", "NO_STRIPE_API_KEY_YOU_CREATED")
signing_secret = os.environ.get("YOUR_SIGNING_SECRET", "NO_YOUR_SIGNING_SECRET")

# Set up logging for troubleshooting and stuff
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get the Stripe signature and the raw body of the request
def payment_intent_cf(request):
    
    # Raw Body is Required to Verify the Signature
    raw_body = request.data.decode("utf-8")
    
    # Get the Stripe signature from the headers
    sig_header = request.headers['STRIPE_SIGNATURE']

    # Verify the Signature
    try:
        event = stripe.Webhook.construct_event(
            raw_body, sig_header, signing_secret
        )
    except ValueError as e:
        # Invalid Signature Error
        logger.error("Signature Verification Failed: %s", e)
        return {'statusCode': 400, 'body': 'Invalid Stripe Signature'}

    # Clean up the payload and get what you want here
    try:
        data = event["data"]["object"]
        failure_code = data["charges"]["data"][0]["failure_code"]
        network_status = data["charges"]["data"][0]["outcome"]["network_status"]
        declined_reason = data["charges"]["data"][0]["outcome"]["reason"]
        payment_intent_status = event["type"]
        receipt_email = data["receipt_email"]
        payment_status = data["status"]
        payment_method_types = data["payment_method_types"][0]
        transaction_id = data["id"]
        created_at = str(datetime.datetime.fromtimestamp(data["created"]))
        failure_message = data["charges"]["data"][0]["failure_message"]
    except KeyError as e:
        logger.error("Error accessing data in event: %s", e)
        return {'statusCode': 400, 'body': 'Error accessing data in event'}

    # Create a new payload with the data extracted from above
    new_payload = {
        'transaction_id': transaction_id,
        'created_at': date_time,
        'receipt_email': receipt_email,
        'failure_message': failure_message,
        'failure_code': failure_code,
        'network_status': network_status,
        'declined_reason': declined_reason,
        'payment_intent_status': payment_intent_status,
        'payment_status': payment_status,
        'payment_method_types': payment_method_types
    }

    # BigQuery Details
    client = bigquery.Client(project="YourProjectNameHere")
    dataset_name = "YourDataSet"
    table_name = "yourTable"
    table = client.get_table(f"{dataset_name}.{table_name}")

    # Insert into BQ
    # Use insert_rows_json Method from BQ Client to write JSON Payload into the BQ
    # You Can Create a BQ Schema, Just Print the Output, Create a table from the JSON you got
    try:
        bq_insert = client.insert_rows_json(table, [new_payload])
        logger.info("Successfully inserted data into table %s.%s", dataset_name, table_name)
    except Exception as e:
        logger.error("Error inserting data into table: %s", e)
        raise