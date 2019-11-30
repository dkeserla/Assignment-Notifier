import bs4 as bs
from login import LoginForm
from connection import connect
from connection import get_credentials
from connection import write_updates
from assignments import get_assignments
from flask import Flask, redirect, url_for, render_template, request

#import the get_assignments method which takes care of getting the grades
from assignments import get_assignments

app = Flask(__name__)
app.config['SECRET_KEY'] = '4faca30a9332cb43549666c4d9b7052f'

@app.route("/", methods = ['GET', 'POST'])
def home():
    form = LoginForm()
    if form.validate_on_submit():
            return redirect(url_for('assignments'))
    return render_template('form.html', title= "Login", form=form)


# ImmutableMultiDict([('csrf_token', 'ImZlYzViN2QyNmY4OWM5NjNkODUyMzYyNGEyZWIwNzI0ODU4MWNjNmUi.XeHYAA.zrF95d0d3GwNjrQxQ8K_pRKdc_U'), ('email', 'dinesh.keserla49@k12.leanderisd.org'), ('password', 'Dinesh21'), ('submit', 'Login')])
@app.route("/assignments", methods = ['POST'])
def assignments():
    if request.method == 'POST':
        result = request.form
        assignments_page = connect(result['email'], result['password'])
        assignments = bs.BeautifulSoup(assignments_page.content, 'html5lib')
        class_assignments = get_assignments(assignments)
        return render_template("assignments.html", title="Assignment", class_assignments=class_assignments)
    else:
        return render_template("assignments.html", title="Assignment", class_assignments={})

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
