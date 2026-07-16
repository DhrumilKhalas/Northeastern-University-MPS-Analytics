import json
import boto3
import uuid

table = boto3.resource("dynamodb").Table("DriversLanguageTable")

def lambda_handler(event, context):
    body = json.loads(event["body"]) if "body" in event else event

    # Generate a unique driver ID
    driver_id = "DRV_" + str(uuid.uuid4())[:6].upper()

    primary_language = body.get("primary_language", "English")
    additional_languages = body.get("additional_languages", [])
    location_zone = body.get("location_zone", "Toronto-Downtown")

    # Make sure primary language is not duplicated in additional_languages
    additional_languages = [lang for lang in additional_languages if lang != primary_language]

    table.put_item(Item={
        "driver_id": driver_id,
        "primary_language": primary_language,
        "additional_languages": additional_languages,
        "location_zone": location_zone,
        "is_available": True
    })

    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*"
        },
        "body": json.dumps({
            "message": "Driver registered successfully.",
            "driver_id": driver_id
        })
    }