import mysql.connector as MyS
Pass = input("Enter MYSQL password:")

if Pass:
    # Create the database if it does not already exist.
    server_conn = MyS.connect(
        host="localhost",
        user="root",
        password=Pass,
    )
    server_cursor = server_conn.cursor()
    server_cursor.execute("CREATE DATABASE IF NOT EXISTS patient_management")
    server_cursor.close()
    server_conn.close()

    # Connect to the patient management database.
    conn = MyS.connect(
        host="localhost",
        user="root",
        password=Pass,
        database="patient_management",
    )
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS patients (
            Patient_ID INT PRIMARY KEY,
            Name VARCHAR(50),
            Age INT,
            Gender VARCHAR(10),
            Phone VARCHAR(15),
            Disease VARCHAR(50),
            Doctor VARCHAR(50),
            Admission_Date DATE
        )
    """)
    cursor.execute("SELECT 1 FROM patients LIMIT 1")
    if cursor.fetchone() is None:
        cursor.executemany(
            """
            INSERT INTO patients
                (Patient_ID, Name, Age, Gender, Phone, Disease, Doctor, Admission_Date)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """,
            [
                (101, 'Arun Kumar', 45, 'Male', '9876543210', 'Diabetes', 'Dr. Thomas', '2026-10-01'),
                (102, 'Anjali Nair', 32, 'Female', '9847123456', 'Fever', 'Dr. Meera', '2026-10-02'),
                (103, 'Rahul Das', 28, 'Male', '9895123456', 'Asthma', 'Dr. Joseph', '2026-10-03'),
                (104, 'Sneha Menon', 51, 'Female', '9633456789', 'Hypertension', 'Dr. Thomas', '2026-10-04'),
                (105, 'Vivek Raj', 19, 'Male', '9746123456', 'Migraine', 'Dr. Meera', '2026-10-05'),
            ],
        )
    conn.commit()

    def display():
        cursor.execute("SELECT * FROM patients")
        patients = cursor.fetchall()
        headers = [description[0] for description in cursor.description]

        if patients:
            widths = [max(len(str(header)), *(len(str(row[i])) for row in patients))
                      for i, header in enumerate(headers)]
            separator = "+-" + "-+-".join("-" * width for width in widths) + "-+"
            print(separator)
            print("| " + " | ".join(str(header).ljust(width)
                                  for header, width in zip(headers, widths)) + " |")
            print(separator)
            for patient in patients:
                print("| " + " | ".join(str(value).ljust(width)
                                      for value, width in zip(patient, widths)) + " |")
            print(separator)
        else:
            print("No patients found.")

    def add_patient():
        patient_id = input("Enter patient ID: ")
        name = input("Enter patient name: ")
        age = input("Enter patient age: ")
        gender = input("Enter patient gender: ")
        phone = input("Enter patient phone number: ")
        disease = input("Enter patient disease: ")
        doctor = input("Enter doctor assigned: ")
        admission_date = input("Enter admission date (YYYY-MM-DD): ")
        cursor.execute(
            "INSERT INTO patients (patient_id, name, age, gender, phone, disease, doctor, admission_date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
            (patient_id, name, age, gender, phone, disease, doctor, admission_date)
        )
        conn.commit()

    def update_patient():
        patient_id = input("Enter patient ID to update: ")
        name = input("Enter new patient name: ")
        age = input("Enter new patient age: ")
        gender = input("Enter new patient gender: ")
        phone = input("Enter new patient phone number: ")
        disease = input("Enter new patient disease: ")
        doctor = input("Enter new doctor assigned: ")
        admission_date = input("Enter new admission date (YYYY-MM-DD): ")
        cursor.execute(
            "UPDATE patients SET name=%s, age=%s, gender=%s, phone=%s, disease=%s, doctor=%s, admission_date=%s WHERE patient_id=%s",
            (name, age, gender, phone, disease, doctor, admission_date, patient_id)
        )
        conn.commit()

    def delete_patient():
        patient_id = input("Enter patient ID to delete: ")
        cursor.execute("DELETE FROM patients WHERE patient_id=%s", (patient_id,))
        conn.commit()

    def search_patient():
        patient_id = input("Enter patient ID to search: ")
        cursor.execute("SELECT * FROM patients WHERE patient_id=%s", (patient_id,))
        patient = cursor.fetchone()
        if patient:
            print(patient)
        else:
            print("Patient not found.")

    while True:
        print("Welcome to the Patient Management System! Please choose what you want to do:")
        print("1. Display all patients")
        print("2. Add a new patient")
        print("3. Update patient information")
        print("4. Delete a patient")
        print("5. Search for a patient")
        print("6. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            display()
        elif choice == "2":
            add_patient()
        elif choice == "3":
            update_patient()
        elif choice == "4":
            delete_patient()
        elif choice == "5":
            search_patient()
        elif choice == "6":
            break
        else:
            print("Invalid choice. Please try again.")
