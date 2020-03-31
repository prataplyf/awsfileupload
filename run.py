from flask import Flask, render_template, request
import boto3
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        print(file.filename)
        s3 = boto3.resource('s3')
        s3.meta.client.upload_file('/temp/hello.txt', 'wssacademy', file)
        return 'Uploaded'

# @app.route('/download')
# def download():
#     s3 = boto3.resource('s3')
#     s3.meta.client.download_file('wssacademy', 'aa.JPG', '/temp/aa.JPG')
#     print(open('/temp/aa.JPG').read())
#     return "downloaded"


if __name__ == '__main__':
    app.run(debug=True)