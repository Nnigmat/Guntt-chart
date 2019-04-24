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
    cur.execute(f'''SELECT * FROM event WHERE (data->>'start_date') <= ''{date}'' AND (data->>'end_date') >= '{date}' ''')
    return cur.fetchall()
