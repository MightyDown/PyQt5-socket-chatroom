# client.py
import socket
import threading
import json
from PyQt5.QtCore import pyqtSignal, QObject

class Client(QObject):
    login_result = pyqtSignal(str)  # 成功后跳转到聊天界面
    error_occurred = pyqtSignal(str)  # 显示错误

    def __init__(self):
        super().__init__()
        self.HOST = '127.0.0.1'
        self.PORT = 8888
        self.client_socket = None

    def connect_to_server(self):
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((self.HOST, self.PORT))
            return True
        except Exception as e:
            self.error_occurred.emit(f"连接失败: {e}")
            return False

    def on_login(self, username, password):
        def worker():
            if not self.connect_to_server():
                return
            try:
                data = json.dumps({"type": "login", "username": username, "password": password})
                self.client_socket.send(data.encode('utf-8'))

                response = self.client_socket.recv(1024).decode('utf-8')
                res_json = json.loads(response)
                if res_json.get("type") == "system":
                    if "登录成功" in res_json.get("content", ""):
                        self.login_result.emit(username)
                    else:
                        self.error_occurred.emit(res_json["content"])
                else:
                    self.error_occurred.emit("收到非预期的响应")
            except Exception as e:
                self.error_occurred.emit(f"登录失败: {e}")

        threading.Thread(target=worker, daemon=True).start()

    def on_register(self, username, password):
        def worker():
            if not self.connect_to_server():
                return
            try:
                data = json.dumps({"type": "register", "username": username, "password": password})
                self.client_socket.send(data.encode('utf-8'))

                response = self.client_socket.recv(1024).decode('utf-8')
                res_json = json.loads(response)
                self.error_occurred.emit(res_json.get("content", "注册失败"))
            except Exception as e:
                self.error_occurred.emit(f"注册失败: {e}")

        threading.Thread(target=worker, daemon=True).start()
