import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import mysql.connector
from admin_page import AdminPage
from reset_database import reset_database
admin_account = "admin"
admin_password = "admin"
class LoginPage:
    def __init__(self, root):
        self.root = root
        self.root.title("学生信息管理系统")  # 设置窗口标题

        # 连接数据库
        try:
            self.db_connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="jiayu123",
                database="work"
            )
            self.cursor = self.db_connection.cursor()
            print("成功连接到数据库")
        except mysql.connector.Error as err:
            print(f"数据库连接错误：{err}")

        # 添加标题标签
        self.title_label = tk.Label(root, text="学生信息管理系统", font=("weiruanyahei", 20))
        self.title_label.grid(row=0, column=0, columnspan=3, pady=10)

        # 创建PanedWindow
        self.paned_window = ttk.PanedWindow(root, orient=tk.HORIZONTAL)
        self.paned_window.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

        # 标签和输入框
        tk.Label(self.paned_window, text="账号：").grid(row=0, column=0, sticky="w")
        tk.Label(self.paned_window, text="密码：").grid(row=1, column=0, sticky="w")

        self.account_entry = tk.Entry(self.paned_window)
        self.password_entry = tk.Entry(self.paned_window, show="*")

        self.account_entry.grid(row=0, column=1, sticky="ew")
        self.password_entry.grid(row=1, column=1, sticky="ew")

        # 登录和退出按钮
        tk.Button(root, text="登录", command=self.login,width=14).grid(row=2, column=1, pady=10)
        tk.Button(root, text="退出", command=self.quit,width=14).grid(row=2, column=2, pady=10)
        

    def login(self):
        # 获取输入的账号和密码
        account = self.account_entry.get()
        password = self.password_entry.get()

        # 检查账号和密码是否正确
        if account == admin_account and password == admin_password:
            # 清空输入框内容
            self.account_entry.delete(0, tk.END)
            self.password_entry.delete(0, tk.END)

            # 跳转到管理员界面
            self.root.destroy()  # 销毁登录界面窗口
            admin_root = tk.Tk()  # 创建管理员界面窗口
            admin_app = AdminPage(admin_root)  # 运行管理员界面
            admin_root.mainloop()
        else:
            # 弹出错误信息窗口
            messagebox.showerror("登录失败", "账号或密码错误")

            # 清空输入框内容
            self.account_entry.delete(0, tk.END)
            self.password_entry.delete(0, tk.END)


    def quit(self):
        self.root.destroy()

if __name__ == "__main__":
    reset_database()
    root = tk.Tk()
    app = LoginPage(root)
    root.mainloop()
