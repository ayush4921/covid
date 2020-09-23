import os
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
from os.path import join, dirname, realpath
import cv2
import image
from keras.models import model_from_json
import tensorflow as tf


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
            
            image.save('beach1.bmp')
        except:
            return render_template('index.html', results="No File Found")
        file_path = "beach1.bmp"

    def load_model():
        # load json and create model
        json_file = open('./model.json', 'r')
        loaded_model_json = json_file.read()
        json_file.close()
        loaded_model = model_from_json(loaded_model_json)
        # load weights into new model
        loaded_model.load_weights("./model.h5")
        # load training history
        #json_file = open('history.json', 'r')
        #loaded_history = json_file.read()
        #json_file.close()
        print("Loaded model from disk") 
        return loaded_model
                    
 # to load pre-saved model
    (loaded_model, history) = load_model()
    def predict_pathogen(img, loaded_model):
        image = cv2.imread(img)
        image = cv2.resize(image, (128, 128), interpolation=cv2.INTER_CUBIC)
        image = img_to_array(image)
        image = np.array(image, dtype="float") / 255.0
        image = np.expand_dims(image, axis=0)
        outcome = loaded_model.predict(image)
        print(outcome)
        return outcome
    
# test
        pathogen = predict_pathogen("./image.png", loaded_model)
        return render_template('index.html', results=result,result2=result2,pathogen=pathogen)
    return None




if __name__ == '__main__':
    app.run(debug=True)
