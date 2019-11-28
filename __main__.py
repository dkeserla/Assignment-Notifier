import bs4 as bs
from connection import connect
from connection import get_credentials
from connection import write_updates
from assignments import get_assignments
from flask import Flask, redirect, url_for, render_template

#import the get_assignments method which takes care of getting the grades
from assignments import get_assignments

app = Flask(__name__)

@app.route("/")
def home():
    user_name, pass_word = get_credentials()
    assignments_page = connect(user_name, pass_word)
    assignments = bs.BeautifulSoup(assignments_page.content, 'html5lib')
    class_assignments = get_assignments(assignments)
    return render_template("assignments.html", class_assignments=class_assignments)

# def to_file():
#     user_name, pass_word = get_credentials()
#     assignments_page = connect(user_name, pass_word)
#     assignments = bs.BeautifulSoup(assignments_page.content, 'html5lib')
#     class_assignments = get_assignments(assignments)
#
#     reminders = ''
#     for course in class_assignments:
#         reminders += str(course) + '\n'
#         for assignment in class_assignments[course]:
#             reminders += '\t' + str(assignment)
#             reminders += '\n'
#         reminders += '\n'
#
#     write_updates(reminders)

if __name__ == "__main__":
    app.run(debug=True)
