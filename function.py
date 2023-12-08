import tensorflow as tf
import cv2
from io import BytesIO
from google.cloud import storage
import numpy as np

def read_image_from_bucket(bucket_name, blob_name):
    """Reads an image from a GCP Storage bucket."""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    
    # Download content as bytes
    content = blob.download_as_bytes()

    # Convert the content to a numpy array
    np_array = np.frombuffer(content, np.uint8)

    # Decode the image using OpenCV
    img = cv2.imdecode(np_array, cv2.IMREAD_COLOR)
    return img

def get_prediction(image,model):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = tf.image.resize(image,(256,256))
    image = tf.expand_dims(image,axis = 0)
    predictions = model.predict(image)
    return predictions

def draw_prediction(image,model):
    #compute class mapping
    class_ids = ["salmo",'cocci','healthy','ncd',]
    class_mapping = dict(zip(range(len(class_ids)), class_ids))
    color_list = [(231,76,60),(52,152,219),(39, 231, 96),(243,156,18)]
    #get original image
    original_image = image

    #original_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB)
    width = original_image.shape[1]
    height = original_image.shape[0]

    #get scaled image
    scale_width = width / 256
    scale_height = height / 256

    #get predictions
    predictions = get_prediction(image,model)

    #get boxes, confindences and classes
    num_detections = int(predictions['num_detections'][0])
    classes = predictions['classes'][0]
    confindences = predictions['confidence'][0]
    boxes = predictions['boxes'][0]
    confidences_tmp = []
    classes_tmp = []

    for i in range(num_detections):
        class_id = int(classes[i])
        class_name = class_mapping[class_id]
        classes_tmp.append(class_name)
        confidences_tmp.append(str(confindences[i]))
        x,y,w,h = boxes[i]
        x1 = int(x * scale_width)
        y1 = int(y * scale_height)
        w = int(w * scale_width)
        h = int(h * scale_height)
        x2 = x1 + w
        y2 = y1 + h
        #check if box is out of bounds
        if x1 < 0:
            x1 = int(0 + width*0.05)
        if y1 < 0:
            y1 = int(0 + height*0.05)
        if x2 > width:
            x2 = int(width - width*0.05)
        if y2 > height:
            y2 = int(height - height*0.05)

        cv2.rectangle(original_image, (x1, y1), (x2, y2), color_list[class_id], 1)

        linewidth = min(int((x2-x1)*0.2),int((y2-y1)*0.2))
        cv2.line(original_image, (x1, y1), (x1+linewidth, y1), color_list[class_id], 4)
        cv2.line(original_image, (x1, y1), (x1, y1+linewidth), color_list[class_id], 4)
        cv2.line(original_image, (x2, y1), (x2-linewidth, y1), color_list[class_id], 4)
        cv2.line(original_image, (x2, y1), (x2, y1+linewidth), color_list[class_id], 4)

        cv2.line(original_image, (x1, y2), (x1+linewidth, y2), color_list[class_id], 4)
        cv2.line(original_image, (x1, y2), (x1, y2-linewidth), color_list[class_id], 4)
        cv2.line(original_image, (x2, y2), (x2-linewidth, y2), color_list[class_id], 4)
        cv2.line(original_image, (x2, y2), (x2, y2-linewidth), color_list[class_id], 4)

    prediction_final = {
        "num_detection":num_detections,
        "classes":classes_tmp,
        "confindences":confidences_tmp,
    }

    def upload_image_to_bucket(bucket_name, blob_name, image):
        """Uploads an image from an OpenCV image object to a GCP Storage bucket."""
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(blob_name)

        # Convert the OpenCV image to bytes
        _, img_encoded = cv2.imencode('.jpg', image)
        img_bytes = BytesIO(img_encoded.tobytes())

        # Upload the image to GCP Storage
        blob.upload_from_file(img_bytes, content_type='image/jpeg')

    # GCP Storage settings
    gcp_bucket_name = 'chickmedbuckets'
    gcp_blob_name = 'chickmed/prediction3.jpg'

    # Upload the image to GCP Storage
    upload_image_to_bucket(gcp_bucket_name, gcp_blob_name, original_image)

    #save image
    # cv2.imwrite('prediction.jpg',original_image)
    return prediction_final