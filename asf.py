 # to predict assuming the file path to the image.png is
! pip install keras
import keras
def load_model():
    # load json and create model
    json_file = open('../input/hellomanasn/model.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    # load weights into new model
    loaded_model.load_weights("../input/hellomanasn/model.h5")
    # load training history
    #json_file = open('history.json', 'r')
    #loaded_history = json_file.read()
    #json_file.close()
    print("Loaded model from disk") 
    return loaded_model, history
    
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
pathogen = predict_pathogen("../input/nnnnkln/beach1.bmp", loaded_model)
