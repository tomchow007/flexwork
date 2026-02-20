FROM python:3.9-slim

WORKDIR /app
COPY requirements-cloud.txt .
RUN pip install --no-cache-dir -r requirements-cloud.txt

# 复制应用代码
COPY web_app.py .
COPY data_store.py .

# 暴露端口
EXPOSE 8501

# 启动命令
CMD ["streamlit", "run", "web_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
