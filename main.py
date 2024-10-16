import tkinter as tk
from tkinter import ttk, font
from database import Database
from patient_module import PatientModule
from medical_record_module import MedicalRecordModule
# from doctor_module import DoctorModule
# from prescription_module import PrescriptionModule
# from patient_portal import PatientPortal

class EHRSystem:
    def __init__(self, master):
        self.master = master
        self.master.title("Professional EHR System")
        self.master.geometry("1200x800")
        self.master.configure(bg="#f0f0f0")

        self.db = Database()

        self.setup_styles()
        self.create_widgets()

    def setup_styles(self):
        self.style = ttk.Style()
        self.style.theme_use("clam")

        # Configure colors
        self.style.configure(".", background="#f0f0f0", foreground="#333333")
        self.style.configure("TNotebook", background="#ffffff", tabmargins=[2, 5, 2, 0])
        self.style.configure("TNotebook.Tab", background="#e1e1e1", foreground="#333333", padding=[10, 5], font=('Helvetica', 10))
        self.style.map("TNotebook.Tab", background=[("selected", "#ffffff")])

        # Configure fonts
        default_font = font.nametofont("TkDefaultFont")
        default_font.configure(family="Helvetica", size=10)
        self.master.option_add("*Font", default_font)

    def create_widgets(self):
        # Create main frame
        main_frame = ttk.Frame(self.master, padding="10 10 10 10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Create and style the notebook
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Create modules
        self.patient_module = PatientModule(self.notebook, self.db, self.on_patient_select)
        self.medical_record_module = MedicalRecordModule(self.notebook, self.db)
        # self.doctor_module = DoctorModule(self.notebook, self.db)
        # self.prescription_module = PrescriptionModule(self.notebook, self.db)
        # self.patient_portal = PatientPortal(self.notebook, self.db)

        # Create status bar
        status_bar = ttk.Label(self.master, text="Ready", relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def on_patient_select(self, patient_id):
        self.medical_record_module.set_patient_id(patient_id)

if __name__ == "__main__":
    root = tk.Tk()
    app = EHRSystem(root)
    root.mainloop()
