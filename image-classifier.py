import os
from flask import Flask, flash, request, redirect, url_for, jsonify
from flask import render_template
from werkzeug.contrib.fixers import ProxyFix

from cnncifar10use import predict as nn_predict

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)

CLASSES = ['airplane', 'automobile', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 'truck']
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(APP_ROOT, 'static/uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['APP_ROOT'] = APP_ROOT
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        print("/upload post request")
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        print(file)
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(path)
            (pred_f),(pred) = nn_predict(path, app.config['APP_ROOT'])
            result = CLASSES[pred]
            print("%s"%result)
            # os.remove(path)
            for the_file in os.listdir(app.config['UPLOAD_FOLDER']):
                fp = os.path.join(app.config['UPLOAD_FOLDER'], the_file)
                try:
                    if os.path.isfile(fp):
                        os.unlink(fp)
                except Exception as e:
                    print(e)
            return jsonify(class_of_image=result)
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''


@app.route('/')
def hello_world():
    return render_template('home.html')


if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run()
