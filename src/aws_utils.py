"""Utility functions around aws"""
import boto3


def connect_to_s3():
    """Initialize a connection to s3"""
    return boto3.client('s3', aws_access_key_id=os.environ('AWS_ACCESS_KEY'),
                        aws_secret_access_key=os.environ('AWS_SECRET_KEY'))
