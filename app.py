from flask import Flask, redirect, render_template
from forms import EventForm
import psycopg2
app = Flask(__name__)
app.config['SECRET_KEY'] = 'any string works here'
conn = psycopg2.connect(dbname='testdb', user='postgres', password='postgres', host='localhost')
cur = conn.cursor()

cur.execute('CREATE TABLE products (id SERIAL PRIMARY KEY, name TEXT);')
cur.execute("INSERT INTO products (name) VALUES ('almar');")
cur.execute('SELECT name FROM products; ')
print(cur.fetchone())

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
