# 🧩 网络聊天室项目说明文档
作者：<麦当当(mdd)>
这是一个基于 PyQt5 + Socket + MySQL 的 简单网络聊天室应用。
支持用户注册、登录、发送消息，并将数据持久化到数据库中。
 
# 📁 项目结构

`.
├── server.py           # 服务端程序（需先运行）
├── client.py           # 客户端通信模块
├── auth_window.py      # 登录/注册界面
├── chat_window.py      # 聊天主界面
├── models.py           # 数据库模型（使用 SQLAlchemy）
├── main.py             # 主入口（启动图形界面）
├── README.md           # 当前文件
└── requirements.txt    # Python 依赖包列表
`

# ⚙️ 环境要求
Python 3.7+
MySQL 5.7+（已安装并运行）


# 🔧 安装依赖
pip install -r requirements.txt


# 🗃️ 数据库配置
本项目使用 MySQL 存储用户信息和聊天记录。


# ✅ 创建数据库与表
进入 MySQL 命令行，执行以下 SQL 语句：

```
CREATE DATABASE chat_db;
USE chat_db;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);

CREATE TABLE messages (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    content TEXT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

# 📂 修改数据库连接地址（models.py）

### 在 models.py 中修改如下一行以匹配你的 MySQL 配置：

DATABASE_URI = 'mysql+mysqlconnector://root:your_password@localhost/chat_db'

### 如果你没有设置密码，可改为：

DATABASE_URI = 'mysql+mysqlconnector://root@localhost/chat_db'


# ▶️ 启动顺序
## 启动服务端
    python server.py
## 启动客户端
    python main.py


 或者按顺序启动dist目录下的server.exe和main.exe


# 📌 使用说明
支持多用户同时在线聊天。
注册后即可登录，用户名唯一。
所有聊天记录会保存到数据库。
支持中文、英文等 UTF-8 编码内容。


# 常见问题：
1、数据库连接失败
2、表不存在
3、客户端无法链接
4、没有mysqlclient

# 解决方案：
1、检查 MySQL 服务是否启动，用户名和密码是否正确。
2、在 MySQL 中创建数据库和表。
3、检查server.py和main.py中的IP地址和端口号是否正确。
4、使用 pip install mysqlclient 或 mysql-connector-python

# 📝 其他资源
示例账号：注册后即可登录使用
多人同时使用：支持 TCP 多客户端连接
可扩展性：可添加群聊、私聊、表情、文件传输等功能