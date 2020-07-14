import json
import urllib.request
import re
import hmac
import binascii
import hashlib

def lambda_handler(event, context):
    path = event['path']
    header = event['headers']
    domainName = 'domain_name_of_origin'
    proto = header.get('cloudfront-forwarded-proto')
    url = proto+'://'+domainName+path
    status = event['queryStringParameters'].get('hdnts')
    if status:
        token = event['queryStringParameters']['hdnts']
        data =  urllib.request.urlopen(url)
        line = data.read().decode("utf-8")
        if '.m3u8' in line:
            encoded_content = line.replace('.m3u8','.m3u8?hdnts='+token)
        elif '.ts' in line:
            encoded_content = line.replace('.ts','.ts?hdnts='+token)
        return {
                    'statusCode': 200,
                    'body': encoded_content
                }
    else:
        return {
            'statusCode': 403,
            'body': 'Forbidden'
        }
