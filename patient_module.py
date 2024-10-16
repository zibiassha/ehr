import tkinter as tk
from tkinter import ttk, messagebox

class PatientModule:
    def __init__(self, notebook, db, on_patient_select):
        self.notebook = notebook
        self.db = db
        self.on_patient_select = on_patient_select
        self.frame = ttk.Frame(self.notebook, padding="20 20 20 20")
        self.notebook.add(self.frame, text="Patients")

        self.create_widgets()

    def create_widgets(self):
        # Create left frame for input fields and buttons
        left_frame = ttk.Frame(self.frame, padding="0 0 20 0")
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Create input fields
        input_frame = ttk.LabelFrame(left_frame, text="Patient Information", padding="10 10 10 10")
        input_frame.pack(fill=tk.X, pady=(0, 20))

        ttk.Label(input_frame, text="Name:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.name_entry = ttk.Entry(input_frame, width=30)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(input_frame, text="Date of Birth:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.dob_entry = ttk.Entry(input_frame, width=30)
        self.dob_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(input_frame, text="Gender:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.gender_entry = ttk.Combobox(input_frame, values=["Male", "Female", "Other"], width=28)
        self.gender_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(input_frame, text="Contact:").grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
        self.contact_entry = ttk.Entry(input_frame, width=30)
        self.contact_entry.grid(row=3, column=1, padx=5, pady=5)

        # Create buttons
        button_frame = ttk.Frame(left_frame)
        button_frame.pack(fill=tk.X, pady=10)

        ttk.Button(button_frame, text="Add Patient", command=self.add_patient).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Update Patient", command=self.update_patient).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Delete Patient", command=self.delete_patient).pack(side=tk.LEFT, padx=5)

        # Create right frame for treeview
        right_frame = ttk.Frame(self.frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Create and style treeview
        self.tree = ttk.Treeview(right_frame, columns=("ID", "Name", "DOB", "Gender", "Contact"), show="headings", selectmode="browse")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="Name")
        self.tree.heading("DOB", text="Date of Birth")
        self.tree.heading("Gender", text="Gender")
        self.tree.heading("Contact", text="Contact")

        self.tree.column("ID", width=50)
        self.tree.column("Name", width=150)
        self.tree.column("DOB", width=100)
        self.tree.column("Gender", width=80)
        self.tree.column("Contact", width=120)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Add scrollbar to treeview
        scrollbar = ttk.Scrollbar(right_frame, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

        self.load_patients()

    def load_patients(self):
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Fetch patients from database
        patients = self.db.fetch_data("SELECT * FROM patients")
        for patient in patients:
            self.tree.insert("", "end", values=patient)

    def add_patient(self):
        name = self.name_entry.get()
        dob = self.dob_entry.get()
        gender = self.gender_entry.get()
        contact = self.contact_entry.get()

        if name and dob and gender and contact:
            self.db.execute_query("INSERT INTO patients (name, dob, gender, contact) VALUES (?, ?, ?, ?)",
                                  (name, dob, gender, contact))
            self.load_patients()
            self.clear_entries()
        else:
            messagebox.showerror("Error", "Please fill in all fields")

    def update_patient(self):
        selected_item = self.tree.selection()
        if selected_item:
            patient_id = self.tree.item(selected_item)['values'][0]
            name = self.name_entry.get()
            dob = self.dob_entry.get()
            gender = self.gender_entry.get()
            contact = self.contact_entry.get()

            if name and dob and gender and contact:
                self.db.execute_query("UPDATE patients SET name=?, dob=?, gender=?, contact=? WHERE id=?",
                                      (name, dob, gender, contact, patient_id))
                self.load_patients()
                self.clear_entries()
            else:
                messagebox.showerror("Error", "Please fill in all fields")
        else:
            messagebox.showerror("Error", "Please select a patient to update")

    def delete_patient(self):
        selected_item = self.tree.selection()
        if selected_item:
            patient_id = self.tree.item(selected_item)['values'][0]
            self.db.execute_query("DELETE FROM patients WHERE id=?", (patient_id,))
            self.load_patients()
            self.clear_entries()
        else:
            messagebox.showerror("Error", "Please select a patient to delete")

    def clear_entries(self):
        self.name_entry.delete(0, tk.END)
        self.dob_entry.delete(0, tk.END)
        self.gender_entry.delete(0, tk.END)
        self.contact_entry.delete(0, tk.END)

    def on_tree_select(self, event):
        selected_item = self.tree.selection()
        if selected_item:
            values = self.tree.item(selected_item)['values']
            self.name_entry.delete(0, tk.END)
            self.name_entry.insert(0, values[1])
            self.dob_entry.delete(0, tk.END)
            self.dob_entry.insert(0, values[2])
            self.gender_entry.delete(0, tk.END)
            self.gender_entry.insert(0, values[3])
            self.contact_entry.delete(0, tk.END)
            self.contact_entry.insert(0, values[4])

            # Call the callback function with the selected patient's ID
            self.on_patient_select(values[0])
