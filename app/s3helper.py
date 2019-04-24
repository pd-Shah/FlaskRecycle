import os

import uuid
import boto3


s3 = boto3.client(
   "s3",
   aws_access_key_id=os.getenv('S3_KEY'),
   aws_secret_access_key=os.getenv('S3_SECRET')
)


ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def check_file_before_upload(file):
    if file.filename == "":
        return 'Please select a file'

    if file and allowed_file(file.filename):
        return True


def upload_file(file, bucket_name, acl="public-read"):

    try:
        filename = str(uuid.uuid4())
        s3.upload_fileobj(
            file,
            bucket_name,
            filename,
            ExtraArgs={
               "ACL": acl,
               "ContentType": file.content_type
            }
         )

    except Exception as e:
        print("Something Happened: ", e)
        return e

    return filename
