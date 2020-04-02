from flask import Flask, render_template, request, redirect, url_for
import boto3
from botocore.exceptions import NoCredentialsError
import uuid

app = Flask(__name__)
ACCESS_KEY = 'AKIA5UIN4AZSHBYGSNEY'
SECRET_KEY = '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'
S3_BUCKET = 'wssacademy'


def create_temp_file(size, file_name, file_content):
    random_file_name = file_name
    with open(random_file_name, 'w') as f:
        f.write(str(file_content) * size)
    return random_file_name


@app.route('/')
@app.route('/upload', methods=['POST', 'GET'])
def upload():
    if request.method == 'POST':
        count = 0
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
            count = 1
            s3.meta.client.upload_file(Filename=first_file_name, Bucket=S3_BUCKET,
                                        Key=first_file_name)
            url = 'https://%s.s3.amazonaws.com/%s' % (S3_BUCKET, first_file_name)
            print('URL:', url)
            print('File uploaded successfully')
            return render_template('upload.html', url=url, Filename=Filename, count=count)
        except FileNotFoundError:
            print("The file was not found")
            return 'The file was not found'
        except NoCredentialsError:
            print("Credentials not available")
            return 'Credentials not available'
    else:
        return render_template('upload.html')

@app.route('/download')
def download():
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
        try: # Filename=first_file_name, Bucket=S3_BUCKET, Key=first_file_name
            s3.meta.client.download_file(Filename=first_file_name, Bucket=S3_BUCKET, Key=first_file_name)
            # print(open('/temp/aa.JPG').read())
            return "downloaded"
        except FileNotFoundError:
            print("The file was not found")
            return 'The file was not found'
        except NoCredentialsError:
            print("Credentials not available")
            return 'Credentials not available'

# s3.meta.client.download_file('mybucket', 'hello.txt', '/tmp/hello.txt')
if __name__ == '__main__':
    app.run(debug=True)