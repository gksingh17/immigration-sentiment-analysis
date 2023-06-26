import time

import pymysql
from app import app
from config import mysql
from flask import jsonify
from flask import flash, request
import uuid
import json
import requests
from datetime import datetime
from backend.data_service.YTComment import process_comments
from flask_cors import CORS, cross_origin


@app.route('/model')
def model():
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM model_output")
        modelRows = cursor.fetchall()
        response = jsonify(modelRows)
        response.status_code = 200
        return response
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route('/comments', methods=['POST'])
@cross_origin()
def comments():
    conn = None
    cursor = None
    response = "model return nothing!"
    try:
        _json = request.json
        _number = _json['number']
        _url = _json['url']
        if _number and _url and request.method == 'POST':
            job_id = str(uuid.uuid1())

            # datetime object containing current date and time
            job_time = datetime.now()

            # r = requests.post('http://localhost:5000/data', json={
            # "job_id": job_id,
            # "url": _url
            # })
            # print(f"Status Code: {r.status_code}, Response: {r.json()}")

            # call data service
            print("call service...")
            process_comments(_url, _number, job_id)

            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            sqlQuery = "INSERT INTO job(id, video_link, job_time) VALUES(%s, %s, %s)"
            bindData = (job_id, _url, job_time)
            cursor.execute(sqlQuery, bindData)
            conn.commit()

            # while (get_result(job_id)==[]):
            time.sleep(15)
            resultRows=get_result(job_id)
            print("result: ",resultRows)
            print("get data from database!")
            response = jsonify(resultRows)
            response.status_code = 200
    except Exception as e:
        print(e)
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
    return response

@app.route('/model/result', methods=['POST'])
@cross_origin()
def model_output():
    conn = None
    cursor = None
    try:
        _json = request.json
        _result = _json["result"]
        job_id = _json["job_id"]
        print("before result")
        print(_result, job_id)

        # if _result and job_id and request.method == 'POST':
        # store result into database
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)

        # iterate over each result and insert into database
        for label, ratio in _result.items():
            # SQL insert statement
            sql = "INSERT INTO job_output(label, ratio, job_id) VALUES(%s, %s, %s)"
            cursor.execute(sql, (label, ratio, job_id))
        conn.commit()
        return jsonify(message='result added successfully!', status=200)
    except Exception as e:
        print(e)
        return jsonify(message=str(e), status=500) # added this line
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()




@app.errorhandler(404)
def showMessage(error=None):
    message = {
        'status': 404,
        'message': 'Record not found: ' + request.url,
    }
    response = jsonify(message)
    response.status_code = 404
    return response


def get_result(job_id):
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    # try to get model output from DB
    sqlQuery = "SELECT * FROM job_output where job_id=%s"
    cursor.execute(sqlQuery, (job_id,))
    resultRows = cursor.fetchall()
    print("length of result "+str(len(resultRows)))
    return resultRows


if __name__ == "__main__":
    app.run(debug=True)
