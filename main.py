from tkinter import *
from PIL import ImageTk, Image
from tkinter import filedialog
from functions import *
import sqlite3


root = Tk()
root.title('Program') 
root.geometry("500x500")


# Connect to Database and create a cursor
conn = sqlite3.connect('iscon.db')
c = conn.cursor()



# Create top buttons
employees_btn = Button(root, text = "Employees", width = 20, height = 2, command = employees_btn).grid(row = 0, column = 0)
designation_btn = Button(root, text = 'Designations', width = 20, height = 2, command = designations_btn).grid(row = 0, column = 1)
project_btn = Button(root, text = 'Projects', width = 20, height = 2, command = projects_btn).grid(row = 0, column = 2)

space_inBetween = Label(root, text = "       ", width = 8, height = 2).grid(row = 1, column = 1)
enter_employee_id_label = Label(root, text = "Enter Employee Number : ", width = 20, height = 2).grid(row = 2, column = 0)
enter_employee_id = Entry(root, width = 20)
enter_employee_id.grid(row = 2, column = 1)
enter_btn = Button(root, text = "Enter", width = 20, height = 1).grid(row = 2, column = 2)

# Create textboxes for top-button tabs  


# Commit changes
conn.commit()  
# Close the connection
conn.close()

root.mainloop()