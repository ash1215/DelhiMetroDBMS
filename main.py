from flask import Flask, render_template, url_for, flash, redirect, request
from forms import RegistrationForm, LoginForm
from flask_mysqldb import MySQL
from mysql.connector import Error
import mysql.connector


try:
	connection=mysql.connector.connect(user='root',password='12345678',host='localhost',database='DelhiMetro')
	cursor=connection.cursor()
	print("connected")

except:
	print("not connected")

app = Flask(__name__)

app.config['SECRET_KEY']='2c64ff2e0958e6af6abb6f1e493ed4dc'

posts = [
	{
		'author': 'Ashwini Jha',
		'title': 'Blog Post 1',
		'content': 'Huh! I was born today',
		'date_posted': 'September 04, 2018'
	},
	{
		'author': 'Jhalak Gupta',
		'title': 'Blog Post 2',
		'content': "Hey! It's my birthday today. Can I get 100 likes?",
		'date_posted': 'October 27, 2018'
	}
]

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts=posts, title='Home')

@app.route("/accounthome")
@app.route("/accounthome<passengerID>")
def accounthome(passengerID):
	query = ('SELECT Name from Passenger where PassengerId="'+passengerID+'";')
	cursor.execute(query)
	result = cursor.fetchall()
	name = result[0][0]
	return render_template('accounthome.html',title=name, pID=passengerID)

@app.route("/accountprofile<passengerID>")
def accountprofile(passengerID):
	query = ('SELECT PassengerId,Name,DOB,timestampdiff(YEAR,DOB,CURDATE()) AS Age,House_No,Street,City,PINCODE FROM Passenger where PassengerId="'+passengerID+'";')
	cursor.execute(query)
	result = cursor.fetchall()
	name = result[0][0]
	return render_template('accountprofile.html',title=name,data=result[0])


@app.route("/about")
def about():
	return render_template('about.html', title='About')

@app.route("/register", methods=['GET', 'POST'])
def register():
	form = RegistrationForm()
	if form.validate_on_submit():
		name=form.name.data
		date=form.DOB_date.data
		month=form.DOB_month.data
		year=form.DOB_year.data
		house=form.Address_HouseNo.data
		street=form.Address_Street.data
		city=form.Address_City.data
		pin=form.Address_PIN.data
		password=form.password.data
		query=("INSERT INTO Passenger(Name,DOB,House_No,Street,City,PINCODE) values('"+name+"','"+year+"-"+month+"-"+date+"','"+house+"','"+street+"','"+city+"','"+pin+"');")
		cursor.execute(query)
		connection.commit()
		query=("SELECT PassengerID from Passenger;")
		cursor.execute(query)
		x=cursor.rowcount
		result = cursor.fetchall()
		query=("INSERT INTO Account(PassengerId,password) values("+str(result[x][0])+",'"+password+"');")
		cursor.execute(query)
		connection.commit()
		
		flash(f'Account created for {form.name.data}! Your Passenger ID is {result[x][0]} ', 'success')
		return redirect(url_for('home'))
	return render_template('register.html', title="Register", form=form)




@app.route("/login", methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		query = ('SELECT PassengerId, password FROM Account WHERE PassengerId="'+form.passengerID.data+'"')
		cursor.execute(query)
		result=cursor.fetchall()
		if result:
			if result[0][1]==form.password.data:
				#flash('Welcome user!', 'success')
				#return accounthome(form.passengerID.data)
				return redirect(url_for('accounthome', passengerID=form.passengerID.data))
			else:
				flash('Incorrect Password!', 'danger')	
		else:
			flash('This passenger is not registered!', 'danger')
	return render_template('login.html', title="Login", form=form)

if __name__=='__main__':
	app.run(debug=True)