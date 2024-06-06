import mysql.connector

def reset_database():
    try:
        # 连接数据库
        db_connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="jiayu123",
            database="work"
        )
        cursor = db_connection.cursor()

        # 删除表
        cursor.execute("DROP TABLE IF EXISTS student_courses")
        cursor.execute("DROP TABLE IF EXISTS students")
        cursor.execute("DROP TABLE IF EXISTS courses")

        # 创建学生信息表
        cursor.execute("""
            CREATE TABLE students (
                student_id INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
                name VARCHAR(255),
                gender ENUM('Male', 'Female'),
                age INT
            );
        """)

        # 创建课程表
        cursor.execute("""
            CREATE TABLE courses (
                course_id INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
                course_name VARCHAR(255),
                teacher VARCHAR(255),
                credits DECIMAL(4,2)
            );
        """)

        # 创建学生选课表
        cursor.execute("""
            CREATE TABLE student_courses (
                student_id INT NOT NULL,
                course_id INT,
                grade DECIMAL(5,2),
                PRIMARY KEY (student_id, course_id),
                FOREIGN KEY (student_id) REFERENCES students(student_id),
                FOREIGN KEY (course_id) REFERENCES courses(course_id)
            );
        """)

        # 插入示例数据到学生信息表
        cursor.execute("""
            INSERT INTO students (name, gender, age) VALUES
            ('Alice', 'Female', 20),
            ('Bob', 'Male', 22),
            ('Charlie', 'Male', 21);
        """)

        # 插入示例数据到课程表
        cursor.execute("""
            INSERT INTO courses (course_name, teacher, credits) VALUES
            ('Mathematics', 'Dr. Smith', 3.00),
            ('Physics', 'Dr. Johnson', 4.00),
            ('Chemistry', 'Dr. Lee', 3.50);
        """)

        # 插入示例数据到学生选课表
        cursor.execute("""
            INSERT INTO student_courses (student_id, course_id, grade) VALUES
            (1, 1, 85.00),
            (1, 2, 90.00),
            (2, 1, 78.00),
            (3, 3, 88.50);
        """)

        # 提交更改
        db_connection.commit()
        print("数据库重置并初始化成功")

    except mysql.connector.Error as err:
        print(f"数据库错误：{err}")
    finally:
        if db_connection.is_connected():
            cursor.close()
            db_connection.close()

if __name__ == "__main__":
    reset_database()
