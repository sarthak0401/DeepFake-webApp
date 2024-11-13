import boto3
from botocore.exceptions import NoCredentialsError, EndpointConnectionError

s3_client = boto3.client('s3', region_name='us-east-1')

try:
    response = s3_client.list_buckets()
    print(response)
except EndpointConnectionError as e:
    print("Connection failed:", e)
except NoCredentialsError:
    print("Credentials not available")
