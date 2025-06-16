# PyQt5-socket-chatroom 网络聊天室项目说明文档

## 一、项目基本信息  
**作者**：麦当当(mdd)  
这是一个基于 **PyQt5 + Socket + MySQL** 技术栈开发的简单网络聊天室应用，具备用户注册、登录、发送消息功能，且能将聊天数据持久化存储到数据库中。  


## 二、项目结构  
项目文件及功能说明如下：  

### 📦 项目文件结构  
- `server.py`  
  - 服务端程序（需先运行，负责接收/转发消息、处理服务端核心逻辑）  
- `client.py`  
  - 客户端通信模块（处理 socket 连接、数据收发，对接服务端）  
- `auth_window.py`  
  - 登录/注册界面（提供用户注册、登录交互入口，含表单校验）  
- `chat_window.py`  
  - 聊天主界面（实时展示消息、支持发送交互，含 UI 渲染逻辑）  
- `models.py`  
  - 数据库模型（用 SQLAlchemy 定义表结构，实现 ORM 映射）  
- `main.py`  
  - 主入口（启动图形界面，串联登录、聊天等模块的流程控制）  
- `README.md`  
  - 项目说明文档（指导部署、使用、配置，含环境要求/常见问题）  
- `requirements.txt`  
  - Python 依赖清单（记录所需包版本，如 PyQt5、SQLAlchemy 等）  


## 三、环境要求  
- Python 版本：3.7 及以上  
- MySQL 版本：5.7 及以上（需确保已安装并正常运行）  


## 四、安装依赖
通过 pip 工具安装项目所需 Python 依赖包，执行以下命令：

```bash
pip install -r requirements.txt  
```

## 五、数据库配置

本项目使用 MySQL 数据库存储用户信息和聊天记录，配置步骤如下：

（一）创建数据库与表
进入 MySQL 命令行（或数据库管理工具），依次执行以下 SQL 语句：

```sql
-- 1. 创建数据库  
CREATE DATABASE chat_db;  

-- 2. 使用该数据库  
USE chat_db;  

-- 3. 创建用户表（存储注册信息）  
CREATE TABLE users (  
    id INT AUTO_INCREMENT PRIMARY KEY,  
    username VARCHAR(50) UNIQUE NOT NULL,  
    password VARCHAR(255) NOT NULL  
);  

-- 4. 创建消息表（存储聊天记录）  
CREATE TABLE messages (  
    id INT AUTO_INCREMENT PRIMARY KEY,  
    username VARCHAR(50) NOT NULL,  
    content TEXT NOT NULL,  
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP  
);  
```



（二）修改数据库连接配置
在项目代码中找到 models.py 文件，修改以下内容以匹配你的 MySQL 环境：

```python
# models.py 中的数据库连接配置  
DATABASE_URI = 'mysql+mysqlconnector://root:your_password@localhost/chat_db'  

# 说明：  
# - root：替换为你的 MySQL 用户名  
# - your_password：替换为你的 MySQL 密码（无密码则省略）  
# - localhost：若数据库不在本地，替换为实际 IP/域名  
```
### （二）修改数据库连接配置（models.py）
打开 `models.py` 文件，找到数据库连接配置相关代码，按实际 MySQL 配置修改：  
- 若 MySQL 设置了密码，修改为：  
```python
DATABASE_URI = 'mysql+mysqlconnector://root:your_password@localhost/chat_db'
```  
- 若未设置密码，修改为：  
```python
DATABASE_URI = 'mysql+mysqlconnector://root@localhost/chat_db'
```  
（将 `your_password` 替换为你实际的 MySQL 密码，若有其他用户名也需对应替换 ）


## 六、启动与运行

### （一）启动顺序
1. **启动服务端**  
打开终端，执行命令：  
```bash
python server.py
```  
也可直接运行编译后 `dist` 目录下的 `server.exe`（若有编译产物）。  

2. **启动客户端**  
另开一个终端，执行命令：  
```bash
python main.py
```  
同样可运行 `dist` 目录下的 `main.exe`（若有编译产物）。  


## 七、使用说明
- 支持多用户同时在线聊天，利用 Socket 实现实时通信。  
- 注册时用户名需唯一，系统会校验避免重复。  
- 所有聊天记录会通过 MySQL 持久化保存，支持中文、英文等 UTF-8 编码内容发送。  


## 八、常见问题与解决方案
| 常见问题                | 解决方案                                                                 |
|-------------------------|--------------------------------------------------------------------------|
| 数据库连接失败          | 检查 MySQL 服务是否启动，确认 `models.py` 中用户名、密码、数据库名配置正确   |
| 表不存在                | 按照“五、（一）”步骤，在 MySQL 中创建对应的数据库和表结构                   |
| 客户端无法连接          | 检查 `server.py` 和 `main.py` 中设置的 IP 地址和端口号是否一致、可访问       |
| 缺少 `mysqlclient` 依赖 | 执行 `pip install mysqlclient` 或 `pip install mysql-connector-python` 安装 |  


## 九、可扩展方向
- 增加群聊、私聊功能，实现更丰富的聊天场景。  
- 支持表情发送、文件传输，提升聊天体验。  
- 优化界面布局与样式，添加主题切换等个性化设置。  
- 实现消息撤回、编辑功能，增强交互性。 
```

