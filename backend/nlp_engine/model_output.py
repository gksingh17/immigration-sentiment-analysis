from pymongo import MongoClient
import requests
import os
import tensorflow as tf
import numpy as np
import json
import os
from dotenv import load_dotenv
import mysql.connector

load_dotenv()
def SQLConnector(prediction_summary, jobID):
    connection = mysql.connector.connect(
        user=os.getenv('MYSQL_ROOT_USERNAME'),
        password=os.getenv('MYSQL_ROOT_PASSWORD'),
        host=os.getenv('MYSQL_HOST'),
        database=os.getenv('MYSQL_DB')
    )
    try:
        with connection.cursor() as cursor:
            for label, ratio in prediction_summary.items():
                # SQL insert statement
                sql = "INSERT INTO job_output(label, ratio, job_id) VALUES(%s, %s, %s)"
                cursor.execute(sql, (label, ratio, jobID))

            # connection is not autocommit by default. So you must commit to save your changes.
            connection.commit()

    finally:
        connection.close()

def model_runner(jobID):
    try:
        CONNECTION_STRING = os.getenv('MONGO_URI')
        client= MongoClient(CONNECTION_STRING)
        db=client.get_database('Vector_Data')
        collection=db.preprocessed_data
    except Exception as e:
        print('Connection Failed')
        print(str(e))
        return
    vector_data = []
    alldocuments = collection.find({str(jobID): {'$exists': True}})
    for document in alldocuments:
        vector_data.append(document[str(jobID)])
    vector_array = np.array(vector_data)
    print(len(vector_array))
    prediction_summary = predictions(vector_array)
    SQLConnector(prediction_summary,jobID)
    # send_request(prediction_summary, jobID)
    

def predictions(padded_sequences):
    MAX_SEQUENCE_LENGTH = 100
    class_labels = ['Hateful', 'Non-Hateful', 'Neutral']
    #current_dir = os.path.dirname(os.path.abspath(__file__))
    #model_dir = os.path.abspath(os.path.join(current_dir, '..', '..', 'nlp code', 'savedModels', 'CNN_Model'))
    #relative_path = os.path.relpath(model_dir, current_dir)
    #padded_sequences= padded_sequences.reshape(padded_sequences.shape[0], padded_sequences.shape[1], 1)
    loaded_model = tf.keras.models.load_model("savedModels/CNN_Model")
    predictions = loaded_model.predict(padded_sequences)
    predicted_classes = np.argmax(predictions, axis=1)
    prediction_summary = {label: 0 for label in class_labels}
    for predicted_class in predicted_classes:
        predicted_label = class_labels[predicted_class]
        prediction_summary[predicted_label] += 1
    return prediction_summary

def send_request(prediction_summary, jobID):
    url = 'http://127.0.0.1:5000/model/result'
    data = {
        "result": prediction_summary,
        "job_id": jobID
    }
    print("In model_output")
    print(data)
    headers = {'Content-Type': 'application/json'}

    response = requests.post(url, json=data, headers=headers)
    print(f"Status Code: {response.status_code}, Response: {response.text}")

# model_runner('a4ca21c2-1444-11ee-9dcf-fefcbf0ffb95')