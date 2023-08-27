# client.py
import rpyc

def execute_remote_command(command):
    conn = rpyc.connect("localhost", 18861)  # 替换为服务器的IP地址
    remote_service = conn.root

    result = remote_service.exposed_execute_command(command)
    conn.close()
    return result

if __name__ == "__main__":
    command_to_execute = "python notiontessx.py"  # 替换为你要执行的实际命令
    output = execute_remote_command(command_to_execute)
    print("Remote command output:")
    print(output)
