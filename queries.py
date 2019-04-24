import datetime
# Select event with start_date equal to date
def query1(cur, date):
    cur.execute(f'''SELECT * FROM event WHERE (data->>'start_date') = '{date}' ''')
    return cur.fetchall()

# Select all event and sort them
def query2(cur):
    cur.execute(f'''SELECT * FROM event ORDER BY (data->>'start_date')''')
    return cur.fetchall()

# Select event with date between start_date and end_date
def query3(cur, date):
    cur.execute(f'''SELECT * FROM event WHERE {date} between TO_DATE((data->>'start_date'), 'DD.MM.YYYY') AND TO_DATE((data->>'start_date'), 'DD.MM.YYYY') ''')
    return cur.fetchall()











# distance function
def distance(start_date1, end_date1, start_date2, end_date2):
    x = start_date1 - start_date2
    x = abs(x.total_second())
    y = end_date1 - end_date2
    y = abs(y.total_second())
    return x*x + y*y
