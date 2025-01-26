from flask import Flask, request, redirect, url_for, render_template, session, flash
#from flask_mysqldb import MySQL
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from werkzeug.security import generate_password_hash, check_password_hash
#import MySQLdb
#from MySQLdb import _mysql
from datetime import datetime
import os
from graf import generate_graph
from db import create_database
import mysql.connector



connection = mysql.connector.connect(
        host="localhost",
        user="sugrp005",
        password="E24x100GRPx62484",
        database="sugrp005"

    )
create_database(connection)

app = Flask(__name__)
app.secret_key = '1234'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
UPLOAD_FOLDER = '/home/sugrp005/PythonProject/static/gemt_graf'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#  MariaDB connection
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'sugrp005'
app.config['MYSQL_PASSWORD'] = 'E24x100GRPx62484'
app.config['MYSQL_DB'] = 'sugrp005'

#mysql = MySQL(app)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/db_test')
def db_test():
    try:
        cursor = connection.cursor()
        cursor.execute('SELECT 1')
        cursor.close()
        return 'Database connection successful!'
    except Exception as e:
        return f'Error connecting to the database: {e}'


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        sygesikring_id = request.form['sygesikring_id']
        age = int(request.form['age'])
        date_of_birth = request.form['date_of_birth']

        try:
            date_of_birth = datetime.strptime(date_of_birth, "%d/%m/%Y").date()  # Example: "24/01/2025"
        except ValueError:
            flash('Invalid date format. Please use DD/MM/YYYY.', 'danger')
            return render_template('register.html')

        hashed_password = generate_password_hash(password)  # Hash the password
        cursor = connection.cursor()
        cursor.execute(
            'INSERT INTO users (username, password, sygesikring_id, age, date_of_birth) VALUES (%s, %s, %s, %s, %s)',
            (username, hashed_password, sygesikring_id, age, date_of_birth)
        )
        connection.commit()
        cursor.close()

        flash('Bruger registreret! Log ind.', 'success')
        return redirect(url_for('index'))
    return render_template('register.html')




@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cursor = connection.cursor(dictionary = True)
        cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
        user = cursor.fetchone()

        if user and check_password_hash(user['password'], password):  # Check password
            flash('Login successful!', 'success')
            session['username'] = username
            return redirect(url_for('Patient_homepage'))
        else:
            flash('Login failed. Check your username or password.', 'danger')
    return "Invalid credentials. Please try again."

# Route for healthcare personnel login page
@app.route('/logindsundhedsp', methods=['GET'])
def logindsundhedsp():
    return render_template('Logindsundhedsp.html')




# Route for healthcare personnel login processing
@app.route('/login_personale', methods=['POST'])
def login_personale():
    username = request.form.get('username')
    password = request.form.get('password')

    if username == 'personale' and password == '1234':
        return redirect(url_for('Personale_homepage'))
    return "Invalid credentials. Please try again."

class UploadFileform(FlaskForm):
    file= FileField("file")
    submit = SubmitField("Upload File")

@app.route('/Patient_homepage', methods=['GET', 'POST'])
def Patient_homepage():
    form = UploadFileform()
    if form.validate_on_submit():
        file = form.file.data  # Get the uploaded file

        if file and allowed_file(file.filename):  # Check if file is valid
            username = session.get('username')  # logged-in user's username

            cursor = connection.cursor(dictionary= True)

            # Query the database
            cursor.execute('SELECT file_data, file_data2 FROM users WHERE username = %s', (username,))
            user_data = cursor.fetchone()  # Fetch the data for the current user
            cursor.close()

            if user_data:  # Ensure we found the user data
                # Check if the first file (file_data) is uploaded
                if user_data['file_data'] is None:  # If the first file is not uploaded
                    file_binary = file.read()  # Read the file contents
                    cursor = connection.cursor()
                    cursor.execute('UPDATE users SET file_data = %s WHERE username = %s', (file_binary, username))
                    connection.commit()
                    cursor.close()
                    flash('First file uploaded successfully!', 'success')

                #  Check if the second file (file_data2) is uploaded
                elif user_data['file_data2'] is None:  # If the second file is not uploaded
                    file_binary = file.read()  # Read the file contents
                    cursor = connection.cursor()
                    cursor.execute('UPDATE users SET file_data2 = %s WHERE username = %s', (file_binary, username))
                    connection.commit()
                    cursor.close()
                    flash('Second file uploaded successfully!', 'success')

                else:
                    # If both files are already uploaded
                    flash('You have already uploaded both files.', 'danger')

                return redirect(url_for('Patient_homepage'))  # Redirect to the same page

            else:
                flash('No user data found.', 'danger')
                return redirect(url_for('index'))  # Redirect to index if no user data

        else:
            flash('Invalid file type. Please upload a valid file.', 'danger')

    return render_template('Patienthomepage.html', form=form)

#tjekke om filen er uploaded
@app.route('/check_file')
def check_file():
    username = session.get('username')
    cursor = connection.cursor(dictionary= True)
    cursor.execute('SELECT file_data FROM users WHERE username = %s', (username,))
    file_data = cursor.fetchone()
    cursor.close()

    if file_data and file_data['file_data']:
        return f"File found for {username}. Size: {len(file_data['file_data'])} bytes."
    else:
        return f"No file found for {username}."


@app.route('/Personale_homepage')
def Personale_homepage():
    # Får patientinfo fra databasen
    cursor = connection.cursor(dictionary=True)
    cursor.execute('SELECT username, sygesikring_id, age, date_of_birth FROM users')
    patients = cursor.fetchall()
    cursor.close()

    return render_template('Personalehomepage.html', patients=patients)



@app.route('/patientdata')
def patientdata():
    return render_template('Patientdata.html')


@app.route('/view_patient_graph/<username>', methods=['GET'])
def view_patient_graph(username):
    try:
        # Fetch data from the database
        cursor = connection.cursor()
        cursor.execute("SELECT file_data, file_data2 FROM users WHERE username = %s", (username,))
        result = cursor.fetchone()

        if not result:
            print("No data fetched from the database.")
            return "Error: No data available in the database."

        file_data = result[0]
        file_data2 = result[1]

        # Save files to the upload folder
        file1_path = os.path.join(app.config['UPLOAD_FOLDER'], 'rec_1.dat')
        file2_path = os.path.join(app.config['UPLOAD_FOLDER'], 'rec_1.hea')

        # Ensure the folder exists
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

        with open(file1_path, 'wb') as f:
            f.write(file_data)
        with open(file2_path, 'wb') as f:
            f.write(file_data2)

        print(f"Files saved: {file1_path}, {file2_path}")

        # Generate the graph and get the result message
        result = generate_graph()
        print(result)

        # Path to the saved graph image
        graph_path = 'patient_graph.png'

        # Ensure the graph has been created
        if not os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], graph_path)):
            return "Graph not found", 404

        # Render the graph in the template
        return render_template('Personalehomepage.html', graph_path=graph_path)

    except Exception as e:
        print(f"An error occurred: {e}")
        return f"Error: {e}"


if __name__ == '__main__':
    app.run(debug=True)