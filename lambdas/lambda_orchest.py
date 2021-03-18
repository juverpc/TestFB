import json
import boto3
import re
import random

def inference(event, context):

    lambda_client = boto3.client('lambda', region_name='us-east-1')
    funcs = lambda_client.list_functions()

    arns = [f["FunctionArn"] for f in funcs['Functions'] if bool(re.match(r'.*second-test.*lambda-0', f["FunctionArn"]))]
    lambda_choice = random.choice(arns)

    print(lambda_choice)

    lambda_res = lambda_client.invoke(
        FunctionName = lambda_choice,
        InvocationType = 'RequestResponse',
    )

    payload = json.load(lambda_res['Payload'])
    print(payload)

    # body = {
    #     "message": res,
    #     "input": event
    # }

    # response = {
    #     "statusCode": 200,
    #     "body": json.dumps(body)
    # }

    return payload

    # Use this code if you don't use the http event with the LAMBDA-PROXY
    # integration
    """
    return {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "event": event
    }
    """
