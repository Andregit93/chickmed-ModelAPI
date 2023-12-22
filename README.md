<h1 align="center">ChickMed - Chicken Disease Detection</h1>
<h2>Prediction Model API Documentation</h2>

## 🛠️ Installation Steps

1. Clone the repository

```bash
git clone https://github.com/Andregit93/chickmed-ModelAPI.git
```

2. Change the working directory

```bash
cd chickmed-ModelAPI
```

3. Install dependencies

```bash
!pip install -r requirements.txt
```

4. Run the app

```bash
python main.py
```

## 📝 REST API Documentation

The REST API to the ChickMed Prediction Model is described below.

## Create Prediction Request

### Request

`POST /predict/`

     http://localhost:8000/predict

### Response

    message = {
        'user_id': user_id,
        'status': 200,
        'message': 'OK',
        'data': results,
        'processed_image': image_processed_url,
        'raw_image': "https://storage.cloud.google.com/chickmedbuckets/" + raw_image_url,
        'date': time_now
    }



## 🏆 Contributor

1. Syair Dafiq Faizur Rahman (M200BSY0683) - ML - Universitas Diponegoro
2. Jihan Apriliani Nurhasanah (M116BSX1565) - ML - Institut Teknologi Kalimantan
3. Muhammad Insan Kamil (M116BSY0541) - ML - Institut Teknologi Kalimantan
4. Oktonius Zevanya Simanungkalit (C172BSY3184) - CC - Universitas Mikroskil
5. Andre Sevtian (C687BSY4375) - CC - - Universitas Muhammadiyah Bangka Belitung
6. Hengki Agung Prayoga (A116BSY2327) - MD -Institut Teknologi Kalimantan

<h3 align="left">Languages and Tools:</h3>
<p align="left"> <a href="https://cloud.google.com" target="_blank" rel="noreferrer"> <img src="https://www.vectorlogo.zone/logos/google_cloud/google_cloud-icon.svg" alt="gcp" width="40" height="40"/> </a>  <a href="https://www.python.org/" target="_blank" rel="noreferrer"> <img src="https://banner2.cleanpng.com/20180412/kye/kisspng-python-programming-language-computer-programming-language-5acfdc3636bac7.8891188615235717662242.jpg" alt="react" width="40" height="40"/> </a> <a href="https://flask.palletsprojects.com/en/3.0.x/" target="_blank" rel="noreferrer"> <img src="https://seeklogo.com/images/F/flask-logo-44C507ABB7-seeklogo.com.png" alt="tailwind" width="40" height="40"/> </a> </p>