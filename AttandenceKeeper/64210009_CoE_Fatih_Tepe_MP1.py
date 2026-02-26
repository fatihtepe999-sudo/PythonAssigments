import tkinter  # I can use tkinter library now
from tkinter import *
from tkinter import ttk  # it helps to use ttk
from tkinter import filedialog  # it helps to use filedialog
import openpyxl  # it helps to use Excel
from nameparser import HumanName
# I learn from internet it helps to detect names and surnames who have two names


# Define the student class
class Student:
    def __init__(self, student_id, name, department, section):
        self.student_id = student_id
        parsed_name = HumanName(name)  # Parse the name into first and last name
        self.name = parsed_name.first
        self.surname = parsed_name.last
        self.department = department
        self.section = section

    # I will use below information outside the class so, I used return.
    def __str__(self):
        return f"{self.surname},{self.name},{self.student_id},{self.department}"


# Define the StudentList class
class StudentList:
    def __init__(self):
        self.students = []  # This is empty because I will append for left_listbox

    # for add student to list
    def add_student(self, student):
        self.students.append(student)

    # if user change section, it will be clear right_listbox
    def clear_students(self):
        self.students.clear()


# Define the GUI class
class GUI:
    def __init__(self, window):
        self.window = window
        self.window.title("tk")  # it is a title for window
        self.window.geometry('600x300')

        self.student_list = StudentList()

        self.create_widgets()

    def create_widgets(self):
        self.title = Label(self.window, text="AttendanceKeeper v1.0", font="Times 15 bold")  # it is a title for app.
        # it's size is 15 and it is bold
        self.title.grid(row=0, column=1)  # I preferred use grid to place.

        # Frames : Frames helps to me for resizing to cells
        self.frame = Frame(self.window)
        self.frame.grid(row=3, column=1, sticky=N)
        self.frame1 = Frame(self.window)
        self.frame1.grid(row=6, column=0)
        self.frame2 = Frame(self.window)
        self.frame2.grid(row=6, column=2)
        ##################################

        # Comboboxs
        self.Which_Section = ttk.Combobox(self.frame, values=[f"AP {i:02}" for i in range(1, 21)])
        #                                                         it helps to short for options
        self.Which_Section.grid(row=0, column=0)
        self.Which_Section.current(0)  # when the program open .txt will show first
        self.filetype = ttk.Combobox(self.frame1, values=[".txt", ".xls", ".csv"])  # these are options for filetype
        self.filetype.grid(row=0, column=1)
        self.filetype.current(0)
        self.filetype.config(width=4)  # set combobox width
        #################################

        # Labels
        self.label1 = Label(self.frame1, text="Please choose file type:", font="Times 9 bold")
        self.label1.grid(row=0, column=0)
        self.label2 = Label(self.window, text="Select student list Excel file:", font="Times 9 bold")
        self.label2.grid(row=1, column=0)
        self.label3 = Label(self.window, text="Select a Student:", font="Times 9 bold")
        self.label3.grid(row=2, column=0)
        self.label4 = Label(self.window, text="Please Enter week:")
        self.label4.grid(row=6, column=1)
        self.label4 = Label(self.window, text="Section", font="Times 9 bold")
        self.label4.grid(row=2, column=1)
        self.label4 = Label(self.window, text="Attended Students", font="Times 9 bold")
        self.label4.grid(row=2, column=2)
        ################################

        # Buttons
        self.button1 = Button(self.window, text="Import List", command=self.import_list_from_excel)
        self.button1.grid(row=1, column=1)
        self.button1.config(width=15)
        self.button2 = Button(self.frame, text="Add=>", command=self.add_student)
        self.button2.grid(row=1, column=0)
        self.button3 = Button(self.frame, text="<=Remove", command=self.remove_student)
        self.button3.grid(row=2, column=0)
        self.button4 = Button(self.frame2, text="Export as File", command=self.export_to_file)
        self.button4.grid(row=0, column=1)
        self.button4.config(width=10)
        ############################

        # Listboxs
        self.left_listbox = Listbox(self.window, selectmode=MULTIPLE)
        self.left_listbox.grid(row=3, column=0)
        self.left_listbox.config(width=29)
        self.right_listbox = Listbox(self.window, selectmode=MULTIPLE)
        self.right_listbox.grid(row=3, column=2, sticky=W)
        self.right_listbox.config(width=29)
        ####################################

        # Entries
        self.entry = Entry(self.frame2)
        self.entry.grid(row=0, column=0)
        self.entry.config(width=15)
        ###############################
        self.Which_Section.bind("<<ComboboxSelected>>", self.filter_students_by_section)

    # top row triggers `self.filter_students_by_section` when a selection is made in `self.Which_Section` Combobox.

    # This function to add item to the right_listbox
    def add_student(self):
        selected_students = self.left_listbox.curselection()
        for index in selected_students[::-1]:   # Get the student at the current index.
            student = self.left_listbox.get(index)  # Insert the student into the right listbox.
            self.right_listbox.insert(tkinter.END, student)
            self.left_listbox.delete(index)  # Delete the student from the left listbox.

    # This function to remove item to the left_listbox
    def remove_student(self):
        selected_students = self.right_listbox.curselection()
        for index in selected_students[::-1]:  # Get the student at the current index.
            student = self.right_listbox.get(index)  # Insert the student into the left listbox.
            self.left_listbox.insert(tkinter.END, student)
            self.right_listbox.delete(index)  # Delete the student from the right listbox.

    def import_list_from_excel(self):  # This function to import student list from an Excel file.
        # Open a file dialog to select an Excel file.
        file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
        if file_path:
            try:
                workbook = openpyxl.load_workbook(file_path)
                sheet = workbook.active  # this helps to find active page from Excel. It is not too important
                # because  we have one page in sample input. When we have more than one page this will be important
                self.student_list.clear_students()
                for row in sheet.iter_rows(min_row=2, values_only=True):  # This line reads through the rows in the
                    # Excel sheet, starting from the second row, and collects only the cell values.
                    student = Student(*row)  # create a class in every loop
                    self.student_list.add_student(student)  # and append students list

                self.filter_students_by_section()  # Filter the students based on the selected section.

            except Exception as e:  # if there is an exception
                print("Error:", e)  # it is an error

    def filter_students_by_section(self, event=None):
        # Clear both listboxes
        self.left_listbox.delete(0, tkinter.END)
        self.right_listbox.delete(0, tkinter.END)
        selected_section = self.Which_Section.get()  # Get the selected section from the combobox
        for student in self.student_list.students:
            if student.section == selected_section:
                self.left_listbox.insert(tkinter.END, str(student))

    # This function is helping export selected students to file
    def export_to_file(self):
        file_type = self.filetype.get()  # Get the selected file type
        selected_section = self.Which_Section.get() # Get the selected section (I will need for filename)
        file_name = f"{selected_section} Week {self.entry.get()}{file_type}"  # it makes automatic for names

        if file_type == ".csv":  # if the selected file type is CSV
            raise Exception("File type is not supported")  # Raise an exception because CSV file type is not supported

        elif file_type == ".xls":  # if the selected file type is XLS
            workbook = openpyxl.Workbook()  # Create a new workbook
            sheet = workbook.active  # Get the active sheet
            sheet.append(["ID", "Name", "Department"])  # Write first lines

            # Set column widths
            sheet.column_dimensions['A'].width = 10  # ID column
            sheet.column_dimensions['B'].width = 20  # Name column
            sheet.column_dimensions['C'].width = 15  # Department column

            for index in range(self.right_listbox.size()):
                student_info = self.right_listbox.get(index)
                surname, name, student_id, department = student_info.split(',')  # This line split from (,) students
                # info because I need them all separately
                sheet.append([student_id, surname + " " + name, department])
            workbook.save(file_name)  # Save the workbook with the generated file name


        elif file_type == ".txt":  # if the selected file type is TXT
            with open(file_name, "w") as file:  # open a file with write mode
                file.write(f"ID        Name                                      Department\n")  # Write the header line
                for index in range(self.right_listbox.size()):
                    student_info = self.right_listbox.get(index)
                    surname, name, student_id, department = student_info.split(',')
                    # Formatting
                    formatted_line = f"{student_id.ljust(10)} {surname.ljust(20)} {name.ljust(20)} {department}\n"
                    file.write(formatted_line)  # Write the formatted line to the file


# Create the main window
window = Tk()
app = GUI(window)
# Make a loop for window
window.mainloop()

# I used these websites for study
# https://jorgepit-14189.medium.com/full-name-parser-with-python-c4edc7f7b0f2
# https://openpyxl.readthedocs.io/en/stable/tutorial.html
# https://www.tutorialspoint.com/combobox-widget-in-python-tkinter
