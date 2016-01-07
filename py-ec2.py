"""
simple sample to start/stop EC2 instance
"""
import os, botocore
import config as cfg
from boto3 import client
from flask import Flask, render_template, redirect

# create EC2 service client
client = client('ec2', 
                aws_access_key_id = cfg.AWS_ACCESS_ID, 
                aws_secret_access_key=cfg.AWS_ACCESS_KEY, 
                region_name=cfg.AWS_ACCESS_REGION)

app = Flask(__name__)


@app.route('/')
def show_instance():
    """
    list all instance in your EC2 service
    """
    instances = client.describe_instances()
    return render_template('show_instance.html', reservations=instances['Reservations'])

@app.route('/start/<instanceid>')
def start_instance(instanceid):
    """
    start the specific EC2 instance
    """
    try:
        response = client.start_instances(InstanceIds=[instanceid])
        return redirect('/')
    except botocore.exceptions.ClientError as e:
        return render_template('show_error.html', error_msg=str(e.response['Error']))

@app.route('/stop/<instanceid>')
def stop_instance(instanceid):
    """
    stop the specific EC2 instance
    """
    try:
        response = client.stop_instances(InstanceIds=[instanceid])
        return redirect('/')
    except botocore.exceptions.ClientError as e:
        return render_template('show_error.html', error_msg=str(e.response['Error']))

if __name__ == '__main__':   
    # run flask app according to specific setting
    app.run(host=cfg.SITE_ADDRESS, 
            port=cfg.SITE_PORT, 
            debug=cfg.SITE_DEBUG)

