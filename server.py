# server.py
import socket
import threading
import json
from models import SessionLocal, User, Message

HOST = '127.0.0.1'
PORT = 8888
clients = []

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))
server.listen()

print(f"服务器启动在 {HOST}:{PORT}")

def broadcast(message):
    for client in clients:
        try:
            client.send(json.dumps(message).encode('utf-8'))
        except:
            client.close()
            clients.remove(client)

def save_message(username, content):
    db = SessionLocal()
    msg = Message(username=username, content=content)
    db.add(msg)
    db.commit()
    db.refresh(msg)

def handle_client(client_socket):
    while True:
        try:
            msg = client_socket.recv(1024).decode('utf-8')
            if not msg:
                break
            message = json.loads(msg)

            # 注册逻辑
            if message['type'] == 'register':
                db = SessionLocal()
                user = User(username=message['username'], password=message['password'])
                try:
                    db.add(user)
                    db.commit()
                    broadcast({"type": "system", "content": "注册成功，请登录"})
                except Exception as e:
                    db.rollback()
                    broadcast({"type": "system", "content": "用户名已存在"})
                finally:
                    db.close()
                continue

            # 登录逻辑
            if message['type'] == 'login':
                db = SessionLocal()
                user = db.query(User).filter(
                    User.username == message['username'],
                    User.password == message['password']
                ).first()
                if user:
                    broadcast({"type": "system", "content": f"{message['username']} 登录成功"})
                else:
                    broadcast({"type": "system", "content": "用户名或密码错误"})
                db.close()
                continue

            # 聊天消息处理
            if message['type'] == 'message':
                save_message(message['username'], message['content'])
                broadcast(message)

        except Exception as e:
            print(f"错误: {e}")
            break

    client_socket.close()
    if client_socket in clients:
        clients.remove(client_socket)

def accept_connections():
    while True:
        client_socket, addr = server.accept()
        print(f"新客户端连接: {addr}")
        clients.append(client_socket)
        threading.Thread(target=handle_client, args=(client_socket,)).start()

if __name__ == '__main__':
    print("等待客户端连接...")
    accept_connections()
