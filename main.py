from flask import Flask, request, jsonify
import tensorflow as tf
import keras_cv
from function import *
import datetime
import io
from PIL import Image

app = Flask(__name__)


@app.route('/predict', methods=['POST'])
def predict():

    time_now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    original_file_name = 'original_image' + '_' + time_now + '.jpg'

    bucket_name = "chickmedbuckets"
    raw_image_url = "raw_images/" + original_file_name
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

    blob = bucket.blob(raw_image_url)
    blob.upload_from_file(bs, content_type="image/jpeg")

    # GCP Storage settings
    gcp_bucket_name = 'chickmedbuckets'

    # Read the image from GCP Storage
    image = read_image_from_bucket(gcp_bucket_name, raw_image_url)

    model = load_model('model.h5')

    processed_file_name = 'processed_images/process_image' + '_' + time_now + '.jpg'

    results, image_processed = draw_prediction(image, model)
    # Upload the image to GCP Storage
    image_processed_url = upload_image_to_bucket(
        gcp_bucket_name, processed_file_name, image_processed)

    message = {
        'status': 200,
        'message': 'OK',
        'data': results,
        'image_url': image_processed_url,
        'date': time_now
    }

    store_to_db(results, image_processed_url, time_now)

    return jsonify(message)


if __name__ == '__main__':
    app.run()
