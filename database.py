import sqlite3

def get_connection():
    connection=sqlite3.connect("Job_Tracker.db")
    connection.row_factory=sqlite3.Row  
    return connection

def initialise():
    connection=get_connection()
    cursor=connection.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS jobs(
    id INTEGER PRIMARY KEY,
    company TEXT,
    location TEXT,
    role TEXT,
    salary INTEGER,
    status TEXT
    )
    """)
    connection.commit()
    connection.close()


def add_job(company, location, role, salary, status):
    try:
        connection=get_connection()
        cursor=connection.cursor()
        cursor.execute("""
        INSERT INTO jobs(company, location, role, salary, status)
        VALUES(?,?,?,?,?)
        """,(company, location, role, salary, status))
        connection.commit()
        id=cursor.lastrowid
        connection.close()
        return id
    except sqlite3.Error as error:
        connection.rollback()
        print(f"Database error: {error}")
        
def view_jobs():
    try:
        connection=get_connection()
        cursor=connection.cursor()
        cursor.execute("SELECT * FROM jobs")
        jobs=cursor.fetchall()
        connection.close()
        return jobs
    except sqlite3.Error as  error:
        print(f"Database error: {error}")    
        return None
        

def search(key_word):
    try:
        connection=get_connection()
        cursor=connection.cursor()
        cursor.execute("""
        SELECT * from jobs
        WHERE company LIKE ?
        OR location LIKE ?
        OR role LIKE ?
        OR status LIKE ?
        """,(f'%{key_word}%',f'%{key_word}%',f'%{key_word}%', f'%{key_word}%'))
        results=cursor.fetchall()
        connection.close()
        return results 
    except sqlite3.Error as error:
        print(f"Database error: {error}")
        return None


def update_job(id, field, new_value):
    try:
        connection=get_connection()
        cursor=connection.cursor()
        field_map={
            1:"company",
            2:"role",
            3:"status",
            4:"location",
            5:"salary"
        }
        column_name=field_map.get(field)
        cursor.execute(f"UPDATE jobs SET {column_name}=? WHERE id=?",(new_value, id))
        connection.commit()
        rows_affected=cursor.rowcount
        connection.close()
        return rows_affected
    except sqlite3.Error as error:
        connection.rollback()
        return None
           



def delete_job(id):
    try:
        connection=get_connection()
        cursor=connection.cursor()
        cursor.execute("DELETE FROM jobs WHERE id=?",(id,))
        connection.commit()
        rows_affected=cursor.rowcount
        connection.close()
        return rows_affected
    except sqlite3.Error as error:
        connection.rollback()
        print(f"Database error: {error}")
        return None

def get_job_by_id(id):
    connection=get_connection()
    try:
        cursor=connection.cursor()
        cursor.execute("""
        SELECT * FROM jobs
        WHERE id=?
        """,(id,))
        return cursor.fetchone()
    finally:
        connection.close()    
    
       
    

def get_job_by_status(status):
    try:
        connection=get_connection()
        cursor=connection.cursor()
        cursor.execute("""SELECT * FROM jobs WHERE status=?""",(status,))
        jobs=cursor.fetchall()
        connection.close()
        return jobs
    except sqlite3.Error as error:
        return None

def get_job_by_status_and_keyword(keyword, status):
        try:
            connection=get_connection()
            cursor=connection.cursor()
            cursor.execute("""SELECT * FROM jobs WHERE (company LIKE ? OR location LIKE ? OR role LIKE ?) AND status=?""",(f'%{keyword}%', f'%{keyword}%', f'%{keyword}%', status))
            jobs=cursor.fetchall()
            connection.close()
            return jobs
        except sqlite3.Error as error:
            return None
def delete_all():
    connection=get_connection()
    cursor=connection.cursor()
    cursor.execute("DELETE FROM jobs")
    connection.commit()
    rows_affected=cursor.rowcount
    return rows_affected        