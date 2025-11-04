# -*- coding: utf-8 -*-
# @Time : 2020/12/21 22:42
# @Author : Lee
# @FileName: first_test.py
# @Application_Function:
from datetime import timedelta
from functools import wraps

from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFProtect
from wtforms import PasswordField, StringField
from wtforms.validators import DataRequired

import configparser
import json
import json_format
import list_current_coupus
import update_config
from load_corpus import load_ners, load_sents2
from path_utils import CONFIG_PATH, as_config_path, ensure_directory, static_root

# 初始化csrf保护机制
csrf = CSRFProtect()


# 初始化自定义表单和验证机制
class UserForm(FlaskForm):
    name = StringField('用户名', validators=[DataRequired(message='请输入用户名')])
    pwd = PasswordField('密码', validators=[DataRequired(message='请输入密码')])


def login_required(view_func):
    @wraps(view_func)
    def wrapped_view(*args, **kwargs):
        if 'username' not in session:
            flash('请先登录系统。', 'warning')
            return redirect(url_for('index'))
        return view_func(*args, **kwargs)

    return wrapped_view


def _load_progress(cfg, corpus_mapping):
    progress = []
    for key in corpus_mapping.keys():
        try:
            progress.append(cfg.getint('INITIAL', key))
        except (configparser.NoOptionError, configparser.NoSectionError, ValueError):
            progress.append(0)
    return progress


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
    form = UserForm()
    current_user = session.get('username')
    if form.validate_on_submit():
        username = form.name.data.strip()
        password = form.pwd.data
        if update_config.check_login(username, password):
            session.permanent = True
            session['username'] = username
            flash(f'欢迎回来，{username}！', 'success')
            return redirect(url_for('select_corpus'))
        flash('账号或密码错误！', 'danger')
    elif request.method == 'POST':
        flash('请输入完整的用户名和密码。', 'warning')
    return render_template('index.html', form=form, logged_in_user=current_user)


# 选择需要标注的语料章节
@app.route('/select_corpus')
@login_required
def select_corpus():
    form = FlaskForm()
    all_corpus = list_current_coupus.list_chapter_len()
    if all_corpus:
        update_config.update_config_keys(all_corpus.keys())
    cfg = configparser.ConfigParser()
    cfg.read(CONFIG_PATH, encoding='utf-8')
    global_progress = _load_progress(cfg, all_corpus) if all_corpus else []
    username = session.get('username', '无名英雄')
    return render_template('select_corpus.html', form=form, corpus=all_corpus, progress=global_progress,
                           name=username)


# 进行标注的界面
@app.route('/show_corpus')
@app.route('/show_corpus/<path>')
@login_required
def show_corpus():
    """
    :return: 将获取到的语料集传输到一个jinja模板
    """
    form = FlaskForm()
    if request.method == 'GET' and request.args.get('file_path'):
        cfg = configparser.ConfigParser()
        cfg.read(CONFIG_PATH, encoding='utf-8')
        lines = cfg.getint('GLOBAL', 'load_lines', fallback=5)
        filePath = request.args.get('file_path')
        if not filePath:
            flash('缺少语料文件标识。', 'warning')
            return redirect(url_for('select_corpus'))
        try:
            initial_index = cfg.getint('INITIAL', filePath)
        except (configparser.NoOptionError, configparser.NoSectionError, ValueError):
            initial_index = 0
        try:
            res = load_sents2(filePath, initial_index, lines)
        except FileNotFoundError:
            flash('未找到请求的语料文件，请检查配置。', 'danger')
            return redirect(url_for('select_corpus'))
        try:
            ners = load_ners()
        except FileNotFoundError:
            flash('未找到NER标签定义，将以空白标签展示。', 'warning')
            ners = []
        username = session.get('username', '无名英雄')
        return render_template('show_corpus.html', sentences=res, form=form, path=filePath,
                               index_sentence=initial_index, ners=ners, username=username)

    return redirect(url_for('index'))


# 显示从表单提交的数据信息
@app.route('/labeled_res', methods=['GET', 'POST'])
@login_required
def labeled_res():
    if request.method == 'GET':
        flash('请通过页面表单提交标注结果。', 'info')
        return redirect(url_for('select_corpus'))

    cfg = configparser.ConfigParser()
    cfg.read(CONFIG_PATH, encoding='utf-8')
    write_file_path = cfg.get('PATHS', 'raw_submit_dir', fallback='labeled_dataset/raw_labeled_data_from_web')
    output_path = cfg.get('PATHS', 'labeled_results_dir', fallback='labeled_dataset/labeled_results')
    rename_arg = request.args.get('rename')
    if not rename_arg:
        flash('缺少语料定位信息，无法保存标注结果。', 'danger')
        return redirect(url_for('select_corpus'))
    output_fileName = rename_arg.split('/')[-1]  # 获取进行编辑的文件名全程，默认是csv格式；
    raw_fileName = output_fileName.split('.')[0] + '.json'
    # 下面是将表单form中获取的数据，进行格式化处理，将处理的结果写入到一个文件名（wirte_file_path）中
    res = request.form.to_dict()
    try:
        res_json = json.dumps(res, ensure_ascii=False)
    except (TypeError, ValueError) as exc:
        app.logger.exception('序列化提交内容失败: %s', exc)
        flash('提交内容解析失败，请重试。', 'danger')
        return redirect(url_for('show_corpus', file_path=rename_arg))

    raw_dir = ensure_directory(write_file_path)
    output_dir = ensure_directory(output_path)
    raw_file_path = raw_dir / raw_fileName
    try:
        with raw_file_path.open('w', encoding='utf-8') as w:
            w.writelines(res_json)
    except OSError as exc:
        app.logger.exception('写入临时标注文件失败: %s', exc)
        flash('写入标注文件失败，请检查磁盘权限。', 'danger')
        return redirect(url_for('show_corpus', file_path=rename_arg))

    try:
        output_res_status = json_format.format_json_to_dataFrame(output_dir, output_fileName,
                                                                 raw_file_path)
    except Exception as exc:  # pylint: disable=broad-except
        app.logger.exception('生成标注结果文件失败: %s', exc)
        flash('生成标注结果文件失败，请联系管理员。', 'danger')
        return redirect(url_for('show_corpus', file_path=rename_arg))
    if output_res_status:
        # 如果每次提交成功，也就是output_res_status为True，就从源文件中删除对应的行数；
        # 确定源文件是哪个？
        # 更新本次完成标注的句子数量
        # 读入全局配置文件
        current_file = request.args.get('rename')
        try:
            finished_lines = cfg.getint('INITIAL', current_file)
        except (configparser.NoOptionError, configparser.NoSectionError, ValueError, TypeError):
            finished_lines = 0
        finished_lines += cfg.getint('GLOBAL', 'load_lines', fallback=5)  # 表示当前已经完成标注的语料行数

        update_status = update_config.update_config(current_file, finished_lines)
        if update_status is True:
            output_display = as_config_path(output_dir / output_fileName)
            return render_template('success.html', output_file=output_display)
        flash('配置文件未能更新成功，请联系管理员。', 'warning')
        app.logger.warning('Update config failed for %s: %s', current_file, update_status)
        return redirect(url_for('show_corpus', file_path=rename_arg))
    return render_template('error.html')


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

