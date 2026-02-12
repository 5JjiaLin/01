"""
直接创建管理员账户 hjl
"""
import sys
import os
from pathlib import Path
from werkzeug.security import generate_password_hash
from datetime import datetime

# 添加backend目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database.init_db import get_connection

def create_admin_hjl():
    """创建管理员账户 hjl"""
    username = "hjl"
    email = "hjl@example.com"
    full_name = "黄金龙"
    password = "hjl123456"

    try:
        conn = get_connection()
        cursor = conn.cursor()

        # 检查用户名是否已存在
        cursor.execute("SELECT id, is_admin FROM users WHERE username = ?", (username,))
        existing_user = cursor.fetchone()

        if existing_user:
            user_id, is_admin = existing_user
            if is_admin:
                print(f"⚠️  用户 '{username}' 已经是管理员")
                conn.close()
                return
            else:
                # 将现有用户升级为管理员
                cursor.execute("UPDATE users SET is_admin = 1 WHERE id = ?", (user_id,))
                conn.commit()
                print(f"✅ 用户 '{username}' 已升级为管理员")
                conn.close()
                return

        # 检查邮箱是否已存在
        cursor.execute("SELECT id FROM users WHERE email = ?", (email,))
        if cursor.fetchone():
            print(f"❌ 邮箱 '{email}' 已被使用")
            conn.close()
            return

        # 创建管理员账户
        password_hash = generate_password_hash(password)

        cursor.execute("""
            INSERT INTO users (username, email, password_hash, full_name, is_admin, is_active, created_at, updated_at)
            VALUES (?, ?, ?, ?, 1, 1, ?, ?)
        """, (username, email, password_hash, full_name, datetime.utcnow(), datetime.utcnow()))

        conn.commit()
        user_id = cursor.lastrowid

        print("\n" + "=" * 50)
        print("✅ 管理员账户创建成功！")
        print("=" * 50)
        print(f"用户ID: {user_id}")
        print(f"用户名: {username}")
        print(f"邮箱: {email}")
        print(f"全名: {full_name}")
        print(f"管理员权限: 是")
        print("\n请使用此账户登录管理后台: http://localhost:5000/admin-login.html")
        print("=" * 50)

        conn.close()

    except Exception as e:
        print(f"❌ 创建管理员失败: {str(e)}")
        if conn:
            conn.rollback()
            conn.close()


if __name__ == "__main__":
    create_admin_hjl()
