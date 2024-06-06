import tkinter as tk
from tkinter import messagebox
import mysql.connector
import insert

class AdminPage:
    def __init__(self, root):
        self.root = root
        self.root.title("管理员界面")  # 设置窗口标题

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

        # 设置窗口大小
        self.root.geometry("800x600")

        # 创建按钮框架
        button_frame = tk.Frame(root)
        button_frame.pack(fill=tk.X)

        # 创建按钮
        tk.Button(button_frame, text="学生", command=self.show_students).pack(side=tk.LEFT, fill=tk.X, expand=True)
        tk.Button(button_frame, text="课程", command=self.show_courses).pack(side=tk.LEFT, fill=tk.X, expand=True)
        tk.Button(button_frame, text="选课", command=self.show_student_courses).pack(side=tk.LEFT, fill=tk.X, expand=True)
        tk.Button(button_frame, text="插入", command=self.insert_data).pack(side=tk.LEFT, fill=tk.X, expand=True)
        tk.Button(button_frame, text="查询", command=self.query_data).pack(side=tk.LEFT, fill=tk.X, expand=True)
        tk.Button(button_frame, text="删除", command=self.delete_data).pack(side=tk.LEFT, fill=tk.X, expand=True)
        tk.Button(button_frame, text="更新", command=self.update_data).pack(side=tk.LEFT, fill=tk.X, expand=True)

        # 创建属性名框架
        self.attributes_frame = tk.Frame(self.root)
        self.attributes_frame.pack(fill=tk.X)

        # 创建学生数据框架
        self.data_frame = tk.Frame(self.root)
        self.data_frame.pack(fill=tk.BOTH, expand=True)

    def show_students(self):
        try:
            # 重新连接数据库
            self.db_connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="jiayu123",
                database="work"
            )
            self.cursor = self.db_connection.cursor()
            # 清空现有的学生数据部分
            for widget in self.data_frame.winfo_children():
                widget.destroy()
            for widget in self.attributes_frame.winfo_children():
                widget.destroy()
            # 学生属性名
            student_attributes = ["学生ID", "姓名", "性别", "年龄"]
            # 显示属性名
            for i, attribute in enumerate(student_attributes):
                tk.Label(self.attributes_frame, text=attribute, relief=tk.RIDGE, width=28).grid(row=0, column=i)

            # 查询学生表的数据
            self.cursor.execute("SELECT * FROM students")
            students = self.cursor.fetchall()

            # 显示学生数据
            for i, student in enumerate(students):
                for j, data in enumerate(student):
                    tk.Label(self.data_frame, text=data, relief=tk.RIDGE, width=28).grid(row=i+1, column=j)  # 将数据放在属性名下方

        except mysql.connector.Error as err:
            print(f"数据库错误：{err}")

    def show_courses(self):
        try:
            # 重新连接数据库
            self.db_connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="jiayu123",
                database="work"
            )
            self.cursor = self.db_connection.cursor()

            # 清空现有的课程数据部分
            for widget in self.data_frame.winfo_children():
                widget.destroy()
            for widget in self.attributes_frame.winfo_children():
                widget.destroy()
            # 课程属性名
            course_attributes = ["课程ID", "课程名称", "教师", "学分"]

            # 显示属性名
            for i, attribute in enumerate(course_attributes):
                tk.Label(self.attributes_frame, text=attribute, relief=tk.RIDGE, width=28).grid(row=0, column=i)

            # 查询课程表的数据
            self.cursor.execute("SELECT * FROM courses")
            courses = self.cursor.fetchall()

            # 显示课程数据
            for i, course in enumerate(courses):
                for j, data in enumerate(course):
                    tk.Label(self.data_frame, text=data, relief=tk.RIDGE, width=28).grid(row=i+1, column=j)  # 将数据放在属性名下方

        except mysql.connector.Error as err:
            print(f"数据库错误：{err}")



    def show_student_courses(self):
        try:
            # 重新连接数据库
            self.db_connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="jiayu123",
                database="work"
            )
            self.cursor = self.db_connection.cursor()

            # 清空现有的学生选课数据部分
            for widget in self.data_frame.winfo_children():
                widget.destroy()
            for widget in self.attributes_frame.winfo_children():
                widget.destroy()
            # 学生选课属性名
            student_courses_attributes = ["学生ID", "课程ID", "成绩"]

            # 显示属性名
            for i, attribute in enumerate(student_courses_attributes):
                tk.Label(self.attributes_frame, text=attribute, relief=tk.RIDGE, width=38).grid(row=0, column=i)

            # 查询学生选课表的数据
            self.cursor.execute("SELECT * FROM student_courses")
            student_courses = self.cursor.fetchall()

            # 显示学生选课数据
            for i, sc in enumerate(student_courses):
                for j, data in enumerate(sc):
                    tk.Label(self.data_frame, text=data, relief=tk.RIDGE, width=38).grid(row=i+1, column=j)  # 将数据放在属性名下方

        except mysql.connector.Error as err:
            print(f"数据库错误：{err}")


    def insert_data(self):
        insert_window = tk.Toplevel(self.root)
        insert_window.title("插入数据")

        options = ["学生", "课程", "选课"]
        selected_option = tk.StringVar(insert_window)
        selected_option.set(options[0])

        dropdown = tk.OptionMenu(insert_window, selected_option, *options, command=lambda option: self.dropdown_callback(option, insert_window))
        dropdown.pack()

        insert_button = tk.Button(insert_window, text="插入", command=lambda: self.insert_record(selected_option, insert_window))
        insert_button.pack()

        self.dropdown_callback(selected_option.get(), insert_window)
    def dropdown_callback(self, selected_option, window):
        self.clear_input_fields(window)
        if selected_option == "学生":
            self.show_student_input_fields(window)
        elif selected_option == "课程":
            self.show_course_input_fields(window)
        elif selected_option == "选课":
            self.show_student_course_input_fields(window)
            
            
    def insert_record(self, selected_option, window):
        if selected_option.get() == "学生":
            student_id = self.student_id_entry.get()
            name = self.name_entry.get()
            gender = self.gender_entry.get()
            age = self.age_entry.get()
            try:
                self.cursor.execute("INSERT INTO students (student_id, name, gender, age) VALUES (%s, %s, %s, %s)", (student_id, name, gender, age))
                self.db_connection.commit()
                messagebox.showinfo("成功", "学生信息插入成功")
                window.destroy()  # 销毁对话框
            except mysql.connector.Error as err:
                messagebox.showerror("错误", f"插入学生信息时发生错误: {err}")
        elif selected_option.get() == "课程":
            course_id = self.course_id_entry.get()
            course_name = self.course_name_entry.get()
            teacher = self.teacher_entry.get()
            credits = self.credits_entry.get()
            try:
                self.cursor.execute("INSERT INTO courses (course_id, course_name, teacher, credits) VALUES (%s, %s, %s, %s)", (course_id, course_name, teacher, credits))
                self.db_connection.commit()
                messagebox.showinfo("成功", "课程信息插入成功")
                window.destroy()  # 销毁对话框
            except mysql.connector.Error as err:
                messagebox.showerror("错误", f"插入课程信息时发生错误: {err}")
        elif selected_option.get() == "选课":
            student_id = self.sc_student_id_entry.get()
            course_id = self.sc_course_id_entry.get()
            grade = self.grade_entry.get()
            try:
                self.cursor.execute("INSERT INTO student_courses (student_id, course_id, grade) VALUES (%s, %s, %s)", (student_id, course_id, grade))
                self.db_connection.commit()
                messagebox.showinfo("成功", "选课信息插入成功")
                window.destroy()  # 销毁对话框
            except mysql.connector.Error as err:
                messagebox.showerror("错误", f"插入选课信息时发生错误: {err}")

    def show_student_input_fields(self, window):
        self.clear_input_fields(window)
        student_id_label = tk.Label(window, text="学生ID:")
        student_id_label.pack()
        self.student_id_entry = tk.Entry(window)
        self.student_id_entry.pack()

        name_label = tk.Label(window, text="姓名:")
        name_label.pack()
        self.name_entry = tk.Entry(window)
        self.name_entry.pack()

        gender_label = tk.Label(window, text="性别:")
        gender_label.pack()
        self.gender_entry = tk.Entry(window)
        self.gender_entry.pack()

        age_label = tk.Label(window, text="年龄:")
        age_label.pack()
        self.age_entry = tk.Entry(window)
        self.age_entry.pack()

    def show_course_input_fields(self, window):
        self.clear_input_fields(window)
        course_id_label = tk.Label(window, text="课程ID:")
        course_id_label.pack()
        self.course_id_entry = tk.Entry(window)
        self.course_id_entry.pack()

        course_name_label = tk.Label(window, text="课程名称:")
        course_name_label.pack()
        self.course_name_entry = tk.Entry(window)
        self.course_name_entry.pack()

        teacher_label = tk.Label(window, text="教师:")
        teacher_label.pack()
        self.teacher_entry = tk.Entry(window)
        self.teacher_entry.pack()

        credits_label = tk.Label(window, text="学分:")
        credits_label.pack()
        self.credits_entry = tk.Entry(window)
        self.credits_entry.pack()

    def show_student_course_input_fields(self, window):
        self.clear_input_fields(window)
        sc_student_id_label = tk.Label(window, text="学生ID:")
        sc_student_id_label.pack()
        self.sc_student_id_entry = tk.Entry(window)
        self.sc_student_id_entry.pack()

        sc_course_id_label = tk.Label(window, text="课程ID:")
        sc_course_id_label.pack()
        self.sc_course_id_entry = tk.Entry(window)
        self.sc_course_id_entry.pack()

        grade_label = tk.Label(window, text="成绩:")
        grade_label.pack()
        self.grade_entry = tk.Entry(window)
        self.grade_entry.pack()

    def clear_input_fields(self, window):
        for widget in window.winfo_children():
            if isinstance(widget, tk.Entry) or isinstance(widget, tk.Label):
                widget.pack_forget()

    
    
    
    
    def create_view(self):
        try:
            # 创建视图
            self.cursor.execute("""
                CREATE OR REPLACE VIEW student_course_view AS
                SELECT s.student_id, s.age, sc.course_id
                FROM students s
                JOIN student_courses sc ON s.student_id = sc.student_id;
            """)
            self.db_connection.commit()
            print("视图创建成功")
        except mysql.connector.Error as err:
            print(f"创建视图错误：{err}")
            
    def query_data(self):
        try:
            self.create_view()
            # 清空现有的数据部分
            for widget in self.data_frame.winfo_children():
                widget.destroy()
            for widget in self.attributes_frame.winfo_children():
                widget.destroy()

            # 创建视图属性名
            view_attributes = ["学生ID", "年龄", "课程ID"]

            # 显示属性名
            for i, attribute in enumerate(view_attributes):
                tk.Label(self.attributes_frame, text=attribute, relief=tk.RIDGE, width=28).grid(row=0, column=i)

            # 查询视图的数据
            self.cursor.execute("SELECT * FROM student_course_view")
            result = self.cursor.fetchall()

            # 显示视图数据
            for i, row in enumerate(result):
                for j, data in enumerate(row):
                    tk.Label(self.data_frame, text=data, relief=tk.RIDGE, width=28).grid(row=i+1, column=j)  # 将数据放在属性名下方

        except mysql.connector.Error as err:
            print(f"数据库错误：{err}")
            messagebox.showerror("错误", f"查询错误：{err}")
    
    
    

    def delete_data(self):
        # 清除现有的属性名框架和数据框架
        self.attributes_frame.destroy()
        self.data_frame.destroy()

        # 创建新的属性名框架
        self.attributes_frame = tk.Frame(self.root)
        self.attributes_frame.pack(fill=tk.X)

        # 创建新的数据框架
        self.data_frame = tk.Frame(self.root)
        self.data_frame.pack(fill=tk.BOTH, expand=True)

        # 显示删除条件信息
        tk.Label(self.data_frame, text="涉及学生表和选课表").pack()
        tk.Label(self.data_frame, text="表连接字段为student_id").pack()
        entry_label = tk.Label(self.data_frame, text="删除选了“1”课程的且年龄大于20的学生的选课信息:")
        entry_label.pack()

        def perform_deletion():

            try:
                # 检查是否存在事务
                if self.db_connection.in_transaction:
                    self.db_connection.commit()

                # 开始新的事务
                self.db_connection.start_transaction()

                # 构建 SQL 查询
                sql = "DELETE student_courses \
                    FROM student_courses \
                    JOIN students ON students.student_id = student_courses.student_id \
                    WHERE students.age > 20 AND student_courses.course_id = '1'"

                # 执行删除操作
                self.cursor.execute(sql)

                # 提交事务
                self.db_connection.commit()

                messagebox.showinfo("成功", "删除操作已成功执行！")

            except mysql.connector.Error as err:
                # 出现错误时回滚事务
                self.db_connection.rollback()
                messagebox.showerror("错误", f"删除操作失败: {err}")


        # 创建删除按钮
        delete_button = tk.Button(self.data_frame, text="删除", command=perform_deletion)
        delete_button.pack()



    def update_data(self):
        # 清除现有的属性名框架和数据框架
        self.attributes_frame.destroy()
        self.data_frame.destroy()

        # 创建新的属性名框架
        self.attributes_frame = tk.Frame(self.root)
        self.attributes_frame.pack(fill=tk.X)

        # 创建新的数据框架
        self.data_frame = tk.Frame(self.root)
        self.data_frame.pack(fill=tk.BOTH, expand=True)

        # 显示更新提示信息
        tk.Label(self.data_frame, text="更新选课表中年龄大于").pack()
        input_age_entry = tk.Entry(self.data_frame)
        input_age_entry.pack()
        tk.Label(self.data_frame, text="的学生的成绩为0").pack()

        # 创建更新按钮
        update_button = tk.Button(self.data_frame, text="更新", command=lambda: self.perform_update(input_age_entry.get()))
        update_button.pack()

    def perform_update(self, input_age):
        try:
            input_age = int(input_age)  # 将输入的年龄转换为整数

            # 创建存储过程
            def create_update_student_score_procedure(self):
                try:
                    # 检查是否存在同名的存储过程，如果存在则删除
                    self.cursor.execute("DROP PROCEDURE IF EXISTS UpdateStudentScore")

                    # 创建存储过程
                    self.cursor.execute(f"""
                        CREATE PROCEDURE UpdateStudentScore(IN input_age INT)
                        BEGIN
                            UPDATE student_courses sc
                            JOIN students s ON sc.student_id = s.student_id
                            SET sc.grade = 0
                            WHERE s.age > input_age AND sc.course_id = '2';
                        END
                    """)
                    print("存储过程创建成功")
                except mysql.connector.Error as err:
                    print(f"创建存储过程错误：{err}")

            # 调用存储过程
            def call_update_student_score_procedure(cursor, input_age):
                try:
                    cursor.callproc("UpdateStudentScore", [input_age])
                    print("存储过程调用成功")
                    self.db_connection.commit()  # 提交事务
                    messagebox.showinfo("成功", "更新操作已成功执行！")
                except mysql.connector.Error as err:
                    print(f"调用存储过程错误：{err}")
                    self.db_connection.rollback()  # 回滚事务
                    messagebox.showerror("错误", f"更新操作失败: {err}")

            # 创建存储过程
            create_update_student_score_procedure(self)

            # 调用存储过程
            call_update_student_score_procedure(self.cursor, input_age)

        except ValueError:
            messagebox.showerror("错误", "年龄必须为整数！")
        except mysql.connector.Error as err:
            print(f"数据库错误：{err}")


if __name__ == "__main__":
    root = tk.Tk()
    app = AdminPage(root)
    root.mainloop()
