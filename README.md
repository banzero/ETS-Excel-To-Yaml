# 数据处理工具（网页版）

一个简单易用的网页工具，支持两种数据处理功能：
1. **Excel 转 YAML** - 将Excel文件转换为YAML格式
2. **XML 批量修改** - 使用Excel数据批量更新XML文件

## 🌟 功能特点

- 🖥️ **网页界面** - 无需安装软件，打开浏览器即可使用
- 📊 **Excel 转 YAML** - 支持自定义字段映射，智能处理数据类型
- 🔧 **XML 批量修改** - 批量更新XML文件中的GroupAddress名称
- 🐳 **Docker 部署** - 支持Docker容器化部署，简单易用
- 📱 **响应式设计** - 支持桌面和移动设备访问

## 📋 系统要求

- Docker 和 Docker Compose（推荐）
- 或 Python 3.8+ 环境

## 🚀 快速开始

### 方法一：Docker 部署（推荐）

1. **下载项目文件**
   ```bash
   # 将项目文件下载到本地目录
   cd /path/to/your/directory
   ```

2. **修改配置（可选）**
   ```bash
   # 编辑 docker-compose.yml 文件
   nano docker-compose.yml
   # 修改 FLASK_SECRET_KEY 为你的密钥
   ```

3. **启动服务**
   ```bash
   # 构建并启动容器
   docker-compose up -d
   ```

4. **访问应用**
   - 打开浏览器访问：`http://你的服务器IP:5678`
   - 例如：`http://192.168.1.100:5678`

### 方法二：Python 环境部署

1. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

2. **启动应用**
   ```bash
   python app.py
   ```

3. **访问应用**
   - 打开浏览器访问：`http://127.0.0.1:5678`

## 📖 使用教程

### 模块一：Excel 转 YAML

**适用场景**：将Excel表格数据转换为YAML配置文件

**操作步骤**：

1. **准备Excel文件**
   - 确保Excel文件格式为 `.xlsx`
   - 第一行为表头（字段名）
   - 从第二行开始为数据

2. **上传文件**
   - 点击"选择 Excel 文件"按钮
   - 选择你的 `.xlsx` 文件
   - 系统会自动读取表头

3. **自定义字段映射（可选）**
   - 系统会显示Excel中的所有字段名
   - 在右侧输入框中输入新的字段名
   - 留空则保持原字段名

4. **开始转换**
   - 点击"开始转换"按钮
   - 系统会自动下载转换后的 `.yaml` 文件

**示例**：

原始Excel数据：
| name | address | state_address |
|------|---------|---------------|
| 1    | 0/0/1   | 0/1/1         |
| 2    | 0/0/2   | 0/1/2         |

转换后的YAML：
```yaml
- name: 1
  address: "0/0/1"
  state_address: "0/1/1"
- name: 2
  address: "0/0/2"
  state_address: "0/1/2"
```

### 模块二：XML 批量修改

**适用场景**：批量更新XML文件中的GroupAddress名称

**操作步骤**：

1. **准备Excel文件**
   - 确保Excel文件包含两列：`Address` 和 `Name`
   - `Address` 列：XML中GroupAddress的地址值
   - `Name` 列：要设置的新名称

2. **准备XML文件**
   - 确保XML文件格式正确
   - 包含需要更新的GroupAddress元素

3. **上传文件**
   - 选择包含Address和Name列的Excel文件
   - 选择要修改的XML文件

4. **开始处理**
   - 点击"开始处理"按钮
   - 系统会自动下载修改后的XML文件

**示例**：

Excel数据：
| Address | Name        |
|---------|-------------|
| 0/0/1   | 客厅灯      |
| 0/0/2   | 卧室灯      |

XML修改前：
```xml
<GroupAddress Address="0/0/1" Name=""/>
<GroupAddress Address="0/0/2" Name=""/>
```

XML修改后：
```xml
<GroupAddress Address="0/0/1" Name="客厅灯"/>
<GroupAddress Address="0/0/2" Name="卧室灯"/>
```

## 🔧 高级配置

### Docker 环境变量

在 `docker-compose.yml` 中可以配置以下环境变量：

```yaml
environment:
  - FLASK_SECRET_KEY=your-very-secure-secret-key  # 应用密钥
  - FLASK_ENV=production                          # 运行环境
```

### 文件大小限制

默认最大上传文件大小为 16MB，如需修改：

1. 编辑 `app.py` 文件
2. 修改 `MAX_CONTENT_LENGTH` 值：
   ```python
   app.config['MAX_CONTENT_LENGTH'] = 32 * 1024 * 1024  # 32MB
   ```

### 端口配置

默认端口为 5678，如需修改：

1. 编辑 `docker-compose.yml` 文件
2. 修改端口映射：
   ```yaml
   ports:
     - "8080:5678"  # 外部端口:内部端口
   ```

## 🌐 远程访问配置

### 使用 Lucky 反向代理

1. **登录 Lucky 管理界面**
   - 访问：`http://你的公网IP:16601`

2. **添加反向代理规则**
   - 规则名称：数据处理工具
   - 域名：`data.yourdomain.com`（或你想要的子域名）
   - 目标地址：`http://你的内网IP:5678`
   - 启用：勾选

3. **配置域名解析**
   - 在你的域名服务商处添加A记录
   - 主机记录：`data`
   - 记录值：你的公网IP

4. **SSL证书（推荐）**
   - 在Lucky中配置SSL证书
   - 或使用Let's Encrypt自动申请

### 直接端口访问

如果不需要域名，可以直接通过端口访问：
- 确保防火墙开放 5678 端口
- 访问：`http://你的公网IP:5678`

## 🛠️ 故障排除

### 常见问题

1. **无法访问网页**
   - 检查Docker容器是否正常运行：`docker ps`
   - 检查端口是否被占用：`netstat -tulpn | grep 5678`
   - 检查防火墙设置

2. **文件上传失败**
   - 检查文件大小是否超过限制
   - 确认文件格式正确（.xlsx 或 .xml）
   - 检查网络连接

3. **Excel读取失败**
   - 确认Excel文件格式为 .xlsx
   - 检查Excel文件是否损坏
   - 确认Excel文件包含正确的列名

4. **XML修改失败**
   - 确认XML文件格式正确
   - 检查Excel中是否包含Address和Name列
   - 确认Address值在XML中存在

### 查看日志

```bash
# Docker 方式
docker logs data-processor

# 或实时查看
docker logs -f data-processor
```

### 重启服务

```bash
# Docker 方式
docker-compose restart

# 或完全重新部署
docker-compose down
docker-compose up -d
```

## 📁 项目结构

```
xml批量修改/
├── app.py                 # Flask 主应用
├── process_core.py        # 核心处理逻辑
├── requirements.txt       # Python 依赖
├── Dockerfile            # Docker 镜像配置
├── docker-compose.yml    # Docker 编排配置
├── templates/
│   └── index.html        # 网页模板
├── 部署说明.md           # 详细部署说明
└── README.md            # 本文档
```

## 🔄 更新应用

```bash
# 停止当前服务
docker-compose down

# 拉取最新代码（如果有）
git pull

# 重新构建并启动
docker-compose up -d --build
```

## 📞 技术支持

如果遇到问题，请检查：

1. **系统要求**：确保Docker或Python环境正确安装
2. **文件格式**：确保上传的文件格式正确
3. **网络连接**：确保网络连接正常
4. **日志信息**：查看应用日志获取详细错误信息

## 📄 许可证

本项目仅供学习和个人使用。

---

**享受使用！** 🎉
