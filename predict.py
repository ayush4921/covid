from google.cloud import automl
import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="abc.json"
# TODO(developer): Uncomment and set the following variables
project_id = "refreshing-cat-289711"
model_id = "ICN7554104478681530368"

file_path = "abc.jpg"

prediction_client = automl.PredictionServiceClient()

# Get the full path of the model.
model_full_id = automl.AutoMlClient.model_path(
    project_id, "us-central1", model_id
)

prediction_client = automl.PredictionServiceClient()

# Read the file.
with open(file_path, "rb") as content_file:
    content = content_file.read()

image = automl.Image(image_bytes=content)
payload = automl.ExamplePayload(image=image)

# params is additional domain-specific parameters.
# score_threshold is used to filter the result
# https://cloud.google.com/automl/docs/reference/rpc/google.cloud.automl.v1#predictrequest
params = {"score_threshold": "0.8"}

request = automl.PredictRequest(
    name=model_full_id,
    payload=payload,
    params=params
)
# 'content' is base-64-encoded image data.



response = prediction_client.predict(request=request)

print("Prediction results:")
for result in response.payload:
    print("Predicted class name: {}".format(result.display_name))
    print(
        "Predicted class{}".format(
            result.classification
        )
    )


