#!/bin/bash
## author:lee
## This shell script is used to automatically start related services for web_annotation system!

# 启动nginx服务
exec nohup nginx -c /root/miniconda3/etc/nginx/nginx.conf > /root/web_annotation/process_log/nginx_process.log &
echo "nginx start successfully, and then hidden!"

# >>> conda initialize >>>
# !! Contents within this block are managed by 'conda init' !!
__conda_setup="$('/root/miniconda3/bin/conda' 'shell.bash' 'hook' 2> /dev/null)"
if [ $? -eq 0 ]; then
    eval "$__conda_setup"
else
    if [ -f "/root/miniconda3/etc/profile.d/conda.sh" ]; then
        . "/root/miniconda3/etc/profile.d/conda.sh"
    else
        export PATH="/root/miniconda3/bin:$PATH"
    fi
fi
unset __conda_setup
# <<< conda initialize <<<

conda activate web_annotation
exec gunicorn -c '/root/web_annotation/gunicorn.py' first_test:app > /root/web_annotation/process_log/gunicorn_process.log &
echo "gunicorn start successfully!"