# main.py
import sys
from PyQt5.QtWidgets import QApplication
from auth_window import AuthWindow
from chat_window import ChatWindow
from client import Client

def main():
    app = QApplication(sys.argv)

    client = Client()

    auth_window = AuthWindow()

    def handle_login(username, password):
        client.on_login(username, password)

    def handle_register(username, password):
        client.on_register(username, password)

    auth_window.login_success.connect(handle_login)
    auth_window.register_success.connect(handle_register)

    def on_login_success(username):
        chat_window = ChatWindow(username, client.client_socket)
        chat_window.show()
        auth_window.hide()

    def on_error(message):
        from PyQt5.QtWidgets import QMessageBox
        QMessageBox.critical(None, "错误", message)

    client.login_result.connect(on_login_success)
    client.error_occurred.connect(on_error)

    auth_window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
