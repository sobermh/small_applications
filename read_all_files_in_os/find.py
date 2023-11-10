"""
@author:mh
Code is far away from bug
"""
import os
import re

from read_all_files_in_os.oa_api import InteractiveOaApi
from read_all_files_in_os.save import SaveToMysql


class Find(SaveToMysql):
    """寻找符合条件的文件"""

    def all_files(self):
        """所有文件存为参数为dict的list"""
        try:
            sql = "select * from save_files;"
            self.cursor.execute(sql)
            res = self.cursor.fetchall()
            all_file_list = []
            for row in res:
                one_file_dict = {}
                binary_data = row[11]
                # Decode the binary data to text
                decoded_text = binary_data.decode('utf-8')
                one_file_dict["file"] = decoded_text
                one_file_dict["name"] = row[1]
                one_file_dict["ip"] = str(row[2])
                all_file_list.append(one_file_dict)
            # print(all_file_list)
            print("user in mysql:", len(all_file_list))
            return all_file_list
        except Exception as e:
            print(f"Error:{e}")

    def according_condition_find_file(self, *args):
        """根据条件找到对应的用户文件"""
        category_name_list = []

        all_file_list = self.all_files()
        for condition in args:
            name_list = []
            for file in all_file_list:
                if condition.lower() in file.get("file").lower():
                    # print(file.get("name"))
                    name_list.append(file.get("name"))
            category_name_list.append(name_list)
            # print(name_list)
        # print(category_name_list)
        return category_name_list

    def find_username(self, *args):
        """找到工号对应的人名"""
        userlist = InteractiveOaApi().get_all_oa_member()
        category_username_list = []
        # 条件
        for category_name in self.according_condition_find_file(*args):
            # 每个条件下符合条件的
            username_list = []
            for number in category_name:
                for username in userlist:
                    username_dict = {}
                    if number.lower() == username.get("username").lower():
                        username_dict[number] = username.get("name")
                        username_list.append(username_dict)
                        break
            category_username_list.append(username_list)
            # print(username_list)
        # print(category_username_list)
        return category_username_list

    def save_find_username(self, *args):
        """保存找到的用户"""
        # 在初始化时检测文件是否存在
        if os.path.exists("finally.txt"):
            # 如果文件存在，清空文件内容
            with open("finally.txt", 'w') as file:
                file.truncate(0)

        category_username_list = self.find_username(*args)
        for index in range(len(category_username_list)):
            # 写入finally
            with open(f'finally.txt', 'a', encoding="utf-8") as file:
                file.write(args[index] + '\n')
                # file.write("---------------"+'\n')
                file.write(str(category_username_list[index]) + '\n')
                file.write("---------------" + '\n')

    def find_user(self):
        """找到没有扫描的人员"""
        try:
            sql = "select name from save_files;"
            self.cursor.execute(sql)
            res = self.cursor.fetchall()
            # 数据库已扫描的
            sql_list = []
            for i in res:
                sql_list.append(i[0])
            # oa中公司所有人
            remain_list = []
            oa_user_list = InteractiveOaApi().get_all_oa_member()
            # for i in oa_user_list:
            #     oa_list.append(i["username"])
            for oa_user in oa_user_list:
                flag = 0
                for sql_user in sql_list:
                    if sql_user.lower() == oa_user["username"].lower():
                        flag = 1
                        break
                if flag == 0:
                    match = re.match(r"^\w+-1$", oa_user["username"])
                    if match is None:
                        # print(oa_user["username"])
                        # print(match.group())
                        user_dict = {
                            "name": oa_user["name"],
                            "username": oa_user["username"],
                            "subcompanyid1span_in_oa": oa_user["subcompanyid1span_in_oa"],
                            "departmentidspan_in_oa": oa_user["departmentidspan_in_oa"]
                        }
                        remain_list.append(user_dict)
            print(remain_list)
            print(len(remain_list))
        except Exception as e:
            print(f"Error:{e}")

# if __name__ == '__main__':
#     find_instance = Find()
#     # find_instance.all_files()
#     # find_instance.according_condition_find_file("cad", "photoshop")
#     # find_instance.find_username("cad", "photoshop")
#
#     # 找到符合要求的用户
#     find_instance.save_find_username("autocad", "photoshop", "solid", "altium designer", "graphpad", "matlab","pycharm")
#
#     # 找到没扫描的人
#     find_instance.find_user()
#
#     find_instance.close_db()
