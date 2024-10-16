# Electronic Health Record (EHR) System

This is a simple Electronic Health Record (EHR) system built using Python and Tkinter. The application allows users to manage patient information and medical records through a graphical user interface.

## Features

- Patient management (Add, Update, Delete)
- Medical record management (Add, Update, Delete)
- User-friendly interface with tabbed navigation
- SQLite database for data storage

## Prerequisites

Before running the application, make sure you have the following installed:

- Python 3.6 or higher
- Tkinter (usually comes pre-installed with Python)
- SQLite3 (usually comes pre-installed with Python)

## Environment Setup

1. Clone this repository or download the source code.

2. (Optional) Create a virtual environment:
   ```
   python -m venv venv
   ```

3. Activate the virtual environment:
   - On Windows:
     ```
     venv\Scripts\activate
     ```
   - On macOS and Linux:
     ```
     source venv/bin/activate
     ```

4. Install the required packages:
   ```
   pip install tk
   ```

## Project Structure

The project consists of the following files:

- `main.py`: The main application file that sets up the GUI and manages the modules.
- `database.py`: Handles database operations and table creation.
- `patient_module.py`: Manages patient-related operations and UI.
- `medical_record_module.py`: Manages medical record-related operations and UI.

## Running the Application

To run the EHR system, follow these steps:

1. Ensure you're in the project directory and your virtual environment is activated (if you're using one).

2. Run the following command:
   ```
   python main.py
   ```

3. The application window should appear, allowing you to interact with the EHR system.

## Usage

- Use the tabs at the top of the application to switch between different modules (Patients and Medical Records).
- In each module, you can add, update, or delete records using the provided forms and buttons.
- The treeview on the right side of each module displays the current records in the database.
- Selecting a record in the treeview will populate the form fields for easy editing.

## Future Improvements

- Implement Doctor and Prescription modules
- Add user authentication and access control
- Enhance data validation and error handling
- Implement a patient portal for self-service options
- Add reporting and data export features
