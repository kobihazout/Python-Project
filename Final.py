#import os
import random
import matplotlib
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import pickle
import warnings
warnings.filterwarnings("ignore", category=RuntimeWarning)
import datetime

global Max_Capacity
Max_Capacity = 30
CONST_COLO = 6
CONST_INCOME = 6000
CONST_EXPENSES = 3500

def main():
    try:
        answer = 999
############# MAIN MENU - employees / courses / KPI SHOW ###########################################################
        print('Welcome to John Bryce by MATRIX')
        ans = int(input('To Manage employees press 1--->\n'
                        'To Manage a courses press 2--->\n'
                        'To KPI press 3--->\n'
                        'To EXIT press 0--->\n'))
######################## Employees Management menu ###############################################################
        while ans != 0:
            if ans == 1:
                answer = 999
                while answer != 0:
                    print('Welcome to Employees Management menu')
                    answer = int(input('To Add Employee press 1--->\n'
                                        'To Delete Employee from the lists press 2--->\n'
                                        'To Search for Employee press 3--->\n'
                                        'To Update a Employee Age press 4--->\n'
                                        'To Change Password press 5--->\n'
                                        'To Show all Employees Details press 6--->\n'
                                        'To Change Phone Number Press 7--->\n'
                                        'To Main menu press 0--->\n'))
                    if answer == 1:
                        AddEmployee()
                    if answer == 2:
                        DeleteEmployee()
                    if answer == 3:
                        SearchEmployee()
                    if answer == 4:
                        UpdateAge()
                    if answer == 5:
                        ChangePassword()
                    if answer == 6:
                        ShowAllEmployees()
                    if answer == 7:
                        UpdatePhoneNumber()
######################## Courses Management menu ###############################################################
            if ans == 2:
                answer = 999
                while answer != 0:
                    print('Welcome to Courses Management menu')
                    answer = int(input('To Add course press 1--->\n'
                                        'To Delete course press 2--->\n'
                                        'To Search course press 3--->\n'
                                        'To Show all Courses Details press 4--->\n'
                                        'To Update Capacity press 5--->\n'
                                        'To Main menu press 0--->\n'))
                    if answer == 2:
                        DeleteCourse()
                    if answer == 1:
                        AddCourse()
                    if answer == 3:
                        SearchCourse()
                    if answer == 4:
                        ShowAllCourses()
                    if answer == 5:
                        UpdateCapacity()
######################## KPI Management menu ######################################################################
            if ans == 3:
                answer = 999
                while answer != 0:
                    print('Welcome to KPI menu')
                    answer = int(input('To Show KPI press 1--->\n'
                                       'To Main menu press 0--->\n'))
                    if answer == 1:
                        RevenueGraph()
                        Graph_Capacity()
                        Graph_CourseCapacity()
                        EmployeeGenderGraph()
            ans = int(input('To Manage employees press 1--->\n'
                            'To Manage a courses press 2--->\n'
                            'To KPI press 3--->\n'
                            'To EXIT press 0--->\n'))
    except ValueError:
        print('Please enter only numbers' + '\n')

def CalculateIncomeAndExpensesByYear(num):
    num_of_courses = int(NumOfcourses() / 4)  # /4 give us the number of courses
    zumzum = BuildDict()
    dicts = [{'income': {}, 'month': {}, 'expenses': {}} for k in range(12)]
    for i in range(0, 12):
        dicts[i]['month'] = i + 1
    for i in range(num_of_courses):
        str1 = str(zumzum[i]['course date'])
        year = " "
        for index in range(0, 4):
            year = str(year) + str(str1[index])
        year = int(year)
        if year == num:
            month = " "
            for index in range(5, 7):
                month = str(month) + str(str1[index])
            dicts[int(month)-1]['income'] = int(zumzum[i]['course capacity']) * CONST_INCOME
            dicts[int(month)-1]['expenses'] = int(zumzum[i]['course capacity']) * CONST_EXPENSES
    file = open('important.dat', 'wb')
    pickle.dump(dicts, file)
    file.close()

def CountMaleAndFemale():
    zumzum = Buildmatrix()
    countM = 0
    num_of_employee = int(NumOfEmployee() / 6)  # /6 give us the number of employee
    if num_of_employee == 0:  # if the #employee.txt is empty but exist, no one to edit
        print("Please add employee first")
        return 0
    for i in range(0,num_of_employee):
        if zumzum[i][2] == "Male":
            countM = countM+1
    return countM

def EmployeeGenderGraph():    # https://www.datapine.com/kpi-examples-and-templates/human-resources#female-to-male-ratio
    countM = CountMaleAndFemale()
    countF =int(NumOfEmployee()/6)
    countF = countF - countM
    counts = (countM, countF)
    labels = ('Males', 'Females')
    plt.pie(counts, labels=labels, autopct="%0.2f%%", explode=[0, 0.1], startangle=90)
    plt.title("Female to male KPI",fontsize = 18)
    plt.show()

def RevenueGraph():       #https://www.datapine.com/kpi-examples-and-templates/customer-service#support-costs-vs-revenue
    try:
        num_of_courses = int(NumOfcourses() / 4)  # /4 give us the number of courses
        if num_of_courses == 0:  # if the #courses.txt is empty but exist
            print("Please add courses first")
            return 0
        year = int(input("Please Enter a year to Calculate Income And Expenses--->"))
        if year < 2003 or year > 2019:
            print("Income and Expenses Reports can only be generated from 2003. Please try again")
            return
        CalculateIncomeAndExpensesByYear(year)
        file = open('important.dat', 'rb')
        dicts = pickle.load(file)
        file.close()
        income = [0]*12
        expenses = [0]*12
        for i in range(0, 12):
            if dicts[i]['income'] == {}:
                dicts[i]['income'] = 0
                dicts[i]['expenses'] = 0
            income[i] = int(dicts[i]['income'])
            expenses[i] = int(dicts[i]['expenses'])
        df = pd.DataFrame({'Month': range(1, 13), 'Income': income, 'Expenses': expenses})
        plt.plot('Month', 'Income', data=df, marker='o', markerfacecolor='blue', markersize=12, color='skyblue', linewidth=4)
        plt.plot('Month', 'Expenses', data=df, marker='', color='red', linewidth=2)
        plt.xlabel("Month",fontsize=12)
        plt.ylabel("Amount", fontsize=12)
        plt.title("Income and Expenses KPI for: "+str(year), fontsize=15, fontweight=0, color='green')
        plt.legend()
        plt.show()
    except ValueError:
        print('Please enter only numbers.' + '\n')

def Graph_Capacity():       #https://www.slideteam.net/project-status-kpi-dashboard-showing-performance-and-resource-capacity.html
    num_of_courses = int(NumOfcourses() / 4)  # /4 give us the number of courses
    if num_of_courses == 0:  # if the #courses.txt is empty but exist,
        print("Please add employee first")
        return 0
    num = int(input("Please Enter a year to View Capacity--->"))
    if num < 2003 or num > 2019:
        print("Income and Expenses Reports can only be generated from 2003. Please try again")
        return
    zumzum = BuildDict()
    couresnames = []
    couresescapacity = []
    dicts = [{'month': {}} for k in range(12)]
    for i in range(0, 12):
        dicts[i]['month'] = i + 1
    for i in range(num_of_courses):
        str1 = str(zumzum[i]['course date'])
        year = " "
        for index in range(0, 4):
            year = str(year) + str(str1[index])
        year = int(year)
        if year == num:
            month = " "
            for index in range(5, 7):
                month = str(month) + str(str1[index])
            couresnames.append(zumzum[i]['course name'])
            couresescapacity.append(int(zumzum[i]['course capacity']))
    barWidth = 0.2
    bars1 = [Max_Capacity] * len(couresnames)
    r1 = np.arange(len(couresnames))
    r2 = [x + barWidth for x in r1]
    plt.bar(r1, bars1, width=barWidth, color='blue', edgecolor='black', capsize=7, label='Max capacity')
    plt.bar(r2, couresescapacity, width=barWidth, color='cyan', edgecolor='black', capsize=7, label='Course capacity')
    plt.xticks([r + barWidth for r in range(len(couresnames))], couresnames, fontsize=4.7)
    plt.title("Capacity by courses for: " + str(num), fontsize=15, fontweight=0, color='green')
    plt.ylabel('Capacity of courses', fontsize=15)
    plt.xlabel("Name of courses", fontsize=15)
    plt.legend()
    plt.show()

def Graph_CourseCapacity():     #https://www.slideteam.net/project-status-kpi-dashboard-showing-performance-and-resource-capacity.html
    num_of_courses = int(NumOfcourses() / 4)  # /4 give us the number of courses
    if num_of_courses == 0:  # if the #employee.txt is empty but exist, no one to edit
        print("Please add employee first")
        return 0
    num = int(NumOfcourses()/4)
    zumzum = BuildDict()
    totalcapacity = num*Max_Capacity
    current_capacity = 0
    for index in range(0, num):
        current_capacity = current_capacity + int(zumzum[index]['course capacity'])
    num1 = float(current_capacity/totalcapacity)*100
    num1 = int(num1)
    num2 = 100-num1
    courselist=[num1, num2]
    course_labels = ['Taken: '+str(num1)+'%', 'Free: '+str(num2)+'%']
    plt.pie(courselist, labels=course_labels, colors=('r', 'b'))
    plt.title('Capacity in all courses')
    plt.show()      #https://www.slideteam.net/project-status-kpi-dashboard-showing-performance-and-resource-capacity.html
#######################################
def NumOfcourses():      #count the number of lines in the file text
    id = open('courses.txt', 'r')
    line = id.readline()
    count = 0
    while line != '':
        count += 1
        line = id.readline()
    id.close()
    return count

def NumOfEmployee():      #count the number of lines in the file text
    id = open('employee.txt', 'r')
    line = id.readline()
    count = 0
    while line != '':
        count += 1
        line = id.readline()
    id.close()
    return count        #count/6 give us the number of employee

def Buildmatrix():
    try:
        ROWS = int(NumOfEmployee() / 6)
        zumzum = [[0 for x in range(CONST_COLO)] for y in range(ROWS)] # נגדיר מטריצה
        temp = open('employee.txt', 'r+')
        line = temp.readline()
        line = line.rstrip('\n')
        for r in range(ROWS):
            for c in range(CONST_COLO):
                zumzum[r][c] = line
                line = temp.readline()
                line = line.rstrip('\n')
        temp.close()
        return zumzum
    except FileNotFoundError:
        print("File does not exist, add employee first")

def CreatePassword(id):
    id = int(id)
    id = int(id/100)
    id = str(id)
    password = id+str(random.randint(1000, 9999))
    return password

def Chage(num):
    #func check that age
    count = 0
    num = int(num)
    if num < 18:
        print("Invalid Age, Please try again with only between 18-80")
        return False
    if num > 80:
        print("Invalid Age, Please try again with only between 18-80")
        return False
    while num != 0:
        num = int(num / 10)
        count = count + 1
    if count == 2:
        return True
    else:
        print("Invalid Age, Please try again with only between 18-80")
        return False

def BuildDict():
    try:
        ROWS = int(NumOfcourses()/4)
        array = [0] * 4
        dicts = [{'course name': {}, 'course id': {}, 'course capacity': {}, 'course date': {}} for k in range(ROWS)]
        temp = open('courses.txt', 'r+')
        line = temp.readline()
        line = line.rstrip('\n')
        for i in range(ROWS):
            for c in range(4):
                array[c] = line
                line = temp.readline()
                line = line.rstrip('\n')
            dicts[i] = {'course name': array[0], 'course id': array[1], 'course capacity': array[2], 'course date': array[3]}
        temp.close()
        return dicts
    except FileNotFoundError:
        print("File does not exist, add course first")

def CheckPhonenumber(num):
    #func check that phone number include 10 digits
    count = 0
    while num >= 10:
        count = count + 1
        num = int(num) / 10
        num = int(num)
    if count == 8 and num == 5:
        return True
    else:
        print("Invalid Phone Number, Please try again with only 10 digits, 05XXXXXXXX")
        return False

def CheckID(num):
    #func check that employee include 5 digits
    count = 0
    while num != 0:
        count = count + 1
        num = int(num) / 10
        num = int(num)
    if count == 5:
        return True
    else:
        print("Invalid Employee ID, Please try again with only 5 digits")
        return False

def CheckFullName(str):
    if str.replace(" ", "").isalpha():
        return True
    else:
        print("please enter only letters")
        return False

def checkEmploDuplicated(num):
    zumzum = Buildmatrix()
    num = int(num)
    count = int(NumOfEmployee() / 6)
    for i in range(0,count):
        if num == int(zumzum[i][0]):
            return False
    return True

def checkcourseduplicated(num):
    zumzum = BuildDict()
    num = int(num)
    num_of_courses = int(NumOfcourses() / 4)
    for i in range(0,num_of_courses):
        if num == int(zumzum[i]["course id"]):
            return False
    return True

def Gender():
    try:
        ans = 0
        while ans != 1 and ans != 2:
            ans = input("Please choose Gender\n"
                        "For Female Press 1--->\n"
                        "For Male Press 2--->\n")
            ans = int(ans)
            if ans == 1:
                temp = "Female"
            elif ans == 2:
                temp = "Male"
            if ans == 1 or ans == 2:
                return temp
    except ValueError:
        print('Please Enter only numbers 1 or 2' + '\n')

def CheckCourseID(num):
    temp = int(num)
    count = 0
    while temp != 0:
        count = count+1
        temp = temp/10
        temp = int(temp)
    if count == 4:
        return True
    else:
        return False

def CheckCapacity(num):
    num = int(num)
    if num <= Max_Capacity and num >= 0:
        return True
    else:
        print("Invalid Capacity Course, Please try again capacity between 0-30")
        return False
#################################
def ChangePassword():
    try:
        chID = False
        num_of_employee = int(NumOfEmployee() / 6)  # /6 give us the number of employee
        if num_of_employee == 0:        # if the #employee.txt is empty but exist, no one to edit
            print("Please add employee first")
            return 0
        print("Welcome to Change Password for Employee")
        employee_id = input("Please Enter employee ID for Change Password ---> ")
        x = int(employee_id)
        zumzum = Buildmatrix()
        chID = CheckID(employee_id)
        if chID == True:
            for index in range(0, num_of_employee):
                if zumzum[index][0] == employee_id:
                    temp = CreatePassword(employee_id)
                    zumzum[index][5] = temp
            num_of_employee = int(NumOfEmployee()/6)     #כתיבה של כל הנתונים בקובץ לאחר שינוי סיסמא
            id = open('employee.txt', 'w')
            for items in range(0, num_of_employee):
                for line in range(0, CONST_COLO):
                    id.write(zumzum[items][line] + '\n')
            id.close()
            print('The Password has been changed successfully!')
            print("Employee ID is: ", employee_id,"The Password is:",temp)
        else:
            print('Invalid ID')
    except FileNotFoundError:
        print("File does not exist, Please add employee first")

def UpdatePhoneNumber():
    try:
        Flag = False
        chID = False
        num_of_employee = int(NumOfEmployee() / 6)  # /6 give us the number of employee
        if num_of_employee == 0:        # if the #employee.txt is empty but exist, no one to edit
            print("Please add employee first")
            return 0
        print("Welcome To Update Phone number for Employee")
        employee_id = input("Please Enter employee ID for Update Phone Number ---> ")
        x = int(employee_id)
        zumzum = Buildmatrix()
        chID = CheckID(employee_id)
        if chID == True:
            for index in range(0, num_of_employee):
                if zumzum[index][0] == employee_id:
                    num = int(input("Please Enter New Phone Number--->"))
                    temp = CheckPhonenumber(num)
                    if temp == True:
                        Flag = True
                        zumzum[index][3] = '0' + str(num)
                    else:
                        num = int(input("Please Enter New Phone Number--->"))
                        temp = CheckPhonenumber(num)
                        if temp == True:
                            zumzum[index][3] = '0' + str(num)
                            Flag = True
            if Flag == True:
                num_of_employee = int(NumOfEmployee()/6)     #כתיבה של כל הנתונים בקובץ לאחר שינוי גיל
                id = open('employee.txt', 'w')
                for items in range(0, num_of_employee):
                    for line in range(0, CONST_COLO):
                        id.write(zumzum[items][line] + '\n')
                id.close()
                print('The Phone Number has been changed successfully!')
            else:
                print('Invalid ID')
        else:
            return
    except FileNotFoundError:
        print("File does not exist, Please add employee first")

def UpdateAge():
    try:
        Flag = False
        chID = False
        num_of_employee = int(NumOfEmployee() / 6)  # /6 give us the number of employee
        if num_of_employee == 0:        # if the #employee.txt is empty but exist, no one to edit his
            print("Please add employee first")
            return 0
        print("Welcome To Update Age for Employee")
        employee_id = input("Please Enter employee ID for Change Age ---> ")
        x = int(employee_id)
        zumzum = Buildmatrix()
        chID = CheckID(employee_id)
        if chID == True:
            for index in range(0, num_of_employee):
                if zumzum[index][0] == employee_id:
                    age = input("Please Enter New Age--->")
                    temp = Chage(age)
                    if temp == True:
                        Flag = True
                        zumzum[index][4] = age
                    else:
                        age = input("Please Enter New Age--->")
                        temp = Chage(age)
                        if temp == True:
                            zumzum[index][4] = age
                            Flag = True
            if Flag == True:
                num_of_employee = int(NumOfEmployee()/6)     #כתיבה של כל הנתונים בקובץ לאחר שינוי גיל
                id = open('employee.txt', 'w')
                for items in range(0, num_of_employee):
                    for line in range(0, CONST_COLO):
                        id.write(zumzum[items][line] + '\n')
                id.close()
                print('The Age has been changed successfully!')
            else:
                print('Invalid ID')
        else:
            return
    except FileNotFoundError:
        print("File does not exist, Please add employee first")

def AddEmployee():        #add employee to file text
    ans = 1
    zumzum = Buildmatrix()
    i = 1
    z = 0
    chID = False
    chPN = False
    chFN = False
    Flag = False
    try:
        print("welcome to Add Employees")
        id = open('employee.txt', 'a+')
        num_of_employee = int(NumOfEmployee() / 6)  # 6 give us the number of employee
        while ans != 0:
            print("Current number of employee: ", z+num_of_employee)
            print('Enter details employee number: ', i+num_of_employee)
            i = i + 1
            z = z + 1
            employee_id = input('Please enter ID number---> ')
            x = int(employee_id)
            chID = CheckID(employee_id)
            Flag = checkEmploDuplicated(x)
            if Flag == False:
                print("Employee ID exist")
                break
            else:
                Flag = True
            chage = False
            if chID == True:
                chID = True
            else:
                break
            fullname = input('Please Enter Full Name--->')
            chFN = CheckFullName(fullname)
            if chFN == True:
                chFN == True
            else:
                break
            gender = Gender()
            gender = str(gender)
            age = input("Please enter your Age--->")
            x = int(age)
            chage = Chage(age)
            if chage == True:
                chage == True
            else:
                break
            phone_number = input('Please enter phone number---> ')
            x = int(phone_number)
            chPN = CheckPhonenumber(x)
            if chPN == True:
                chPN == True
            else:
                break
            password = CreatePassword(employee_id)
            print("Welcome ", fullname, " your employee ID is: ", employee_id,"The Password is:", password)
            newrow = [employee_id, fullname, gender, phone_number, age, password]
            zumzum = [zumzum, newrow]
            ans = int(input('To continue adding persons please press 1. for exit press 0. ---> '))
            for items in newrow:
                id.write(items+'\n')
        id.close()
    except IOError:
        print('Error occurred while trying to read the source file. THE FILE JUST CREATED.')
        num_of_employee = 0
    except ValueError:
        print('Please enter only numbers.' + '\n')

def DeleteEmployee(): #delete func, input ID number and the func delete all the details about the the employee
    try:
        Flag = False
        chID = False
        num_of_employee = int(NumOfEmployee() / 6)           # /6 give us the number of employee
        if num_of_employee == 0:                           # if the 'employee.txt' is empty but exist, no one to delete
            print("Please add employee first")
            return 0
        print("Welcome to Delete Employee")
        id_num1 = input("Enter employee ID to delete from the list---> ")
        x = int(id_num1)
        chID = CheckID(id_num1)
        zumzum = Buildmatrix()
        if chID == True:
            for index in range(0, num_of_employee):
                    if zumzum[index][0] == id_num1:
                        zumzum.remove(zumzum[index])
                        Flag = True
                        break
            if Flag == True:
                num_of_employee = num_of_employee-1
                id = open('employee.txt', 'w')
                for items in range(0, num_of_employee):
                    for line in range(0, CONST_COLO):
                        id.write(zumzum[items][line] + '\n')
                id.close()
                print('The Employee has been removed from the list successfully.')
            else:
                print('ID Employee doesnt exist in list')                    # if the ID doesnt exist in the 'employee.txt'
        else:
            return                  # ID number under 9 digits
    except ValueError:
        print('Please enter numbers only' + '\n')
    except FileNotFoundError:
        print("File does not exist, add employee first")

def SearchEmployee():       #search func with id--->bring the phone number    עבר בדיקה
    try:
        flag = False
        chID = False
        temp = open('employee.txt', 'r')
        num_of_employee = int(NumOfEmployee() / 6)  # /6 give us the number of employee
        if num_of_employee == 0: # if the employee.txt is empty but exist, no one to delete
            print("Please add employee first")
            return 0
        employee_id = input("Enter employee id for search ---> ")
        x = int(employee_id)
        zumzum = Buildmatrix()
        num = int(NumOfEmployee()/6)
        chID = CheckID(employee_id)
        if chID == True:
            print("Welcome to Employees search")
            for index in range(0, num):
                if zumzum[index][0] == employee_id:
                    flag = True
                    break
            if flag == False:
                print("Employee ID not found")
            else:
                print("Phone number --->", zumzum[index][3])
        else:
            return
        temp.close()
    except ValueError:
        print('Please enter only numbers' + '\n')
    except FileNotFoundError:
        print("File wansn't found, New file just created")
        id = open('employee.txt', 'w')
        id.close()

def ShowAllEmployees():
    try:
        temp = open('employee.txt', 'r')
        num_of_employee = int(NumOfEmployee() / 6)          # /6 give us the number of employee
        if num_of_employee == 0:                            # if the employee.txt is empty but exist, no one to delete
            print("Please add employee first")
            return 0
        zumzum = Buildmatrix()
        print(" Welcome to Details of Employees")
        for index in range(0, num_of_employee):
            print("Employee ID:", zumzum[index][0],"Name:", zumzum[index][1],"Gender:",zumzum[index][2],"Phone Number:", zumzum[index][3],"Age:", zumzum[index][4],"Password:", zumzum[index][5])
        temp.close()
    except FileNotFoundError:
        print("File wansn't found, New file just created")
        id = open('employee.txt', 'w')
        id.close()
####################################
def AddCourse():
    try:
        i = 1
        z = 0
        ans = 1
        print("Welcome to add Course")
        id = open('courses.txt', 'a+')
        num_of_courses = int(NumOfcourses()/4)
        while ans != 0:
            capacity_flag = False
            Flag2 = False
            Flag = False
            Flag3 = False
            print("Current number of courses: ", z + num_of_courses)
            print('Enter details course number: ', i + num_of_courses)
            i = i + 1
            z = z + 1
            while Flag == False:
                course_name = input("Please Enter course name--->")
                Flag = CheckFullName(course_name)
            year = int(input('Enter a year--->'))
            while year < 2003 and year > 2022:
                if year < 2003 and year > 2022:
                    print("Details can be entered afterwards, but from 2003, Date of purchase of John Bryce by MATRIX, try again")
                    year = int(input('Enter a year--->'))
            month = int(input('Enter a month--->'))
            while month < 1 or month > 12:
                if month < 1 or month > 12:
                    print("Please try again with MONTH between 1-12")
                    month = int(input('Enter a month--->'))
            date1 = datetime.date(year, month, 1)
            while capacity_flag == False:
                course_capacity = int(input("Please Enter course capacity ( 30 Max) --->"))
                capacity_flag = CheckCapacity(course_capacity)
            while Flag2 == False or Flag3 == False:
                course_id = input("Please Enter course id ( 4 Digits )--->")
                Flag3 = checkcourseduplicated(course_id)
                if Flag3 == False:
                    print("Course ID exist")
                Flag2 = CheckCourseID(course_id)
            dicts = {'course name': course_name, 'course id': course_id, 'course capacity': course_capacity, 'course date': date1}
            print("Welcome ", course_name, " your course ID is: ", course_id, "date:", date1)
            ans = int(input('To continue adding course please press 1. for exit press 0. ---> '))
            for items in dicts.values():
                items = str(items)
                id.write(items + '\n')
        id.close()
    except IOError:
        print('Error occurred while trying to read the source file. THE FILE JUST CREATED.')
        num_of_courses = 0
    except ValueError:
        print('Please enter only numbers.' + '\n', 'Month only between 1-12')

def DeleteCourse():
    try:
        Flag = False
        Flag2 = False
        num_of_courses = int(NumOfcourses()/4)           # /4 give us the number of courses
        if num_of_courses == 0:                           # if the 'courses.txt' is empty but exist, no one to delete
            print("Please add Course first")
            return 0
        print("Welcome to Delete Course")
        course_id = input("Enter Course ID to delete from the list ---> ")
        x = int(course_id)
        Flag2 = CheckCourseID(course_id)
        dicts = BuildDict()
        if Flag2 == True:
            for index in range(0, num_of_courses):
                if dicts[index]['course id'] == course_id:
                        dicts.remove(dicts[index])
                        Flag = True
                        break
            if Flag == True:
                num_of_courses = num_of_courses-1
                id = open('courses.txt', 'w')
                for index in range(0, num_of_courses):
                    for items in dicts[index].values():
                        id.write(items + '\n')
                id.close()
                print('The course has been removed from the list successfully.')
            else:
                print('Course ID doesnt exist in list')                    # if the ID doesnt exist in the 'courses.txt'
        else:
            return                  # Course ID != 4
    except ValueError:
        print('Please enter numbers only')
    except FileNotFoundError:
        print("File does not exist, add course first")

def SearchCourse():
    try:
        flag = False
        Flag2 = False
        temp = open('courses.txt', 'r')
        num_of_courses = int(NumOfcourses() / 4)    # /4 give us the number of courses
        if num_of_courses == 0:                     # if the courses.txt is empty but exist, no one to delete
            print("Please add course first")
            return 0
        course_id = input("Enter course ID for search ---> ")
        x = int(course_id)
        dicts = BuildDict()
        num = int(NumOfcourses() / 4)
        Flag2 = CheckCourseID(course_id)
        if Flag2 == True:
            print("Welcome to Course search")
            count = int(NumOfEmployee())
            for index in range(0, num):
                if dicts[index]['course id'] == course_id:
                    flag = True
                    break
            if flag == False:
                print("Course ID not found")
            else:
                print("Course:", dicts[index]['course name'], ",the capacity is: ", dicts[index]['course capacity'], ",Date:", dicts[index]['course date'])
        else:
            return          # Course ID != 4
            temp.close()
    except ValueError:
        print('Please enter only numbers' + '\n')
    except FileNotFoundError:
        print("File wansn't found, New file just created")
        id = open('courses.txt', 'w')
        id.close()

def ShowAllCourses():
    try:
        temp = open('courses.txt', 'r')
        num_of_courses = int(NumOfcourses() / 4)        # /4 give us the number of course
        if num_of_courses == 0:                         # if the course.txt is empty but exist, no one to delete
            print("Please add course first")
            return 0
        dicts = BuildDict()
        print("Welcome to Details of Courses")
        for index in range(0, num_of_courses):
            print("Course ID:", dicts[index]['course id'], ",Course Name:", dicts[index]['course name'], ",Capacity:", dicts[index]['course capacity'], ",Date:", dicts[index]['course date'])
        temp.close()
    except FileNotFoundError:
        print("File wansn't found, New file just created")
        id = open('courses.txt', 'w')
        id.close()

def UpdateCapacity():
    try:
        Flag = False
        Flag2 = False
        num_of_courses = int(NumOfcourses() / 4)  # /4 give us the number of courses
        if num_of_courses == 0:  # if the 'courses.txt' is empty but exist, no one to delete
            print("Please add Course first")
            return 0
        print("Welcome to Update capacity Course")
        course_id = input("Enter Course ID to update capacity---> ")
        x = int(course_id)
        Flag2 = CheckCourseID(course_id)
        newcapacity = input("Please enter New capacity--->")
        Flag = CheckCapacity(newcapacity)
        if Flag == False:
            return
        dicts = BuildDict()
        if Flag2 == True:
            for index in range(0, num_of_courses):
                if dicts[index]['course id'] == course_id:
                        dicts[index]['course capacity'] = newcapacity
            if Flag == True:
                id = open('courses.txt', 'w')
                for index in range(0, num_of_courses):
                    for items in dicts[index].values():
                        id.write(items + '\n')
                id.close()
                print('Capacity course has been updated successfully.')
            else:
                print('Course ID doesnt exist in list')  # if the ID doesnt exist in the 'courses.txt'
        else:
            return  # Course ID != 4
    except ValueError:
        print('Please enter numbers only')
    except FileNotFoundError:
        print("File does not exist, add course first")

main()
