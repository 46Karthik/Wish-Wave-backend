import random
from django.db import connection
import json
import jwt 
from django.conf import settings
import boto3
import base64
import io
from botocore.exceptions import NoCredentialsError, ClientError
def Decode_JWt(auth_header):
    token = auth_header.split(" ")[1]
    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
    return payload

def generate_numeric_otp(length=6):
    otp = ''.join([str(random.randint(0, 9)) for _ in range(length)])
    return otp

def return_sql_results(sql):
    cursor = connection.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    result = []
    if rows:
        result = [json.loads(row[0]) for row in rows]
    return result

def return_response(statuscode, message, data=None):
    if data is not None:
        return {
            'status': statuscode,
            'message': message,
            'data': data
        }
    else:
        return {
            'status': statuscode,
            'message': message
        }

def upload_image_to_s3(file, path,content_type):
    # Initialize the boto3 S3 client
    s3_client = boto3.client(
        's3',
        aws_access_key_id="AKIA2FXAD2D3VJBIBS6D",
        aws_secret_access_key="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",
        region_name="ap-south-1"
    )
    try:
        # Upload the file to the specified folder in the S3 bucket
        s3_client.upload_fileobj(
            file,
            "wishwave", 
            f"{path}/{file.name}",  
            ExtraArgs={
                "ContentType": content_type  
            }
        )

        # Construct the file URL
        file_path = f"{path}/{file.name}"

        return file_path

    except NoCredentialsError:
        # print("Invalid AWS credentials")
        return "error"

    except Exception as e:
        # print("error": str(e))
        return f"Error: {str(e)}"

def upload_base64_image_to_s3(base64_string, path, file_name, content_type):
    # Initialize the boto3 S3 client
    s3_client = boto3.client(
        's3',
        aws_access_key_id="AKIA2FXAD2D3VJBIBS6D",
        aws_secret_access_key="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",
        region_name="ap-south-1"
    )
    
    try:
        # Decode the Base64 string into binary data
        file_data = base64.b64decode(base64_string)

        # Create a file-like object using BytesIO
        file_like_object = io.BytesIO(file_data)

        # Set the file name if necessary
        if not file_name:
            file_name = "default_file_name.png"  # You can modify this default as needed

        # Upload the file to the specified folder in the S3 bucket
        s3_client.upload_fileobj(
            file_like_object,
            "wishwave",  # Replace with your S3 bucket name
            f"{path}/{file_name}",  # Construct the full path in the bucket
            ExtraArgs={
                "ContentType": content_type  # Set the content type (e.g., 'image/png')
            }
        )

        # Construct the file path
        file_path = f"{path}/{file_name}"

        return file_path

    except NoCredentialsError:
        return "Invalid AWS credentials"

    except Exception as e:
        return f"Error: {str(e)}"


def delete_image_from_s3(file_key):
    """
    Delete an image or file from an S3 bucket.

    :param bucket_name: The name of the S3 bucket.
    :param file_key: The key (path and file name) of the file to delete in the S3 bucket.
    :return: Success or error message.
    """
    # Initialize the boto3 S3 client
    bucket_name = "wishwave"
    s3_client = boto3.client(
        's3',
        aws_access_key_id="AKIA2FXAD2D3VJBIBS6D",
        aws_secret_access_key="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",
        region_name="ap-south-1"
    )

    try:
        # Delete the file from the specified S3 bucket
        s3_client.delete_object(Bucket=bucket_name, Key=file_key)
        return True

    except NoCredentialsError:
        return False

    except ClientError as e:
        # If the file doesn't exist or other errors occur
        return False

    except Exception as e:
        return False

