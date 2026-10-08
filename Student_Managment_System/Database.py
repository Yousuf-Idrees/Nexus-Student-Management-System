import mysql.connector
import csv

class Database:

    def __init__(self,host='localhost',user='root',password='',database='Students_db'):
        self.host=host
        self.user=user
        self.password=password
        self.database=database

    def connect(self):
        return mysql.connector.connect(
            host=self.host,
            database=self.database,
            user=self.user,
            password=self.password
        )

    def insert_student(self,student):
        conn=self.connect()
        cursor=conn.cursor()
        query="INSERT INTO Students (name,age,grade) VALUES (%s, %s, %s)"
        cursor.execute(query,(student.name,student.age,student.grade))
        conn.commit()
        cursor.close()
        conn.close()

    def fetch_all_students(self):
        conn=self.connect()
        cursor=conn.cursor()
        query="SELECT * FROM Students"
        cursor.execute(query)
        rows=cursor.fetchall()
        cursor.close()
        conn.close()
        return rows

    def fetch_students_by_id(self,student_id):
        conn=self.connect()
        cursor=conn.cursor()
        query="SELECT * FROM Students WHERE id=%s"
        cursor.execute(query,(student_id,))
        rows=cursor.fetchone()
        cursor.close()
        conn.close()
        return rows

    def update_student(self, student):
        conn = None
        cursor = None
        try:
            conn = self.connect()
            cursor = conn.cursor()
            query = "UPDATE Students SET name=%s, age=%s, grade=%s WHERE id=%s"
            cursor.execute(query, (student.name, student.age, student.grade, student.student_id))
            conn.commit()

            if cursor.rowcount > 0:
                result = (True, f"Updated record #{student.student_id} successfully!")
            else:
                result = (False, f"No student found with ID #{student.student_id}.")

            cursor.close()
            conn.close()
            return result

        except Exception as e:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
            return False, f"Database error: {str(e)}"

    def delete_student(self, student_id):
        conn = None
        cursor = None
        try:
            conn = self.connect()
            cursor = conn.cursor()
            
            query = "DELETE FROM Students WHERE id = %s"
            cursor.execute(query, (student_id,))
            conn.commit()
            
            # Check if any row was affected
            if cursor.rowcount > 0:
                result = (True, f"Record #{student_id} deleted successfully.")
            else:
                result = (False, f"No student found with ID #{student_id}.")
                
            cursor.close()
            conn.close()
            return result

        except Exception as e:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
            return False, f"Database error: {str(e)}"

    def bulk_insert_csv(self,file_path_or_buffer):
        conn=self.connect()
        cursor=conn.cursor()

        if hasattr(file_path_or_buffer,'read'):
            content=file_path_or_buffer.read().decode('utf-8').splitlines()
            reader=csv.DictReader(content)
        else:
            with open(file_path_or_buffer,'r',encoding='utf-8') as f:
                reader=csv.DictReader(f)
        query="INSERT INTO Students (name,age,grade) VALUES (%s,%s,%s)"
        data=[(row['name'], int(row['age']), row['grade']) for row in reader]

        cursor.executemany(query,data)
        conn.commit()
        cursor.close()
        conn.close()