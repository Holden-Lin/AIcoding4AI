# gunicorn_conf.py
workers = 4  # 根据您的服务器配置调整
worker_class = "uvicorn.workers.UvicornWorker"
bind = "0.0.0.0:8001"  # 确保端口不与 Flask 应用冲突
loglevel = "debug"
accesslog = "logs/access.log"
errorlog = "logs/error.log"
capture_output = True  # To capture output in the log files
