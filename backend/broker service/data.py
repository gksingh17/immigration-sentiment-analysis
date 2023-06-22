import pandas as pd
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv
# pip install python-dotenv
from app import app
from flaskext.mysql import MySQL
load_dotenv()

import pandas as pd
import pymysql

# 读取 Excel 文件
df = pd.read_excel('/Users/vincent/Desktop/UCD/courses/team project/YoutubeComments.xlsx', engine='openpyxl')

# 创建数据库连接
connection = pymysql.connect(
                             host=os.getenv('MYSQL_HOST'),
                             user=os.getenv('MYSQL_ROOT_USERNAME'),
                             password=os.getenv('MYSQL_ROOT_PASSWORD'),
                             database=os.getenv('MYSQL_DB')
                             )

try:
    with connection.cursor() as cursor:
        # 准备 SQL 插入语句
        # 假设 Excel 文件有三列：column1, column2, column3
        sql = "INSERT INTO `model_output` (`text`, `label`) VALUES (%s, %s)"

        # 循环读取 DataFrame 的每一行数据
        for row in df.itertuples(index=False):
            # 使用预处理语句插入数据
            cursor.execute(sql, row)

    # 提交数据库事务
    connection.commit()
finally:
    # 关闭数据库连接
    connection.close()