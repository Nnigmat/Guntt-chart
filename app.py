from flask import Flask, redirect, render_template, request
from forms import EventForm
from create_data import Data
from queries import *
import psycopg2
import datetime
from flask_bootstrap import Bootstrap
from flask import jsonify

app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config['SECRET_KEY'] = 'any string works here'
conn = psycopg2.connect(dbname='testdb', user='postgres', password='postgres', host='localhost')
cur = conn.cursor()

#cur.execute('DROP TABLE IF EXISTS event;')
cur.execute(f'''CREATE TABLE IF NOT EXISTS event (
    data JSONB,
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

@app.route('/data/', methods=['GET'])
def give_data():
    q = request.args.get('query')
    print(q)
    cur.execute(q)
    d = cur.fetchall()
    data = {
    'has':True,
    'data':d}
    return jsonify(data)


# Generate initial data
for assigned_to, event, start, end  in Data().get_data(n=10):
    insert(task_name=event, assigned_to=assigned_to, start_date=start, end_date=end)

#cur.execute('''SELECT * from event where to_timestamp(data->>'start_date', 'DD.MM.YYYY') > to_timestamp('2019-06-01', 'YYYY-MM-DD')''')
#print(cur.fetchall())
#print(query4(cur, datetime.date(day=5, month=7, year=2019), datetime.date(day=5, month=7, year=2019), k=3))
#print(query5(cur, datetime.date(day=5, month=7, year=2019), datetime.date(day=5, month=7, year=2019), k=3))
