import json

def lambda_handler(event, context):
    response = event['Records'][0]['cf']['response']
    
    response['headers']['access-control-allow-origin'] = [{'key': 'Access-Control-Allow-Origin', 'value': '*'}]
    response['headers']['access-control-allow-credentials'] = [{'key': 'Access-Control-Allow-Credentials', 'value': 'true'}]
    response['headers']['access-control-allow-methods'] = [{'key': 'Access-Control-Allow-Methods', 'value': 'OPTIONS, GET, POST, HEAD'}]
    response['headers']['access-control-allow-headers'] = [{'key': 'Access-Control-Allow-Headers', 'value': 'Content-Type, User-Agent, If-Modified-Since, Cache-Control, Range'}]
    
    return response
