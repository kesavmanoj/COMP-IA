"""
Data models and database operations for the project management system.
Separates database logic from UI code and provides a clean API.
"""

import sqlite3
from typing import List, Dict, Optional, Tuple
from contextlib import contextmanager
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DatabaseManager:
    """Manages database connections and provides context management."""
    
    def __init__(self, db_path: str = 'iscon.db'):
        self.db_path = db_path
    
    @contextmanager
    def get_connection(self):
        """Context manager for database connections."""
        conn = None
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row  # Enable dict-like access
            yield conn
        except sqlite3.Error as e:
            if conn:
                conn.rollback()
            logger.error(f"Database error: {e}")
            raise
        finally:
            if conn:
                conn.close()

class Employee:
    """Employee data model with CRUD operations."""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager
    
    def create(self, employee_data: Dict) -> bool:
        """Create a new employee."""
        try:
            with self.db.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO employees 
                    (id_number, full_name, hour_per_week, salary, designation, project_number, attendance)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    employee_data['id_number'],
                    employee_data['full_name'],
                    employee_data['hour_per_week'],
                    employee_data['salary'],
                    employee_data['designation'],
                    employee_data['project_number'],
                    0  # Default attendance
                ))
                conn.commit()
                logger.info(f"Created employee {employee_data['id_number']}")
                return True
        except sqlite3.Error as e:
            logger.error(f"Failed to create employee: {e}")
            return False
    
    def get_by_id(self, employee_id: int) -> Optional[Dict]:
        """Get employee by ID."""
        try:
            with self.db.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT * FROM employees WHERE id_number = ?", 
                    (employee_id,)
                )
                row = cursor.fetchone()
                if row:
                    return dict(row)
                return None
        except sqlite3.Error as e:
            logger.error(f"Failed to get employee {employee_id}: {e}")
            return None
    
    def update(self, employee_id: int, employee_data: Dict) -> bool:
        """Update employee information."""
        try:
            with self.db.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE employees SET
                        id_number = ?,
                        full_name = ?,
                        hour_per_week = ?,
                        salary = ?,
                        designation = ?,
                        project_number = ?,
                        attendance = ?
                    WHERE id_number = ?
                """, (
                    employee_data['id_number'],
                    employee_data['full_name'],
                    employee_data['hour_per_week'],
                    employee_data['salary'],
                    employee_data['designation'],
                    employee_data['project_number'],
                    employee_data['attendance'],
                    employee_id
                ))
                conn.commit()
                logger.info(f"Updated employee {employee_id}")
                return True
        except sqlite3.Error as e:
            logger.error(f"Failed to update employee {employee_id}: {e}")
            return False
    
    def get_all(self) -> List[Dict]:
        """Get all employees."""
        try:
            with self.db.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM employees")
                return [dict(row) for row in cursor.fetchall()]
        except sqlite3.Error as e:
            logger.error(f"Failed to get all employees: {e}")
            return []

class Sector:
    """Sector/Designation data model with CRUD operations."""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager
    
    def create(self, sector_data: Dict) -> bool:
        """Create a new sector."""
        try:
            with self.db.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO sector (sector_id, sector_name, sector_wage)
                    VALUES (?, ?, ?)
                """, (
                    sector_data['sector_id'],
                    sector_data['sector_name'],
                    sector_data['sector_wage']
                ))
                conn.commit()
                logger.info(f"Created sector {sector_data['sector_name']}")
                return True
        except sqlite3.Error as e:
            logger.error(f"Failed to create sector: {e}")
            return False
    
    def get_by_id(self, sector_id: int) -> Optional[Dict]:
        """Get sector by ID."""
        try:
            with self.db.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT * FROM sector WHERE sector_id = ?", 
                    (sector_id,)
                )
                row = cursor.fetchone()
                if row:
                    return dict(row)
                return None
        except sqlite3.Error as e:
            logger.error(f"Failed to get sector {sector_id}: {e}")
            return None
    
    def get_by_name(self, sector_name: str) -> Optional[Dict]:
        """Get sector by name."""
        try:
            with self.db.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT * FROM sector WHERE sector_name = ?", 
                    (sector_name,)
                )
                row = cursor.fetchone()
                if row:
                    return dict(row)
                return None
        except sqlite3.Error as e:
            logger.error(f"Failed to get sector {sector_name}: {e}")
            return None
    
    def update(self, sector_id: int, sector_data: Dict) -> bool:
        """Update sector information."""
        try:
            with self.db.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE sector SET
                        sector_id = ?,
                        sector_name = ?,
                        sector_wage = ?
                    WHERE sector_id = ?
                """, (
                    sector_data['sector_id'],
                    sector_data['sector_name'],
                    sector_data['sector_wage'],
                    sector_id
                ))
                conn.commit()
                logger.info(f"Updated sector {sector_id}")
                return True
        except sqlite3.Error as e:
            logger.error(f"Failed to update sector {sector_id}: {e}")
            return False

class Project:
    """Project data model with CRUD operations."""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager
    
    def create(self, project_data: Dict) -> bool:
        """Create a new project."""
        try:
            with self.db.get_connection() as conn:
                cursor = conn.cursor()
                # Insert into projects table
                cursor.execute("""
                    INSERT INTO projects (
                        price, estimated_man_hours, project_number,
                        welder_manhours, builder_manhours, painter_manhours,
                        engineer_manhours, manager_manhours, fitter_manhours,
                        current_manhours, percentage_completion, wages_payable
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 0, 0, 0)
                """, (
                    project_data['price'],
                    project_data['estimated_man_hours'],
                    project_data['project_number'],
                    project_data['welder_manhours'],
                    project_data['builder_manhours'],
                    project_data['painter_manhours'],
                    project_data['engineer_manhours'],
                    project_data['manager_manhours'],
                    project_data['fitter_manhours']
                ))
                
                # Initialize specific_man_hours table
                cursor.execute("""
                    INSERT INTO specific_man_hours 
                    (project_number, Welder, Builder, Painter, Engineer, Manager, Fitter)
                    VALUES (?, 0, 0, 0, 0, 0, 0)
                """, (project_data['project_number'],))
                
                conn.commit()
                logger.info(f"Created project {project_data['project_number']}")
                return True
        except sqlite3.Error as e:
            logger.error(f"Failed to create project: {e}")
            return False
    
    def get_by_number(self, project_number: int) -> Optional[Dict]:
        """Get project by number."""
        try:
            with self.db.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT * FROM projects WHERE project_number = ?", 
                    (project_number,)
                )
                row = cursor.fetchone()
                if row:
                    return dict(row)
                return None
        except sqlite3.Error as e:
            logger.error(f"Failed to get project {project_number}: {e}")
            return None
    
    def get_specific_manhours(self, project_number: int) -> Optional[Dict]:
        """Get specific manhours for a project."""
        try:
            with self.db.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT * FROM specific_man_hours WHERE project_number = ?", 
                    (project_number,)
                )
                row = cursor.fetchone()
                if row:
                    return dict(row)
                return None
        except sqlite3.Error as e:
            logger.error(f"Failed to get specific manhours for project {project_number}: {e}")
            return None
    
    def update_percentage(self, project_number: int, percentage: float) -> bool:
        """Update project completion percentage."""
        try:
            with self.db.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE projects 
                    SET percentage_completion = ?
                    WHERE project_number = ?
                """, (percentage, project_number))
                conn.commit()
                logger.info(f"Updated project {project_number} percentage to {percentage}")
                return True
        except sqlite3.Error as e:
            logger.error(f"Failed to update project percentage: {e}")
            return False

class TimeTracking:
    """Handles time tracking and wage calculations."""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager
        self.employee = Employee(db_manager)
        self.sector = Sector(db_manager)
        self.project = Project(db_manager)
    
    def record_hours(self, employee_id: int, project_number: int, hours: int) -> bool:
        """Record hours worked by an employee on a project."""
        try:
            with self.db.get_connection() as conn:
                cursor = conn.cursor()
                
                # Get employee info
                employee_data = self.employee.get_by_id(employee_id)
                if not employee_data:
                    logger.error(f"Employee {employee_id} not found")
                    return False
                
                designation = employee_data['designation']
                
                # Get sector wage
                sector_data = self.sector.get_by_name(designation)
                if not sector_data:
                    logger.error(f"Sector {designation} not found")
                    return False
                
                sector_wage = sector_data['sector_wage']
                calculated_wage = sector_wage * hours
                
                # Update employee attendance and project
                cursor.execute("""
                    UPDATE employees 
                    SET attendance = attendance + 1,
                        project_number = ?
                    WHERE id_number = ?
                """, (project_number, employee_id))
                
                # Update project manhours and wages
                cursor.execute("""
                    UPDATE projects
                    SET current_manhours = current_manhours + ?,
                        wages_payable = wages_payable + ?
                    WHERE project_number = ?
                """, (hours, calculated_wage, project_number))
                
                # Update specific manhours by designation
                designation_column = designation.capitalize()
                cursor.execute(f"""
                    UPDATE specific_man_hours
                    SET {designation_column} = {designation_column} + ?
                    WHERE project_number = ?
                """, (hours, project_number))
                
                conn.commit()
                logger.info(f"Recorded {hours} hours for employee {employee_id} on project {project_number}")
                return True
                
        except sqlite3.Error as e:
            logger.error(f"Failed to record hours: {e}")
            return False

# Validation functions
def validate_employee_data(data: Dict) -> Tuple[bool, str]:
    """Validate employee data."""
    required_fields = ['id_number', 'full_name', 'hour_per_week', 'salary', 'designation', 'project_number']
    
    for field in required_fields:
        if field not in data or not data[field]:
            return False, f"Missing required field: {field}"
    
    try:
        int(data['id_number'])
        int(data['hour_per_week'])
        float(data['salary'])
        int(data['project_number'])
    except ValueError:
        return False, "Invalid numeric values"
    
    if data['hour_per_week'] < 0 or data['hour_per_week'] > 168:
        return False, "Hours per week must be between 0 and 168"
    
    if data['salary'] < 0:
        return False, "Salary cannot be negative"
    
    return True, ""

def validate_sector_data(data: Dict) -> Tuple[bool, str]:
    """Validate sector data."""
    required_fields = ['sector_id', 'sector_name', 'sector_wage']
    
    for field in required_fields:
        if field not in data or not data[field]:
            return False, f"Missing required field: {field}"
    
    try:
        int(data['sector_id'])
        float(data['sector_wage'])
    except ValueError:
        return False, "Invalid numeric values"
    
    if data['sector_wage'] < 0:
        return False, "Wage cannot be negative"
    
    return True, ""