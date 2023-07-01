from pymongo import MongoClient
import requests
import os
import tensorflow as tf
import numpy as np
import json
import os
from dotenv import load_dotenv
import mysql.connector
from flask import Flask
from flask import request, jsonify, Response
app = Flask(__name__)

load_dotenv()

# mise en place
savedModels={1: "savedModels/CNN_Model", 2: "savedModels/LSTM_Model"}
@app.route("/api/callmodel", methods=['POST'])
def model_runner():
    data = request.json
    jobID = data.get('jobID')
    model_id = data.get('model_id')
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
    prediction_summary = predictions(vector_array, model_id)
    if SQLConnector(prediction_summary, jobID):
        return jsonify({'status': 'success', 'message': 'Model execution completed successfully'}), 200
    else:
        return jsonify({'status': 'error', 'message': 'Failed to execute model_runner'}), 500


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
            return True

    except Exception as e:
        # Handle the exception or log the error if needed
        print(f"An error occurred while storing data: {str(e)}")
        return False

    finally:
        connection.close()

    # send_request(prediction_summary, jobID)
    

def predictions(padded_sequences, model_id):
    class_labels = ['Hateful', 'Non-Hateful', 'Neutral']
    loaded_model = tf.keras.models.load_model(savedModels[model_id])
    predictions = loaded_model.predict(padded_sequences)
    predicted_classes = np.argmax(predictions, axis=1)
    prediction_summary = {label: 0 for label in class_labels}
    for predicted_class in predicted_classes:
        predicted_label = class_labels[predicted_class]
        prediction_summary[predicted_label] += 1
    return prediction_summary


if __name__ == '__main__':
    app.run(debug = True, port=5003)
# model_runner('a4ca21c2-1444-11ee-9dcf-fefcbf0ffb95')