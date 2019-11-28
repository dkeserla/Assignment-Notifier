import bs4 as bs
import re

def get_assignments(assignments):
    class_assignments_containers = assignments.find_all(attrs={'class': 'AssignmentClass'})
    class_assignments = {}
    for assignment in class_assignments_containers:
        class_string = clean_string(assignment.find_all(attrs={'class': 'sg-header-heading'})[0].text)
        class_grade = assignment.find_all(attrs={'class': 'sg-header-heading sg-right'})[0].text
        class_grade = class_grade[class_grade.rfind(" ")+1:].strip()
        course = Class(class_string, class_grade)
        assigns = assignment.find_all(attrs={'class': 'sg-asp-table-data-row'})
        assignment_data = []
        for assign in assigns:
            list = assign.find_all('a')
            for a in list:
                nums = re.findall('[0-9.]+', str(assign.find_all('td')[4]))
                total = re.findall('[0-9.]+', str(assign.find_all('td')[5]))
                assignment_data.append(Assignment(a.attrs['title'], nums, total))
        class_assignments[course] = assignment_data
    # for course in class_assignments:
    #     print(course)
    #     for assignment in class_assignments[course]:
    #         print('\t' + str(assignment))
    #     print()
    return class_assignments

def clean_string(class_string):
    class_string = class_string.strip()
    number_chars = re.findall('[0-9]+', class_string)
    last_num = number_chars[len(number_chars)-1]
    class_string = class_string[class_string.rfind(last_num)+1:].strip()
    return class_string

class Class:
    name = ''
    grade = ''

    def __init__(self, name, grade):
        self.name = name
        self.grade = grade

    def __str__(self):
        return self.name + " - " + self.grade

class Assignment:
    classwork = ''
    category = ''
    due_date = ''
    grade = ''
    total_points = ''

    def __init__(self, title_vals, grade, total_points):
        self.classwork, self.category, self.due_date = self.parse_elements(title_vals)
        self.grade = 'not put in yet' if len(grade) == 0 else "{:.2f}".format(float(grade[0]))
        self.total_points = "" if self.grade == 'not put in yet' else "{:.2f}".format(float(total_points[0]))

    def parse_elements(self, title_vals):
        assignment_details = []

        for i in range(3):
            title_vals = title_vals[title_vals.index('\n')+1:]
            assignment_details.append(title_vals[title_vals.index(' ')+1: title_vals.index('\n')])

        return assignment_details[0], assignment_details[1], assignment_details[2]

    def __str__(self):
        out = 'classwork is ' + self.classwork + ', category is ' + self.category + ', due date is ' + self.due_date + ', and your grade is ' + self.grade
        return out + "/" + self.total_points if self.total_points != "" else out
