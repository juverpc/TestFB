import json
from sklearn.externals import joblib
import boto3

model_name = 'model_1615506186.2672553.joblib'
model = joblib.load(model_name)

def predict(event, context):
    body = {
        "message": "OK",
    }

    if 'queryStringParameters' in event.keys():
        params = event['queryStringParameters']

        medInc = float(params['medInc']) / 100000
        houseAge = float(params['houseAge'])
        aveRooms = float(params['aveRooms'])
        aveBedrms = float(params['aveBedrms'])
        population = float(params['population'])
        aveOccup = float(params['aveOccup'])
        latitude = float(params['latitude'])
        longitude = float(params['longitude'])

        inputVector = [medInc, houseAge, aveRooms, aveBedrms, population, aveOccup, latitude, longitude]
        data = [inputVector]
        predictedPrice = model.predict(data)[0] * 100000 # convert to units of 1 USDs
        predictedPrice = round(predictedPrice, 2)
        body['predictedPrice'] = predictedPrice
    
    else:
        body['message'] = 'queryStringParameters not in event.'

    print(body['message'])

    response = {
        "statusCode": 200,
        "body": json.dumps(body),
        "headers": {
            "Content-Type": 'application/json',
            "Access-Control-Allow-Origin": "*" # request from any domain ( not safe!!)
        }
    }
    # Method 1: Object.put()
    some_binary_data = b'Here we have some data'
    s3 = boto3.resource('s3')
    object_s3 = s3.Object('test-lambda-zd', 'filename.txt')
    object_s3.put(Body=some_binary_data)

    return response
# Test predictr function before deploy 

def do_main():
    event = {
        'queryStringParameters': {
            'medInc': 200000,
            'houseAge': 10,
            'aveRooms': 4,
            'aveBedrms': 1,
            'population': 800,
            'aveOccup': 3,
            'latitude': 37.54,
            'longitude': -121.72
        }
    }

    response = predict(event, None) # no need context
    body = json.loads(response['body'])
    print('Price:', body['predictedPrice'])

    # save the event
    with open('event.json', 'w') as event_file:
        event_file.write(json.dumps(event))
    

# do_main()