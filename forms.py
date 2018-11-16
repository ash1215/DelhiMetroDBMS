from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class RegistrationForm(FlaskForm):
	name = StringField('Name', validators=[DataRequired(), Length(min=1, max=20)])
	DOB_date = StringField('Date', validators=[DataRequired()])
	DOB_month = StringField('Month', validators=[DataRequired()])
	DOB_year = StringField('Year', validators=[DataRequired()])
	Address_HouseNo = StringField('House Number')
	Address_Street = StringField('Street')
	Address_City = StringField('City')
	Address_PIN = StringField('PINCODE')
	password = PasswordField('Password', validators=[DataRequired(), Length(min=1, max=30)])
	confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
	passengerID = StringField('Passenger ID', validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired()])
	remember = BooleanField('Remember Me')
	submit = SubmitField('Login')

class NotifyPosts(FlaskForm):
	notify = StringField('Write the post', validators=[DataRequired(), Length(min=1, max=500)])
	post = SubmitField('Post')

class AdminLogin(FlaskForm):
	adminID = StringField('Admin ID', validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired()])
	remember = BooleanField('Remember Me')
	submit = SubmitField('Login')

class StationForm(FlaskForm):
	ID = StringField('Station ID', validators=[DataRequired()])
	Name = StringField('Name', validators=[DataRequired()])
	Parking = StringField('Parking Facility', validators=[DataRequired()])
	Feeder = StringField('Feeder Bus Service', validators=[DataRequired()])
	Distance = StringField('Distance From Rithala', validators=[DataRequired()])
	add = SubmitField('Add Station')