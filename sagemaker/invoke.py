import boto3
import json
import io

runtime_client = boto3.client('sagemaker-runtime')
content_type = "application/json"
request_body = {'Songs' : [{'name': 'Got It On Me', 'year': 2020},
                {'name': 'Mannequin (feat. Lil Tjay)', 'year': 2020},
                {'name': 'Dior', 'year': 2019},
                {'name': 'Welcome To The Party', 'year': 2019}], 'Number' : 10}
data = json.loads(json.dumps(request_body))
payload = json.dumps(data)
endpoint_name = "sklearn-local-ep2022-05-02-00-35-41"

response = runtime_client.invoke_endpoint(
    EndpointName=endpoint_name,
    Body=payload,
    ContentType=content_type,
    Accept='Accept')
result = json.loads(response['Body'].read().decode())['Songs']
print(result)