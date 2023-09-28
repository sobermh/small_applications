"""
@author:maohui
@time:9/11/2023 9:00 AM
  　　　　　　　 ┏┓    ┏┓+ +
  　　　　　　　┏┛┻━━━━┛┻┓ + +
  　　　　　　　┃        ┃ 　 
  　　　　　　　┃     ━  ┃ ++ + + +
  　　　　　 　████━████ ┃+
  　　　　　　　┃        ┃ +
  　　　　　　　┃   ┻    ┃
  　　　　　　　┃        ┃ + +
  　　　　　　　┗━┓   ┏━━┛
  　　　　　　　  ┃   ┃
  　　　　　　　  ┃   ┃ + + + +
  　　　　　　　  ┃   ┃　　　Code is far away from bug with the animal protecting
  　　　　　　　  ┃   ┃+ 　　　　神兽保佑,代码无bug
  　　　　　　　  ┃   ┃
  　　　　　　　  ┃   ┃　　+
  　　　　　　　  ┃   ┗━━━━━━━┓ + +     
  　　　　　　　  ┃           ┣┓
  　　　　　　　  ┃           ┏┛
  　　　　　　　  ┗┓┓┏━━━━━┳┓┏┛ + + + +
  　　　　　　　   ┃┫┫     ┃┫┫
  　　　　　　　   ┗┻┛     ┗┻┛+ + + +
"""
import asyncio
import datetime
import time

import pymysql


class SaveToMysql:
    def __init__(self):
        try:
            # self.db = pymysql.connect(host='47.97.118.247',
            #                           user='root',
            #                           password='sober123',
            #                           database='small_applications',
            #                           charset='utf8')
            self.db = pymysql.connect(host='',
                                      user='',
                                      password='',
                                      database='small_applications',
                                      charset='utf8')

            # 使用 cursor() 方法创建一个游标对象 cursor
            self.cursor = self.db.cursor()

            # 使用 execute()  方法执行 SQL 查询
            self.cursor.execute("SELECT VERSION()")

            # 使用 fetchone() 方法获取单条数据.
            data = self.cursor.fetchone()
            print("数据库连接成功！")
        except Exception as e:
            print(e)

        # 关闭数据库连接
        # self.db.close()

    def create_table(self):
        """创建数据库表"""
        sql = """create table if not exists save_files(
                id          int(11) primary key auto_increment,
                name        varchar(25),
                ip          varchar(25) not null,
                mac         varchar(100),
                memory      varchar(25),
                cpu         varchar(100),
                device_name varchar(100),
                os_version  varchar(100),
                flash       varchar(255),
                is_success  boolean,
                error_msg   varchar(255),
                file_data   longblob,
                update_time datetime,
                create_time datetime
        ); """
        self.cursor.execute(sql)
        print("数据表创建成功")

    def insert_data(self, name, ip, mac, memory, cpu, device_name, os_version, flash, is_success, error_msg, data_txt):
        """save files and os data"""
        # print(name,ip, memory, cpu, error_msg, data_txt)
        try:
            sql = f"""
                insert into save_files(`name`,`ip`,`mac`, `memory`, `cpu`,`device_name`,`os_version`,`flash`,`is_success`,
                `error_msg`,`file_data`, `create_time`, `update_time`) values ( %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);
            """
            create_time = datetime.datetime.now()
            update_time = datetime.datetime.now()
            values = (
                name, ip, mac, memory, cpu, device_name, os_version, flash, is_success, error_msg, data_txt,
                create_time,
                update_time)
            self.cursor.execute(sql, values)
            self.db.commit()
        except Exception as e:
            print(e)
            raise e

    def read_data(self, ip=None):
        """read data from database"""
        try:
            if ip:
                sql = "select * from save_files where ip = %s;"
                self.cursor.execute(sql, ip)
            else:
                sql = "select * from save_files;"
                self.cursor.execute(sql)
            res = self.cursor.fetchall()
            for row in res:
                # print(row)
                with open(f'../files/{row[1]}_{row[2]}.txt', 'wb') as file:
                    file.write(row[11])
                    # print(file.read())
                    print("BLOB data successfully converted and saved as output.txt")
        except Exception as e:
            print(f"Error:{e}")

    def read_scan_times(self, ip):
        """select times that one ip scan """
        sql = f"""
            select count(*) from save_files where ip = %s and is_success=1; 
        """
        values = ip
        self.cursor.execute(sql, ip)
        row = self.cursor.fetchone()
        return row[0]

    def close_db(self):
        self.db.close()


if __name__ == '__main__':
    instance = SaveToMysql()
    # instance.create_table()
    instance.read_data()
    # instance.read_data('172.16.10.123')
    instance.close_db()
