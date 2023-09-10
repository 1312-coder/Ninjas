from google.cloud import storage

# Create a client object
client = storage.Client()

# Get a reference to the destination bucket and blob
bucket = client.get_bucket('asia-south1-gcp-mn1-5ed87924-bucket')
blob = bucket.blob('api/api.csv')

# Upload the file to Google Cloud Storage
blob.upload_from_filename('D:/Git_training/Practice/api.csv')

print(blob)
