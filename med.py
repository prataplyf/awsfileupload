from flask import Flask, render_template, request
import boto3
from botocore.exceptions import NoCredentialsError
import uuid

app = Flask(__name__)
ACCESS_KEY = 'AKIA5UIN4AZSH5WAA2DM'
SECRET_KEY = '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'
S3_BUCKET = 'wssacademy'

def create_bucket_name(bucket_prefix):
    # The generated bucket name must be between 3 and 63 chars long
    return ''.join([bucket_prefix, str(uuid.uuid4())])

def create_bucket(bucket_prefix, s3_connection):
    session = boto3.session.Session()
    current_region = session.region_name
    bucket_name = create_bucket_name(bucket_prefix)
    bucket_response = s3_connection.create_bucket(
        Bucket=bucket_name,
        CreateBucketConfiguration={
        'LocationConstraint': current_region})
    print(bucket_name, current_region)
    return bucket_name, bucket_response

def create_temp_file(size, file_name, file_content):
    random_file_name = file_name
    with open(random_file_name, 'w') as f:
        f.write(str(file_content) * size)
    return random_file_name


@app.route('/')
def index():
    return render_template('upload.html')


@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        print(file)
        print(file.filename)
        print(type(file.filename))
        Filename = file.filename
        first_file_name = create_temp_file(300, Filename, file)
        s3 = boto3.resource('s3',
                            aws_access_key_id=ACCESS_KEY,
                            aws_secret_access_key=SECRET_KEY)
        try:
            # first_bucket_name, first_response = create_bucket(bucket_prefix='firstpythonbucket', s3_connection=s3.meta.client)
            s3.meta.client.upload_file(Filename=first_file_name, Bucket=S3_BUCKET,
                                        Key=first_file_name)
            # s3.meta.client.upload_file(Filename, S3_BUCKET, file)
            print("Upload Successful")
            # wssacademy is my s3_bucket name
            # file is used to be upload
            # /temp/ is folder inside 'wssacademy' s3_bucket and want to store with 'hello.txt' file name
            return 'Uploaded'
        except FileNotFoundError:
            print("The file was not found")
            return 'The file was not found'
        except NoCredentialsError:
            print("Credentials not available")
            return 'Credentials not available'

# @app.route('/download')
# def download():
#     s3 = boto3.resource('s3')
#     s3.meta.client.download_file('wssacademy', 'aa.JPG', '/temp/aa.JPG')
#     print(open('/temp/aa.JPG').read())
#     return "downloaded"


if __name__ == '__main__':
    app.run(debug=True)