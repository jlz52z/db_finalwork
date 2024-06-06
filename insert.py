import mysql.connector

# 连接到数据库
db_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="jiayu123",
    database="work"
)

# 创建游标对象
cursor = db_connection.cursor()

# 查询数据库中所有的触发器名称
cursor.execute("SHOW TRIGGERS")
triggers = cursor.fetchall()

# 删除每个触发器
for trigger in triggers:
    trigger_name = trigger[0]
    drop_trigger_query = f"DROP TRIGGER IF EXISTS {trigger_name}"
    cursor.execute(drop_trigger_query)

# 创建触发器检查学生插入操作的参数合法性
create_student_insert_trigger_query = """
CREATE TRIGGER before_insert_student
BEFORE INSERT ON students
FOR EACH ROW
BEGIN
    IF NEW.gender NOT IN ('Male', 'Female') THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Error: Gender must be Male or Female';
    END IF;
    
    -- 检查年龄是否合法
    IF NEW.age <= 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Error: Age must be non-negative';
    END IF;
    
    IF NEW.age > 35 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Error: Age must be smaller than 36';
    END IF;

    -- 检查姓名是否为空
    IF NEW.name = '' THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Error: Name cannot be empty';
    END IF;

END;
"""

cursor.execute(create_student_insert_trigger_query)

# 创建触发器检查课程插入操作的参数合法性
create_courses_insert_trigger_query = """
CREATE TRIGGER before_insert_course
BEFORE INSERT ON courses
FOR EACH ROW
BEGIN
    -- 检查课程名称是否为空
    IF NEW.course_name = '' THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Error: Course name cannot be empty';
    END IF;

    -- 检查教师名称是否为空
    IF NEW.teacher = '' THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Error: Teacher name cannot be empty';
    END IF;

    -- 检查学分是否合法
    IF NEW.credits <= 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Error: Credits must be greater than 0';
    END IF;
    
    IF NEW.credits > 5 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Error: Credits must be smaller than 6';
    END IF;
    
END;
"""

cursor.execute(create_courses_insert_trigger_query)

# 创建触发器检查学生选课插入操作的参数合法性
create_student_courses_insert_trigger_query = """
CREATE TRIGGER before_insert_student_course
BEFORE INSERT ON student_courses
FOR EACH ROW
BEGIN
    -- 检查成绩是否合法
    IF NEW.grade < 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Error: Grade must be non-negative';
    END IF;
    
    
    IF NEW.grade > 100 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Error: Grade must be smaller than 101';
    END IF;
END;
"""
cursor.execute(create_student_courses_insert_trigger_query)


