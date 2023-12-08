from tqdm.auto import tqdm
import xml.etree.ElementTree as ET
import tensorflow as tf
from tensorflow import keras
from itertools import chain
import cv2
from function import *
from google.cloud import storage
import io
from io import BytesIO
from PIL import Image
import numpy as np
import keras_cv

# Define variables
bucket_name = "chickmedbuckets"
destination_blob_filename = "chickmed/prediction3.jpg"
project_name = "chickmed"

# Configure bucket and blob
client = storage.Client(project=project_name)
bucket = client.bucket(bucket_name)

# Load the image
im = Image.open("cocci.1.jpg")

# Convert image to bytes
bs = io.BytesIO()
im.save(bs, "JPEG")
bs.seek(0)

blob = bucket.blob(destination_blob_filename)
blob.upload_from_file(bs, content_type="image/jpeg")

# # GCP Storage settings
# gcp_bucket_name = 'chickmedbuckets'
# gcp_blob_name = 'chickmed/prediction3.jpg'

# Read the image from GCP Storage
# image = read_image_from_bucket(gcp_bucket_name, gcp_blob_name)

# model_2 = tf.keras.models.load_model("Best_Model_YOLOv8.h5",
# custom_objects={
# "YOLOV8Detector": keras_cv.models.YOLOV8Detector,
# "YOLOV8Backbone": keras_cv.models.YOLOV8Backbone
#         },
# compile = False)

# prediction = draw_prediction(image,model_2)

# print(type(prediction))

# def upload_image_to_bucket(bucket_name, blob_name, image):
#         """Uploads an image from an OpenCV image object to a GCP Storage bucket."""
#         storage_client = storage.Client()
#         bucket = storage_client.bucket(bucket_name)
#         blob = bucket.blob(blob_name)

#         # Convert the OpenCV image to bytes
#         _, img_encoded = cv2.imencode('.jpg', image)
#         img_bytes = BytesIO(img_encoded.tobytes())

#         # Upload the image to GCP Storage
#         blob.upload_from_file(img_bytes, content_type='image/jpeg')

# # GCP Storage settings
# gcp_bucket_name = 'chickmedbuckets'
# gcp_blob_name = 'chickmed/prediction3.jpg'

        
# width, height = 640, 480
# image = np.zeros((height, width, 3), dtype=np.uint8)  

# # Upload the image to GCP Storage
# upload_image_to_bucket(gcp_bucket_name, gcp_blob_name, image)

    

# print(type(message))