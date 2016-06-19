import os
from werkzeug.utils import secure_filename
from flask import *

UPLOAD_FOLDER = 'flasktestimages/'
ALLOWED_EXTENSIONS = set(['jpg', 'jpeg'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# @app.route('/')
# def index():
#     return render_template('index.html')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            dirname = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename))
            print dirname
            if not os.path.exists(dirname):
                os.makedirs(dirname)
            file.save(os.path.join(dirname, 'og.jpg'))
            return redirect(url_for('uploaded_file',
                                    filename=file.filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(
        os.path.join(app.config['UPLOAD_FOLDER'], filename),
                               'og.jpg')

if __name__ == '__main__':
    app.debug = True
    app.run()
