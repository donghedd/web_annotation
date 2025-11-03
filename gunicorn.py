# 并行工作进程数
workers = 1
# 指定每个工作者的线程数
threads = 2
# 监听内网端口5000
bind = '127.0.0.1:7001'
# 设置守护进程,将进程交给supervisor管理
daemon = 'false'
# 工作模式协程
worker_class = 'gevent'
# 设置最大并发量
worker_connections = 2000
# 设置进程文件目录
pidfile = 'log/gunicorn.pid'
# 设置访问日志和错误信息日志路径
# access_log_format = '%(t)s %(p)s %(h)s "%(r)s" %(s)s %(L)s %(b)s %(f)s" "%(a)s"'
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" "%({X-Real-IP}i)s"'
accesslog = 'log/gunicorn_acess.log'
errorlog = 'log/gunicorn_error.log'
# 设置日志记录水平
loglevel = 'debug'

debug = True

# 设置进程名称
proc_name = 'web_annotation'
