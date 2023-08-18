import boto3
import os
import constants

s3 = boto3.resource(
    service_name="s3",
    region_name="us-east-2",
    aws_access_key_id=os.environ["ACCESS_KEY"],
    aws_secret_access_key=os.environ["SECRET_KEY"],
)
s3_client = s3.meta.client
bucket = s3.Bucket(os.environ["BUCKET"])


def get_names():
    names = []
    response = s3_client.list_objects_v2(Bucket=os.environ["BUCKET"])
    if "Contents" in response:
        for obj in response["Contents"]:
            if obj["Key"].endswith("/"):
                names.append(obj["Key"][:-1])
    return names


def get_excel_file(folder_to_write):
    bucket.download_file(
        Key=constants.FILE, Filename=os.path.join(folder_to_write, constants.FILE)
    )


def upload_to_bucket(filename, key):
    bucket.upload_file(Filename=filename, Key=key)
