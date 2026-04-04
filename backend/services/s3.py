import boto3

s3 = boto3.client("s3")

BUCKET_NAME = "your-bucket-name"

def upload_to_s3(file):
    s3.upload_fileobj(file.file, BUCKET_NAME, file.filename)
    return f"https://{BUCKET_NAME}.s3.amazonaws.com/{file.filename}"