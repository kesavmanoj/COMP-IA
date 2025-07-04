"""
Reusable UI components for the project management system.
Separates UI logic from business logic and provides clean interfaces.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Dict, List, Callable, Optional
from models import DatabaseManager, Employee, Sector, Project, TimeTracking
from models import validate_employee_data, validate_sector_data

class BaseForm:
    """Base class for forms with common functionality."""
    
    def __init__(self, parent, title: str, size: str = "400x500"):
        self.parent = parent
        self.window = tk.Toplevel(parent)
        self.window.title(title)
        self.window.geometry(size)
        self.fields = {}
        self.current_row = 0
    
    def add_field(self, label: str, field_name: str, field_type: str = "entry", 
                  validation: Optional[Callable] = None, **kwargs) -> tk.Widget:
        """Add a labeled field to the form."""
        # Label
        tk.Label(self.window, text=label).grid(
            row=self.current_row, column=0, sticky="w", padx=5, pady=5
        )
        
        # Field
        if field_type == "entry":
            widget = tk.Entry(self.window, **kwargs)
        elif field_type == "text":
            widget = tk.Text(self.window, height=3, **kwargs)
        elif field_type == "combobox":
            widget = ttk.Combobox(self.window, **kwargs)
        else:
            raise ValueError(f"Unknown field type: {field_type}")
        
        widget.grid(row=self.current_row, column=1, sticky="ew", padx=5, pady=5)
        
        # Store field reference
        self.fields[field_name] = {
            'widget': widget,
            'validation': validation
        }
        
        self.current_row += 1
        return widget
    
    def add_button(self, text: str, command: Callable, **kwargs):
        """Add a button to the form."""
        button = tk.Button(self.window, text=text, command=command, **kwargs)
        button.grid(row=self.current_row, column=0, columnspan=2, 
                   pady=10, padx=5, sticky="ew")
        self.current_row += 1
        return button
    
    def add_space(self, height: int = 1):
        """Add vertical spacing."""
        tk.Label(self.window, text="", height=height).grid(
            row=self.current_row, column=0, columnspan=2
        )
        self.current_row += 1
    
    def get_form_data(self) -> Dict[str, str]:
        """Get data from all form fields."""
        data = {}
        for field_name, field_info in self.fields.items():
            widget = field_info['widget']
            if isinstance(widget, tk.Entry):
                data[field_name] = widget.get()
            elif isinstance(widget, tk.Text):
                data[field_name] = widget.get("1.0", tk.END).strip()
            elif isinstance(widget, ttk.Combobox):
                data[field_name] = widget.get()
        return data
    
    def clear_form(self):
        """Clear all form fields."""
        for field_info in self.fields.values():
            widget = field_info['widget']
            if isinstance(widget, tk.Entry):
                widget.delete(0, tk.END)
            elif isinstance(widget, tk.Text):
                widget.delete("1.0", tk.END)
            elif isinstance(widget, ttk.Combobox):
                widget.set("")
    
    def validate_form(self) -> tuple[bool, str]:
        """Validate all form fields."""
        for field_name, field_info in self.fields.items():
            validation = field_info['validation']
            if validation:
                widget = field_info['widget']
                value = widget.get()
                is_valid, error_msg = validation(value)
                if not is_valid:
                    return False, f"{field_name}: {error_msg}"
        return True, ""
    
    def populate_form(self, data: Dict[str, any]):
        """Populate form with data."""
        for field_name, value in data.items():
            if field_name in self.fields:
                widget = self.fields[field_name]['widget']
                if isinstance(widget, tk.Entry):
                    widget.delete(0, tk.END)
                    widget.insert(0, str(value))
                elif isinstance(widget, tk.Text):
                    widget.delete("1.0", tk.END)
                    widget.insert("1.0", str(value))
                elif isinstance(widget, ttk.Combobox):
                    widget.set(str(value))

class EmployeeManagementWindow:
    """Employee management interface with proper separation of concerns."""
    
    def __init__(self, parent, db_manager: DatabaseManager):
        self.parent = parent
        self.db_manager = db_manager
        self.employee_service = Employee(db_manager)
        
        self.window = tk.Toplevel(parent)
        self.window.title('Employee Management')
        self.window.geometry("500x600")
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the user interface."""
        # Title
        title_label = tk.Label(self.window, text="Employee Management", 
                              font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=10)
        
        # Employee list frame
        list_frame = tk.LabelFrame(self.window, text="Employees", padx=10, pady=10)
        list_frame.grid(row=1, column=0, columnspan=3, sticky="ew", padx=10, pady=5)
        
        # Employee listbox with scrollbar
        self.employee_listbox = tk.Listbox(list_frame, height=8)
        scrollbar = tk.Scrollbar(list_frame, orient="vertical")
        self.employee_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.employee_listbox.yview)
        
        self.employee_listbox.grid(row=0, column=0, sticky="ew")
        scrollbar.grid(row=0, column=1, sticky="ns")
        
        # Buttons frame
        buttons_frame = tk.Frame(self.window)
        buttons_frame.grid(row=2, column=0, columnspan=3, pady=10)
        
        tk.Button(buttons_frame, text="Add Employee", 
                 command=self.show_add_form, width=15).pack(side=tk.LEFT, padx=5)
        tk.Button(buttons_frame, text="Edit Employee", 
                 command=self.show_edit_form, width=15).pack(side=tk.LEFT, padx=5)
        tk.Button(buttons_frame, text="Refresh", 
                 command=self.refresh_employee_list, width=15).pack(side=tk.LEFT, padx=5)
        
        # Load initial data
        self.refresh_employee_list()
    
    def refresh_employee_list(self):
        """Refresh the employee list."""
        self.employee_listbox.delete(0, tk.END)
        employees = self.employee_service.get_all()
        for employee in employees:
            display_text = f"ID: {employee['id_number']} - {employee['full_name']} ({employee['designation']})"
            self.employee_listbox.insert(tk.END, display_text)
    
    def show_add_form(self):
        """Show form to add new employee."""
        form = EmployeeForm(self.window, "Add Employee", self.employee_service)
        form.on_success = lambda: self.refresh_employee_list()
    
    def show_edit_form(self):
        """Show form to edit selected employee."""
        selection = self.employee_listbox.curselection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select an employee to edit")
            return
        
        # Extract employee ID from the selected text
        selected_text = self.employee_listbox.get(selection[0])
        employee_id = int(selected_text.split(" - ")[0].replace("ID: ", ""))
        
        employee_data = self.employee_service.get_by_id(employee_id)
        if employee_data:
            form = EmployeeForm(self.window, "Edit Employee", self.employee_service, employee_data)
            form.on_success = lambda: self.refresh_employee_list()

class EmployeeForm(BaseForm):
    """Form for adding/editing employees."""
    
    def __init__(self, parent, title: str, employee_service: Employee, 
                 employee_data: Optional[Dict] = None):
        super().__init__(parent, title, "400x500")
        self.employee_service = employee_service
        self.employee_data = employee_data
        self.is_edit_mode = employee_data is not None
        self.on_success: Optional[Callable] = None
        
        self.setup_form()
        
        if self.is_edit_mode:
            self.populate_form(employee_data)
    
    def setup_form(self):
        """Setup the form fields."""
        # Add form fields
        self.add_field("Employee ID:", "id_number", validation=self.validate_employee_id)
        self.add_field("Full Name:", "full_name", validation=self.validate_required)
        self.add_field("Hours per Week:", "hour_per_week", validation=self.validate_hours)
        self.add_field("Salary:", "salary", validation=self.validate_salary)
        
        # Designation dropdown
        designations = ["Welder", "Builder", "Painter", "Engineer", "Manager", "Fitter"]
        self.add_field("Designation:", "designation", "combobox", values=designations)
        
        self.add_field("Project Number:", "project_number", validation=self.validate_project_number)
        
        self.add_space()
        
        # Buttons
        button_text = "Update Employee" if self.is_edit_mode else "Add Employee"
        self.add_button(button_text, self.save_employee)
        self.add_button("Cancel", self.window.destroy)
    
    def validate_required(self, value: str) -> tuple[bool, str]:
        """Validate required field."""
        if not value.strip():
            return False, "This field is required"
        return True, ""
    
    def validate_employee_id(self, value: str) -> tuple[bool, str]:
        """Validate employee ID."""
        if not value.strip():
            return False, "Employee ID is required"
        try:
            employee_id = int(value)
            if employee_id <= 0:
                return False, "Employee ID must be positive"
            
            # Check for duplicates in add mode
            if not self.is_edit_mode:
                existing = self.employee_service.get_by_id(employee_id)
                if existing:
                    return False, "Employee ID already exists"
        except ValueError:
            return False, "Employee ID must be a number"
        return True, ""
    
    def validate_hours(self, value: str) -> tuple[bool, str]:
        """Validate hours per week."""
        try:
            hours = int(value)
            if hours < 0 or hours > 168:
                return False, "Hours must be between 0 and 168"
        except ValueError:
            return False, "Hours must be a number"
        return True, ""
    
    def validate_salary(self, value: str) -> tuple[bool, str]:
        """Validate salary."""
        try:
            salary = float(value)
            if salary < 0:
                return False, "Salary cannot be negative"
        except ValueError:
            return False, "Salary must be a number"
        return True, ""
    
    def validate_project_number(self, value: str) -> tuple[bool, str]:
        """Validate project number."""
        try:
            project_num = int(value)
            if project_num <= 0:
                return False, "Project number must be positive"
        except ValueError:
            return False, "Project number must be a number"
        return True, ""
    
    def save_employee(self):
        """Save employee data."""
        # Validate form
        is_valid, error_msg = self.validate_form()
        if not is_valid:
            messagebox.showerror("Validation Error", error_msg)
            return
        
        # Get form data
        data = self.get_form_data()
        
        # Convert numeric fields
        try:
            data['id_number'] = int(data['id_number'])
            data['hour_per_week'] = int(data['hour_per_week'])
            data['salary'] = float(data['salary'])
            data['project_number'] = int(data['project_number'])
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid data: {e}")
            return
        
        # Additional validation using models
        is_valid, error_msg = validate_employee_data(data)
        if not is_valid:
            messagebox.showerror("Validation Error", error_msg)
            return
        
        # Save to database
        try:
            if self.is_edit_mode:
                original_id = self.employee_data['id_number']
                success = self.employee_service.update(original_id, data)
                action = "updated"
            else:
                success = self.employee_service.create(data)
                action = "created"
            
            if success:
                messagebox.showinfo("Success", f"Employee {action} successfully!")
                if self.on_success:
                    self.on_success()
                self.window.destroy()
            else:
                messagebox.showerror("Error", f"Failed to {action.replace('d', '')} employee")
                
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

class SectorManagementWindow:
    """Sector/Designation management interface."""
    
    def __init__(self, parent, db_manager: DatabaseManager):
        self.parent = parent
        self.db_manager = db_manager
        self.sector_service = Sector(db_manager)
        
        self.window = tk.Toplevel(parent)
        self.window.title('Sector Management')
        self.window.geometry("450x500")
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the user interface."""
        # Title
        title_label = tk.Label(self.window, text="Sector Management", 
                              font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=10)
        
        # Sector list frame
        list_frame = tk.LabelFrame(self.window, text="Sectors", padx=10, pady=10)
        list_frame.grid(row=1, column=0, columnspan=3, sticky="ew", padx=10, pady=5)
        
        # Sector listbox with scrollbar
        self.sector_listbox = tk.Listbox(list_frame, height=8)
        scrollbar = tk.Scrollbar(list_frame, orient="vertical")
        self.sector_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.sector_listbox.yview)
        
        self.sector_listbox.grid(row=0, column=0, sticky="ew")
        scrollbar.grid(row=0, column=1, sticky="ns")
        
        # Buttons frame
        buttons_frame = tk.Frame(self.window)
        buttons_frame.grid(row=2, column=0, columnspan=3, pady=10)
        
        tk.Button(buttons_frame, text="Add Sector", 
                 command=self.show_add_form, width=15).pack(side=tk.LEFT, padx=5)
        tk.Button(buttons_frame, text="Edit Sector", 
                 command=self.show_edit_form, width=15).pack(side=tk.LEFT, padx=5)
        tk.Button(buttons_frame, text="Refresh", 
                 command=self.refresh_sector_list, width=15).pack(side=tk.LEFT, padx=5)
        
        # Initial form fields for quick add
        form_frame = tk.LabelFrame(self.window, text="Quick Add", padx=10, pady=10)
        form_frame.grid(row=3, column=0, columnspan=3, sticky="ew", padx=10, pady=5)
        
        tk.Label(form_frame, text="Sector ID:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.sector_id_entry = tk.Entry(form_frame)
        self.sector_id_entry.grid(row=0, column=1, sticky="ew", padx=5, pady=5)
        
        tk.Label(form_frame, text="Sector Name:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.sector_name_entry = tk.Entry(form_frame)
        self.sector_name_entry.grid(row=1, column=1, sticky="ew", padx=5, pady=5)
        
        tk.Label(form_frame, text="Hourly Wage:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.sector_wage_entry = tk.Entry(form_frame)
        self.sector_wage_entry.grid(row=2, column=1, sticky="ew", padx=5, pady=5)
        
        tk.Button(form_frame, text="Add", command=self.quick_add_sector).grid(
            row=3, column=0, columnspan=2, pady=10)
        
        # Load initial data
        self.refresh_sector_list()
    
    def refresh_sector_list(self):
        """Refresh the sector list."""
        # This would need to be implemented with a get_all method in Sector class
        # For now, showing placeholder
        self.sector_listbox.delete(0, tk.END)
        # Add some sample data
        sectors = [
            "ID: 1 - Builder ($16.00/hr)",
            "ID: 2 - Painter ($23.00/hr)",
        ]
        for sector in sectors:
            self.sector_listbox.insert(tk.END, sector)
    
    def show_add_form(self):
        """Show form to add new sector."""
        # Implementation similar to EmployeeForm
        pass
    
    def show_edit_form(self):
        """Show form to edit selected sector."""
        # Implementation similar to EmployeeForm
        pass
    
    def quick_add_sector(self):
        """Quick add sector from inline form."""
        data = {
            'sector_id': self.sector_id_entry.get(),
            'sector_name': self.sector_name_entry.get(),
            'sector_wage': self.sector_wage_entry.get()
        }
        
        # Validate
        is_valid, error_msg = validate_sector_data(data)
        if not is_valid:
            messagebox.showerror("Validation Error", error_msg)
            return
        
        # Convert types
        try:
            data['sector_id'] = int(data['sector_id'])
            data['sector_wage'] = float(data['sector_wage'])
        except ValueError:
            messagebox.showerror("Error", "Invalid numeric values")
            return
        
        # Save
        if self.sector_service.create(data):
            messagebox.showinfo("Success", "Sector created successfully!")
            self.clear_quick_form()
            self.refresh_sector_list()
        else:
            messagebox.showerror("Error", "Failed to create sector")
    
    def clear_quick_form(self):
        """Clear the quick add form."""
        self.sector_id_entry.delete(0, tk.END)
        self.sector_name_entry.delete(0, tk.END)
        self.sector_wage_entry.delete(0, tk.END)

class ProjectManagementWindow:
    """Project management interface."""
    
    def __init__(self, parent, db_manager: DatabaseManager):
        self.parent = parent
        self.db_manager = db_manager
        self.project_service = Project(db_manager)
        
        self.window = tk.Toplevel(parent)
        self.window.title('Project Management')
        self.window.geometry("600x700")
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the user interface."""
        # Implementation similar to other management windows
        # This would include project search, add, edit functionality
        title_label = tk.Label(self.window, text="Project Management", 
                              font=("Arial", 16, "bold"))
        title_label.pack(pady=10)
        
        # Add project management functionality here
        tk.Label(self.window, text="Project management functionality will be implemented here").pack()

# Factory function to create management windows
def create_management_window(window_type: str, parent, db_manager: DatabaseManager):
    """Factory function to create management windows."""
    if window_type == "employees":
        return EmployeeManagementWindow(parent, db_manager)
    elif window_type == "sectors":
        return SectorManagementWindow(parent, db_manager)
    elif window_type == "projects":
        return ProjectManagementWindow(parent, db_manager)
    else:
        raise ValueError(f"Unknown window type: {window_type}")