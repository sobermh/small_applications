"""
@author:maohui
@time:9/8/2023 1:18 PM
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
import os
import socket
import threading
import time

import psutil

from read_all_files_in_os.save import SaveToMysql


class VerboseOs:
    """操作系统详情"""

    def get_cpu_info(self):
        """cpu"""
        # Get CPU count and usage percentage
        cpu_count = psutil.cpu_count(logical=False)
        cpu_percent = psutil.cpu_percent(interval=1, percpu=True)

        print(f"CPU Count: {cpu_count}")
        return f"{cpu_count}"
        # print("CPU Usage Percentage:")
        # for i, percent in enumerate(cpu_percent):
        #     print(f"Core {i + 1}: {percent}%")

    def get_memory_info(self):
        """memory"""
        # Get memory information
        virtual_memory = psutil.virtual_memory()

        print(f"Total Memory: {virtual_memory.total / (1024 ** 3):.2f} GB")
        return f'{virtual_memory.total / (1024 ** 3) :.2f}'
        # print(f"Available Memory: {virtual_memory.available / (1024 ** 3):.2f} GB")
        # print(f"Used Memory: {virtual_memory.used / (1024 ** 3):.2f} GB")

    # def get_ip_info(self):
    #     """ip"""
    #     # Get the host name
    #     host_name = socket.gethostname()
    #
    #     # Get the IP address associated with the host name
    #     ip_address = socket.gethostbyname(host_name)
    #
    #     print(f"Host Name: {host_name}")
    #     print(f"IP Address: {ip_address}")

    def get_ip_info(self):
        try:
            # Create a socket object to get the local IP address
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.settimeout(0.1)  # Set a timeout in case the network is not reachable

            # Connect to a remote server (doesn't actually send data)
            # s.connect(("8.8.8.8", 80))  # Google's public DNS server and port 80
            s.connect(("114.114.114.144", 80))  # Google's public DNS server and port 80

            # Get the local IP address from the connected socket
            local_ip_address = s.getsockname()[0]
            s.close()
            print(f"Local IP Address: {local_ip_address}")

            return local_ip_address
        except socket.error:
            return "Unable to retrieve IP address"


class FileScanner:
    """扫描文件"""

    def __init__(self):
        self.file_lock = threading.Lock()  # 添加文件写入锁
        self.stop_threads = False  # 线程停止标志

        # 在初始化时检测文件是否存在
        if os.path.exists('filepath.txt'):
            # 如果文件存在，清空文件内容
            with open('filepath.txt', 'w') as file:
                file.truncate(0)

    # def get_disk_size(self, partition):
    #     disk = psutil.disk_usage(partition.mountpoint)
    #     total_size = disk.total  # 总容量

    def get_entire_disks(self):
        """
        获取windows中所有磁盘
        :return:磁盘列表
        """

        # 包括挂载点、设备名称、文件系统类型等
        partitions = psutil.disk_partitions(all=True)
        disk_list = []

        for partition in partitions:
            try:
                # disk = psutil.disk_usage(partition.mountpoint)
                # total_size = disk.total  # 总容量
                # if total_size > 0:
                disk_list.append(partition.mountpoint)
            except Exception as e:
                print(str(e))
                continue
        return disk_list

    def scan_disk(self, disk):
        """
        读取磁盘列表的所有以.exe结尾的文件
        :param disk: 磁盘
        :return:
        """
        print(f"Scanning {disk}...")
        files_to_scan = []

        for root, dirs, files in os.walk(disk):
            if self.stop_threads:
                return  # 标志为Ture,退出线程
            for file in files:
                filepath = os.path.join(root, file)
                if str(filepath).endswith(".exe"):
                    files_to_scan.append(filepath)

        files_to_write = self.remove_repeated_exe(files_to_scan)

        with self.file_lock:  # 使用文件写入锁来确保线程安全
            with open("filepath.txt", 'a', encoding="utf-8") as f:  # a,追加
                for filepath in files_to_write:
                    f.write(filepath + '\n')

        print(f"Scanning {disk} over")

    def list_files(self, disk_list):
        """
        每个磁盘使用不同线程的扫描
        :param disk_list:
        :return:
        """

        # # 创建一个计时器线程，用于在达到最大运行时间时停止主程序
        # # 创建一个计时器，用于在达到最大运行时间时停止主程序 10分钟
        # timer = threading.Timer(10 * 60, read_instance.timeout)
        # timer.start()

        # 创建一个空的线程列表 threads 用于存储将要启动的线程对象。
        threads = []
        for disk in disk_list:
            # 对于每个磁盘路径 disk，创建一个新的线程 thread，并设置线程的目标函数为 self.scan_disk，并传入 disk 作为参数。
            thread = threading.Thread(target=self.scan_disk, args=(disk,))
            threads.append(thread)
            # 启动每个线程，使其开始执行 self.scan_disk(disk) 函数。
            thread.start()

        # 使用 for 循环遍历 threads 列表，并在每个线程上调用 thread.join()，这将等待每个线程执行完毕，确保所有线程都已完成后再继续执行主线程
        for thread in threads:
            thread.join(10 * 60)
        unfinished_threads = [thread for thread in threads if thread.is_alive()]
        if len(unfinished_threads) > 0:
            self.stop_threads = True
            raise TimeoutError("timeout")
        # print(unfinished_threads)

    def remove_repeated_exe(self, files_to_scan):
        """
        移除重复的exe文件
        :param files_to_scan: 扫描到的文件列表
        :return: files_to_write:返回需要写入的数据列表
        """
        files_to_write = []
        parent_path_flag = ""
        exe_name_flag = ""
        for i in files_to_scan:
            parent_path, exe_name = i.rsplit("\\", 1)[0], i.rsplit("\\", 1)[1]
            # exe_name, parent_path, = i.rsplit("\\", 1)[1], ("\\".join(i.split("\\", 4))[0:-1])
            # 程序集会被安装到应用程序的安装目录或系统的Program Files目录中。 $RECYCLE.BIN为回收站文件
            if "$RECYCLE.BIN" in i or r"C:\Windows" in i or r"C:\Users\PC\AppData" in i:
                continue
            #  先判断如果exe文件名是否一样, # 如果不一样那么再判断是否是一个文件夹下
            if exe_name != exe_name_flag and parent_path != parent_path_flag:
                # 软件的.exe文件不会放在软件文件夹外面，所以parent_path_flag下只保留一个.exe文件，
                # 可以通过相同长度的parent_path_flag，排除该文件夹下的其他.exe文件
                if len(parent_path_flag) > 2 and i[:len(parent_path_flag)] == parent_path_flag:
                    continue
                files_to_write.append(i)
                parent_path_flag = parent_path
                exe_name_flag = exe_name
        return files_to_write

    def timeout(self):
        # 添加等待时间（以秒为单位）
        # time.sleep(60)  # 等待2秒
        raise TimeoutError("timeout")


if __name__ == "__main__":

    os_instance = VerboseOs()
    mysql_instance = SaveToMysql()
    ip = str(os_instance.get_ip_info())
    cpu = str(os_instance.get_cpu_info())
    memory = str(os_instance.get_memory_info())
    times = mysql_instance.read_scan_times(ip)
    try:
        if times > 0:
            print(f"========本机已成功进行{times}次扫描========")
        print("=========开始扫描========")
        print("=========扫描结束会自动关闭窗口，如扫描时间超过15分钟，请联系管理员................")
        read_instance = FileScanner()
        disks = read_instance.get_entire_disks()
        read_instance.list_files(disks)
        print("=========结束扫描========")
        print("=========正在保存数据========")
        # 保存到数据库中
        with open('./filepath.txt', 'rb') as file:
            mysql_instance.insert_data(ip, memory, cpu, 1, error_msg="", data_txt=file.read())
    except Exception as e:
        mysql_instance.insert_data(ip, memory, cpu, 0, error_msg=str(e), data_txt="")
        print(f"error:{e}")
    finally:
        os.remove("./filepath.txt")
        mysql_instance.close_db()
