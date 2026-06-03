from flask import Flask, render_template, request

app = Flask(__name__)

# Store notes
notes = []

@app.route('/', methods=['GET', 'POST'])
def index():

    if request.method == 'POST':

        # Get note from form
        note = request.form.get('note')

        # Avoid empty notes
        if note:
            notes.append(note)

    return render_template('home.html', notes=notes)


if __name__ == '__main__':
    app.run(debug=True)