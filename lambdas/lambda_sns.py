import json


def greetings(event, context):

    print(f'Event from SNS. {json.dumps(event)}' )

    body = {
        "message": "This is the output of lambda sns",
        "input": event
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response
