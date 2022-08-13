from wtforms import StringField, SubmitField, IntegerField, FloatField, DateField
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm


class CitizenForm(FlaskForm):
    name = StringField('Enter a Name', validators=[DataRequired()])
    year = IntegerField('Year', validators=[DataRequired()])
    month = IntegerField('Month', validators=[DataRequired()])
    day = IntegerField('Day', validators=[DataRequired()])
    submit = SubmitField('Submit')
