import names
from os.path import abspath, join, dirname
import random
from datetime import datetime as dt

full_path = lambda filename: abspath(join(*[dirname(__file__), 'names', filename]))

class Names:
    def __init__(self):

        self.FILES = {
            'first:male': full_path('dist.male.first'),
            'first:female': full_path('dist.female.first'),
            'last': full_path('dist.all.last'),}


    def get_name(self, filename):
        selected = random.random() * 90
        with open(filename) as name_file:
            for line in name_file:
                name, _, cummulative, _ = line.split()
                if float(cummulative) > selected:
                    return name
        return ""

    def get_first_name(self, gender=None):
        if gender is None:
            gender = random.choice(('male', 'female'))
        if gender not in ('male', 'female'):
            raise ValueError("Only 'male' and 'female' are supported as gender")
        return self.get_name(self.FILES['first:%s' % gender]).capitalize()

    def get_last_name(self):
        return self.get_name(self.FILES['last']).capitalize()

    def get_full_name(self, gender=None):
        return "{0} {1}".format(self.get_first_name(gender), self.get_last_name())

class Data:
    def __init__(self):
        self.__names = Names()

    def get_data(self, n=10, delta=18000, start_date=1556119825, finish_date=1587655825):
        data = []
        for i in range(n):
            date1 = random.randint(start_date, finish_date)
            date2 = date1+random.randint(10, delta)
            if date1>date2:
                date1, date2 = date2, date1
            date1st, date2st = dt.fromtimestamp(date1), dt.fromtimestamp(date2)
            create_date = lambda timestamp: "{0}.{1}.{2}".format(timestamp.day, timestamp.month, timestamp.year)

            data.append([self.__names.get_full_name(), 'task{0}'.format(str(i)), create_date(date1st), create_date(date2st)])
        return data
