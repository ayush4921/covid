import os
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
from os.path import join, dirname, realpath
import cv2
import image
from keras.models import model_from_json
from keras.preprocessing.image import img_to_array
import cv2
import tensorflow as tf
import numpy as np


UPLOADS_PATH = join(dirname(realpath(__file__)), 'static\\imgages')


ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'bmp'}
app = Flask(__name__)



# Some hard-coded info
cutoff_val = 0.5

diag_info_dict = {
    'No Finding': 'No significant result',
    'Effusion': 'Requires a medical diagnosis, Symptoms include coughing, sharp chest pain or shortness of breath.',
    'Infiltration': 'A pulmonary infiltrate is a substance denser than air, such as pus, blood, or protein, which lingers within the parenchyma of the lungs. Pulmonary infiltrates are associated with pneumonia, tuberculosis, and nocardiosis',
    'Atelectasis': 'There may be no obvious symptoms of atelectasis. When symptoms occur, they may include trouble breathing, cough and low-grade fever.',
    'Edema': 'Depending on the cause, pulmonary oedema symptoms may appear suddenly or develop over time. Mild to extreme breathing difficulty can occur. Cough, chest pain and fatigue are other symptoms.',
    'Consolidation': 'Lung consolidation occurs when the air that usually fills the small airways in your lungs isreplaced with something else. Depending on the cause, the air may be replaced with: a fluid, such as pus, blood, or water, or a solid, such as stomach contents or cells',
    'Mass': 'Consider serious medical diagnosis. Lung cancer is a mass or growth in the lung made up of cancer cells, but not all masses in the lung are caused by cancer',
    'Nodule': 'A lung nodule or pulmonary nodule is a relatively small focal density in the lung. A solitary pulmonary nodule or coin lesion, is a mass in the lung smaller than 3 centimeters in diameter. There may also be multiple nodules. One or more lung nodules can be an incidental finding found in up to 0.2% of chest X-rays and around 1% of CT scans.',
    'Fibrosis': 'Pulmonary fibrosis is a lung disease that occurs when lung tissue becomes damaged and scarred. Causes of pulmonary fibrosis include environmental pollutants, some medicines, some connective tissue diseases, and interstitial lung disease.'
}


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

            # to load pre-saved model
            loaded_model = load_model()

            image = request.files['image']
            
            image.save('temp_image.bmp')

            pathogen = predict_pathogen("./temp_image.bmp", loaded_model)

            current_labels = ['No Finding', 'Effusion', 'Infiltration', 'Atelectasis', 'Edema', 'Consolidation', 'Mass', 'Nodule', 'Fibrosis']

            pathogen = pathogen[0]

            result_dict = dict(zip(current_labels, pathogen))

            filtered_list = []



            for key, value in result_dict.items():
                if value > cutoff_val:
                    if key in diag_info_dict.keys():
                        filtered_list.append([key, str(value), diag_info_dict[key]])
                    else:
                        filtered_list.append([key, str(value), 'No additional info'])


            result = ','.join([travel, tiredcough, breath, exposure])

            result2 = 'result 2'

            return render_template('index.html', results=result, result2=result2, pathogen=filtered_list)

        except:

            return render_template('index.html', results="No File Found")


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


def predict_pathogen(img, loaded_model):
    image = cv2.imread(img)
    image = cv2.resize(image, (128, 128), interpolation=cv2.INTER_CUBIC)
    image = img_to_array(image)
    image = np.array(image, dtype="float") / 255.0
    image = np.expand_dims(image, axis=0)
    outcome = loaded_model.predict(image)
    #print(outcome)
    return outcome


if __name__ == '__main__':
    app.run(debug=True)
