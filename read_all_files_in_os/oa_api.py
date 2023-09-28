"""
@author:maohui
@time:12/29/2022 9:59 AM
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
# from xpinyin import Pinyin
#
# from apps.user.models import User
import requests




# oa服务访问地址
OA_HOST = "http://39.170.75.112:9019"
# OA超级管理员账号
OA_SUPER_USERNAME = "idc"
OA_SUPER_PASSWORD = "idc!@123456"



class HRM:
    """
    人力资源
    """

    def __init__(self, username=OA_SUPER_USERNAME, password=OA_SUPER_PASSWORD):
        """初始化登录超级管理员账号"""
        self.username = username
        self.password = password
        # self.session = requests.session()
        self.cookie = self.checklogin().headers.get("Set-Cookie")

    def checklogin(self):
        """人员登录接口"""
        url = OA_HOST + "/api/hrm/login/checkLogin"
        data = {
            "loginid": self.username,
            "userpassword": self.password
        }
        response = requests.post(url, data=data)
        return response

    def get_hrm_search_result(self):
        """通讯录---获取人员列表"""
        url = OA_HOST + "/api/hrm/search/getHrmSearchResult"
        headers = {
            "Cookie": self.cookie
        }
        data = {}
        response = requests.post(url, data=data, headers=headers)
        return response

    def get_all_members(self, sessionkey, current_page=1):
        """按照sessionkey获取所有人员列表"""
        url = OA_HOST + "/api/ec/dev/table/datas"
        headers = {
            "Cookie": self.cookie,
        }
        data = {
            "dataKey": sessionkey,
            "current": current_page
        }
        response = requests.post(url, data=data, headers=headers)
        return response

    def get_member_info(self, userid):
        """人员小卡片信息"""
        url = OA_HOST + "/api/hrm/simpleinfo/getHrmSimpleInfo"
        headers = {
            "Cookie": self.cookie
        }
        data = {
            "userid": userid
        }
        response = requests.get(url, params=data, headers=headers)
        return response


class Flow:
    """
    工作流程
    """

    def __init__(self, cookie):
        self.cookie = cookie

    def get_work_flow_data(self, requestId):
        """获取流程信息"""
        url = OA_HOST + "/api/workflow/paService/getWorkflowRequest"
        data = {
            "requestId": requestId,
        }
        headers = {
            "Cookie": self.cookie
        }
        response = requests.request("GET", url, headers=headers, params=data)
        return response


class MonitorFlow:
    """
    监控-流程信息
    """

    def __init__(self, cookie):
        self.cookie = cookie

    def get_monitor_flow_data(self, requestId):
        """
        获取监控的流程信息
        :param requestId: 请求id
        :return: 流程信息
        """
        url = OA_HOST + "/api/workflow/paService/getWorkflowRequest"
        data = {
            "requestId": requestId,
            "otherParams": '{"ismonitor": "1"}'
        }
        headers = {
            "Cookie": self.cookie
        }
        response = requests.request("GET", url, headers=headers, params=data)
        return response


class InteractiveOaApi(HRM, Flow, MonitorFlow):
    """
    与oa接口的交互
    """

    def get_all_oa_member(self):
        """获得oa中所有用户"""
        sessionkey = self.get_hrm_search_result().json()  # 保持一个cookie，不然的话session_key无效
        current_page = 1
        member_all_list = list()
        while True:
            response = super().get_all_members(sessionkey["sessionkey"],
                                               current_page=current_page)
            if not response.json()["datas"]:
                return member_all_list
            # 需要进行反序列化的字段
            response_data_list = list()
            for key in response.json()["datas"]:
                # # 解决子公司负责人有两个号，其中一个号后面多一个-1
                # if key["workcode"].endswith("-1"):
                #     key["workcode"] = key["workcode"].split("-")[0]

                # 如果没有邮箱：自建邮箱
                # 规则姓名全拼+@well-healthcare.com,查询数据库中该邮箱是否存在，存在就+1

                # if key["email"] == "":
                #     result = Pinyin().get_pinyin(key["lastname"])
                #     key["email"] = result.replace("-", "") + "@well-healthcare.com"

                # 跳过没有员工编号的用户
                if key["workcode"] == "":
                    continue
                response_data_dict = {
                    "email": key["email"],
                    "id_in_oa": key["id"],
                    "name": key["lastname"],
                    "superiorid_in_oa": key["managerid"],
                    'superiorname_in_oa': key["manageridspan"],
                    "mobile": key["mobile"],
                    "subcompanyid_in_oa": key["subcompanyid1"],
                    "subcompanyid1span_in_oa": key["subcompanyid1span"],
                    "username": key["workcode"],  # 员工编号作为username
                    "departmentidspan_in_oa": key["departmentidspan"],
                    "departmentid": key["departmentid"],
                    "password": "123456",
                }

                response_data_list.append(response_data_dict)
            member_all_list.extend(response_data_list)
            current_page += 1

    def get_member_superior(self, userid):
        """获取该成员的上级"""
        response_json = self.get_member_info(userid).json()
        return response_json["simpleInfo"]["managerName"]


# if __name__ == '__main__':
#     userlist = InteractiveOaApi().get_all_oa_member()
#     print(userlist)