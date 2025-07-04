"""
Refactored main application using proper separation of concerns.
This replaces the old main.py with a cleaner, more maintainable structure.
"""

import tkinter as tk
from tkinter import messagebox
from models import DatabaseManager, TimeTracking, validate_employee_data
from ui_components import create_management_window
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class ProjectManagementApp:
    """Main application class with proper structure."""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('Project Management System')
        self.root.geometry("500x400")
        
        # Initialize services
        self.db_manager = DatabaseManager('iscon.db')
        self.time_tracking = TimeTracking(self.db_manager)
        
        # Setup UI
        self.setup_main_window()
        
        logger.info("Application initialized successfully")
    
    def setup_main_window(self):
        """Setup the main application window."""
        # Title
        title_label = tk.Label(
            self.root, 
            text="Project Management System", 
            font=("Arial", 18, "bold"),
            fg="navy"
        )
        title_label.pack(pady=20)
        
        # Navigation buttons frame
        nav_frame = tk.Frame(self.root)
        nav_frame.pack(pady=20)
        
        # Top navigation buttons (original functionality)
        button_style = {"width": 20, "height": 2, "font": ("Arial", 10)}
        
        tk.Button(
            nav_frame, 
            text="Employees", 
            command=self.open_employees,
            bg="#4CAF50",
            fg="white",
            **button_style
        ).grid(row=0, column=0, padx=10, pady=5)
        
        tk.Button(
            nav_frame, 
            text="Designations", 
            command=self.open_designations,
            bg="#2196F3",
            fg="white",
            **button_style
        ).grid(row=0, column=1, padx=10, pady=5)
        
        tk.Button(
            nav_frame, 
            text="Projects", 
            command=self.open_projects,
            bg="#FF9800",
            fg="white",
            **button_style
        ).grid(row=0, column=2, padx=10, pady=5)
        
        # Time tracking section
        self.setup_time_tracking_section()
    
    def setup_time_tracking_section(self):
        """Setup the time tracking input section."""
        # Separator
        separator = tk.Frame(self.root, height=2, bg="gray")
        separator.pack(fill=tk.X, padx=20, pady=20)
        
        # Time tracking frame
        tracking_frame = tk.LabelFrame(
            self.root, 
            text="Record Work Hours", 
            padx=20, 
            pady=20,
            font=("Arial", 12, "bold")
        )
        tracking_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # Input fields
        tk.Label(tracking_frame, text="Project Number:", font=("Arial", 10)).grid(
            row=0, column=0, sticky="w", pady=5
        )
        self.project_number_entry = tk.Entry(tracking_frame, width=20)
        self.project_number_entry.grid(row=0, column=1, padx=10, pady=5)
        
        tk.Label(tracking_frame, text="Employee ID:", font=("Arial", 10)).grid(
            row=1, column=0, sticky="w", pady=5
        )
        self.employee_id_entry = tk.Entry(tracking_frame, width=20)
        self.employee_id_entry.grid(row=1, column=1, padx=10, pady=5)
        
        tk.Label(tracking_frame, text="Hours Worked:", font=("Arial", 10)).grid(
            row=2, column=0, sticky="w", pady=5
        )
        self.hours_entry = tk.Entry(tracking_frame, width=20)
        self.hours_entry.grid(row=2, column=1, padx=10, pady=5)
        
        # Submit button
        submit_button = tk.Button(
            tracking_frame,
            text="Record Hours",
            command=self.record_hours,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 10, "bold"),
            width=15,
            height=2
        )
        submit_button.grid(row=3, column=0, columnspan=2, pady=15)
    
    def open_employees(self):
        """Open employee management window."""
        try:
            create_management_window("employees", self.root, self.db_manager)
            logger.info("Opened employee management window")
        except Exception as e:
            logger.error(f"Failed to open employee management: {e}")
            messagebox.showerror("Error", f"Failed to open employee management: {str(e)}")
    
    def open_designations(self):
        """Open designation/sector management window."""
        try:
            create_management_window("sectors", self.root, self.db_manager)
            logger.info("Opened sector management window")
        except Exception as e:
            logger.error(f"Failed to open sector management: {e}")
            messagebox.showerror("Error", f"Failed to open sector management: {str(e)}")
    
    def open_projects(self):
        """Open project management window."""
        try:
            create_management_window("projects", self.root, self.db_manager)
            logger.info("Opened project management window")
        except Exception as e:
            logger.error(f"Failed to open project management: {e}")
            messagebox.showerror("Error", f"Failed to open project management: {str(e)}")
    
    def record_hours(self):
        """Record hours worked by an employee on a project."""
        try:
            # Get input values
            project_number = self.project_number_entry.get().strip()
            employee_id = self.employee_id_entry.get().strip()
            hours = self.hours_entry.get().strip()
            
            # Validate inputs
            if not all([project_number, employee_id, hours]):
                messagebox.showerror("Error", "All fields are required")
                return
            
            # Convert to appropriate types
            try:
                project_number = int(project_number)
                employee_id = int(employee_id)
                hours = int(hours)
            except ValueError:
                messagebox.showerror("Error", "Please enter valid numbers")
                return
            
            # Validate ranges
            if project_number <= 0:
                messagebox.showerror("Error", "Project number must be positive")
                return
            
            if employee_id <= 0:
                messagebox.showerror("Error", "Employee ID must be positive")
                return
            
            if hours <= 0 or hours > 24:
                messagebox.showerror("Error", "Hours must be between 1 and 24")
                return
            
            # Record the hours
            success = self.time_tracking.record_hours(employee_id, project_number, hours)
            
            if success:
                messagebox.showinfo("Success", f"Successfully recorded {hours} hours for employee {employee_id} on project {project_number}")
                # Clear the form
                self.clear_time_tracking_form()
                logger.info(f"Recorded {hours} hours for employee {employee_id} on project {project_number}")
            else:
                messagebox.showerror("Error", "Failed to record hours. Please check that the employee and project exist.")
        
        except Exception as e:
            logger.error(f"Error recording hours: {e}")
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
    
    def clear_time_tracking_form(self):
        """Clear the time tracking form."""
        self.project_number_entry.delete(0, tk.END)
        self.employee_id_entry.delete(0, tk.END)
        self.hours_entry.delete(0, tk.END)
    
    def run(self):
        """Start the application."""
        try:
            self.root.mainloop()
        except Exception as e:
            logger.error(f"Application error: {e}")
            messagebox.showerror("Critical Error", f"Application encountered an error: {str(e)}")
        finally:
            logger.info("Application shutting down")

def main():
    """Main entry point."""
    try:
        app = ProjectManagementApp()
        app.run()
    except Exception as e:
        logger.critical(f"Failed to start application: {e}")
        print(f"Failed to start application: {e}")

if __name__ == "__main__":
    main()