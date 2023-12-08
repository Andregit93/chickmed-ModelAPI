from flask import Flask, request, jsonify
import tensorflow as tf
import keras_cv
from function import *
import io
from PIL import Image

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():

    bucket_name = "chickmedbuckets"
    destination_blob_filename = "chickmed/prediction3.jpg"
    project_name = "chickmed"

    # Configure bucket and blob
    client = storage.Client(project=project_name)
    bucket = client.bucket(bucket_name)

    # Load the image from the POST request
    im = request.files['image']

    im = Image.open(im)

    # Convert image to bytes
    bs = io.BytesIO()
    im.save(bs, "JPEG")
    bs.seek(0)

    blob = bucket.blob(destination_blob_filename)
    blob.upload_from_file(bs, content_type="image/jpeg")

    # GCP Storage settings
    gcp_bucket_name = 'chickmedbuckets'
    gcp_blob_name = 'chickmed/prediction3.jpg'

    # Read the image from GCP Storage
    image = read_image_from_bucket(gcp_bucket_name, gcp_blob_name)

    model_2 = tf.keras.models.load_model("Best_Model_YOLOv8.h5",
    custom_objects={
    "YOLOV8Detector": keras_cv.models.YOLOV8Detector,
    "YOLOV8Backbone": keras_cv.models.YOLOV8Backbone
            },
    compile = False)

    prediction = draw_prediction(image,model_2)

    message = {
        'status': 200,
        'message': 'OK',
        'result': prediction
    }

    return jsonify(message)

if __name__ == '__main__':
    app.run()