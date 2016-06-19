import os
from werkzeug.utils import secure_filename
from flask import *
from multiprocessing import Process
from seam_carve import CAIS

UPLOAD_FOLDER = 'flasktestimages/'
ALLOWED_EXTENSIONS = set(['jpg', 'jpeg'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/pretty')
def index():
    return render_template('index.html')

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
        resolution = (int(request.form["width"]), int(request.form["height"]))
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            dirname = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename))
            print dirname, resolution
            if not os.path.exists(dirname):
                os.makedirs(dirname)
            file.save(os.path.join(dirname, 'og.jpg'))
            start_stuff(file.filename, resolution)
            return redirect(url_for('uploaded_file',
                                    filename=file.filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
        <input type=number name=width>
        <input type=number name=height>
         <input type=submit value=Upload>
    </form>
    '''

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(
        os.path.join(app.config['UPLOAD_FOLDER'], filename),
                               'og.jpg')

def get_og_filename(filename):
    return os.path.join(app.config['UPLOAD_FOLDER'], filename, 'og.jpg')

def get_sc_filename(filename):
    return os.path.join(app.config['UPLOAD_FOLDER'], filename, 'sc.jpg')

def get_sm_filename(filename):
    return os.path.join(app.config['UPLOAD_FOLDER'], filename, 'sm.jpg')

def get_scsm_filename(filename):
    return os.path.join(app.config['UPLOAD_FOLDER'], filename, 'scsm.jpg')

def start_stuff(filename, resolution):
    # p = Process(target=do_image_stuff, args=(filename, resolution))
    # p.start()
    print "do stuff go"
    do_image_stuff(filename, resolution)

def do_image_stuff(filename, resolution):
    dirname = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    ## TODO check if it is done (by checking if file exists)
    status_filename = os.path.join(dirname, 'started.txt')
    if os.path.isfile(status_filename):
        return
    ## write "in progress" file
    open(status_filename, 'a').close()
    ## start all the image processing stuff
    og_filename = get_og_filename(filename)

    ## seam carver
    # p_sc = Process(target=do_sc, args=(filename, resolution))
    # p_sc.start()
    ## saliency map
    # p_sm = Process(target=do_sm, args=(filename, resolution))
    # p_sm.start()
    # ## seam carver with saliency map
    # p_scsm = Process(target=do_scsm, args=(filename, resolution))
    # p_scsm.start()
    print "start"
    do_sc(filename, resolution)
    print "start"
    do_sm(filename, resolution)
    print "start"
    do_scsm(filename, resolution)

    print 'joins'
    # p_sc.join()
    # p_sm.join()
    # p_scsm.join()

    ## delete in progress file
    os.remove(status_filename)

def do_sc(filename, resolution):
    sc_filename = get_sc_filename(filename)
    if (os.path.isfile(sc_filename)):
        return
    og_filename = get_og_filename(filename)
    print 'seam carver start'
    CAIS(og_filename, resolution, sc_filename, False, 'lame_old_version')
    print 'sc done'
    return

def do_sm(filename, resolution):
    sm_filename = get_sm_filename(filename)
    if (os.path.isfile(sm_filename)):
        return
    og_filename = get_og_filename(filename)
    print 'saliency map start'
    CAIS(og_filename, resolution, sm_filename, False, 'energy')
    print 'sm done'
    return

def do_scsm(filename, resolution):
    scsm_filename = get_scsm_filename(filename)
    if (os.path.isfile(scsm_filename)):
        return
    og_filename = get_og_filename(filename)
    print 'good start'
    CAIS(og_filename, resolution, scsm_filename, False)
    print 'good done'
    return

if __name__ == '__main__':
    app.debug = True
    app.run()
