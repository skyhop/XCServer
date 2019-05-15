import os
from flask import Flask, flash, request, redirect, url_for, jsonify
from werkzeug.utils import secure_filename
import xcsoar

UPLOAD_FOLDER = './UPLOADS/'
ALLOWED_EXTENSIONS = set(['igc'])

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
  return '.' in filename and \
    filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
  if request.method == 'POST':
    # check if the post request has the file part
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    # if user does not select file, browser also
    # submit an empty part without filename
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(path)

        flight = xcsoar.Flight(path, False)
        times = flight.times()

        for dtime in times:
          takeoff = dtime['takeoff']
          release = dtime['release']
          landing = dtime['landing']

        fixes = flight.path(takeoff['time'], release['time'])

        flight.reduce(takeoff['time'], landing['time'], max_points=10)

        analysis = flight.analyse(takeoff=takeoff['time'],
                                  scoring_start=release['time'],
                                  scoring_end=landing['time'],
                                  landing=landing['time'])
        os.remove(path)
        return jsonify(analysis)

  return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''