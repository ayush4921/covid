import os
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
from os.path import join, dirname, realpath
from google.cloud import automl
import image
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="abc.json"
# TODO(developer): Uncomment and set the following variables
project_id = "refreshing-cat-289711"
model_id = "ICN7554104478681530368"

prediction_client = automl.PredictionServiceClient()

# Get the full path of the model.
model_full_id = automl.AutoMlClient.model_path(
    project_id, "us-central1", model_id
)

prediction_client = automl.PredictionServiceClient()


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

        with open(file_path, "rb") as content_file:
            content = content_file.read()
        image = automl.Image(image_bytes=content)
        payload = automl.ExamplePayload(image=image)

        # params is additional domain-specific parameters.
        # score_threshold is used to filter the result
        # https://cloud.google.com/automl/docs/reference/rpc/google.cloud.automl.v1#predictrequest
        params = {"score_threshold": "0.8"}

        request2 = automl.PredictRequest(
            name=model_full_id,
            payload=payload,
            params=params
        )
        # 'content' is base-64-encoded image data.

        response = prediction_client.predict(request=request2)

        for result in response.payload:
            var1 = result.display_name
            var2 = result.classification




        result2='Disease: ',var1,' Probability of disease: ',var2
        result = 'here, '+travel, tiredcough, breath, exposure+" you go"
        return render_template('index.html', results=result,result2=result2)
    return None




if __name__ == '__main__':
    app.run(debug=True)
