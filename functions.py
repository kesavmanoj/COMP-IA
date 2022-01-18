from tkinter import *
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
    projects.geometry("410x600")

    def search():
        search_projects = Toplevel()
        search_projects.title('Search for project')
        search_projects.geometry("540x450")

         # Connect to database
        conn = sqlite3.connect('iscon.db')
        c = conn.cursor()
        x = 3

        space_inBetween = Label(search_projects, text = "   ", width = 15, height = 2).grid(column = 0, row = 0)
        project_number_label = Label(search_projects, text = '   Project Number   ').grid(column = 0, row = x+1)
        project_number = Entry(search_projects)
        project_number.grid(column = 1, row = x+1)

        total_current_manhours_label = Label(search_projects, text = "    Total current man hours     ").grid(column = 0, row = x+2)
        total_current_manhours = Entry(search_projects)
        total_current_manhours.grid(column = 1, row = x+2)

        estimated_current_manhours_label = Label(search_projects, text = "    Estimated man hours     ").grid(column = 0, row = x+3)
        estimated_current_manhours = Entry(search_projects)
        estimated_current_manhours.grid(column = 1, row = x+3)

        percentage_completion_label = Label(search_projects, text = "    Total % Completion     ").grid(column = 0, row = x+4)
        percentage_completion = Entry(search_projects)
        percentage_completion.grid(column = 1, row = x+4)
        
        wages_paid_label = Label(search_projects, text = "Wages paid").grid(column = 0, row = x+5)
        wages_paid = Entry(search_projects)
        wages_paid.grid(column = 1, row = x+5)

        total_estimated_wage_label = Label(search_projects, text = "Total estimated wage").grid(column = 0, row = x+6)
        total_estimated_wage = Entry(search_projects)
        total_estimated_wage.grid(column = 1, row = x+6)

        space_inBetween = Label(search_projects, text = " ", width = 8, height = 2).grid(column = 0, row = 10) 
        specific_estimated_man_hours_label = Label(search_projects, text = '   SPECIFIC MAN HOURS  :    ').grid(column = 0, row = 11)
        current_man_hours__label = Label(search_projects, text = 'Current man hours').grid(column = 1, row = 11)
        estimated_man_hours = Label(search_projects, text = 'Estimated man hours').grid(column = 2, row = 11)

        welder_manhours_label = Label(search_projects, text = 'Welder').grid(column = 0, row = 12)
        welder_manhours = Entry(search_projects)
        welder_manhours.grid(column = 1, row = 12)
        estimated_welder_manhours = Entry(search_projects)
        estimated_welder_manhours.grid(column = 2, row = 12)

        builder_manhours_label = Label(search_projects, text = 'Builder').grid(column = 0, row = 13 )
        builder_manhours = Entry(search_projects)
        builder_manhours.grid(column = 1, row =13 )
        estimated_builder_manhours = Entry(search_projects)
        estimated_builder_manhours.grid(column = 2, row = 13)

        painter_manhours_label = Label(search_projects, text = 'Painter').grid(column = 0, row =14 )
        painter_manhours = Entry(search_projects)
        painter_manhours.grid(column = 1, row =14 )  
        estimated_painter_manhours = Entry(search_projects)
        estimated_painter_manhours.grid(column = 2, row = 14)

        engineer_manhours_label = Label(search_projects, text = 'Engineer').grid(column = 0, row =15 )
        engineer_manhours = Entry(search_projects)
        engineer_manhours.grid(column = 1, row =15 )
        estimated_engineer_manhours = Entry(search_projects)
        estimated_engineer_manhours.grid(column = 2, row = 15)

        manager_manhours_label = Label(search_projects, text = 'Manager').grid(column = 0, row =16 )
        manager_manhours = Entry(search_projects)
        manager_manhours.grid(column = 1, row =16 )
        estimated_manager_manhours = Entry(search_projects)
        estimated_manager_manhours.grid(column = 2, row = 16)

        fitter_manhours_label = Label(search_projects, text = 'Fitter').grid(column = 0, row =17 )
        fitter_manhours = Entry(search_projects)
        fitter_manhours.grid(column = 1, row =17 )
        estimated_fitter_manhours = Entry(search_projects)
        estimated_fitter_manhours.grid(column = 2, row = 17)

        # get the project detail from project number
        global project_number2
        project_number2 = project_number_search.get()
        projects_records = c.execute("SELECT * FROM projects WHERE project_number = " + project_number2)
        project_records = c.fetchall()

        for project_record in project_records:

            project_number.insert(0, project_record[4])
            estimated_current_manhours.insert(0, project_record[1])
            total_current_manhours.insert(0, project_record[2])
            percentage_completion.insert(0, project_record[3])
            total_estimated_wage.insert(0, project_record[0])
            estimated_welder_manhours.insert(0, project_record[5])
            estimated_builder_manhours.insert(0, project_record[6])
            estimated_painter_manhours.insert(0, project_record[7])
            estimated_engineer_manhours.insert(0, project_record[8])
            estimated_manager_manhours.insert(0, project_record[9])
            estimated_fitter_manhours.insert(0, project_record[10])
            wages_paid.insert(0, project_record[11])
        
        currents_manhours = c.execute("SELECT * FROM specific_man_hours WHERE project_number = "+ project_number2)
        current_manhours = c.fetchall()
        
        for current_manhour in current_manhours:
            welder_manhours.insert(0, current_manhour[1])
            builder_manhours.insert(0, current_manhour[2])
            painter_manhours.insert(0, current_manhour[3])
            engineer_manhours.insert(0, current_manhour[4])
            manager_manhours.insert(0, current_manhour[5])
            fitter_manhours.insert(0, current_manhour[6])

        # Commit changes
        conn.commit()
        # Close the connection
        conn.close()         
        return

    def save():
        # Connect to database
        conn = sqlite3.connect('iscon.db')
        c = conn.cursor()
        
        # Insert the values
        c.execute("""INSERT INTO projects (
            price,
            estimated_man_hours,
            project_number,
            welder_manhours,
            builder_manhours,
            painter_manhours,
            engineer_manhours,
            manager_manhours,
            fitter_manhours,
            current_manhours,
            percentage_completion,
            wages_payable
            )
            VALUES
                (
                    :price,
                    :estimated_man_hours,
                    :project_number,
                    :welder_manhours,
                    :builder_manhours,
                    :painter_manhours,
                    :engineer_manhours,
                    :manager_manhours,
                    :fitter_manhours,
                    0, 0, 0
                )                          """,
            {
                'price' : total_wage.get(),
                'estimated_man_hours' : estimated_man_hours.get(),
                'project_number' : project_number.get(),
                'welder_manhours' : welder_manhours.get(),
                'builder_manhours' : builder_manhours.get(),
                'painter_manhours' : painter_manhours.get(),
                'engineer_manhours' : engineer_manhours.get(),
                'manager_manhours' : manager_manhours.get(),
                'fitter_manhours' : fitter_manhours.get()
            })
        c.execute(""" INSERT into specific_man_hours (project_number, Welder, Builder, Painter, Engineer, Manager, Fitter)
            VALUES
               (
                        :projectid, 0, 0, 0, 0, 0, 0
                )""",
            {
                "projectid" : project_number.get()
            })

        total_wage.delete(0, END)
        estimated_man_hours.delete(0, END)
        project_number.delete(0, END)
        welder_manhours.delete(0, END)
        builder_manhours.delete(0, END)
        painter_manhours.delete(0, END)
        engineer_manhours.delete(0, END)
        manager_manhours.delete(0, END)
        fitter_manhours.delete(0, END)

        

        # Commit changes
        conn.commit()
        # Close the connection
        conn.close()         
      
    def submit():
        # Connect to database
        conn = sqlite3.connect('iscon.db')
        c = conn.cursor()
        
        c.execute("""UPDATE projects
        SET percentage_completion = :percentagecompletion
        WHERE project_number = :projectNumber""",
        {
            'percentagecompletion' : percentage_completion.get(),
            'projectNumber' : project_number_search.get()
        }
        )

        # Commit changes
        conn.commit()
        # Close the connection
        conn.close() 
        


    # Create text labels
    space_inBetween = Label(projects, text = " ", width = 8, height = 2).grid(column = 0, row = 0)

    project_number_search_label = Label(projects, text = "Project number").grid(column = 0, row = 1)
    project_number_search = Entry(projects)
    project_number_search.grid(column = 1, row = 1)

    percentage_completion_label = Label(projects, text = '               Percentage completion ').grid(column = 0, row = 2)
    percentage_completion = Entry(projects)
    percentage_completion.grid(column = 1, row = 2)

    space_inBetween = Label(projects, text = " ", width = 8, height = 2).grid(column = 0, row = 3)

    search_button = Button(projects, text = "Search", width = 20, height = 2, command = search).grid(column = 0, row = 4)
    submit_button = Button(projects, text = "Submit", width = 20, height = 2, command = submit).grid(column = 1, row = 4)

    space_inBetween = Label(projects, text = " ", width = 8, height = 2).grid(column = 0, row = 5)
    add_new_project_label = Label(projects, text ="    ADD NEW PROJECT  :  ").grid(column = 0, row = 6)
    
    total_wage_label = Label(projects, text = 'Total Wage').grid(column = 0, row = 7)
    total_wage = Entry(projects)
    total_wage.grid(column = 1, row = 7)

    estimated_man_hours_label = Label(projects, text = "Estimated Man Hours").grid(column = 0, row = 8)
    estimated_man_hours = Entry(projects)
    estimated_man_hours.grid(column = 1, row = 8)
    
    project_number_label = Label(projects, text = "Project number").grid(column = 0, row = 9)
    project_number = Entry(projects)
    project_number.grid(column = 1, row = 9)
    space_inBetween = Label(projects, text = " ", width = 8, height = 2).grid(column = 0, row = 10) 
    specific_estimated_man_hours_label = Label(projects, text = '   SPECIFIC ESTIMATED MAN HOURS  :    ').grid(column = 0, row = 11)

    welder_manhours_label = Label(projects, text = 'Welder').grid(column = 0, row = 12)
    welder_manhours = Entry(projects)
    welder_manhours.grid(column = 1, row = 12)

    builder_manhours_label = Label(projects, text = 'Builder').grid(column = 0, row = 13 )
    builder_manhours = Entry(projects)
    builder_manhours.grid(column = 1, row =13 )

    painter_manhours_label = Label(projects, text = 'Painter').grid(column = 0, row =14 )
    painter_manhours = Entry(projects)
    painter_manhours.grid(column = 1, row =14 )   

    engineer_manhours_label = Label(projects, text = 'Engineer').grid(column = 0, row =15 )
    engineer_manhours = Entry(projects)
    engineer_manhours.grid(column = 1, row =15 )

    manager_manhours_label = Label(projects, text = 'Manager').grid(column = 0, row =16 )
    manager_manhours = Entry(projects)
    manager_manhours.grid(column = 1, row =16 )

    fitter_manhours_label = Label(projects, text = 'Fitter').grid(column = 0, row =17 )
    fitter_manhours = Entry(projects)
    fitter_manhours.grid(column = 1, row =17 )

    space_inBetween = Label(projects, text = " ", width = 8, height = 2).grid(column = 0, row = 18)    
    save_button = Button(projects, text = "Save", width = 40, height = 2, command = save).grid(column = 0, row = 19, columnspan=2)   


