from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox
from PyQt5.QtCore import pyqtSignal, QPropertyAnimation, QEasingCurve, QRect


class AuthWindow(QWidget):
    login_success = pyqtSignal(str, str)  # 用户名, 密码
    register_success = pyqtSignal(str, str)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("网络聊天室 - 登录")
        self.resize(400, 380)  # 调整窗口高度，优化布局空间
        self.setStyleSheet("background-color: #f0f0f0;")  # 浅灰色背景（对应设计图纯色背景）
        self.layout = QVBoxLayout()
        self.layout.setSpacing(20)  # 增加组件间距
        self.layout.setContentsMargins(80, 60, 80, 60)  # 增加边距
        self.setLayout(self.layout)
        self.show_login_page()

    def show_login_page(self):
        self.clear_layout()
        self.setWindowTitle("网络聊天室 - 登录")

        # 输入框样式优化（扁平风格：简洁边框+内阴影）
        self.username_input = QLineEdit()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.username_input.setStyleSheet("""
            QLineEdit {
                height: 45px;
                border: none;
                border-bottom: 2px solid #ccc;  /* 仅底部边框，扁平风格 */
                background-color: white;
                border-radius: 2px;
                padding: 0 10px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border-bottom: 2px solid #3498db;  /* 聚焦时蓝色边框 */
            }
        """)
        self.password_input.setStyleSheet(self.username_input.styleSheet())
        self.username_input.setPlaceholderText("请输入用户名")
        self.password_input.setPlaceholderText("请输入密码")

        # 登录按钮（蓝色扁平按钮，带悬停效果）
        login_btn = QPushButton("登录")
        login_btn.setStyleSheet("""
            QPushButton {
                height: 50px;
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 25px;  /* 圆角按钮 */
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980b9;  /* 悬停时深色 */
                border-radius: 26px;  /* 微小动画效果 */
            }
            QPushButton:pressed {
                background-color: #2c3e50;  /* 点击时深色 */
            }
        """)

        # 注册链接（文本按钮，扁平风格）
        register_link = QPushButton("没有账号？去注册")
        register_link.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #3498db;
                border: none;
                font-size: 14px;
            }
            QPushButton:hover {
                color: #2980b9;
                text-decoration: underline;  /* 悬停下划线 */
            }
        """)

        # 布局排列
        self.layout.addWidget(QLabel("用户名"))
        self.layout.addWidget(self.username_input)
        self.layout.addWidget(QLabel("密码"))
        self.layout.addWidget(self.password_input)
        self.layout.addWidget(login_btn)
        self.layout.addWidget(register_link)

        # 事件绑定
        login_btn.clicked.connect(self.handle_login)
        register_link.clicked.connect(self.show_register_page)

        # 回车触发登录
        self.username_input.returnPressed.connect(self.handle_login)
        self.password_input.returnPressed.connect(self.handle_login)

    def show_register_page(self):
        self.clear_layout()
        self.setWindowTitle("网络聊天室 - 注册")

        # 注册页面输入框（与登录页统一风格）
        self.register_username = QLineEdit()
        self.register_password = QLineEdit()
        self.confirm_password = QLineEdit()
        self.register_password.setEchoMode(QLineEdit.Password)
        self.confirm_password.setEchoMode(QLineEdit.Password)
        for input_field in [self.register_username, self.register_password, self.confirm_password]:
            input_field.setStyleSheet(self.username_input.styleSheet())
        self.register_username.setPlaceholderText("请设置用户名")
        self.register_password.setPlaceholderText("请设置密码")
        self.confirm_password.setPlaceholderText("请确认密码")

        # 注册按钮（黄色扁平按钮，对应设计图风格）
        register_btn = QPushButton("注册")
        register_btn.setStyleSheet("""
            QPushButton {
                height: 50px;
                background-color: #f39c12;  /* 黄色按钮 */
                color: white;
                border: none;
                border-radius: 25px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #e67e22;  /* 悬停时深色 */
            }
            QPushButton:pressed {
                background-color: #d35400;  /* 点击时深色 */
            }
        """)

        # 返回按钮（文本按钮，带动画效果）
        back_btn = QPushButton("返回登录")
        back_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #7f8c8d;
                border: none;
                font-size: 14px;
            }
            QPushButton:hover {
                color: #34495e;
                text-decoration: underline;
            }
        """)
        # 为返回按钮添加轻微缩放动画（模拟设计图中的动画效果）
        self.back_animation = QPropertyAnimation(back_btn, b"geometry")
        self.back_animation.setDuration(200)
        self.back_animation.setEasingCurve(QEasingCurve.OutBounce)

        # 布局排列
        self.layout.addWidget(QLabel("用户名"))
        self.layout.addWidget(self.register_username)
        self.layout.addWidget(QLabel("密码"))
        self.layout.addWidget(self.register_password)
        self.layout.addWidget(QLabel("确认密码"))
        self.layout.addWidget(self.confirm_password)
        self.layout.addWidget(register_btn)
        self.layout.addWidget(back_btn)

        # 事件绑定
        register_btn.clicked.connect(self.handle_register)
        back_btn.clicked.connect(self.show_login_page)
        back_btn.clicked.connect(lambda: self.back_animation.start())

        # 回车触发注册
        self.register_username.returnPressed.connect(self.handle_register)
        self.register_password.returnPressed.connect(self.handle_register)
        self.confirm_password.returnPressed.connect(self.handle_register)

    def handle_login(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        if not username or not password:
            QMessageBox.warning(self, "输入错误", "用户名或密码不能为空")
            return
        self.login_success.emit(username, password)

    def handle_register(self):
        username = self.register_username.text().strip()
        password = self.register_password.text().strip()
        confirm = self.confirm_password.text().strip()
        if not username or not password or not confirm:
            QMessageBox.warning(self, "输入错误", "所有字段都必须填写")
            return
        if password != confirm:
            QMessageBox.warning(self, "验证失败", "两次输入的密码不一致")
            return
        self.register_success.emit(username, password)

    def clear_layout(self):
        while self.layout.count():
            child = self.layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()