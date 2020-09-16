import os
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
from os.path import join, dirname, realpath

UPLOADS_PATH = join(dirname(realpath(__file__)), 'static\\imgages')


ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def hello_world():
    return render_template("index.html")

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/inputform", methods=["GET", "POST"])

def input_symptoms():
    

    if request.method == 'POST':
        travel = str(request.form['travel'])
        tiredcough = str(request.form['commonsym'])
        breath = str(request.form['majorsym'])
        exposure = str(request.form['exposure'])
        try:

            image = request.files['image']
            
            image.save(os.path.join(UPLOADS_PATH, secure_filename(image.filename)))
        except:
            return render_template('index.html', results="No File Found")

            
        result = 'here, '+travel, tiredcough, breath, exposure+" you go"
        return render_template('index.html', results=result)
    return None




if __name__ == '__main__':
    app.run(debug=True)
