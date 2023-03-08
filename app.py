from flask import Flask, render_template, request

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


questions = ['Are you a member of the LGBTQ+ community?', 'In the past 6 months, have you used alcohol or drugs to cope with stress or bad moods?', 'Have you or someone close to you struggled to deal with your sexuality?', 'Have you struggled with the expectations and stresses ofentering adulthood?', 'In the past 6 months, have you had trouble sleeping or been sleeping too much?', 'In the past 6 months, have you had less energy/motivation?', 'In the past 6 months, have you had a notable change in appetite? Eating more/less?', 'In the past 6 months, have you felt like a failure or that you have let down others around you?',
             'In the past 6 months, have you often felt down, depressed or hopeless?', 'In the past 6 months, have you suffered an anxiety attack?', 'In the past 6 months, have you felt more irritable or annoyed?', "In the past 6 months, have you felt like you've had no one to turn to?"]


@app.route("/quiz")
def quiz():
    return render_template('quiz.html')


@app.route("/q/<q_number>")
def quiz_main(q_number):
    question_number = int(q_number)+1
    question= questions[question_number]
    return render_template('quiz2.html', question=question, q_number=question_number)


if __name__ == '__main__':
    app.run(debug=True, threaded=True)

