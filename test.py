from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# define the quiz questions and answers
questions = [
    {
        'id': 1,
        'question': 'What is the capital of France?',
        'options': ['Paris', 'London'],
        'answer': 'Paris'
    },
    {
        'id': 2,
        'question': 'What is the largest ocean in the world?',
        'options': ['Atlantic Ocean', 'Pacific Ocean'],
        'answer': 'Pacific Ocean'
    }
]

# initialize the quiz score
score = 0


@app.route('/')
def index():
    # redirect to the first question
    return redirect(url_for('question', id=1))


@app.route('/question/<int:id>', methods=['GET', 'POST'])
def question(id):
    global score

    # find the question with the given ID
    question = next((q for q in questions if q['id'] == id), None)

    # check if the question exists
    if not question:
        return render_template('quiz_result.html', score=score)

    if request.method == 'POST':
        # check if the selected answer is correct
        selected_answer = request.form.get('answer')
        if selected_answer == question['answer']:
            score += 1

        # redirect to the next question
        next_id = id + 1
        if next_id > len(questions):
            return render_template('quiz_result.html', score=score)
        else:
            return redirect(url_for('question', id=next_id))

    # render the question template
    return render_template('quiz_question.html', question=question)


@app.route('/answer', methods=['POST'])
def answer():
    global current_question
    answer = request.form['answer']
    # Do something with answer (e.g. store it in a database)
    # Move on to next question or show results if there are no more questions
    current_question += 1
    if current_question == len(questions):
        return redirect(url_for('results'))
    else:
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
