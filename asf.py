 # to predict assuming the file path to the image.png is
import keras
from keras.models import model_from_json
from keras.preprocessing.image import img_to_array
import cv2
import numpy as np

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
    print(outcome)
    return outcome

# test
# to load pre-saved model
loaded_model = load_model()

pathogen = predict_pathogen("./beach1.bmp", loaded_model)
