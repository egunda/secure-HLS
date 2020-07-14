import json
import binascii
import hashlib
import hmac
import urllib.parse
import time
import calendar;

def lambda_handler(event, context):
    
    #Auth Token Verificatin Code
    EDGE_PRIVATE_KEY = 'Enter_Your_Secret_Key_Here'
    newToken = []
    hashSource = []
    field_delimiter = '~'
    
    currentTime = calendar.timegm(time.gmtime())
    
    html_page= 'Access Denied'
    request = event['Records'][0]['cf']['request']
    queryString1 = request['querystring']
    if(queryString1 == ""):
        response = {
                'status': "403",
                'body': html_page,
                'headers': {
                    'content-type': [{
                        'key': 'Content-Type',
                        'value': 'text/html'
                     }]
                }
            }       
        return response
    else:
        queryString = urllib.parse.unquote(queryString1)
        tokenName = queryString.split('=',1)[0]
        token = queryString.split('=',1)[1]
        expires = token.split('~')[1].split('=')[1]      
        if currentTime <= int(expires):
            hashSrc = token.rsplit('~',1)[0]
            sha256_request = token.rsplit('~',1)[1]
            sha256_request = sha256_request.split('=')[1]
            sha256_request = sha256_request.split('&')[0]
            key = binascii.a2b_hex(EDGE_PRIVATE_KEY)
            token_hmac = hmac.new(key,hashSrc.encode(),getattr(hashlib, 'sha256'))
            value = token_hmac.hexdigest()
            newToken.append('hmac={0}'.format(value))
            status = (value == sha256_request)
            if status == True:
                request['headers']['Access-Control-Allow-Origin'] = [{'key': 'access-control-allow-origin', 'value': '*'}]
                request['querystring'] = queryString
                return request
            else:
                response = {
                    'status': "403",
                    'body': html_page,
                    'headers': {
                        'content-type': [{
                            'key': 'Content-Type',
                            'value': 'text/html'
                         }]
                    }
                }     
                return response
        else:
            response = {
                    'status': "403",
                    'body': html_page,
                    'headers': {
                        'content-type': [{
                            'key': 'Content-Type',
                            'value': 'text/html'
                         }]
                    }
                }        
            return response
