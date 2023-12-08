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

    model = load_model('model.h5')

    results, image_processed = draw_prediction(image, model)
    # Upload the image to GCP Storage
    image_processed_url = upload_image_to_bucket(
        gcp_bucket_name, gcp_blob_name, image_processed)

    message = {
        'status': 200,
        'message': 'OK',
        'data': results,
        'image_url': image_processed_url
    }

    return jsonify(message)


if __name__ == '__main__':
    app.run()
