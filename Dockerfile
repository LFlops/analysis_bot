FROM python:3.12-slim

WORKDIR /app

# 复制项目文件
COPY . .

# 安装依赖
RUN pip install --no-cache-dir -e .

# 暴露端口（如果需要）
EXPOSE 5000

# 启动命令
CMD ["python", "okx_mcp_server.py"]
