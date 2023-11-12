import boto3
import json
import io

runtime_client = boto3.client('sagemaker-runtime')
content_type = "application/json"
request_body = {'Songs' : [{'name': 'HiTek Tek', 'artist': 'Future'},
                {'name': 'Ridin Strikers', 'artist': 'Future'},
                {'name': 'Touch The Sky', 'artist': 'Future'},
                {'name': 'One Of My', 'artist': 'Future'},
                {'name': 'Hard To Choose One', 'artist': 'Future'},
                {'name': 'Solitaires (feat. Travis Scott)', 'artist': 'Future'},
                {'name': 'Harlem Shake (feat. Young Thug)', 'artist': 'Future'},
                {'name': 'Too Comfortable', 'artist': 'Future'}], 'Number' : 10}
data = json.loads(json.dumps(request_body))
payload = json.dumps(data)
endpoint_name = "sklearn-local-ep2023-11-12-18-41-34"

response = runtime_client.invoke_endpoint(
    EndpointName=endpoint_name,
    Body=payload,
    ContentType=content_type,
    Accept='Accept')
result = json.loads(response['Body'].read().decode())['Songs']
print(result)