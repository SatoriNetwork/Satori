from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, SelectField, TextAreaField
from satori import config


class EditConfigurationForm(FlaskForm):
    flaskPort = IntegerField(config.verbose('flaskPort'), validators=[])
    nodejsPort = IntegerField(config.verbose('nodejsPort'), validators=[])
    dataPath = StringField(config.verbose('dataPath'), validators=[])
    modelPath = StringField(config.verbose('modelPath'), validators=[])
    walletPath = StringField(config.verbose('wallletPath'), validators=[])
    defaultSource = SelectField(config.verbose(
        'defaultSource'), validators=[], choices=['streamr', 'satori'])
    # todo: make this two fields: a list where you can select and remove (can't remove the last one), and you can add by typing in the name on a textfield...
    electrumxServers = SelectField(config.verbose('electrumxServers'), validators=[
    ], choices=[config.electrumxServers()])
    submit = SubmitField('Save')


class RawStreamForm(FlaskForm):
    # str
    name = StringField(config.verbose('name'), validators=[])
    # str or None
    target = StringField(config.verbose('target'), validators=[])
    # number of seconds between api hits, not None
    cadence = IntegerField(config.verbose('cadence'), validators=[])
    # number of seconds to offset from utc or None
    offset = IntegerField(config.verbose('offset'), validators=[])
    # type of data, just a str right now, whatever
    datatype = StringField(config.verbose('datatype'), validators=[])
    # str, not exceeding 1000 chars
    description = TextAreaField(config.verbose('description'), validators=[])
    # comma separated string list, each element trimmed
    tag = StringField(config.verbose('tag'), validators=[])
    # location of API
    url = StringField(config.verbose('url'), validators=[])
    # location of API + details or credentials like API key
    uri = StringField(config.verbose('uri'), validators=[])
    # headers for API call
    headers = TextAreaField(config.verbose('headers'), validators=[])
    # python script of a certain structure (a named method with specific inputs)
    hook = TextAreaField(config.verbose('hook'), validators=[])
    submit = SubmitField('Save')
