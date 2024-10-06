import streamlit as st
import hashlib
import base64
from io import BytesIO
from PIL import Image
import uuid
import json
import os
from datetime import datetime, timedelta
import pytz
import calendar
import pandas as pd
import plotly.graph_objects as go # type: ignore
import numpy as np
import re
import html
import streamlit.components.v1 as components

# 文件路径
POSTS_FILE = "posts.json"
USERS_FILE = "users.json"
VIEWS_FILE = "views.json"

# 设置管理员密码
ADMIN_PASSWORD = "8zT@qR6#nP$1vW5!fL3x"

def set_custom_theme():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@300;400;500;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Noto Sans SC', sans-serif;
    }
    
    .stApp {
        background-color: #ffffff;
    }
    
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    h1 {
        font-size: 2.5rem !important;
        font-weight: 700 !important;
        color: #2e7d32 !important;
    }
    
    h2 {
        font-size: 1.8rem !important;
        font-weight: 500 !important;
        color: #388e3c !important;
    }
    
    .stButton>button {
        background-color: #4caf50;
        color: white;
        border-radius: 20px;
        padding: 0.5rem 1rem;
        font-size: 1rem;
        font-weight: 500;
        border: none;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        background-color: #45a049;
    }
    
    .blog-post {
        background-color: #f1f8e9;
        border-radius: 18px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    
    .blog-post h3 {
        font-size: 1.3rem !important;
        font-weight: 600 !important;
        color: #1b5e20 !important;
        margin-bottom: 0.5rem;
    }
    
    .blog-post p {
        color: #333;
        line-height: 1.5;
    }

    .category-tag {
        display: inline-block;
        padding: 0.3rem 0.7rem;
        background-color: #4caf50;
        color: white;
        border-radius: 20px;
        font-size: 0.9rem;
        font-weight: bold;
        margin-bottom: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    .delete-button {
        color: #f44336;
        cursor: pointer;
        float: right;
    }

    .delete-button:hover {
        color: #d32f2f;
    }

    .comment {
        background-color: #e8f5e9;
        border-radius: 14px;
        padding: 0.5rem;
        margin-top: 0.5rem;
        display: flex;
        align-items: center;
    }

    .comment-author {
        font-weight: bold;
        color: #1b5e20;
        margin-right: 0.5rem;
    }

    .comment-avatar {
        width: 30px;
        height: 30px;
        border-radius: 50%;
        margin-right: 0.5rem;
    }

    .user-menu {
        position: fixed;
        top: 0.5rem;
        right: 1rem;
        z-index: 1000;
        display: flex;
        align-items: center;
    }

    .user-menu .stButton>button {
        background-color: transparent;
        color: #4caf50;
        border: 1px solid #4caf50;
        padding: 0.3rem 0.7rem;
        font-size: 0.9rem;
    }

    .user-menu .stButton>button:hover {
        background-color: #4caf50;
        color: white;
    }

    .user-avatar {
        width: 30px;
        height: 30px;
        border-radius: 50%;
        margin-right: 0.5rem;
    }

    .upload-time {
        font-size: 0.8rem;
        color: #689f38;
        margin-bottom: 0.5rem;
    }

    .stats-container {
        display: flex;
        justify-content: space-around;
        margin-bottom: 2rem;
    }

    .stat-item {
        background-color: #e8f5e9;
        border-radius: 10px;
        padding: 1rem;
        text-align: center;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }

    .stat-value {
        font-size: 2rem;
        font-weight: bold;
        color: #2e7d32;
    }

    .stat-label {
        font-size: 1rem;
        color: #388e3c;
        margin-top: 0.5rem;
    }

    .sidebar .stRadio > div {
        background-color: #f1f8e9;
        border-radius: 10px;
        padding: 0.5rem;
    }

    .sidebar .stRadio > div > label {
        color: #2e7d32;
    }

    .blog-post-preview {
        background-color: #f1f8e9;
        border-radius: 18px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }

    .post-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 0.5rem;
    }

    .post-header h3 {
        font-size: 1.3rem !important;
        font-weight: 600 !important;
        color: #1b5e20 !important;
        margin: 0;
    }

    .category-tag {
        display: inline-block;
        padding: 0.3rem 0.7rem;
        background-color: #4caf50;
        color: white;
        border-radius: 20px;
        font-size: 0.9rem;
        font-weight: bold;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    .upload-time {
        font-size: 0.8rem;
        color: #689f38;
        margin-bottom: 0.5rem;
    }

    .stButton>button {
        padding: 0.25rem 0.5rem;
        font-size: 0.8rem;
        border-radius: 12px;
    }

    .full-post {
        background-color: #f1f8e9;
        border-radius: 18px;
        padding: 2rem;
        margin-bottom: 2rem;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }

    .full-post h2 {
        color: #1b5e20;
        margin-bottom: 0.5rem;
    }

    .blog-post-preview {
        background-color: #f1f8e9;
        border-radius: 18px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }

    .post-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 0.5rem;
    }

    .post-header h3 {
        font-size: 1.3rem !important;
        font-weight: 600 !important;
        color: #1b5e20 !important;
        margin: 0;
    }

    .category-tag {
        display: inline-block;
        padding: 0.3rem 0.7rem;
        background-color: #4caf50;
        color: white;
        border-radius: 20px;
        font-size: 0.9rem;
        font-weight: bold;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    .upload-time {
        font-size: 0.8rem;
        color: #689f38;
        margin-bottom: 0.5rem;
    }

    .full-post {
        background-color: #ffffff;
        border-radius: 18px;
        padding: 1.5rem;
        margin-top: 1rem;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }

    .stButton>button {
        padding: 0.25rem 0.5rem;
        font-size: 0.8rem;
        border-radius: 12px;
    }

    /* 自定义 expander 样式 */
    .streamlit-expanderHeader {
        font-size: 0.9rem !important;
        color: #4caf50 !important;
    }

    .streamlit-expanderContent {
        background-color: #ffffff;
        border-radius: 0 0 18px 18px;
    }

    .blog-post-preview {
        background-color: #f1f8e9;
        border-radius: 18px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }

    .post-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 0.5rem;
    }

    .post-header h3 {
        font-size: 1.3rem !important;
        font-weight: 600 !important;
        color: #1b5e20 !important;
        margin: 0;
    }

    .category-tag {
        display: inline-block;
        padding: 0.3rem 0.7rem;
        background-color: #4caf50;
        color: white;
        border-radius: 20px;
        font-size: 0.9rem;
        font-weight: bold;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    .upload-time {
        font-size: 0.8rem;
        color: #689f38;
        margin-bottom: 0.5rem;
    }

    .post-content {
        line-height: 1.6;
    }

    .read-more {
        color: #4caf50;
        text-decoration: none;
        font-weight: bold;
    }

    .read-more:hover {
        text-decoration: underline;
    }

    .post-content {
        line-height: 1.6;
    }

    .blog-post-preview {
        background-color: #f1f8e9;
        border-radius: 18px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }

    .post-content {
        line-height: 1.6;
    }

    .blog-post-preview {
        background-color: #f1f8e9;
        border-radius: 18px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }

    .blog-post-preview {
        background-color: #f1f8e9;
        border-radius: 18px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }

    .post-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 0.5rem;
    }

    .post-header h3 {
        font-size: 1.3rem !important;
        font-weight: 600 !important;
        color: #1b5e20 !important;
        margin: 0;
    }

    .category-tag {
        display: inline-block;
        padding: 0.3rem 0.7rem;
        background-color: #4caf50;
        color: white;
        border-radius: 20px;
        font-size: 0.9rem;
        font-weight: bold;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    .upload-time {
        font-size: 0.8rem;
        color: #689f38;
        margin-bottom: 0.5rem;
    }

    .stExpander {
        border: none !important;
        box-shadow: none !important;
    }

    .streamlit-expanderHeader {
        font-size: 1rem !important;
        font-weight: bold !important;
        color: #4caf50 !important;
    }

    .streamlit-expanderContent {
        background-color: white;
        border-radius: 10px;
        padding: 1rem;
    }

    .stButton > button {
        width: 100%;
        text-align: left;
        background-color: #f1f8e9;
        color: #1b5e20;
        font-size: 1.2rem;
        font-weight: 600;
        padding: 0.75rem 1rem;
        border: none;
        border-radius: 18px;
        margin-bottom: 0.5rem;
        transition: background-color 0.3s;
    }

    .stButton > button:hover {
        background-color: #c8e6c9;
    }

    .blog-post-full {
        background-color: #ffffff;
        border-radius: 18px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }

    .upload-time {
        font-size: 0.8rem;
        color: #689f38;
        margin-bottom: 0.5rem;
    }

    .category-tag {
        display: inline-block;
        padding: 0.5rem 1rem;
        color: white;
        font-weight: bold;
        border-radius: 20px;
        text-align: center;
        width: 100%;
    }

    .category-tag.影评 {
        background-color: #FF6B6B;
    }

    .category-tag.日常 {
        background-color: #4ECDC4;
    }

    .category-tag.观察 {
        background-color: #45B7D1;
    }

    .category-selector {
        margin-bottom: 20px;
    }

    .category-selector p {
        font-size: 0.9rem;
        color: #666;
        margin-bottom: 5px;
    }

    .category-buttons {
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
    }

    .category-buttons button {
        background-color: transparent !important;
        color: #333 !important;
        border: 1px solid #ddd !important;
        padding: 5px 15px !important;
        font-size: 0.9rem !important;
        border-radius: 20px !important;
        transition: all 0.3s ease !important;
    }

    .category-buttons button:hover {
        background-color: #f0f0f0 !important;
        border-color: #bbb !important;
    }

    .category-buttons button:focus {
        box-shadow: none !important;
        border-color: #999 !important;
    }

    /* 当分类被选中时的样式 */
    .category-buttons button[data-selected="true"] {
        background-color: #e6f3ff !important;
        border-color: #2196f3 !important;
        color: #2196f3 !important;
    }

    .article-container {
        background-color: #ffffff;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
        cursor: pointer;
    }

    .article-category {
        font-size: 0.9rem;
        font-weight: 500;
        color: #666;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 5px;
    }

    .article-divider {
        height: 1px;
        background-color: #e0e0e0;
        margin: 10px 0;
    }

    .article-title {
        font-size: 1.4rem;
        font-weight: 600;
        color: #333;
        margin: 10px 0;
    }

    .article-meta {
        font-size: 0.8rem;
        color: #999;
        margin-bottom: 10px;
    }

    .article-content {
        font-size: 1rem;
        line-height: 1.6;
        color: #555;
    }

    .article-container {
        background-color: #ffffff;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 10px;
    }

    .article-category {
        font-size: 1.1rem;
        font-weight: 700;
        color: #333;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 10px;
    }

    .article-divider {
        height: 1px;
        background-color: #e0e0e0;
        margin: 10px 0;
    }

    .article-title {
        font-size: 1.4rem;
        font-weight: 600;
        color: #333;
        margin: 10px 0;
    }

    .article-meta {
        font-size: 0.8rem;
        color: #999;
        margin-bottom: 10px;
    }

    .article-content {
        font-size: 1rem;
        line-height: 1.6;
        color: #555;
    }

    .streamlit-expanderHeader {
        font-size: 1.2rem !important;
        font-weight: 600 !important;
        color: #333 !important;
    }

    .streamlit-expanderHeader:hover {
        color: #4CAF50 !important;
    }

    </style>

    <script>
    // 为分类按钮添加选中效果
    document.addEventListener('DOMContentLoaded', (event) => {
        const buttons = document.querySelectorAll('.category-buttons button');
        buttons.forEach(button => {
            button.addEventListener('click', () => {
                buttons.forEach(b => b.setAttribute('data-selected', 'false'));
                button.setAttribute('data-selected', 'true');
            });
        });
    });
    </script>
    """, unsafe_allow_html=True)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def check_password(password, hashed_password):
    return hash_password(password) == hashed_password

def load_data(file_path, default_data):
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            return json.load(f)
    return default_data

def save_data(file_path, data):
    with open(file_path, 'w') as f:
        json.dump(data, f)

def user_auth():
    login_tab, register_tab = st.tabs(["登录", "注册"])
    
    with login_tab:
        username = st.text_input("用户名", key="login_username")
        password = st.text_input("密码", type="password", key="login_password")
        if st.button("用户登录", key="user_login"):
            users = load_data(USERS_FILE, {})
            if username in users and check_password(password, users[username]['password']):
                st.session_state.user = username
                st.session_state.show_auth = False
                st.success("登录成功!")
                st.rerun()
            else:
                st.error("用户名或密码错误")
    
    with register_tab:
        new_username = st.text_input("用户名", key="register_username")
        new_password = st.text_input("密码", type="password", key="register_password")
        avatar = st.file_uploader("上传头像", type=["png", "jpg", "jpeg"], key="register_avatar")
        if st.button("注册", key="user_register"):
            if new_username and new_password:
                users = load_data(USERS_FILE, {})
                if new_username not in users:
                    avatar_data = None
                    if avatar:
                        avatar_data = base64.b64encode(avatar.getvalue()).decode()
                    users[new_username] = {
                        'password': hash_password(new_password),
                        'avatar': avatar_data
                    }
                    save_data(USERS_FILE, users)
                    st.success("注册成功!请登录")
                    st.rerun()
                else:
                    st.error("用户名已存在")
            else:
                st.error("请填写用户名和密码")

def check_admin_password(password):
    return password == ADMIN_PASSWORD

def admin_login():
    admin_password = st.sidebar.text_input("管理员密码", type="password")
    if st.sidebar.button("管理员登录"):
        if check_admin_password(admin_password):
            st.session_state.admin = True
            st.sidebar.success("管理员登录成功！")
        else:
            st.sidebar.error("管理员密码错误")

def check_admin():
    return st.session_state.get('is_admin', False)

def update_user_profile():
    users = load_data(USERS_FILE, {})
    user = st.session_state.user
    if user in users:
        st.subheader("更新个人信息")
        new_avatar = st.file_uploader("更新头像", type=["png", "jpg", "jpeg"], key="update_avatar")
        if st.button("更新头像"):
            if new_avatar:
                users[user]['avatar'] = base64.b64encode(new_avatar.getvalue()).decode()
                save_data(USERS_FILE, users)
                st.success("头像更新成功!")
                st.rerun()
            else:
                st.error("请选择新的头像图片")

def add_new_post():
    st.header("发布新文章")
    with st.form("new_post_form"):
        title = st.text_input("文章标题")
        category = st.selectbox("选择专题", ["影评", "日常", "观察"])
        content = st.text_area("文章内容")
        image = st.file_uploader("上传图片", type=["png", "jpg", "jpeg"])
        submit_button = st.form_submit_button("发布")
        
        if submit_button:
            if title and content:
                image_data = None
                if image:
                    image_data = base64.b64encode(image.getvalue()).decode()
                posts = load_data(POSTS_FILE, [])
                beijing_tz = pytz.timezone('Asia/Shanghai')
                current_time = datetime.now(beijing_tz).strftime("%Y-%m-%d %H:%M:%S")
                posts.append({
                    "id": str(uuid.uuid4()),
                    "title": title,
                    "category": category,
                    "content": content,
                    "image": image_data,
                    "comments": [],
                    "views": 0,
                    "upload_time": current_time
                })
                save_data(POSTS_FILE, posts)
                st.success("文章发布成功!")
                st.rerun()
            else:
                st.error("请填写标题和内容!")

def delete_post(post_id):
    posts = load_data(POSTS_FILE, [])
    posts = [post for post in posts if post['id'] != post_id]
    save_data(POSTS_FILE, posts)
    st.success("文章删除成功!")
    st.rerun()

def add_comment(post_id, comment):
    posts = load_data(POSTS_FILE, [])
    users = load_data(USERS_FILE, {})
    for post in posts:
        if post['id'] == post_id:
            post['comments'].append({
                "author": st.session_state.user,
                "content": comment,
                "avatar": users[st.session_state.user].get('avatar', None)
            })
            break
    save_data(POSTS_FILE, posts)
    st.rerun()

def get_client_ip():
    try:
        return st.query_params.get('client_ip', ['unknown'])[0]
    except:
        return "unknown"

def view_post(post_id):
    posts = load_data(POSTS_FILE, [])
    views = load_data(VIEWS_FILE, {})
    
    if post_id not in views:
        views[post_id] = {}
    
    client_ip = get_client_ip()
    session_id = st.session_state.get('session_id', str(uuid.uuid4()))
    st.session_state['session_id'] = session_id
    
    current_time = datetime.now().isoformat()
    
    if client_ip not in views[post_id]:
        views[post_id][client_ip] = {}
    
    if session_id not in views[post_id][client_ip]:
        views[post_id][client_ip][session_id] = current_time
        
        # 增加文章的访问量
        for post in posts:
            if post['id'] == post_id:
                post['views'] += 1
                break
        
        save_data(POSTS_FILE, posts)
    else:
        # 检查上次访问时间，如果超过30分钟，视为新的访问
        last_view_time = datetime.fromisoformat(views[post_id][client_ip][session_id])
        if datetime.now() - last_view_time > timedelta(minutes=30):
            views[post_id][client_ip][session_id] = current_time
            
            # 增加文章的访问量
            for post in posts:
                if post['id'] == post_id:
                    post['views'] += 1
                    break
            
            save_data(POSTS_FILE, posts)
    
    save_data(VIEWS_FILE, views)

def get_unique_visitors(post_id):
    views = load_data(VIEWS_FILE, {})
    if post_id in views:
        return len(views[post_id])
    return 0

def count_words(text):
    # 计算所有字符的数量，包括中文字符、数字和标点符号
    return len(text)

def get_post_stats():
    posts = load_data(POSTS_FILE, [])
    total_posts = len(posts)
    total_words = sum(count_words(post['content']) for post in posts)
    
    # 创建发文记录数据
    if posts:
        post_dates = [pd.Timestamp(datetime.strptime(post['upload_time'], "%Y-%m-%d %H:%M:%S").date()) for post in posts]
        date_counts = pd.Series(post_dates).value_counts().sort_index()
        
        # 创建月度热图数据
        start_date = date_counts.index.min().replace(day=1)
        end_date = date_counts.index.max().replace(day=1) + pd.offsets.MonthEnd(1)
        date_range = pd.date_range(start=start_date, end=end_date, freq='D')
        heatmap_data = pd.Series(0, index=date_range)
        heatmap_data.update(date_counts)
    else:
        # 如果没有文章，创建一个月的空Series
        today = pd.Timestamp(datetime.now().date())
        start_date = today.replace(day=1)
        end_date = (start_date + pd.offsets.MonthEnd(1))
        heatmap_data = pd.Series(0, index=pd.date_range(start=start_date, end=end_date, freq='D'))
    
    return total_posts, total_words, heatmap_data

def create_heatmap(heatmap_data):
    current_year = datetime.now().year
    start_date = pd.Timestamp(f"{current_year}-01-01")
    end_date = pd.Timestamp(datetime.now().date())
    full_range = pd.date_range(start=start_date, end=end_date, freq='D')
    heatmap_data = heatmap_data.reindex(full_range, fill_value=0)

    # 创建一个7x53的矩阵，代表一年的52周加上可能的第53周
    calendar_data = [[0 for _ in range(53)] for _ in range(7)]

    for date, value in heatmap_data.items():
        week_num = (date - start_date).days // 7
        weekday = date.weekday()
        calendar_data[weekday][week_num] = value

    # Facebook 风格的颜色方案
    colorscale = [
        [0, "#ebedf0"],  # 最浅的颜色，代表无活动
        [0.2, "#9be9a8"],
        [0.4, "#40c463"],
        [0.6, "#30a14e"],
        [1, "#216e39"]   # 最深的颜色，代表最高活动
    ]

    fig = go.Figure(data=go.Heatmap(
        z=calendar_data,
        colorscale=colorscale,
        showscale=False,
    ))

    # 自定义布局
    fig.update_layout(
        height=200,
        xaxis=dict(
            showticklabels=False,
            showgrid=False,
            zeroline=False,
        ),
        yaxis=dict(
            ticktext=['一', '三', '五', '日'],
            tickvals=[0, 2, 4, 6],
            showgrid=False,
            zeroline=False,
        ),
        font=dict(family="Arial", size=10, color="#586069"),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=40, r=10, t=10, b=10),
    )

    # 添加月份标签
    month_labels = ['1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月']
    for i, month in enumerate(month_labels):
        fig.add_annotation(
            x=i * 4.3,  # 大
            y=-0.1,
            text=month,
            showarrow=False,
            xref="x",
            yref="y",
            xanchor="center",
            yanchor="top",
            font=dict(size=10, color="#586069")
        )

    return fig

def toggle_like(post_id, user):
    posts = load_data(POSTS_FILE, [])
    for post in posts:
        if post['id'] == post_id:
            if 'likes' not in post:
                post['likes'] = []
            if user in post['likes']:
                post['likes'].remove(user)
            else:
                post['likes'].append(user)
            break
    save_data(POSTS_FILE, posts)
    st.rerun()

def main():
    st.set_page_config(layout="wide", page_title="博客统计")
    set_custom_theme()

    # 初始化 session state
    if 'page' not in st.session_state:
        st.session_state.page = 'main'
    if 'show_auth' not in st.session_state:
        st.session_state.show_auth = False

    # 侧边栏
    with st.sidebar:
        st.title("博客导航")
        
        if st.button("回到主界面"):
            st.session_state.page = 'main'
        
        # 分类选择
        categories = ["全部", "影评", "日常", "观察"]
        st.markdown("""
        <div class="category-selector">
            <p>选择分类：</p>
            <div class="category-buttons">
        """, unsafe_allow_html=True)
        
        for category in categories:
            if st.button(category, key=f"cat_{category}", help=f"查看{category}类文章"):
                st.session_state.category_filter = category
        
        st.markdown("</div></div>", unsafe_allow_html=True)

        category_filter = st.session_state.get('category_filter', "全部")

        st.markdown("---")
        st.subheader("用户中心")
        if 'user' not in st.session_state or st.session_state.user is None:
            if st.button("登录/注册"):
                st.session_state.show_auth = True
        else:
            st.write(f"当前用户: {st.session_state.user}")
            if st.button("登出"):
                st.session_state.user = None
                st.session_state.admin = False
                st.rerun()

        if not st.session_state.get('admin', False):
            admin_login()

    # 显示登录/注册界面
    if st.session_state.show_auth:
        user_auth()

    # 主界面内容
    if st.session_state.page == 'main':
        st.title("我的博客")
        
        # 显示统计信息
        total_posts, total_words, heatmap_data = get_post_stats()
        st.markdown(f"""
        <div class="stats-container">
            <div class="stat-item">
                <div class="stat-value">{total_posts}</div>
                <div class="stat-label">总文章数</div>
            </div>
            <div class="stat-item">
                <div class="stat-value">{total_words}</div>
                <div class="stat-label">总字数</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # 显示发文热图
        st.subheader("发文记录")
        fig = create_heatmap(heatmap_data)
        st.plotly_chart(fig, use_container_width=True)

        # 添加新文章（仅管理员可见）
        if st.session_state.get('admin', False):
            add_new_post()

        # 文章列表
        st.header("最新文章")
        posts = load_data(POSTS_FILE, [])
        sorted_posts = sorted(posts, key=lambda x: x.get("upload_time", ""), reverse=True)
        
        for post in sorted_posts:
            if category_filter == "全部" or post["category"] == category_filter:
                with st.expander(f"{post['category']} | {post['title']}", expanded=False):
                    st.markdown(f"""
                    <div class="article-container">
                        <div class="article-category">{post['category']}</div>
                        <div class="article-divider"></div>
                        <h2 class="article-title">{html.escape(post['title'])}</h2>
                        <div class="article-meta">
                            <span class="upload-time">发布时间：{post.get("upload_time", "未知")}</span>
                        </div>
                        <div class="article-content">
                            <p>{html.escape(post['content'])}</p>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if post["image"]:
                        image = Image.open(BytesIO(base64.b64decode(post["image"])))
                        st.image(image, use_column_width=True)
                    
                    # 点赞功能
                    likes = post.get('likes', [])
                    like_count = len(likes)
                    current_user = st.session_state.get('user')
                    if current_user:
                        is_liked = current_user in likes
                        if st.button(
                            "👍 " + ("已赞" if is_liked else "点赞") + f" ({like_count})",
                            key=f"like_{post['id']}",
                            type="secondary" if not is_liked else "primary"
                        ):
                            toggle_like(post['id'], current_user)
                    else:
                        st.write(f"👍 {like_count} 人点赞")

    # 显示完整文章
    if 'current_post' in st.session_state:
        display_full_post(st.session_state.current_post)

# 添加这个新函数来显示完整文章
def display_full_post(post_id):
    posts = load_data(POSTS_FILE, [])
    post = next((p for p in posts if p['id'] == post_id), None)
    if post:
        st.markdown(f"""
        <div class="full-post">
            <h2>{html.escape(post['title'])}</h2>
            <div class="category-tag">{post['category']}</div>
            <p class="upload-time">发布时间：{post.get("upload_time", "未知")} | 字数：{count_words(post["content"])} 字</p>
            <p>{html.escape(post['content'])}</p>
        </div>
        """, unsafe_allow_html=True)
        
        if post["image"]:
            image = Image.open(BytesIO(base64.b64decode(post["image"])))
            st.image(image, use_column_width=True)
        
        # 添加评论功能等其他需要的功能
        
        if st.button("返回文章列表"):
            del st.session_state.current_post
            st.rerun()
    else:
        st.error("文章不存在")

    # 添加自定义 CSS
    st.markdown("""
    <style>
    .stats-container {
        display: flex;
        justify-content: space-between;
        margin-bottom: 16px;
    }
    .stat-item {
        background-color: white;
        border: 1px solid #e1e4e8;
        border-radius: 6px;
        padding: 16px;
        flex: 1;
        margin-right: 16px;
        text-align: center;
    }
    .stat-item:last-child {
        margin-right: 0;
    }
    .stat-value {
        font-size: 24px;
        font-weight: bold;
        color: #24292e;
    }
    .stat-label {
        font-size: 14px;
        color: #586069;
        margin-top: 4px;
    }
    .blog-post {
        margin-bottom: 20px;
    }
    .upload-time {
        color: #586069;
        font-size: 12px;
    }
    .comment {
        margin-bottom: 10px;
    }
    .comment-author {
        font-weight: bold;
    }
    .stButton>button {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        padding: 0.25rem 0.75rem;
        border-radius: 9999px;
        font-size: 14px;
        font-weight: 500;
        cursor: pointer;
        transition: all 0.2s;
    }

    .stButton>button[data-baseweb="button"] {
        background-color: #E7F3FF;
        color: #1877F2;
        border: none;
    }

    .stButton>button[data-baseweb="button"]:hover {
        background-color: #DBE7F2;
    }

    .stButton>button[kind="primary"] {
        background-color: #1877F2;
        color: white;
    }

    .stButton>button[kind="primary"]:hover {
        background-color: #166FE5;
    }
    </style>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()