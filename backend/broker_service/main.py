import pymysql
from app import app
from config import mysql
from flask import jsonify
from flask import flash, request
import uuid
import requests
from datetime import datetime


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
def comments():
    try:
        _json = request.json
        _user = _json['user']
        _url = _json['url']
        if _user and _url and request.method == 'POST':
            job_id = uuid.uuid1()
            
            # datetime object containing current date and time
            now = datetime.now()
            # dd/mm/YY H:M:S
            job_time = now.strftime("%d/%m/%Y %H:%M:%S")
            # r = requests.post('http://localhost:5000/data', json={
            # "job_id": job_id,
            # "url": _url
            # })
            # print(f"Status Code: {r.status_code}, Response: {r.json()}")
            
            # call data service
            get_comments(job_id, _url)

            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)		
            sqlQuery = "INSERT INTO job(id, video_link, job_time) VALUES(%s, %s, %s)"
            bindData = (job_id, _url, job_time)            
            cursor.execute(sqlQuery, bindData)
            conn.commit()
            response = jsonify('Job added successfully!')
            response.status_code = 200
            return response
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        conn.close()  

@app.route('model/result', methods=['POST']) 
def model_output():
    try:
        _json = request.json
        _result = _json['result']
        job_id = _json['job_id']

        # send back to client
        r = requests.post('http://localhost:3000/result', json={
            "job_id": job_id,
            "result": _result
            })
        print(f"Status Code: {r.status_code}, Response: {r.json()}")
        
        #store result into database
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)		
        sqlQuery = "INSERT INTO job_output(label, ratio, job_id) VALUES(%s, %s, %s)"
        
        for each in _result:
            for k, v in each.items():
                bindData = (k, v, job_id)
                cursor.execute(sqlQuery, bindData)
        conn.commit()
        response = jsonify('result added successfully!')
        response.status_code = 200
        return response
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
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
        
if __name__ == "__main__":
    app.run()
