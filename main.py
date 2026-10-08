#CREATE THE DATABASE AND TABLES IN MYSQL BEFORE RUNNING THIS PRG. ALL GIVEN IN TEXT FILE. 

import mysql.connector as MyS
Pass = input("Enter MYSQL password:")

if Pass:
     # Connect to MySQL server
    conn = MyS.connect(
        host="localhost",
        user="root",
        password=Pass,
        database="patient_management",
    )
    cursor = conn.cursor()

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
