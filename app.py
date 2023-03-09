from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/contact")
def contact():
    return render_template('contact_us.html')


@app.route("/getstarted")
def getstarted():
    return render_template('getstarted.html')


@app.route("/mental_health_resources")
def mental_health_resources():
    return render_template('mental_health_resources.html')


@app.route("/quiz_intro")
def quiz_intro():
    return render_template('quiz_intro.html')


@app.route("/what_we_do")
def what_we_do():
    return render_template('what_we_do.html')


questions = ["", "", 'Are you a member of the LGBTQ+ community?', 'In the past 6 months, have you used alcohol or drugs to cope with stress or bad moods?', 'Have you or someone close to you struggled to deal with your sexuality?', 'Have you struggled with the expectations and stresses ofentering adulthood?', 'In the past 6 months, have you had trouble sleeping or been sleeping too much?', 'In the past 6 months, have you had less energy/motivation?', 'In the past 6 months, have you had a notable change in appetite? Eating more/less?', 'In the past 6 months, have you felt like a failure or that you have let down others around you?',
             'In the past 6 months, have you often felt down, depressed or hopeless?', 'In the past 6 months, have you suffered an anxiety attack?', 'In the past 6 months, have you felt more irritable or annoyed?', "In the past 6 months, have you felt like you've had no one to turn to?"]


@app.route("/quiz")
def quiz():
    global current_question
    global answers
    global is_young
    global is_question2
    global total_score

    current_question = 1
    answers = list()
    is_young = 0
    is_question2 = ''
    total_score = 0
    return render_template('quiz.html')


@app.route('/result')
def result():
    global answers
    global total_score
    score = answers.count('yes')
    return render_template('result.html', score=score, total_score=total_score)


current_question = 1
answers = list()
is_young = 0
is_question2 = ''
total_score = 0

@app.route('/quiz_main', methods=['POST'])
def quiz_main():
    global current_question
    global answers
    global is_young
    global is_question2
    global total_score

    answer = request.form['radio']

    if current_question == 1:
        is_young = int(answer)

    if current_question == 2:
        is_question2 = answer

    print(answer)

    if current_question >= 4:
        answers.append(answer)
        total_score += 1
    print(current_question, answers)

    if current_question == 3 and is_question2=='no':
        print("q 2=", is_question2, "skip")
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
        return render_template('quiz_main.html', question=questions[current_question], q_number=current_q)


if __name__ == '__main__':
    app.run(debug=True, threaded=True)



