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
