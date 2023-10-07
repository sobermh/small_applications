"""
@author:mh
Code is far away from bug
"""

from read_all_files_in_os.find import Find
from read_all_files_in_os.oa_api import InteractiveOaApi
from read_all_files_in_os.read import TimerThread, VerboseOs, FileScanner
from read_all_files_in_os.save import SaveToMysql


def main():
    """
    扫描文件
    :return:
    """
    # 在主线程中创建计时线程
    timer_thread = TimerThread()

    name = input(f"请输入工号:")
    os_instance = VerboseOs()
    ip = str(os_instance.get_ip_info())
    mac = str(os_instance.get_mac_address())
    cpu = str(os_instance.get_cpu_info())
    memory = str(os_instance.get_memory_info())
    os_version, device_name = os_instance.get_os_version()
    flash = str(os_instance.get_flash_devices())
    mysql_instance = SaveToMysql()
    times = mysql_instance.read_scan_times(ip)
    try:
        if times > 0:
            print(f"========本机已成功进行{times}次扫描========")
        print("=========开始扫描========")
        print("=========扫描结束会自动关闭窗口，如扫描时间超过15分钟，请联系管理员................")

        # 启动计时线程
        timer_thread.start()
        #  执行扫描代码
        read_instance = FileScanner(ip, name)
        disks = read_instance.get_entire_disks()
        read_instance.list_files(disks)
        print("=========结束扫描========")
        print("=========正在保存数据========")
        # 保存到数据库中
        with open(f'./{name}-{ip}.txt', 'rb') as file:
            mysql_instance.insert_data(name, ip, mac, memory, cpu, device_name, os_version, flash, 1, error_msg="",
                                       data_txt=file.read())
    except Exception as e:
        mysql_instance.insert_data(name, ip, mac, memory, cpu, device_name, os_version, flash, 0, error_msg=str(e),
                                   data_txt="")
        print(f"error:{e}")
    finally:
        # os.remove("./filepath.txt")
        # 停止计时线程
        timer_thread.stop()
        timer_thread.join()  # 等待计时线程结束
        mysql_instance.close_db()


def get_require_user():
    """
    找到符合条件的有哪些用户
    :return: 在同文件夹下生成一个finally.txt文件
    """
    find_instance = Find()
    find_instance.save_find_username("autocad", "photoshop", "solid", "altium designer", "graphpad", "matlab",
                                     "pycharm")
    find_instance.close_db()


def get_remain_user():
    """
    找到没有别扫描的用户
    :return: 打印用户列表
    """
    find_instance = Find()
    find_instance.find_user()
    find_instance.close_db()


def get_all_files():
    """
    获取所有文件信息
    :return: 在files文件夹下新建对应的文件
    """
    instance = SaveToMysql()
    instance.read_data()
    instance.close_db()


def get_all_oa_user():
    """
    获取oa所有的用户
    :return: 打印列表
    """
    user_list = InteractiveOaApi().get_all_oa_member()
    print(user_list)


if __name__ == '__main__':
    # 扫描开始
    main()
