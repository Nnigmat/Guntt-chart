from flask import Flask, redirect, render_template
from forms import EventForm
import psycopg2
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'any string works here'
conn = psycopg2.connect(dbname='testdb', user='postgres', password='postgres', host='localhost')
cur = conn.cursor()

cur.execute((f'''CREATE TABLE event (
    data JSON,
    CONSTRAINT validate_task_name CHECK (lentgh(data->>'task_name') > 0 AND (data->>'task_name') IS NOT NULL),
    CONSTRAINT validate_assigned_to CHECK (lentgh(data->>'assigned_to') > 0 AND (data->>'assigned_to') IS NOT NULL),
    CONSTRAINT validate_start_date CHECK (lentgh(data->>'start_date') > 0 AND (data->>'start_date') IS NOT NULL),
    CONSTRAINT validate_start_date CHECK (lentgh(data->>'end_date') > 0 AND (data->>'end_date') IS NOT NULL),
);'''));

# date - dd.mm.yyyy
def insert(task_name, assigned_to, start_date, end_date):
    duration = end_date - start_date
    if (duration < 0):
        raise Exception('end_date should be after the start_date (idesh nahui)')

    cur.execute(f'''INSERT INTO event (data) VALUES ('{{
    "task_name": "{task_name}",
    "assigned_to": "{assigned_to}",
    "start_date": "{start_date.strftime("%d.%m.%Y")}",
    "end_date": "{end_date.strftime("%d.%m.%Y")}", 
    "duration":  "{duration.days}"
    }}');''')


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
    '''
    ' Return gantt chart template with javascript
    '''
    return render_template('chart.html')


@app.route('/data', methods=['GET'])
def give_data():
    '''
    ' Should send the json to the user, with data specified as here for gantt chart creation.
    ' https://stackoverflow.com/questions/41259441/how-to-draw-gantt-chart-using-chart-js-or-other-libraries
    '''
    pass
