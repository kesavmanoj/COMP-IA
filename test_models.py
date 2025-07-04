"""
Unit tests for the models module.
Demonstrates how the new architecture is testable unlike the old functions.py.
"""

import unittest
import sqlite3
import tempfile
import os
from unittest.mock import patch, MagicMock
from models import (
    DatabaseManager, Employee, Sector, Project, TimeTracking,
    validate_employee_data, validate_sector_data
)

class TestDatabaseManager(unittest.TestCase):
    """Test the DatabaseManager class."""
    
    def setUp(self):
        # Create a temporary database for testing
        self.temp_db = tempfile.NamedTemporaryFile(delete=False)
        self.temp_db.close()
        self.db_manager = DatabaseManager(self.temp_db.name)
        
        # Create test tables
        with self.db_manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE employees (
                    id_number INTEGER,
                    full_name TEXT,
                    hour_per_week INTEGER,
                    salary REAL,
                    designation TEXT,
                    project_number INTEGER,
                    attendance INTEGER
                )
            """)
            cursor.execute("""
                CREATE TABLE sector (
                    sector_id INTEGER,
                    sector_name TEXT,
                    sector_wage REAL
                )
            """)
            cursor.execute("""
                CREATE TABLE projects (
                    price REAL,
                    estimated_man_hours INTEGER,
                    current_manhours INTEGER,
                    percentage_completion REAL,
                    project_number INTEGER,
                    welder_manhours INTEGER,
                    builder_manhours INTEGER,
                    painter_manhours INTEGER,
                    engineer_manhours INTEGER,
                    manager_manhours INTEGER,
                    fitter_manhours INTEGER,
                    wages_payable REAL
                )
            """)
            cursor.execute("""
                CREATE TABLE specific_man_hours (
                    project_number INTEGER,
                    Welder INTEGER,
                    Builder INTEGER,
                    Painter INTEGER,
                    Engineer INTEGER,
                    Manager INTEGER,
                    Fitter INTEGER
                )
            """)
    
    def tearDown(self):
        # Clean up the temporary database
        os.unlink(self.temp_db.name)
    
    def test_connection_context_manager(self):
        """Test that the database connection context manager works."""
        with self.db_manager.get_connection() as conn:
            self.assertIsInstance(conn, sqlite3.Connection)
            cursor = conn.cursor()
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            self.assertEqual(result[0], 1)

class TestEmployee(unittest.TestCase):
    """Test the Employee model class."""
    
    def setUp(self):
        # Set up test database
        self.temp_db = tempfile.NamedTemporaryFile(delete=False)
        self.temp_db.close()
        self.db_manager = DatabaseManager(self.temp_db.name)
        self.employee = Employee(self.db_manager)
        
        # Create employees table
        with self.db_manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE employees (
                    id_number INTEGER,
                    full_name TEXT,
                    hour_per_week INTEGER,
                    salary REAL,
                    designation TEXT,
                    project_number INTEGER,
                    attendance INTEGER
                )
            """)
    
    def tearDown(self):
        os.unlink(self.temp_db.name)
    
    def test_create_employee_success(self):
        """Test successful employee creation."""
        employee_data = {
            'id_number': 1,
            'full_name': 'John Doe',
            'hour_per_week': 40,
            'salary': 50000.0,
            'designation': 'Engineer',
            'project_number': 1
        }
        
        result = self.employee.create(employee_data)
        self.assertTrue(result)
        
        # Verify the employee was created
        created_employee = self.employee.get_by_id(1)
        self.assertIsNotNone(created_employee)
        self.assertEqual(created_employee['full_name'], 'John Doe')
        self.assertEqual(created_employee['designation'], 'Engineer')
        self.assertEqual(created_employee['attendance'], 0)  # Default value
    
    def test_get_employee_not_found(self):
        """Test getting a non-existent employee."""
        result = self.employee.get_by_id(999)
        self.assertIsNone(result)
    
    def test_update_employee(self):
        """Test updating an employee."""
        # First create an employee
        employee_data = {
            'id_number': 1,
            'full_name': 'John Doe',
            'hour_per_week': 40,
            'salary': 50000.0,
            'designation': 'Engineer',
            'project_number': 1
        }
        self.employee.create(employee_data)
        
        # Update the employee
        updated_data = employee_data.copy()
        updated_data['salary'] = 60000.0
        updated_data['designation'] = 'Senior Engineer'
        updated_data['attendance'] = 5
        
        result = self.employee.update(1, updated_data)
        self.assertTrue(result)
        
        # Verify the update
        updated_employee = self.employee.get_by_id(1)
        self.assertEqual(updated_employee['salary'], 60000.0)
        self.assertEqual(updated_employee['designation'], 'Senior Engineer')
        self.assertEqual(updated_employee['attendance'], 5)
    
    @patch('models.logger')
    def test_create_employee_database_error(self, mock_logger):
        """Test error handling when database operation fails."""
        # Close the database to simulate an error
        os.unlink(self.temp_db.name)
        
        employee_data = {
            'id_number': 1,
            'full_name': 'John Doe',
            'hour_per_week': 40,
            'salary': 50000.0,
            'designation': 'Engineer',
            'project_number': 1
        }
        
        result = self.employee.create(employee_data)
        self.assertFalse(result)
        mock_logger.error.assert_called()

class TestValidationFunctions(unittest.TestCase):
    """Test validation functions."""
    
    def test_validate_employee_data_valid(self):
        """Test validation with valid employee data."""
        data = {
            'id_number': 1,
            'full_name': 'John Doe',
            'hour_per_week': 40,
            'salary': 50000.0,
            'designation': 'Engineer',
            'project_number': 1
        }
        is_valid, error = validate_employee_data(data)
        self.assertTrue(is_valid)
        self.assertEqual(error, "")
    
    def test_validate_employee_data_missing_field(self):
        """Test validation with missing required field."""
        data = {
            'id_number': 1,
            # Missing 'full_name'
            'hour_per_week': 40,
            'salary': 50000.0,
            'designation': 'Engineer',
            'project_number': 1
        }
        is_valid, error = validate_employee_data(data)
        self.assertFalse(is_valid)
        self.assertIn("full_name", error)
    
    def test_validate_employee_data_negative_salary(self):
        """Test validation with negative salary."""
        data = {
            'id_number': 1,
            'full_name': 'John Doe',
            'hour_per_week': 40,
            'salary': -1000.0,  # Invalid negative salary
            'designation': 'Engineer',
            'project_number': 1
        }
        is_valid, error = validate_employee_data(data)
        self.assertFalse(is_valid)
        self.assertIn("negative", error.lower())
    
    def test_validate_employee_data_invalid_hours(self):
        """Test validation with invalid hours per week."""
        data = {
            'id_number': 1,
            'full_name': 'John Doe',
            'hour_per_week': 200,  # More than 168 hours in a week
            'salary': 50000.0,
            'designation': 'Engineer',
            'project_number': 1
        }
        is_valid, error = validate_employee_data(data)
        self.assertFalse(is_valid)
        self.assertIn("168", error)
    
    def test_validate_sector_data_valid(self):
        """Test validation with valid sector data."""
        data = {
            'sector_id': 1,
            'sector_name': 'Engineer',
            'sector_wage': 25.0
        }
        is_valid, error = validate_sector_data(data)
        self.assertTrue(is_valid)
        self.assertEqual(error, "")
    
    def test_validate_sector_data_negative_wage(self):
        """Test validation with negative wage."""
        data = {
            'sector_id': 1,
            'sector_name': 'Engineer',
            'sector_wage': -10.0
        }
        is_valid, error = validate_sector_data(data)
        self.assertFalse(is_valid)
        self.assertIn("negative", error.lower())

class TestTimeTracking(unittest.TestCase):
    """Test the TimeTracking class."""
    
    def setUp(self):
        # Set up test database with all required tables
        self.temp_db = tempfile.NamedTemporaryFile(delete=False)
        self.temp_db.close()
        self.db_manager = DatabaseManager(self.temp_db.name)
        self.time_tracking = TimeTracking(self.db_manager)
        
        # Create all required tables and test data
        with self.db_manager.get_connection() as conn:
            cursor = conn.cursor()
            
            # Create tables
            cursor.execute("""
                CREATE TABLE employees (
                    id_number INTEGER,
                    full_name TEXT,
                    hour_per_week INTEGER,
                    salary REAL,
                    designation TEXT,
                    project_number INTEGER,
                    attendance INTEGER
                )
            """)
            cursor.execute("""
                CREATE TABLE sector (
                    sector_id INTEGER,
                    sector_name TEXT,
                    sector_wage REAL
                )
            """)
            cursor.execute("""
                CREATE TABLE projects (
                    price REAL,
                    estimated_man_hours INTEGER,
                    current_manhours INTEGER,
                    percentage_completion REAL,
                    project_number INTEGER,
                    welder_manhours INTEGER,
                    builder_manhours INTEGER,
                    painter_manhours INTEGER,
                    engineer_manhours INTEGER,
                    manager_manhours INTEGER,
                    fitter_manhours INTEGER,
                    wages_payable REAL
                )
            """)
            cursor.execute("""
                CREATE TABLE specific_man_hours (
                    project_number INTEGER,
                    Welder INTEGER,
                    Builder INTEGER,
                    Painter INTEGER,
                    Engineer INTEGER,
                    Manager INTEGER,
                    Fitter INTEGER
                )
            """)
            
            # Insert test data
            cursor.execute("""
                INSERT INTO employees 
                (id_number, full_name, hour_per_week, salary, designation, project_number, attendance)
                VALUES (1, 'John Doe', 40, 50000.0, 'Engineer', 1, 0)
            """)
            cursor.execute("""
                INSERT INTO sector (sector_id, sector_name, sector_wage)
                VALUES (1, 'Engineer', 25.0)
            """)
            cursor.execute("""
                INSERT INTO projects 
                (price, estimated_man_hours, current_manhours, percentage_completion, project_number,
                 welder_manhours, builder_manhours, painter_manhours, engineer_manhours, 
                 manager_manhours, fitter_manhours, wages_payable)
                VALUES (10000.0, 100, 0, 0.0, 1, 10, 10, 10, 10, 10, 10, 0.0)
            """)
            cursor.execute("""
                INSERT INTO specific_man_hours 
                (project_number, Welder, Builder, Painter, Engineer, Manager, Fitter)
                VALUES (1, 0, 0, 0, 0, 0, 0)
            """)
    
    def tearDown(self):
        os.unlink(self.temp_db.name)
    
    def test_record_hours_success(self):
        """Test successful hours recording."""
        result = self.time_tracking.record_hours(
            employee_id=1,
            project_number=1,
            hours=8
        )
        self.assertTrue(result)
        
        # Verify the hours were recorded
        with self.db_manager.get_connection() as conn:
            cursor = conn.cursor()
            
            # Check employee attendance was updated
            cursor.execute("SELECT attendance FROM employees WHERE id_number = 1")
            attendance = cursor.fetchone()[0]
            self.assertEqual(attendance, 1)
            
            # Check project manhours were updated
            cursor.execute("SELECT current_manhours, wages_payable FROM projects WHERE project_number = 1")
            manhours, wages = cursor.fetchone()
            self.assertEqual(manhours, 8)
            self.assertEqual(wages, 200.0)  # 8 hours * $25/hour
            
            # Check specific manhours were updated
            cursor.execute("SELECT Engineer FROM specific_man_hours WHERE project_number = 1")
            engineer_hours = cursor.fetchone()[0]
            self.assertEqual(engineer_hours, 8)
    
    def test_record_hours_employee_not_found(self):
        """Test recording hours for non-existent employee."""
        result = self.time_tracking.record_hours(
            employee_id=999,  # Non-existent employee
            project_number=1,
            hours=8
        )
        self.assertFalse(result)

if __name__ == '__main__':
    # Run tests with verbose output
    unittest.main(verbosity=2)