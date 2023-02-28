from googleapiclient import discovery
from oauth2client.client import GoogleCredentials
import requests

credentials = GoogleCredentials.get_application_default()
service = discovery.build('storage', 'v1', credentials=credentials)

filename = 'D:\Git_training\Practice\api2.csv'   # local file location
bucket = 'asia-northeast2-gcp-mn1-f7977b01-bucket' # GCP bucket name 

body = {'api2.csv': 'api2.csv'}
req = service.objects().insert(bucket=bucket, body=body, media_body=filename)
resp = req.execute() 