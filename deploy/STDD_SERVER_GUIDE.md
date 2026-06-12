# STDD 服务器部署与运维指南

> 最后更新：2026-06-12 | 维护者：小以AI实验室

---

## 一、服务器概览

| 项目 | 信息 |
|------|------|
| 操作系统 | CentOS Linux 7 (Core) |
| Python | 3.8.13（通过 `scl enable rh-python38` 调用） |
| Web 服务器 | Nginx 1.20.1 |
| 进程管理 | systemd 219 |
| 网站目录 | `/var/www/ddyy/stdd-page/` |
| 下载目录 | `/var/www/ddyy/stdd/download/` |
| API 目录 | `/var/www/ddyy/stdd-api/` |

---

## 二、目录结构

```
/var/www/ddyy/
├── stdd-page/                      # 官网静态文件
│   ├── index.html                  # V2.9 官网首页
│   └── playground/                 # 在线体验
├── stdd/download/                  # 白皮书下载（MD 文件）
│   ├── STDD_Whitepaper_CN.md
│   ├── STDD_Whitepaper_EN.md
│   ├── STDD_Whitepaper_CN_AI.md
│   └── STDD_Whitepaper_EN_AI.md
├── stdd-api/                       # Share API 服务
│   └── server-api.py               # 主程序（从 deploy/ 上传）
└── client/                         # 主站 Nuxt 前端
```

---

## 三、Share API 服务

### 3.1 功能

接收客户端 `stdd experience share` 的 POST 请求，通过 GitHub REST API 将经验文件直接写入 `leonai42/stdd-experiences` 仓库的 `pending/` 目录。

### 3.2 工作流程

```
客户端 CLI → POST /stdd/api/share-experience
  → server-api.py 接收 JSON
  → PUT https://api.github.com/repos/leonai42/stdd-experiences/contents/pending/{exp_id}.md
  → 返回 {success: true}
```

无 git 依赖，完全通过 HTTPS API 通信。

### 3.3 首次部署

```bash
# 1. 创建目录
mkdir -p /var/www/ddyy/stdd-api

# 2. 上传 deploy/server-api.py → /var/www/ddyy/stdd-api/server-api.py
chmod +x /var/www/ddyy/stdd-api/server-api.py

# 3. 创建 GitHub Token 文件
mkdir -p /etc/stdd
echo 'github_pat_你的token' > /etc/stdd/github-token
chmod 600 /etc/stdd/github-token

# 4. 注册 systemd 服务（逐行执行）
echo '[Unit]' > /etc/systemd/system/stdd-api.service
echo 'Description=STDD Experience Share API' >> /etc/systemd/system/stdd-api.service
echo 'After=network.target' >> /etc/systemd/system/stdd-api.service
echo '[Service]' >> /etc/systemd/system/stdd-api.service
echo 'Type=simple' >> /etc/systemd/system/stdd-api.service
echo 'ExecStart=/usr/bin/scl enable rh-python38 -- python3 /var/www/ddyy/stdd-api/server-api.py' >> /etc/systemd/system/stdd-api.service
echo 'WorkingDirectory=/var/www/ddyy/stdd-api' >> /etc/systemd/system/stdd-api.service
echo 'Restart=always' >> /etc/systemd/system/stdd-api.service
echo 'RestartSec=5' >> /etc/systemd/system/stdd-api.service
echo 'User=root' >> /etc/systemd/system/stdd-api.service
echo '[Install]' >> /etc/systemd/system/stdd-api.service
echo 'WantedBy=multi-user.target' >> /etc/systemd/system/stdd-api.service

systemctl daemon-reload && systemctl enable stdd-api && systemctl start stdd-api
```

### 3.4 后续更新

上传新版 `deploy/server-api.py` 后：

```bash
systemctl restart stdd-api && systemctl status stdd-api
```

### 3.5 Nginx 配置

文件：`/etc/nginx/conf.d/ddyy.conf`

已添加的配置块（在 `location /stdd/` 之前）：

```nginx
location /stdd/api/ {
    proxy_pass http://127.0.0.1:8800/api/;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_read_timeout 30s;
}
```

修改后重载：`nginx -t && systemctl reload nginx`

### 3.6 API 端点

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/stdd/api/health` | 健康检查 → `{"status":"ok","time":"..."}` |
| POST | `/stdd/api/share-experience` | 提交经验到 pending 池 |

**POST 请求体：**

```json
{
  "experience_id": "EXP-2026-0001",
  "content": "---
category: bug
...
---

# Body...",
  "author": "username（可选）"
}
```

**成功响应：**

```json
{"success": true, "experience_id": "EXP-2026-0001", "message": "submitted to pending"}
```

### 3.7 GitHub Token 管理

- 存放路径：`/etc/stdd/github-token`（权限 600）
- Token 类型：Fine-grained personal access token
- 仓库权限：仅 `leonai42/stdd-experiences` → Contents: Read & Write
- 过期后替换：直接修改 `/etc/stdd/github-token`，无需重启服务

---

## 四、运维命令速查

```bash
# API 服务状态
systemctl status stdd-api

# 重启 API
systemctl restart stdd-api

# 查看日志（最近 30 行）
journalctl -u stdd-api --no-pager -n 30

# 实时日志
journalctl -u stdd-api -f

# 健康检查
curl -s https://hzddyy.com/stdd/api/health

# Nginx 重载
nginx -t && systemctl reload nginx

# Nginx 错误日志
tail -50 /var/log/nginx/error.log
```

---

## 五、开发文件对照

| 仓库文件 | 服务器路径 | 说明 |
|----------|-----------|------|
| `deploy/server-api.py` | `/var/www/ddyy/stdd-api/server-api.py` | Share API 服务 |
| `deploy/STDD_SERVER_GUIDE.md` | — | 本文档 |
| `website/index.html` | `/var/www/ddyy/stdd-page/index.html` | 官网首页 |
| `website/playground/` | `/var/www/ddyy/stdd-page/playground/` | 在线体验 |
| 白皮书 MD | `/var/www/ddyy/stdd/download/` | 下载专区 |

---

## 六、版本变更记录

| 日期 | 内容 |
|------|------|
| 2026-05-14 | 初始部署（官网 + Playground） |
| 2026-06-11 | V2.9 官网升级 + 白皮书下载专区 |
| 2026-06-11 | 新增 Share API 服务（server-api.py） |
| 2026-06-12 | Share API 改为 GitHub REST API 模式（无 git 依赖） |

---

## 七、故障排查

| 现象 | 可能原因 | 检查方法 |
|------|---------|---------|
| API 504 | 服务未运行 | `systemctl status stdd-api` |
| API 502 | Python 环境问题 | `journalctl -u stdd-api -n 30` |
| "Bad credentials" | Token 过期 | 重新生成并更新 `/etc/stdd/github-token` |
| 上传后不可见 | 权限不足 | 确认 Token 有 Contents Write |
