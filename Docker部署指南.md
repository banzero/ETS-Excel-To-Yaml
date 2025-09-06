# Docker 部署指南

## 📋 前提条件

### 1. 安装 Docker

**macOS 系统：**
```bash
# 使用 Homebrew 安装
brew install --cask docker

# 或下载 Docker Desktop for Mac
# 访问：https://www.docker.com/products/docker-desktop
```

**Linux 系统（Ubuntu/Debian）：**
```bash
# 更新包索引
sudo apt update

# 安装必要的包
sudo apt install apt-transport-https ca-certificates curl gnupg lsb-release

# 添加 Docker 官方 GPG 密钥
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

# 设置稳定版仓库
echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# 安装 Docker Engine
sudo apt update
sudo apt install docker-ce docker-ce-cli containerd.io

# 启动 Docker 服务
sudo systemctl start docker
sudo systemctl enable docker

# 将当前用户添加到 docker 组（可选，避免使用 sudo）
sudo usermod -aG docker $USER
```

**Windows 系统：**
- 下载 Docker Desktop for Windows
- 访问：https://www.docker.com/products/docker-desktop

### 2. 验证安装

```bash
# 检查 Docker 版本
docker --version

# 检查 Docker Compose 版本
docker compose version
```

## 🚀 部署步骤

### 步骤 1：准备项目文件

确保你的项目目录包含以下文件：
```
xml批量修改/
├── app.py
├── process_core.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── templates/
    └── index.html
```

### 步骤 2：修改配置（可选）

编辑 `docker-compose.yml` 文件：

```yaml
version: '3.8'

services:
  data-processor:
    build: .
    container_name: data-processor
    restart: unless-stopped
    ports:
      - "5678:5678"  # 可以修改为其他端口，如 "8080:5678"
    environment:
      - FLASK_SECRET_KEY=your-very-secure-secret-key-here  # 修改为强密码
      - FLASK_ENV=production
    volumes:
      - ./logs:/app/logs
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:5678/"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
```

### 步骤 3：构建并启动

```bash
# 进入项目目录
cd /path/to/xml批量修改

# 构建并启动容器
docker compose up -d

# 查看运行状态
docker compose ps

# 查看日志
docker compose logs -f
```

### 步骤 4：访问应用

- 本地访问：`http://localhost:5678`
- 局域网访问：`http://你的IP地址:5678`

## 🔧 常用命令

### 容器管理

```bash
# 启动服务
docker compose up -d

# 停止服务
docker compose down

# 重启服务
docker compose restart

# 查看状态
docker compose ps

# 查看日志
docker compose logs -f

# 进入容器
docker compose exec data-processor bash
```

### 更新应用

```bash
# 停止服务
docker compose down

# 重新构建镜像
docker compose build --no-cache

# 启动服务
docker compose up -d
```

### 清理资源

```bash
# 删除容器和网络
docker compose down

# 删除镜像
docker rmi xml批量修改_data-processor

# 清理所有未使用的资源
docker system prune -a
```

## 🌐 远程访问配置

### 方法 1：端口转发

1. **路由器端口转发**
   - 登录路由器管理界面
   - 设置端口转发：外部端口 5678 → 内网IP:5678

2. **防火墙设置**
   ```bash
   # Ubuntu/Debian
   sudo ufw allow 5678
   
   # CentOS/RHEL
   sudo firewall-cmd --permanent --add-port=5678/tcp
   sudo firewall-cmd --reload
   ```

3. **访问地址**
   - `http://你的公网IP:5678`

### 方法 2：使用 Lucky 反向代理

1. **安装 Lucky**
   - 参考 Lucky 官方文档安装

2. **配置反向代理**
   - 域名：`data.yourdomain.com`
   - 目标：`http://内网IP:5678`

3. **配置域名解析**
   - 添加 A 记录：`data` → 你的公网IP

## 🛠️ 故障排除

### 常见问题

1. **端口被占用**
   ```bash
   # 查看端口占用
   netstat -tulpn | grep 5678
   
   # 修改端口
   # 编辑 docker-compose.yml，修改 ports 配置
   ```

2. **容器启动失败**
   ```bash
   # 查看详细日志
   docker compose logs
   
   # 检查镜像构建
   docker compose build --no-cache
   ```

3. **无法访问应用**
   ```bash
   # 检查容器状态
   docker compose ps
   
   # 检查端口映射
   docker port data-processor
   
   # 检查防火墙
   sudo ufw status
   ```

4. **内存不足**
   ```bash
   # 清理 Docker 资源
   docker system prune -a
   
   # 限制容器内存使用
   # 在 docker-compose.yml 中添加：
   deploy:
     resources:
       limits:
         memory: 512M
   ```

### 性能优化

1. **增加内存限制**
   ```yaml
   services:
     data-processor:
       deploy:
         resources:
           limits:
             memory: 1G
             cpus: '0.5'
   ```

2. **启用日志轮转**
   ```yaml
   services:
     data-processor:
       logging:
         driver: "json-file"
         options:
           max-size: "10m"
           max-file: "3"
   ```

## 📊 监控和维护

### 查看资源使用

```bash
# 查看容器资源使用
docker stats data-processor

# 查看系统资源
docker system df
```

### 备份数据

```bash
# 备份配置文件
cp docker-compose.yml docker-compose.yml.backup

# 备份日志
docker compose logs > logs_backup.txt
```

### 定期维护

```bash
# 创建维护脚本
cat > maintenance.sh << 'EOF'
#!/bin/bash
echo "开始维护..."

# 清理旧日志
docker compose logs --tail=1000 > recent_logs.txt

# 清理未使用的镜像
docker image prune -f

# 重启服务
docker compose restart

echo "维护完成！"
EOF

chmod +x maintenance.sh
```

## 🎉 完成！

现在你的数据处理工具已经成功部署在Docker中，可以通过网页界面使用两个功能模块了！

如果遇到任何问题，请参考故障排除部分或查看应用日志。
