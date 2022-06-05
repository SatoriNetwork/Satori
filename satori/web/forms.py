from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, SelectField

class EditConfigurationForm(FlaskForm):
    flaskPort = IntegerField('user interface port', validators=[])
    nodejsPort = IntegerField('streamr light client port', validators=[])
    defaultSource = SelectField('default source of data streams', validators=[], choices=['streamr', 'satori'])
    dataPath = StringField('absolute data path', validators=[])
    modelPath = StringField('absolute model path', validators=[])
    submit = SubmitField('Save')

