import os
from flask import Flask, render_template, request, redirect, session, url_for, make_response
import sqlite3

app = Flask(__name__)

app.secret_key = os.urandom(24)


#######################
conn = sqlite3.connect('database.db')
c = conn.cursor()

# Create users table if it doesn't exist
c.execute('''CREATE TABLE IF NOT EXISTS users
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              name TEXT NOT NULL,
              email TEXT NOT NULL UNIQUE,
              password TEXT NOT NULL)''')

conn.commit()
conn.close()


######################


@app.route("/home")
def index():
    # Check if user is logged in
    if "user_id" not in session:
        return redirect(url_for('login'))

    return render_template('index.html', user_name=session["user_name"])



@app.route("/contact")
def contact():
    return render_template('contact_us.html')


@app.route("/getstarted")
def getstarted():
    return render_template('getstarted.html')


@app.route("/mental_health_resources")
def mental_health_resources():
    return render_template('mental_health_resources.html')


# @app.route("/login")
# def login():
#     return render_template('login.html')


##############################################
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # Get form data
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        # Connect to database
        conn = sqlite3.connect("database.db")
        c = conn.cursor()

        # Check if email already exists
        c.execute("SELECT * FROM users WHERE email=?", (email,))
        user = c.fetchone()
        if user:
            conn.close()
            return render_template('login.html', class_f= 'right-panel-active', display = 'block')

        # Insert user into database
        c.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
                  (name, email, password))
        conn.commit()
        conn.close()

        return redirect(url_for('login'))

    return render_template("login.html")


@app.route("/", methods=["GET", "POST"])
def login():
    #  Check if user is logged in
    if "user_id" in session:
        return redirect(url_for('index'))

    if request.method == "POST":
        # Get form data
        email = request.form["email"]
        password = request.form["password"]

        # Connect to database
        conn = sqlite3.connect("database.db")
        c = conn.cursor()

        # Check if email and password match
        c.execute("SELECT * FROM users WHERE email=? AND password=?", (email, password))
        user = c.fetchone()
        if not user:
           return render_template('login.html', display='block')

        # Store user data in session
        session["user_id"] = user[0]
        session["user_name"] = user[1]

        conn.close()

        return redirect(url_for('index'))

    return render_template("login.html")


@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return redirect(url_for('login'))

######################################


@app.route("/assessment")
def quiz_intro():
    return render_template('quiz_intro.html')


@app.route("/what_we_do")
def what_we_do():
    return render_template('what_we_do.html')


questions = ["", "", 'Are you a member of the LGBTQ+ community?', 'In the past 6 months, have you used alcohol or drugs to cope with stress or bad moods?', 'Have you or someone close to you struggled to deal with your sexuality?', 'Have you struggled with the expectations and stresses of entering adulthood?', 'In the past 6 months, have you had trouble sleeping or been sleeping too much?', 'In the past 6 months, have you had less energy/motivation?', 'In the past 6 months, have you had a notable change in appetite? Eating more/less?', 'In the past 6 months, have you felt like a failure or that you have let down others around you?',
             'In the past 6 months, have you often felt down, depressed or hopeless?', 'In the past 6 months, have you suffered an anxiety attack?', 'In the past 6 months, have you felt more irritable or annoyed?', "In the past 6 months, have you felt like you've had no one to turn to?"]


@app.route("/quiz")
def quiz():
    global current_question
    global answers
    global is_young
    global q2_ans
    global total_score
    global q3_ans
    global q4_ans

    current_question = 1
    answers = list()
    is_young = 0
    q2_ans = ''
    total_score = 0
    q4_ans = None
    q3_ans = None
    return render_template('quiz.html')


@app.route('/result')
def result():
    global answers
    global total_score
    global result_txt

    nhs_support = None
    sex_support = None
    abuse_support = None

    responses_set = ["From the responses you've given to the questions, there is no indication of mental illness. Please note that these questions do not cover all issues and if you have any more doubts please contact a health professional.",
                     "From the responses you've given to the questions, it is possible that you may be suffering with a mental health illness. For more information please have a look at the following resources or contact a health professional.",
                     "From the responses you have given to the questions it is extremely likely you are suffering from a mental health illness. We have provided a list of resources below which will help you on your journey, specifically picked for you based on your responses."]

    score = answers.count('yes')

    if score <= 3:
        result_txt = responses_set[0] 

    elif score >= 6:
        result_txt = responses_set[2]
        nhs_support = 'block'
        if q4_ans == 'yes':
            sex_support = 'block'
        if q3_ans == 'yes':
            abuse_support = 'block' 

    else:   # for 4 or 5 score
        result_txt = responses_set[1] 

        nhs_support = 'block'
        if q4_ans == 'yes':
            sex_support = 'block'
        if q3_ans == 'yes':
            abuse_support = 'block' 

    return render_template('result.html', score=score, total_score=total_score, result_text=result_txt, nhs_support=nhs_support, sex_support=sex_support, abuse_support=abuse_support)


current_question = 1
answers = list()
is_young = 0
q2_ans = ''
total_score = 0
q4_ans = None
q3_ans = None


@app.route('/quiz_main', methods=['POST', 'GET'])
def quiz_main():
    global current_question
    global answers
    global is_young
    global q2_ans
    global total_score
    global q3_ans
    global q4_ans
  

    if request.method == 'POST':
        answer = request.form['radio']

        if current_question == 1:
            is_young = int(answer)

        if current_question == 2:
            q2_ans = answer

        # store the ans
        if current_question >= 4:
            answers.append(answer)
            total_score += 1

        if current_question == 3:
            q3_ans = answer

        if current_question == 4 and q2_ans == 'yes':
            q4_ans = answer

        print(answers, q3_ans, q4_ans)

        if current_question == 3 and q2_ans == 'no':
            if not is_young:
                current_question += 3
            else:
                current_question += 2
        elif current_question == 4 and not is_young:
            current_question += 2
        else:
            current_question += 1

        if current_question < 4:
            current_q = current_question
        else:
            current_q = 4 + total_score

        if current_question == len(questions):
            return redirect(url_for('result'))
        else:
            session['question'] = questions[current_question]
            session['q_number'] = current_q

            return redirect(f'/quiz_main')

    else:
        if current_question < 4:
            current_q = current_question
        else:
            current_q = 4 + total_score

        return render_template('quiz_main.html', question=questions[current_question], q_number=current_q)



if __name__ == '__main__':
    app.run(threaded=True, debug=True)



