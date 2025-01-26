import mysql.connector

def create_database(connection):

    cursor = connection.cursor()
    cursor.execute("""
           CREATE TABLE IF NOT EXISTS users (
               id INT AUTO_INCREMENT PRIMARY KEY,
               file_data BLOB DEFAULT NULL,
               username VARCHAR(100) NOT NULL,
               password  VARCHAR(250) NOT NULL,
               age INT NOT NULL,
               sygesikring_id VARCHAR(15) NOT NULL,
               date_of_birth DATE NOT NULL,
               file_data2 BLOB DEFAULT NULL
            
           )
       """)
    connection.commit()
    cursor.close()

