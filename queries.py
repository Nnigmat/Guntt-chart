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
    date = date.strftime('%d.%m.%Y')
    cur.execute(
        f'''SELECT * FROM event WHERE to_timestamp((data->>'start_date'), 'DD.MM.YYYY') < to_timestamp('{date}', 'DD.MM.YYYY') 
    AND to_timestamp((data->>'end_date'), 'DD.MM.YYYY') > to_timestamp('{date}', 'DD.MM.YYYY')''')
    return cur.fetchall()


# geospatial search, where the distance function is the Manhattan distance between points with coordinates {start_date, end_date}
# returns the k closest events to the needed one
def query4(cur, s_date, e_date, k):
    cur.execute(
        f'''SELECT * FROM event ORDER BY 
        (EXTRACT(EPOCH FROM TIMESTAMP WITH TIME ZONE '{s_date}') -
        cast(extract(epoch from to_timestamp(data->>'start_date', 'DD.MM.YYYY')) as integer)) *
        (EXTRACT(EPOCH FROM TIMESTAMP WITH TIME ZONE '{s_date}') -
        cast(extract(epoch from to_timestamp(data->>'start_date', 'DD.MM.YYYY')) as integer)) +
        (EXTRACT(EPOCH FROM TIMESTAMP WITH TIME ZONE '{e_date}') -
        cast(extract(epoch from to_timestamp(data->>'end_date', 'DD.MM.YYYY')) as integer)) *
        (EXTRACT(EPOCH FROM TIMESTAMP WITH TIME ZONE '{e_date}') -
        cast(extract(epoch from to_timestamp(data->>'end_date', 'DD.MM.YYYY')) as integer))
        ASC
        LIMIT {k} 
        ''')
    return cur.fetchall()

# aggregate function with count
def query5(cur, s_date, e_date):
    cur.execute(f'''SELECT COUNT(*) FROM event WHERE (data->>'start_date') = '{s_date}' AND (data->>'end_date') = '{e_date}' ''')
    return cur.fetchall()



# distance function
def distance(start_date1, end_date1, start_date2, end_date2):
    x = start_date1 - start_date2
    x = abs(x.total_second())
    y = end_date1 - end_date2
    y = abs(y.total_second())
    return x * x + y * y
