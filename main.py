import time
import yaml
import logging
import paramiko
import pandas as pd
from paramiko import AuthenticationException
from paramiko.ssh_exception import NoValidConnectionsError

# 连接到 ssh，批量执行命令
class SSH():
    def __init__(self):
        super(SSH, self).__init__()
        # 只启用错误日志
        logging.basicConfig(level=logging.INFO)
    
    # 获取配置
    def get_config(self):
        with open("config.yaml", 'r') as stream:
            try:
                config = yaml.safe_load(stream)

                self.hostname = config["server"]["hostname"]
                self.port = config["server"]["port"]
                self.username = config["server"]["username"]
                self.password = config["server"]["password"]
            except Exception as e:
                logging.warning('[SSH] Config read faile: ' + e)

    # 连接到服务器
    def connect(self):
        # 实例化 SSHClient
        self.client = paramiko.SSHClient()

        try:
            # 设置在没有已知主机密钥的情况下连接到服务器时要使用的策略
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            # 连接到 ssh 服务器
            self.client.connect(
                hostname = self.hostname, 
                port = self.port, 
                username = self.username, 
                password = self.password
            )
        except AuthenticationException: # 认证失败
            logging.warning('[SSH] Username or Password error')
            return False
        except NoValidConnectionsError: # 超时
            logging.warning('[SSH] Connect time out')
            return False
        except Exception as e: # 捕获其它异常
            logging.warning(f"[SSH] Unexpected error: {e}")
            raise # 重新抛出异常
        
        # ssh 连接成功
        logging.info("[SSH] Connect success.")
        return True

    # 执行命令
    def execute_command(self):
        self.id_list = []
        self.command_list = []
        self.result_list = []

        # 读取命令
        with open("command_list.txt", "r", encoding="utf-8") as reader:
            row = 0
            # 遍历执行每一条命令
            for line in reader:
                time.sleep(1)

                # 移除换行符和其他额外的空白
                line = line.strip()

                row = row + 1
                self.id_list.append(row)
                self.command_list.append(line)

                # 如果命令行为空的，则跳过
                if not line:
                    self.result_list.append("")
                    continue
                
                logging.info("[SSH] Command execute: " + str(line))
                
                # 执行命令并记录结果
                stdin, stdout, stderr = self.client.exec_command(line)
                output = stdout.read().decode('utf-8')
                error_output = stderr.read().decode('utf-8')
                self.result = ""

                if output != "":
                    self.result = output
                    logging.info("[SSH] Command out: \n" + str(output).strip())
                else:
                    self.result = error_output
                    logging.info("[SSH] Command err: \n" + str(error_output).strip())

                self.result_list.append(self.result)

        # 添加到 excel 表中
        self.df = pd.DataFrame(
            data = {'Id': self.id_list, 'Command': self.command_list, 'Result': self.result_list},
            columns = ["Id", "Command", "Result"]
        )
        self.df.to_excel('./result/output.xlsx', sheet_name="Sheet1", index=False)
                
    # 关闭 ssh 连接
    def close(self):
        logging.info("[SSH] Connect close.")
        self.client.close()

if __name__ == '__main__':
    # 实例化 SSH，并获取配置
    ssh = SSH()
    ssh.get_config()

    # 判断是否连接成功，成功则批量执行所有命令，执行完后关闭 ssh 连接
    if ssh.connect() == True:
        ssh.execute_command()
        ssh.close()
