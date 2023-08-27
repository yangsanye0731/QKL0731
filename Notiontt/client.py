# client.py
import rpyc

conn = rpyc.connect("localhost", 18861)  # 连接到服务器
remote_service = conn.root

x = 5
y = 3
result = remote_service.multiply(x, y)
print(f"{x} multiplied by {y} is {result}")

conn.close()
