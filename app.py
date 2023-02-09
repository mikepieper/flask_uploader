from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import logging
from mimetypes import MimeTypes
import boto3
from botocore.exceptions import ClientError
import os

app = Flask(__name__)


# Upload file to s3 bucket function



def upload_file(f):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    file_name = secure_filename(f.filename)

    # Upload the file
    s3_client = boto3.client('s3', 
                             aws_access_key_id=os.environ['aws_access_key_id'], 
                             aws_secret_access_key=os.environ['aws_secret_access_key'])
    try:
        response = s3_client.upload_fileobj(f, 'assyst-testing', f"test/{file_name}")
        return f"assyst-testing/test/{file_name}"
    except ClientError as e:
        logging.error(e)
        return 'Failed to upload file'

# @app.route('/')
# def hello():
#     return '<h1>Hello, World!</h1>'

@app.route('/home')
def home():
   return render_template('home.html')

@app.route('/upload', methods=['POST'])
def upload():
    f = request.files['file']
    return upload_file(f)
    
# if __name__ == '__main__':
#    app.run()