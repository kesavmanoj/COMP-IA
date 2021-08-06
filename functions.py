from tkinter import *
from PIL import ImageTk, Image
from tkinter import filedialog
import sqlite3


# Function for each top button to open a page

def employees_btn():
    global employees
    employees = Toplevel()
    employees.title('Edit or Add Employees')
    employees.geometry("350x400")

    def add_employee():
        # Connect to database
        conn = sqlite3.connect('iscon.db')
        c = conn.cursor()
        # Insert into table
        c.execute("INSERT INTO employees VALUES (:id_number, :full_name, :hour_per_week, :salary, :designation, :project_number, :attendance)",
        { 
            'id_number': id_number.get(),
            'full_name': full_name.get(),
            'hour_per_week': hours_per_week.get(),
            'salary' : salary.get(),
            'designation': designation.get(),
            'project_number':project_number.get(),
            'attendance' : 0
        })

        id_number.delete(0, END)
        full_name.delete(0, END)
        hours_per_week.delete(0, END)
        salary.delete(0, END)
        designation.delete(0, END)
        project_number.delete(0, END)

        # Commit changes
        conn.commit()
        # Close the connection
        conn.close()
    
    
    def edit_employee():
        edit_employees = Toplevel()
        edit_employees.title('Edit or Add Employees')
        edit_employees.geometry("350x400")

        # Connect to database
        conn = sqlite3.connect('iscon.db')
        c = conn.cursor()

        global id_number_edit
        global full_name_edit
        global hour_per_week_edit
        global salary_edit
        global designation_edit
        global project_number_edit

        space_inBetween = Label(edit_employees, text = "   ", width = 8, height = 2).grid(column = 0, row = 0)
        id_number_edit_label = Label(edit_employees, text = "         ID Number         ").grid(column = 0, row = 1)
        id_number_edit = Entry(edit_employees)
        id_number_edit.grid(column = 1, row = 1)

        full_name_edit_label = Label(edit_employees, text = "Full Name").grid(column = 0, row = 2)
        full_name_edit = Entry(edit_employees)
        full_name_edit.grid(column = 1, row = 2)

        hour_per_week_edit_label = Label(edit_employees, text = "Hours per Week").grid(column = 0, row = 3)
        hour_per_week_edit = Entry(edit_employees)
        hour_per_week_edit.grid(column = 1, row = 3)

        salary_edit_label = Label(edit_employees, text = "Salary").grid(column = 0, row = 4)
        salary_edit = Entry(edit_employees)
        salary_edit.grid(column = 1, row = 4)   
        
        designation_edit_label = Label(edit_employees, text = "Designation").grid(column = 0, row = 5)
        designation_edit = Entry(edit_employees)
        designation_edit.grid(column = 1, row = 5)  

        project_number_edit_label = Label(edit_employees, text = "Project Number").grid(column = 0, row = 6)
        project_number_edit = Entry(edit_employees)
        project_number_edit.grid(column = 1, row = 6)  

        # Create a save button
        save_btn = Button(edit_employees, text = "Save Record", command = save)
        save_btn.grid(column = 1, row = 7)

        # Get the record needed to edit
        global id_number2
        id_number2 = enter_employee_id.get()
        c.execute("SELECT * FROM employees WHERE id_number = " + id_number2)
        records = c.fetchall()

        # Loop through the results
        for record in records:
            id_number_edit.insert(0, record[0])
            full_name_edit.insert(0, record[1])
            hour_per_week_edit.insert(0, record[2])
            salary_edit.insert(0, record[3])
            designation_edit.insert(0, record[4])
            project_number_edit.insert(0, record[5])

            

        # Commit changes
        conn.commit()
        # Close the connection
        conn.close()

    def save():
        # Connect to database
        conn = sqlite3.connect('iscon.db')
        c = conn.cursor()

        c.execute(""" UPDATE employees SET
            id_number = :idnumber,
            full_name = :fullname,
            hour_per_week = :hoursperweek,
            salary = :employee_salary,
            designation = :employee_designation,
            project_number = :projectnumber,
            attendance = :employee_attendance

            WHERE id_number = :id_number2 """, 
            {
                'idnumber' : id_number_edit.get(),
                'fullname' : full_name_edit.get(),
                'hoursperweek' : hour_per_week_edit.get(),
                'employee_salary' : salary_edit.get(),
                'employee_designation' : designation_edit.get(),
                'projectnumber' : project_number_edit.get(),
                'employee_attendance' : 0,
                'id_number2' : id_number2
            }
         )
        id_number_edit.delete(0, END)
        full_name_edit.delete(0, END)
        hour_per_week_edit.delete(0, END)
        salary_edit.delete(0, END)
        designation_edit.delete(0, END)
        project_number_edit.delete(0, END)


        # Commit changes
        conn.commit()
        # Close the connection
        conn.close()

    # Create text labels
    space_inBetween = Label(employees, text = " ", width = 8, height = 2).grid(column = 0, row = 1)

    id_number_label = Label(employees, text = 'ID Number').grid(column = 0, row = 2)
    id_number = Entry(employees)
    id_number.grid(column = 1, row = 2)
    full_name_label = Label(employees, text = 'Full Name').grid(column = 0, row = 3)
    full_name = Entry(employees)
    full_name.grid(column= 1, row = 3)
    hours_per_week_label = Label(employees, text = 'Hours Per Week').grid(column = 0, row = 5)
    hours_per_week = Entry(employees)
    hours_per_week.grid(column= 1, row = 5)
    salary_label = Label(employees, text = 'Salary').grid(column = 0, row = 6)
    salary = Entry(employees)
    salary.grid(column= 1, row = 6)
    designation_label = Label(employees, text = 'Designation').grid(column = 0, row = 7)
    designation = Entry(employees)
    designation.grid(column= 1, row = 7)
    project_number_label = Label(employees, text = 'Project Number').grid(column = 0, row = 8)
    project_number = Entry(employees)
    project_number.grid(column = 1, row =8)
    enter_employee_id_label = Label(employees, text = "Employee ID").grid(column = 0, row = 12)
    enter_employee_id = Entry(employees)
    enter_employee_id.grid(column = 1, row = 12)
    
    # Add edit or add buttons
    add_button = Button(employees, text = "Add", width = 20, height = 2, command = add_employee).grid(column = 1, row = 10)
    edit_button = Button(employees, text = "Edit", width = 20, height = 2, command = edit_employee).grid(column = 1, row = 14)
 
    space_inBetween = Label(employees, text = " ", width = 8, height = 2).grid(column = 0, row = 11)
    space_inBetween = Label(employees, text = " ", width = 8, height = 1).grid(column = 0, row = 9)
    space_inBetween = Label(employees, text = " ", width = 8, height = 1).grid(column = 1, row = 13)


def designations_btn():
    designations = Toplevel()
    designations.title('Edit or Add Designations')
    designations.geometry("350x400")

    def add_designation():
         # Connect to database
        conn = sqlite3.connect('iscon.db')
        c = conn.cursor()

        c.execute("INSERT INTO sector VALUES (:sector_id, :sector_name, :sector_wage)",
        {
            'sector_id' : designation_number.get(),
            'sector_name' : designation.get(),
            'sector_wage' : designation_wage.get()
        }
        )

        # Commit changes
        conn.commit()
        # Close the connection
        conn.close()



    def edit_designation():
        # Connect to database
        conn = sqlite3.connect('iscon.db')
        c = conn.cursor()

        edit_designation = Toplevel()
        edit_designation.title('Edit or Add Designations')
        edit_designation.geometry("350x400")

        # Globalise the variables
        global designation_number_edit
        global designation__edit
        global designation_wage_edit
        

        # Creat the buttons and text
        space_inBetween = Label(edit_designation, text = " ", width = 8, height = 1).grid(column = 0, row = 0)

        designation_number_label_edit = Label(edit_designation, text = '   Designation Number   ').grid(column = 0, row = 1)
        designation_number_edit = Entry(edit_designation)
        designation_number_edit.grid(column = 1, row = 1)

        designation_label_edit = Label(edit_designation, text = '   Designation   ').grid(column = 0, row = 2)
        designation__edit = Entry(edit_designation)
        designation__edit.grid(column = 1, row = 2)

        designation_wage_label_edit = Label(edit_designation, text = '   Designation Wage   ').grid(column = 0, row = 3)
        designation_wage_edit = Entry(edit_designation)
        designation_wage_edit.grid(column = 1, row = 3)

        save_btn = Button(edit_designation, text = "Save Designation", command = save).grid(column = 1, row = 4)

        global designation_number
        designation_number = enter_designation_number.get()
        c.execute("SELECT * FROM sector WHERE sector_id =" + designation_number)
        designations = c.fetchall()

        for designation in designations:
            designation_number_edit.insert(0, designation[0])
            designation__edit.insert(0, designation[1])
            designation_wage_edit.insert(0, designation[2])


        # Commit changes
        conn.commit()
        # Close the connection
        conn.close()

    # Add text labels and entry widgets
    space_inBetween = Label(designations, text = " ", width = 8, height = 1).grid(column = 1, row = 0)
    
    designation_number_label = Label(designations, text = '  Designation Number  ').grid(column = 0, row = 1)
    designation_number = Entry(designations)
    designation_number.grid(column = 1, row = 1)

    designation_label = Label(designations, text = '  Designation  ').grid(column = 0, row = 2)
    designation = Entry(designations)
    designation.grid(column = 1, row = 2)

    designation_wage_label = Label(designations, text = '  Designation Wage  ').grid(column = 0, row = 3)
    designation_wage = Entry(designations)
    designation_wage.grid(column = 1, row = 3)

    enter_designation_number_label = Label(designations, text = "Enter Designation ID").grid(column = 0, row = 7)
    enter_designation_number = Entry(designations)
    enter_designation_number.grid(column = 1, row = 7)

    add_button = Button(designations, text = "Add", width = 20, height = 1, command = add_designation).grid(column = 1, row = 5)
    edit_button = Button(designations, text = "Edit", width = 20, height = 1, command = edit_designation).grid(column = 1, row = 14)

    space_inBetween = Label(designations, text = " ", width = 8, height = 1).grid(column = 1, row = 4)
    space_inBetween = Label(designations, text = " ", width = 8, height = 1).grid(column = 1, row = 6)
    space_inBetween = Label(designations, text = " ", width = 8, height = 1).grid(column = 1, row = 8)
    
    def save():
        # Connect to database
        conn = sqlite3.connect('iscon.db')
        c = conn.cursor()

        c.execute(""" UPDATE sector SET
            sector_id = :sectorid,
            sector_name = :sectorname,
            sector_wage = :sectorwage 
            
            WHERE sector_id = :designation_number""",
            {
                'sectorid' : designation_number_edit.get(),
                'sectorname' : designation__edit.get(),
                'sectorwage' : designation_wage_edit.get(),
                'designation_number': enter_designation_number.get()

            })
        
        designation_number_edit.delete(0, END)
        designation__edit.delete(0, END)
        designation_wage_edit.delete(0, END)

        # Commit changes
        conn.commit()
        # Close the connection
        conn.close()        


def projects_btn():
    projects = Toplevel()
    projects.title('Edit or Add Projects')
    projects.geometry("200x200")
    # Add edit or add buttons
    add_button = Button(projects, text = "Add", width = 20, height = 2).pack()
    update_button = Button(projects, text = "Update", width = 20, height = 2).pack()


