# py-aws
python sample code to connect S3 &amp; EC2

## Prerequisites

- Python 3.4 or above
- boto3 https://github.com/boto/boto3
- Flask http://flask.pocoo.org/

## Setup a virtual environment
- pull code
- run the following command
```
#python3 -m venv py-aws
#cd py-aws && source bin/activate
#pip install -r requirements.txt
```
- Add some information for this simple application
```
#vi config.py
add your AWS access ID & Key and Region
if required, change the site information for Flask
```
## How to run
- run S3 application
```
#python3 py-s3.py
test this with http://SITE_ADDRESS:SITE_PORT
```
![alt tag](https://raw.githubusercontent.com/linsijay/py-aws/master/s3_screenshot.jpg)
- run EC2 application
```
#python3 py-ec2.py
test this with http://SITE_ADDRESS:SITE_PORT
```
![alt tag](https://raw.githubusercontent.com/linsijay/py-aws/master/ec2_screenshot.jpg)
