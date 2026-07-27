import sqlite3

class Patient:
    def __init__(self, patient_id, name, age, priority_level):
        self.patient_id = patient_id
        self.name = name
        self.age = age
        self.priority_level = priority_level
        self.status = "Waiting"

    def __repr__(self):
        return f"ID: {self.patient_id} | Name: {self.name} | Age: {self.age} | Priority: {self.priority_level} | Status: {self.status}"


def setup_database():
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE patients (
            patient_id INTEGER PRIMARY KEY,
            name TEXT,
            age INTEGER,
            priority_level INTEGER,
            status TEXT
        )
    ''')
    
    cursor.execute("INSERT INTO patients VALUES (101, 'bhAAi', 45, 3, 'Waiting')")
    cursor.execute("INSERT INTO patients VALUES (102, 'BoB', 62, 1, 'Waiting')")
    cursor.execute("INSERT INTO patients VALUES (103, 'PraBOSS', 29, 2, 'Waiting')")
    cursor.execute("INSERT INTO patients VALUES (104, 'Cherry', 80, 1, 'Waiting')")
    
    conn.commit()
    return conn


def main():
    conn = setup_database()
    cursor = conn.cursor()

    cursor.execute("SELECT patient_id, name, age, priority_level FROM patients WHERE status = 'Waiting'")
    rows = cursor.fetchall()
    
    patient_list = []
    for row in rows:
        p = Patient(row[0], row[1], row[2], row[3])
        patient_list.append(p)

    def get_priority(patient):
        return patient.priority_level
    
    patient_list.sort(key=get_priority)

    print("=== Current Patient Queue ===")
    for p in patient_list:
        print(p)
    print("\n---------------------------\n")

    patients_to_attend = 2
    
    for i in range(patients_to_attend):
        if len(patient_list) > 0:
            current_patient = patient_list.pop(0)
            
            print(f"Attending Patient: {current_patient.name}")
            
            cursor.execute(
                "UPDATE patients SET status = 'Attended' WHERE patient_id = ?", 
                (current_patient.patient_id,)
            )
            conn.commit()

    print("\n=== Remaining Patients in Queue ===")
    for p in patient_list:
        print(p)

    conn.close()

if __name__ == "__main__":
    main()