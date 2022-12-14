import boto3
import os

AWS_IAM_ACCESS_KEY_ID = os.getenv("AWS_IAM_ACCESS_KEY_ID")
AWS_IAM_SECRET_ACCESS_KEY = os.getenv("AWS_IAM_SECRET_ACCESS_KEY")
REGION_NAME = os.getenv("REGION_NAME")


def init_dynamodb():
    """初期化"""
    session = boto3.session.Session(
        aws_access_key_id=AWS_IAM_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_IAM_SECRET_ACCESS_KEY,
        region_name=REGION_NAME)

    resource = session.resource('dynamodb').Table("IRData")
    return resource


def get_item_to_dynamodb(table, company_name):
    """DynamoDBからデータを取得する
    失敗したらNoneを返す"""
    response = table.get_item(Key={'company_name': company_name})
    if not "Item" in response:
        return None

    item = response["Item"]

    return item


def put_item_to_daynamodb(table, company_name, body):
    """DynamoDBを更新する"""
    item = {
        "company_name": company_name,
        "body": body
    }
    table.put_item(Item=item)
