from flask import Flask, redirect, render_template
from forms import EventForm
app = Flask(__name__)
app.config['SECRET_KEY'] = 'any string works here'

@app.route('/', methods=['GET', 'POST'])
def submit():
    form = EventForm()
    if form.validate_on_submit():

        '''
        ' Here you need to store data to the database.
        ' Get value from field - form.name_of_field.data.
        '
        ' You can find name of fields in forms.py.
        '''
        
        return redirect('../')
    return render_template('submit.html', form=form)

@app.route('/chart', methods=['GET'])
def chart():
    return render_template('chart.html')

