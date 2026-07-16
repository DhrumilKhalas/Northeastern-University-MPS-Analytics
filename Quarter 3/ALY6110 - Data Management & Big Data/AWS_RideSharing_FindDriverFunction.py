import json, boto3
from boto3.dynamodb.conditions import Attr

table = boto3.resource("dynamodb").Table("DriversLanguageTable")

def lambda_handler(event, context):
    body = json.loads(event["body"]) if "body" in event else event
    language = body["preferred_language"]

    response = table.scan(
        FilterExpression=Attr("is_available").eq(True) &
                         Attr("additional_languages").contains(language)
    )

    driver_count = len(response["Items"])

    # Estimate wait time: more drivers = less wait time
    if driver_count == 0:
        wait_time = None
    else:
        wait_time = max(1, 10 - (driver_count * 2))

    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*"
        },
        "body": json.dumps({
            "matching_driver_count": driver_count,
            "estimated_wait_minutes": wait_time
        })
    }