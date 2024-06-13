import sqlite3
from tkinter import messagebox
# Create the SQLite database and Patients table if they don't exist
def create_user_credentials_database():
    # Connect to the new user credentials database
    connection = sqlite3.connect("user_credentials.db")
    cursor = connection.cursor()

    # Create a table to store user credentials
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS UserCredentials (
            ID INTEGER PRIMARY KEY,
            UserName TEXT,
            Password TEXT
        )
    ''')

def create_database(user_id):
    database_name = f"user_{user_id}_data.db"
    connection = sqlite3.connect(database_name)
    cursor = connection.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Patients (
            ID INTEGER PRIMARY KEY,
            Date DATE,
            Name TEXT NOT NULL,
            Age INTEGER,
            Gender TEXT,
            Phone TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Diagnosis2 (
            ID INTEGER PRIMARY KEY,
            PatientID INTEGER,
            ChiefComplaint TEXT,
            ClinicalExamination TEXT,
            ProvisionalDiagnosis TEXT,
            FinalDiagnosis TEXT,
            TreatmentPlan TEXT
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Image (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER,
            image_data1 BLOB,
            image_data2 BLOB,
            image_data3 BLOB,
            FOREIGN KEY (patient_id) REFERENCES Patient(id)
        )
    ''')

# Commit the changes and close the connection
    connection.commit()
    connection.close()

# Insert a new patient record into the database
def insert_patient(date,name, age, gender, phone,user_id):
    connection = sqlite3.connect(f"user_{user_id}_data.db")
    cursor = connection.cursor()
    
    cursor.execute('''
        INSERT INTO Patients (Date,Name, Age, Gender, Phone)
        VALUES (?, ?, ?, ?, ?)
    ''', (date,name, age, gender,  phone))
    
    connection.commit()
    connection.close()

# Retrieve all patient records from the database
def get_all_patients(user_id):
    connection = sqlite3.connect(f"user_{user_id}_data.db")
    cursor = connection.cursor()
    
    cursor.execute("SELECT * FROM Patients")
    patients = cursor.fetchall()
    
    connection.close()
    return patients
def get_patient(patient_id,user_id):
    connection = sqlite3.connect(f"user_{user_id}_data.db")
    cursor = connection.cursor()
    
    cursor.execute("SELECT * FROM Patients WHERE ID = ?", (patient_id,))
    patient = cursor.fetchone()  # Use fetchone() to retrieve a single record
    
    connection.close()
    return patient

# Delete a patient record from the database
def delete_patient(patient_id,user_id):
    connection = sqlite3.connect(f"user_{user_id}_data.db")
    cursor = connection.cursor()
    
    cursor.execute("DELETE FROM Patients WHERE ID=?", (patient_id,))
    
    connection.commit()
    connection.close()

def is_username_present(username):
    connection = sqlite3.connect("user_credentials.db")
    cursor = connection.cursor()

    # Check if the username exists in the UserCredentials table
    cursor.execute("SELECT COUNT(*) FROM UserCredentials WHERE UserName = ?", (username,))
    count = cursor.fetchone()[0]

    # Close the connection
    connection.close()

    # Return  if the usernTrueame is present, False otherwise
    return count > 0

def update_password(username, new_password):
    connection = sqlite3.connect("user_credentials.db")
    cursor = connection.cursor()

    # Check if the username exists
    cursor.execute("SELECT COUNT(*) FROM UserCredentials WHERE UserName = ?", (username,))
    user_count = cursor.fetchone()[0]

    if user_count > 0:
        # Update the password for the given username
        cursor.execute("UPDATE UserCredentials SET Password = ? WHERE UserName = ?", (new_password, username))
        # print("Password updated successfully")
        messagebox.showinfo("Password Changed!", "Password Updated Successfully:)")
    else:
        messagebox.showerror("Update Failed!", "Invalid username")

    # Commit changes and close the connection
    connection.commit()
    connection.close()
def insert_user(username, password):
    connection = sqlite3.connect("user_credentials.db")
    cursor = connection.cursor()
    
    cursor.execute('''
        INSERT INTO UserCredentials (UserName, Password)
        VALUES (?, ?)
    ''', (username,password))
    
    connection.commit()
    connection.close()

def get_all_users():
    connection = sqlite3.connect("user_credentials.db")
    cursor = connection.cursor()
    
    cursor.execute("SELECT * FROM UserCredentials")
    users = cursor.fetchall()
    
    connection.close()
    return users
def get_user_by_primary_key(primary_key):
    connection = sqlite3.connect("user_credentials.db")
    cursor = connection.cursor()

    # Use a WHERE clause to filter by primary key
    cursor.execute("SELECT * FROM UserCredentials WHERE ID=?", (primary_key,))
    user = cursor.fetchone()

    connection.close()
    return user
# Insert a new diagnosis record into the Diagnosis table
def insert_diagnosis2(patient_id, chiefComplaint,clinicalExamination, provisionalDiagnosis, finalDiagnosis, treatmentPlan,user_id):
    connection = sqlite3.connect(f"user_{user_id}_data.db")
    cursor = connection.cursor()
    
    cursor.execute('''
        INSERT INTO Diagnosis2 (PatientID, ChiefComplaint,ClinicalExamination, ProvisionalDiagnosis, FinalDiagnosis,TreatmentPlan)
        VALUES (?, ?, ?, ?, ?,?)
    ''', (patient_id, chiefComplaint,clinicalExamination, provisionalDiagnosis, finalDiagnosis, treatmentPlan))
    
    connection.commit()
    connection.close()
def get_diagnosis2_records(patient_id,user_id):
    connection = sqlite3.connect(f"user_{user_id}_data.db")
    cursor = connection.cursor()
    
    cursor.execute("SELECT * FROM Diagnosis2 WHERE PatientID=?", (patient_id,))
    diagnosis_records = cursor.fetchall()
    
    connection.close()
    return diagnosis_records

def delete_dignosis2_record(patient_id, user_id):
    connection = sqlite3.connect(f"user_{user_id}_data.db")
    cursor = connection.cursor()
    
    cursor.execute("DELETE FROM Diagnosis2 WHERE PatientID=?", (patient_id,))
    
    connection.commit()
    connection.close()

def save_image_to_db(patient_id, image_data1,image_data2, image_data3,user_id):
    
    conn = sqlite3.connect(f"user_{user_id}_data.db")
    cursor = conn.cursor()

        # Save the image data to the database
    cursor.execute('INSERT INTO Image (patient_id, image_data1, image_data2, image_data3) VALUES (?, ?, ?, ?)', (patient_id, image_data1, image_data2, image_data3))

        # Commit the changes and close the connection
    conn.commit()
    conn.close()
def get_image_data(patient_id,user_id):
    connection = sqlite3.connect(f"user_{user_id}_data.db")
    cursor = connection.cursor()
    
    cursor.execute("SELECT * FROM Image WHERE patient_id=?", (patient_id,))
    diagnosis_records = cursor.fetchall()
    
    connection.close()
    l=[]
    l.append(diagnosis_records[0][2])
    l.append(diagnosis_records[0][3])
    l.append(diagnosis_records[0][4])
    # l.append(diagnosis_records[0][5])
    return l
def delete_img(patient_id,user_id):
    connection = sqlite3.connect(f"user_{user_id}_data.db")
    cursor = connection.cursor()
    
    cursor.execute("DELETE FROM Image WHERE patient_id=?", (patient_id,))
    
    connection.commit()
    connection.close()
