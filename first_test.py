# -*- coding: utf-8 -*-
# @Time : 2020/12/21 22:42
# @Author : Lee
# @FileName: first_test.py
# @Application_Function:
from datetime import timedelta

from flask import Flask, url_for, redirect, session
from flask.templating import render_template_string
from markupsafe import escape
from flask import request
from flask import render_template
from load_corpus import load_sents2, load_ners
from flask_bootstrap import Bootstrap
import json_format
import json
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField
from wtforms.validators import DataRequired
from flask_wtf.csrf import CSRFProtect
import list_current_coupus
import configparser
import update_config
from path_utils import CONFIG_PATH, as_config_path, ensure_directory

# 初始化csrf保护机制
csrf = CSRFProtect()


# 初始化自定义表单和验证机制
class UserForm(FlaskForm):
    name = StringField('', validators=[DataRequired()])
    pwd = PasswordField('', validators=[DataRequired()])


# 创建APP初始步骤，并且导入bootstrap样式
def create_app():
    app2 = Flask(__name__)
    Bootstrap(app2)
    csrf.init_app(app2)
    return app2


app = create_app()
# 对app做全局初始化配置
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = b'test a key'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=2)


# 标注系统的首页
@app.route('/', methods=['GET', 'POST'])
def index():
    form = FlaskForm()
    if request.method == 'POST':
        # 读入全局配置文件
        cfg = configparser.ConfigParser()
        cfg.read(CONFIG_PATH, encoding='utf-8')
        if update_config.check_login(request.form['username1'], request.form['pwd']):

            session['username'] = request.form['username1']
            all_corpus = list_current_coupus.list_chapter_len()
            if all_corpus:
                global_progress = []
                for key in all_corpus.keys():
                    try:
                        global_progress.append(cfg.getint('INITIAL', key))
                    except (configparser.NoOptionError, configparser.NoSectionError, ValueError):
                        global_progress.append(0)
            else:
                global_progress = []

            update_config.update_config_keys(all_corpus.keys())
            username = request.form['username1']
            return render_template('select_corpus.html', form=form, corpus=all_corpus, progress=global_progress,
                                   name=username)
        else:
            return render_template('error.html', error_msg="账号或密码错误！")
    elif request.method == 'GET':
        return render_template('index.html', form=form)
        # return render_template_string("test!")


# 选择需要标注的语料章节
@app.route('/select_corpus')
def select_corpus():
    form = FlaskForm()
    if request.url == request.url_root + 'select_corpus':  # 有点问题，因为当环境改变的时候，这个url地址就更改了
        # form = FlaskForm()
        # 读入全局配置文件
        cfg = configparser.ConfigParser()
        cfg.read(CONFIG_PATH, encoding='utf-8')

        all_corpus = list_current_coupus.list_chapter_len()
        if all_corpus:
            global_progress = []
            for key in all_corpus.keys():
                try:
                    global_progress.append(cfg.getint('INITIAL', key))
                except (configparser.NoOptionError, configparser.NoSectionError, ValueError):
                    global_progress.append(0)
        else:
            global_progress = []
        username = session.get('username')
        if username:
            return render_template('select_corpus.html', form=form, corpus=all_corpus, progress=global_progress,
                                   name=username)
        else:
            return render_template('select_corpus.html', form=form, corpus=all_corpus, progress=global_progress,
                                   name='无名英雄')

    return render_template('index.html')


# 进行标注的界面
@app.route('/show_corpus')
@app.route('/show_corpus/<path>')
def show_corpus():
    """
    :return: 将获取到的语料集传输到一个jinja模板
    """
    form = FlaskForm()
    if request.method == 'GET' and request.args.get('file_path'):
        cfg = configparser.ConfigParser()
        cfg.read(CONFIG_PATH, encoding='utf-8')
        lines = cfg.getint('GLOBAL', 'load_lines')
        filePath = request.args.get('file_path')
        initial_index = cfg.getint('INITIAL', filePath)
        try:
            res = load_sents2(filePath, initial_index, lines)
        except FileNotFoundError:
            return render_template('error.html', error_msg="未找到请求的语料文件，请检查配置。")
        try:
            ners = load_ners()
        except FileNotFoundError:
            ners = []
        username = session['username']
        return render_template('show_corpus.html', sentences=res, form=form, path=filePath,
                               index_sentence=initial_index, ners=ners, username=username)

    return redirect(url_for('index'))


# 显示从表单提交的数据信息
@app.route('/labeled_res', methods=['POST'])
def labeled_res():
    # form = UserForm()
    cfg = configparser.ConfigParser()
    cfg.read(CONFIG_PATH, encoding='utf-8')
    write_file_path = cfg.get('PATHS', 'raw_submit_dir', fallback='labeled_dataset/raw_labeled_data_from_web')
    output_path = cfg.get('PATHS', 'labeled_results_dir', fallback='labeled_dataset/labeled_results')
    output_fileName = request.args.get('rename').split('/')[-1]  # 获取进行编辑的文件名全程，默认是csv格式；
    raw_fileName = output_fileName.split('.')[0] + '.json'
    # 下面是将表单form中获取的数据，进行格式化处理，将处理的结果写入到一个文件名（wirte_file_path）中
    res = request.form.to_dict()
    res = json.dumps(res, ensure_ascii=False)
    raw_dir = ensure_directory(write_file_path)
    output_dir = ensure_directory(output_path)
    raw_file_path = raw_dir / raw_fileName
    with raw_file_path.open('w', encoding='utf-8') as w:
        w.writelines(res)
    output_res_status = json_format.format_json_to_dataFrame(output_dir, output_fileName,
                                                             raw_file_path)
    if output_res_status:
        # 如果每次提交成功，也就是output_res_status为True，就从源文件中删除对应的行数；
        # 确定源文件是哪个？
        # 更新本次完成标注的句子数量
        # 读入全局配置文件
        current_file = request.args.get('rename')
        finished_lines = cfg.getint('INITIAL', current_file) + cfg.getint('GLOBAL', 'load_lines')  # 表示当前已经完成标注的语料行数

        if update_config.update_config(current_file, finished_lines):
            output_display = as_config_path(output_dir / output_fileName)
            return render_template('success.html', output_file=output_display)
        else:
            return "本次标注的语料还未更新到最新状态，请联系管理员，或重新操作！"
    return render_template('error.html')
