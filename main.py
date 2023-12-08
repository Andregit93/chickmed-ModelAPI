from flask import Flask, request, jsonify
import tensorflow as tf
import keras_cv
from function import *

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
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