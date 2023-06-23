import pandas as pd
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv
# pip install python-dotenv
from app import app
from flaskext.mysql import MySQL
import pandas as pd
import pymysql

load_dotenv()

# read Excel file
df = pd.read_excel('/Users/vincent/Desktop/UCD/courses/team project/YoutubeComments.xlsx', engine='openpyxl')

# create db conn
connection = pymysql.connect(
                             host=os.getenv('MYSQL_HOST'),
                             user=os.getenv('MYSQL_ROOT_USERNAME'),
                             password=os.getenv('MYSQL_ROOT_PASSWORD'),
                             database=os.getenv('MYSQL_DB')
                             )

try:
    with connection.cursor() as cursor:
        # prepare SQL insert statement
        # 
        sql = "INSERT INTO `model_output` (`text`, `label`) VALUES (%s, %s)"

        # loop read DataFrame lines 
        for row in df.itertuples(index=False):
            # insert data by using prepared statement
            cursor.execute(sql, row)

    # tansaction commit
    connection.commit()
finally:
    # db close
    connection.close()