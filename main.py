from tkinter import *
from tkinter import filedialog
from functions import *
import sqlite3


root = Tk()
root.title('Program') 
root.geometry("449x400")

sectors = ["welder", "builder", "painter", "engineer", "manager", "fitter"]



# Connect to Database and create a cursor
conn = sqlite3.connect('iscon.db')
c = conn.cursor()

# Add number of hours worked and update project manhours
def enter():
    # Connect to Database and create a cursor
    conn = sqlite3.connect('iscon.db')
    c = conn.cursor()

    c.execute("""UPDATE employees 
        SET attendance = attendance + 1,
        project_number = :projectnumber
        WHERE id_number = :idnumber """,
        {
            'projectnumber' : enter_project_number.get(),
            'idnumber' : enter_employee_id.get()
        })
    
    c.execute(""" UPDATE projects
        SET current_manhours = current_manhours + :entered_manhours
        WHERE project_number = :projectnumber
        """,
        {
            'entered_manhours' : enter_hours.get(),  
            'projectnumber' : enter_project_number.get()                                                        
        }
        )
    
    c.execute(""" SELECT designation FROM employees WHERE id_number = :idnumber""",
        {
            'idnumber' : enter_employee_id.get()
        })
    x = c.fetchone()
    designation = x[0]
    print(designation)

    if designation == "Welder":
        c.execute(""" UPDATE specific_man_hours
        SET Welder = Welder + :entered_manhours
        WHERE project_number = :projectnumber""",
         {
           'projectnumber' : enter_project_number.get(),
          'entered_manhours' : enter_hours.get()
       })
    elif designation == "Builder":
        c.execute(""" UPDATE specific_man_hours
        SET Builder = Builder + :entered_manhours
        WHERE project_number = :projectnumber""",
         {
           'projectnumber' : enter_project_number.get(),
          'entered_manhours' : enter_hours.get()
       })
    elif designation == "Painter":
        c.execute(""" UPDATE specific_man_hours
        SET Painter = Painter + :entered_manhours
        WHERE project_number = :projectnumber""",
         {
           'projectnumber' : enter_project_number.get(),
          'entered_manhours' : enter_hours.get()
       })
    elif designation == "Engineer":
        c.execute(""" UPDATE specific_man_hours
        SET Engineer = Engineer + :entered_manhours
        WHERE project_number = :projectnumber""",
         {
           'projectnumber' : enter_project_number.get(),
          'entered_manhours' : enter_hours.get()
       })
    elif designation == "Manager":
        c.execute(""" UPDATE specific_man_hours
        SET Manager = Manager + :entered_manhours
        WHERE project_number = :projectnumber""",
         {
           'projectnumber' : enter_project_number.get(),
          'entered_manhours' : enter_hours.get()
       })
    elif designation == "Fitter":
        c.execute(""" UPDATE specific_man_hours
        SET Fitter = Fitter + :entered_manhours
        WHERE project_number = :projectnumber""",
         {
           'projectnumber' : enter_project_number.get(),
          'entered_manhours' : enter_hours.get()
       })



    # Commit changes
    conn.commit()  
     # Close the connection
    conn.close()
    return

# Create top buttons
employees_btn = Button(root, text = "Employees", width = 20, height = 2, command = employees_btn).grid(row = 0, column = 0)
designation_btn = Button(root, text = 'Designations', width = 20, height = 2, command = designations_btn).grid(row = 0, column = 1)
project_btn = Button(root, text = 'Projects', width = 20, height = 2, command = projects_btn).grid(row = 0, column = 2)

space_inBetween = Label(root, text = "       ", width = 8, height = 2).grid(row = 1, column = 1)
enter_project_number_label = Label(root, text = "Enter Project Number : ", width = 20, height = 2).grid(row = 2, column = 0)
enter_project_number = Entry(root, width = 20)
enter_project_number.grid(row = 2, column = 1)

enter_employee_id_label = Label(root, text = "Enter Employee ID : ",  width = 20, height = 2).grid(row = 3, column = 0)
enter_employee_id = Entry(root, width = 20)
enter_employee_id.grid(row = 3, column = 1)

enter_hours_label = Label(root, text = 'No. of Hours Worked : ',  width = 20, height = 2).grid(row = 4, column = 0)
enter_hours = Entry(root, width = 20)
enter_hours.grid(row = 4, column = 1)

enter_btn = Button(root, text = "Enter", width = 20, height = 2, command= enter).grid(row = 5, column = 1)

# Commit changes
conn.commit()  
# Close the connection
conn.close()

root.mainloop()