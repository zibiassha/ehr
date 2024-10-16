import tkinter as tk
from tkinter import ttk, messagebox

class MedicalRecordModule:
    def __init__(self, notebook, db):
        self.notebook = notebook
        self.db = db
        self.frame = ttk.Frame(self.notebook, padding="20 20 20 20")
        self.notebook.add(self.frame, text="Medical Records")

        self.create_widgets()

    def create_widgets(self):
        # Create left frame for input fields and buttons
        left_frame = ttk.Frame(self.frame, padding="0 0 20 0")
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Create input fields
        input_frame = ttk.LabelFrame(left_frame, text="Medical Record Information", padding="10 10 10 10")
        input_frame.pack(fill=tk.X, pady=(0, 20))

        ttk.Label(input_frame, text="Patient ID:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.patient_id_entry = ttk.Entry(input_frame, width=30)
        self.patient_id_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(input_frame, text="Date:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.date_entry = ttk.Entry(input_frame, width=30)
        self.date_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(input_frame, text="Diagnosis:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.diagnosis_entry = ttk.Entry(input_frame, width=30)
        self.diagnosis_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(input_frame, text="Treatment:").grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
        self.treatment_entry = ttk.Entry(input_frame, width=30)
        self.treatment_entry.grid(row=3, column=1, padx=5, pady=5)

        # Create buttons
        button_frame = ttk.Frame(left_frame)
        button_frame.pack(fill=tk.X, pady=10)

        ttk.Button(button_frame, text="Add Record", command=self.add_record).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Update Record", command=self.update_record).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Delete Record", command=self.delete_record).pack(side=tk.LEFT, padx=5)

        # Create right frame for treeview
        right_frame = ttk.Frame(self.frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Create and style treeview
        self.tree = ttk.Treeview(right_frame, columns=("ID", "Patient ID", "Date", "Diagnosis", "Treatment"), show="headings", selectmode="browse")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Patient ID", text="Patient ID")
        self.tree.heading("Date", text="Date")
        self.tree.heading("Diagnosis", text="Diagnosis")
        self.tree.heading("Treatment", text="Treatment")

        self.tree.column("ID", width=50)
        self.tree.column("Patient ID", width=80)
        self.tree.column("Date", width=100)
        self.tree.column("Diagnosis", width=150)
        self.tree.column("Treatment", width=150)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Add scrollbar to treeview
        scrollbar = ttk.Scrollbar(right_frame, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

        self.load_records()

    def load_records(self):
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Fetch medical records from database
        records = self.db.fetch_data("SELECT * FROM medical_records")
        for record in records:
            self.tree.insert("", "end", values=record)

    def add_record(self):
        patient_id = self.patient_id_entry.get()
        date = self.date_entry.get()
        diagnosis = self.diagnosis_entry.get()
        treatment = self.treatment_entry.get()

        if patient_id and date and diagnosis and treatment:
            self.db.execute_query("INSERT INTO medical_records (patient_id, date, diagnosis, treatment) VALUES (?, ?, ?, ?)",
                                  (patient_id, date, diagnosis, treatment))
            self.load_records()
            self.clear_entries()
        else:
            messagebox.showerror("Error", "Please fill in all fields")

    def update_record(self):
        selected_item = self.tree.selection()
        if selected_item:
            record_id = self.tree.item(selected_item)['values'][0]
            patient_id = self.patient_id_entry.get()
            date = self.date_entry.get()
            diagnosis = self.diagnosis_entry.get()
            treatment = self.treatment_entry.get()

            if patient_id and date and diagnosis and treatment:
                self.db.execute_query("UPDATE medical_records SET patient_id=?, date=?, diagnosis=?, treatment=? WHERE id=?",
                                      (patient_id, date, diagnosis, treatment, record_id))
                self.load_records()
                self.clear_entries()
            else:
                messagebox.showerror("Error", "Please fill in all fields")
        else:
            messagebox.showerror("Error", "Please select a record to update")

    def delete_record(self):
        selected_item = self.tree.selection()
        if selected_item:
            record_id = self.tree.item(selected_item)['values'][0]
            self.db.execute_query("DELETE FROM medical_records WHERE id=?", (record_id,))
            self.load_records()
            self.clear_entries()
        else:
            messagebox.showerror("Error", "Please select a record to delete")

    def on_tree_select(self, event):
        selected_item = self.tree.selection()
        if selected_item:
            values = self.tree.item(selected_item)['values']
            self.patient_id_entry.delete(0, tk.END)
            self.patient_id_entry.insert(0, values[1])
            self.date_entry.delete(0, tk.END)
            self.date_entry.insert(0, values[2])
            self.diagnosis_entry.delete(0, tk.END)
            self.diagnosis_entry.insert(0, values[3])
            self.treatment_entry.delete(0, tk.END)
            self.treatment_entry.insert(0, values[4])

    def clear_entries(self):
        self.patient_id_entry.delete(0, tk.END)
        self.date_entry.delete(0, tk.END)
        self.diagnosis_entry.delete(0, tk.END)
        self.treatment_entry.delete(0, tk.END)

    def set_patient_id(self, patient_id):
        self.patient_id_entry.delete(0, tk.END)
        self.patient_id_entry.insert(0, patient_id)
