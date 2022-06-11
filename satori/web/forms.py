from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, SelectField
from satori.config import verbose

class EditConfigurationForm(FlaskForm):
    flaskPort = IntegerField(verbose('flaskPort'), validators=[])
    nodejsPort = IntegerField(verbose('nodejsPort'), validators=[])
    dataPath = StringField(verbose('dataPath'), validators=[])
    modelPath = StringField(verbose('modelPath'), validators=[])
    defaultSource = SelectField(verbose('defaultSource'), validators=[], choices=['streamr', 'satori'])
    submit = SubmitField('Save')

