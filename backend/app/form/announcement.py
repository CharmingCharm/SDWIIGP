from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField, SelectMultipleField
from wtforms.ext.sqlalchemy.fields import QuerySelectMultipleField
from wtforms.validators import DataRequired, EqualTo, ValidationError
from flask import request
from app.model import Problem, Tag


class Announcement(FlaskForm):

	title = StringField('Title', validators=[DataRequired(message='Title is required')])
	description = TextAreaField('Description', validators=[DataRequired(message='Description is required')])
