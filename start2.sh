#!/bin/bash
#! bin/bash
## author:lee
## This shell script is used to automatically start related services for web_annotation system!

# 启动nginx服务
exec nohup nginx -c /root/miniconda3/etc/nginx/nginx.conf > /root/web_annotation/process_log/nginx_process.log &
echo "nginx start successfully, and then hidden!"
# 启动gunicorn服务
# conda activate web_annotation
exec nohup gunicorn -c '/root/web_annotation/gunicorn.py' first_test:app > /root/web_annotation/process_log/gunicorn_process.log &
echo "gunicorn start successfully!"
# nginx -c /root/miniconda3/etc/nginx/nginx.conf

# 启动gunicorn服务
# gunicorn -c '/root/web_annotation/gunicorn.py' first_test:app

