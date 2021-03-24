import json


def greetings(event, context):
    
    print(f'Event from SQS. {json.dumps(event)}' )

    body = {
        "message": "This is the output of lambda sqs ",
        "input": event
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response
