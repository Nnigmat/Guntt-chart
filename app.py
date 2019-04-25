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
    query = request.args.get('query')
    cur.execute("select * from event order by data->>'start_date' limit 10")
    data = cur.fetchall()
    res = []
    for d in data:
        d[0]['start_date'] = datetime.datetime.strptime(d[0]['start_date'], '%d.%m.%Y').strftime('%Y-%m-%d')
        d[0]['end_date'] = datetime.datetime.strptime(d[0]['end_date'], '%d.%m.%Y').strftime('%Y-%m-%d')
        res.append(d)

    data = {
        'has':True,
        'data':res
    }
    return jsonify(data)


# Generate initial data
for assigned_to, event, start, end  in Data().get_data(n=100):
    insert(task_name=event, assigned_to=assigned_to, start_date=start, end_date=end)


'''
' Query 1
cur.execute('SELECT * from event')
record = cur.fetchone()[0]
print(query1(cur, record['start_date']))
print(query1(cur, '5.7.2019'))
'''

'''
' Query 2
print(query2(cur))
'''

'''
' Query 3
print(query3(cur, datetime.date(day=5, month=7, year=2019)))
'''

''' ' Query 4
print(query4(cur, datetime.date(day=5, month=7, year=2019), datetime.date(day=5, month=7, year=2019), k=3))
'''

'''
' Query 5
cur.execute('SELECT * from event')
record = cur.fetchone()[0]
print(query5(cur, record['start_date'], record['end_date']))
print(query5(cur, '12.7.2019', '15.7.2019'))
print(query5(cur, '20.11.2019', '30.11.2019'))
print(query5(cur, '7.5.2019', '21.5.2019'))
print(query5(cur, '20.10.2019', '1.11.2019'))
print(query5(cur, '28.3.2019', '5.4.2019'))
'''
