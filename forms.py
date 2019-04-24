from flask_wtf import FlaskForm                                             
from wtforms import StringField, DateField
from wtforms.validators import DataRequired
from datetime import datetime

class EventForm(FlaskForm):
    event = StringField('event', validators=[DataRequired()])
    start = DateField('starting date', format='%d.%m.%Y', validators=[DataRequired()])
    end = DateField('ending date', format='%d.%m.%Y', validators=[DataRequired()])

    def validate_on_submit(self):
        result = super(EventForm, self).validate()
        if (self.start.data > self.end.data):
            return False
        else:
            return result
