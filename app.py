from flask import Flask, redirect, render_template, request
from forms import EventForm
from create_data import Data
from queries import *
import psycopg2
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'any string works here'
conn = psycopg2.connect(dbname='testdb', user='postgres', password='postgres', host='localhost')
cur = conn.cursor()

#cur.execute('DROP TABLE IF EXISTS event;')
cur.execute(f'''CREATE TABLE IF NOT EXISTS event (
    data JSON,
    CONSTRAINT validate_task_name CHECK (length(data->>'task_name') > 0 AND (data->>'task_name') IS NOT NULL),
    CONSTRAINT validate_assigned_to CHECK (length(data->>'assigned_to') > 0 AND (data->>'assigned_to') IS NOT NULL),
    CONSTRAINT validate_start_date CHECK (length(data->>'start_date') > 0 AND (data->>'start_date') IS NOT NULL),
    CONSTRAINT validate_end_date CHECK (length(data->>'end_date') > 0 AND (data->>'end_date') IS NOT NULL));''');

# date - dd.mm.yyyy
def insert(task_name, assigned_to, start_date, end_date):
    duration = datetime.datetime.strptime(end_date, "%d.%m.%Y") - datetime.datetime.strptime(start_date, "%d.%m.%Y")

    cur.execute(f'''INSERT INTO event (data) VALUES ('{{
    "task_name": "{task_name}",
    "assigned_to": "{assigned_to}",
    "start_date": "{start_date}",
    "end_date": "{end_date}", 
    "duration":  "{duration.days}"
    }}');''')


@app.route('/', methods=['GET', 'POST'])
def submit():
    form = EventForm()
    if request.method == 'GET':
        return render_template('submit.html', form=form)
    else:
        if form.validate_on_submit():
            insert(form.event.data, form.assigned_to.data, form.start.data.strftime('%d.%m.%Y'), form.end.data.strfitime('%d.%m.%Y'))
        return redirect('../')

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

# Generate initial data
for assigned_to, event, start, end  in Data().get_data(n=1000):
    insert(task_name=event, assigned_to=assigned_to, start_date=start, end_date=end)

print(query3(cur, datetime.datetime(day=5, month=7, year=2019)))


