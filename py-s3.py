"""
simple sample to access S3 service
"""
import os, botocore
import config as cfg
from boto3 import client
from boto3.s3.transfer import S3Transfer
from flask import Flask, request, render_template, redirect, url_for, send_file, make_response
from werkzeug import secure_filename

# create a S3 service client
client = client('s3', 
                aws_access_key_id = cfg.AWS_ACCESS_ID, 
                aws_secret_access_key=cfg.AWS_ACCESS_KEY, 
                region_name=cfg.AWS_ACCESS_REGION)

app = Flask(__name__)


@app.route('/')
def show_bucket():
    """
    list all buckets in your S3 service
    
    :return: flask render template
    """
    buckets = client.list_buckets()
    return render_template('show_bucket.html', buckets=buckets)

@app.route('/bucket/<bucket_name>', methods=['GET', 'POST'])
def show_file(bucket_name):
    """
    if request method is GET, list all files in this bucket, otherwise upload file to S3
    
    :return: flask render template
    """
    try:
        if request.method == 'GET':
            objects = client.list_objects(Bucket=bucket_name)
            return render_template('show_file.html', files=objects, bucket_name=bucket_name)
        else:
            file = request.files['file']
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            upload_file_to_s3(bucket_name, filename)
            remove_temp_file(filename)
            return redirect(url_for('show_file', bucket_name=bucket_name))
    except botocore.exceptions.ClientError as e:
        return render_template('show_error.html', error_msg=str(e.response['Error']))

@app.route('/download/<bucket_name>/<filename>', methods=['GET', 'POST'])
def download_file_from_s3(bucket_name, filename):
    """
    download the file from S3 and return to user
    
    :return: file object
    """
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    transfer = S3Transfer(client)
    try:
        transfer.download_file(bucket_name, filename, filepath)
        return send_file(filepath, as_attachment=True)
    except botocore.exceptions.ClientError as e:
        return render_template('show_error.html', error_msg=str(e.response['Error']))

def upload_file_to_s3(bucket_name, filename):
    """
    create a S3Transfer to upload the file to S3
    """
    transfer = S3Transfer(client)
    transfer.upload_file(os.path.join(app.config['UPLOAD_FOLDER'], filename),
                        bucket_name,
                        filename)

def remove_temp_file(filename):
    """
    remove the temporary file
    """
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(filepath) and os.path.isfile(filepath):
        os.unlink(filepath)

if __name__ == '__main__':
    # a temp folder for uploading
    app.config['UPLOAD_FOLDER'] = cfg.SITE_UPLOAD_TMP_FOLDER
    
    # limit the upload file size
    app.config['MAX_CONTENT_LENGTH'] = 64 * 1024 * 1024
    
    # run flask app according to specific setting
    app.run(host=cfg.SITE_ADDRESS, 
            port=cfg.SITE_PORT, 
            debug=cfg.SITE_DEBUG)

