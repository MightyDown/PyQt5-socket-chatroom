# chat_window.py
from PyQt5.QtWidgets import (
    QWidget, QTextEdit, QLineEdit, QPushButton, QVBoxLayout,
    QHBoxLayout, QLabel, QFrame, QScrollArea
)
from PyQt5.QtCore import Qt, pyqtSignal
import json
import threading
import time


class ChatWindow(QWidget):
    message_received = pyqtSignal(str)

    def __init__(self, username, client_socket):
        super().__init__()
        self.username = username
        self.client_socket = client_socket
        self.setWindowTitle(f"网络聊天室 - {username}")
        self.resize(700, 500)
        self.setStyleSheet("background-color: #f5f5f5;")

        self.init_ui()
        self.receive_thread = threading.Thread(target=self.receive_messages, daemon=True)
        self.receive_thread.start()

        # 为不同用户分配颜色
        self.user_colors = {
            username: "#27ae60",  # 自己用绿色
        }

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(40, 30, 40, 20)
        main_layout.setSpacing(15)

        # 聊天内容区域（滚动区域）
        self.chat_container = QVBoxLayout()
        self.chat_container.setAlignment(Qt.AlignTop)
        self.chat_container.setSpacing(10)

        scroll_area = QScrollArea()
        scroll_content = QWidget()
        scroll_content.setLayout(self.chat_container)
        scroll_area.setWidget(scroll_content)
        scroll_area.setWidgetResizable(True)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setStyleSheet("border: none;")

        # 输入框
        self.message_input = QLineEdit()
        self.message_input.setPlaceholderText("输入消息...")
        self.message_input.setStyleSheet("""
            QLineEdit {
                height: 45px;
                border: none;
                border-bottom: 2px solid #ccc;
                background-color: white;
                border-radius: 2px;
                padding: 0 10px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border-bottom: 2px solid #3498db;
            }
        """)

        # 发送按钮
        send_button = QPushButton("发送")
        send_button.setStyleSheet("""
            QPushButton {
                height: 45px;
                background-color: #3498db;
                color: white;
                border-radius: 22px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #2c3e50;
            }
        """)

        # 输入布局
        input_layout = QHBoxLayout()
        input_layout.addWidget(self.message_input, 8)
        input_layout.addWidget(send_button, 1)

        # 添加到主布局
        main_layout.addWidget(scroll_area, stretch=1)
        main_layout.addLayout(input_layout)

        # 事件绑定
        send_button.clicked.connect(self.send_message)
        self.message_input.returnPressed.connect(self.send_message)
        self.message_received.connect(self.display_message)

    def send_message(self):
        msg = self.message_input.text().strip()
        if not msg:
            return
        try:
            data = json.dumps({
                "type": "message",
                "username": self.username,
                "content": msg
            })
            print(f"Sending message: {msg}")  # 调试输出
            self.client_socket.send(data.encode('utf-8'))
            self.message_input.clear()
        except Exception as e:
            self.add_system_message(f"⚠️ 发送失败: {str(e)}")

    def receive_messages(self):
        while True:
            try:
                if self.client_socket.fileno() == -1:
                    break
                msg = self.client_socket.recv(1024).decode('utf-8')
                if not msg:
                    self.add_system_message("⚠️ 与服务器断开连接")
                    break
                print(f"Received message: {msg}")  # 调试输出
                self.message_received.emit(msg)
            except Exception as e:
                self.message_received.emit(f"❌ 接收错误: {str(e)}")
                break

    def display_message(self, message):
        print(f"Displaying message: {message}")  # 调试输出
        try:
            msg_dict = json.loads(message)
            msg_type = msg_dict.get("type")
            if msg_type == "system":
                self.add_system_message(msg_dict.get("content", ""))
            elif msg_type == "message":
                self.add_chat_message(
                    msg_dict.get("username", "未知用户"),
                    msg_dict.get("content", "")
                )
        except json.JSONDecodeError:
            self.add_system_message(f"非JSON格式: {message}")

    def get_user_color(self, username):
        if username not in self.user_colors:
            colors = ["#e67e22", "#9b59b6", "#f1c40f", "#1abc9c", "#3498db"]
            self.user_colors[username] = colors[len(self.user_colors) % len(colors)]
        return self.user_colors[username]

    def add_local_message(self, content):
        is_self = True
        time_str = time.strftime("%H:%M", time.localtime())
        self._add_bubble(self.username, content, time_str, is_self)

    def add_chat_message(self, username, content):
        is_self = (username == self.username)
        time_str = time.strftime("%H:%M", time.localtime())
        self._add_bubble(username, content, time_str, is_self)

    def add_system_message(self, content):
        time_str = time.strftime("%H:%M", time.localtime())
        html = f"""
            <div style="text-align:center; margin: 10px 0; color:#999;">
                [{time_str}] <span style="color:#e74c3c;">{content}</span>
            </div>
        """
        self._append_html(html)

    def _add_bubble(self, username, content, time_str, is_self=False):
        replaced_content = content.replace('\n', '<br>')
        name_color = self.get_user_color(username)
        name_style = f"color: {name_color}; font-size: 14px; font-weight: bold;"
        text_style = "font-size: 14px; color: #333;"  # 简单的文本样式
        time_style = "color: #999; font-size: 12px; text-align: right; margin-top: 5px;"

        bubble_html = f"""
            <div style="margin-bottom: 15px; text-align: {'right' if is_self else 'left'};">
                <div style="{name_style}">{username}</div>
                <div style="{text_style}">
                    {replaced_content}
                </div>
                <div style="{time_style}">{time_str}</div>
            </div>
        """
        self._append_html(bubble_html)

    def _append_html(self, html):
        chat_widget = QLabel(html)
        chat_widget.setTextFormat(Qt.RichText)
        chat_widget.setWordWrap(True)
        self.chat_container.addWidget(chat_widget)
        self.scrollToBottom()

    def scrollToBottom(self):
        scroll_bar = self.findChild(QScrollArea).verticalScrollBar()
        scroll_bar.setValue(scroll_bar.maximum())

    def closeEvent(self, event):
        self.client_socket.close()
        event.accept()
