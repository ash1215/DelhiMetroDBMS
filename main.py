from flask import Flask, render_template, url_for, flash, redirect, request
from forms import RegistrationForm, LoginForm, NotifyPosts, AdminLogin, StationForm
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
	query = ('SELECT * from notify;')
	cursor.execute(query)
	notification = cursor.fetchall()
	return render_template('home.html', posts=posts, title='Home', notification=notification)

@app.route("/accounthome")
@app.route("/accounthome<passengerID>")
def accounthome(passengerID):
	query = ('SELECT * from notify;')
	cursor.execute(query)
	notification = cursor.fetchall()
	query = ('SELECT Name from Passenger where PassengerId="'+passengerID+'";')
	cursor.execute(query)
	result = cursor.fetchall()
	name = result[0][0]
	return render_template('accounthome.html',title=name, pID=passengerID,notification=notification)

@app.route("/passengerchange<passengerID>", methods=['GET', 'POST'])
def passengerchange(passengerID):
	query = ('SELECT * from notify;')
	cursor.execute(query)
	notification = cursor.fetchall()
	if request.method=='POST':
		name = request.form['pname']
		date = request.form['date']
		month = request.form['month']
		year = request.form['year']
		house = request.form['house']
		street = request.form['street']
		city = request.form['city']
		pin = request.form['pin']
		print(name)
		query = ('UPDATE Passenger SET Name="'+name.strip()+'", DOB="'+year.strip()+'-'+month.strip()+'-'+date.strip()+'", House_No="'+house.strip()+'", Street="'+street.strip()+'", City="'+city.strip()+'", PINCODE="'+pin.strip()+'" WHERE PassengerID="'+passengerID+'";')
		print(query)
		cursor.execute(query)
		connection.commit()
		return 'done'
	else:
		query = ('SELECT PassengerId,Name,DOB,DATE_FORMAT(DOB,"%d"),DATE_FORMAT(DOB,"%m"),DATE_FORMAT(DOB,"%Y"),House_No,Street,City,PINCODE FROM Passenger where PassengerId="'+passengerID+'";')
		cursor.execute(query)
		result = cursor.fetchall()
		print(passengerID)
		name = result[0][0]
		return render_template('passengerchange.html',title='admin',data=result[0], pID=passengerID,notification=notification)


@app.route("/addstation<adminID>", methods=['GET','POST'])
def addstation(adminID):
	form = StationForm()
	if form.validate_on_submit():
		Name=form.Name.data
		ID=form.ID.data
		Parking=form.Parking.data
		Feeder=form.Feeder.data
		Distance=form.Distance.data
		query=("INSERT INTO Stations (Station_ID, Name, Parking_Facility, Feeder_Bus_Availability, Distance_from_Rithala) VALUES ('"+ID+"', '"+Name+"', '"+Parking+"', '"+Feeder+"', '"+Distance+"');")
		cursor.execute(query)
		connection.commit()
		flash(f'Station Added', 'success')
		return redirect(url_for('s_table',adminID=adminID))
	return render_template('addstation.html', title="Register Station", form=form, adminID=adminID)


@app.route("/adminhome<adminID>")
def adminhome(adminID):
	query = ('SELECT Name from adminlogin where Admin_ID="'+adminID+'";')
	cursor.execute(query)
	result = cursor.fetchall()
	name = result[0][0]
	return render_template('adminhome.html',title=name, adminID=adminID)

@app.route("/accountprofile<passengerID>", methods=['GET', 'POST'])
def accountprofile(passengerID):
	query = ('SELECT * from notify;')
	cursor.execute(query)
	notification = cursor.fetchall()
	if request.method=='POST':
		return redirect(url_for('accountchange', passengerID=passengerID),notification=notification)
	else:
		query = ('SELECT PassengerId,Name,DOB,timestampdiff(YEAR,DOB,CURDATE()) AS Age,House_No,Street,City,PINCODE FROM Passenger where PassengerId="'+passengerID+'";')
		cursor.execute(query)
		result = cursor.fetchall()
		name = result[0][0]
		return render_template('accountprofile.html',title=name,data=result[0], pID=passengerID,notification=notification)

@app.route("/accountchange<passengerID>", methods=['GET', 'POST'])
def accountchange(passengerID):
	query = ('SELECT * from notify;')
	cursor.execute(query)
	notification = cursor.fetchall()
	if request.method=='POST':
		name = request.form['pname']
		date = request.form['date']
		month = request.form['month']
		year = request.form['year']
		house = request.form['house']
		street = request.form['street']
		city = request.form['city']
		pin = request.form['pin']
		print(name)
		query = ('UPDATE Passenger SET Name="'+name.strip()+'", DOB="'+year.strip()+'-'+month.strip()+'-'+date.strip()+'", House_No="'+house.strip()+'", Street="'+street.strip()+'", City="'+city.strip()+'", PINCODE="'+pin.strip()+'" WHERE PassengerID="'+passengerID+'";')
		print(query)
		cursor.execute(query)
		connection.commit()
		return redirect(url_for('accountprofile',passengerID=passengerID))
	else:
		query = ('SELECT PassengerId,Name,DOB,DATE_FORMAT(DOB,"%d"),DATE_FORMAT(DOB,"%m"),DATE_FORMAT(DOB,"%Y"),House_No,Street,City,PINCODE FROM Passenger where PassengerId="'+passengerID+'";')
		cursor.execute(query)
		result = cursor.fetchall()
		name = result[0][0]
		return render_template('accountchange.html',title=name,data=result[0], pID=passengerID,notification=notification)


@app.route("/about")
def about():
	query = ('SELECT * from notify;')
	cursor.execute(query)
	notification = cursor.fetchall()
	return render_template('about.html', title='About', notification=notification)

@app.route("/table<adminID>")
def p_table(adminID):
	query = ('SELECT PassengerId,Name,DOB,timestampdiff(YEAR,DOB,CURDATE()) AS Age,House_No,Street,City,PINCODE FROM Passenger;')
	cursor.execute(query)
	table = cursor.fetchall()
	
	return render_template('passengertable.html', title='table', table=table, adminID=adminID)

@app.route("/stationtable<adminID>")
def s_table(adminID):
	query = ('SELECT Station_ID,Name,Parking_Facility,Feeder_Bus_Availability,Distance_from_Rithala from Stations;')
	cursor.execute(query)
	table = cursor.fetchall()
	print(table[2])
	return render_template('stationtable.html', title='table', table=table, adminID=adminID)


@app.route("/accountstations<passengerID>", methods=['GET', 'POST'])
def accountstations(passengerID):
	query = ('SELECT * from notify;')
	cursor.execute(query)
	notification = cursor.fetchall()
	query = ('SELECT PassengerId,Name,DOB,timestampdiff(YEAR,DOB,CURDATE()) AS Age,House_No,Street,City,PINCODE FROM Passenger where PassengerId="'+passengerID+'";')
	cursor.execute(query)
	result = cursor.fetchall()
	name = result[0][0]
	query = ('SELECT Station_ID,Name,Parking_Facility,Feeder_Bus_Availability,Distance_from_Rithala from Stations;')
	cursor.execute(query)
	sta = cursor.fetchall()
	if request.method=='POST':
		Station_ID = request.form['stat_select']
		print(type(Station_ID))
		Station_ID=Station_ID.strip()
		query = ('SELECT Station_ID,Name,Parking_Facility,Feeder_Bus_Availability,Distance_from_Rithala from Stations WHERE Station_ID="'+Station_ID+'";')
		cursor.execute(query)
		info = cursor.fetchall()
		print(type(info))
		print(info[0][0])
		return render_template('accountstations.html',title=name,pID=passengerID,sta_data=sta,data=result[0],info=info[0],x=1,notification=notification)
	else:
		info=('KHT','Kohat Enclave',1,1,4)
		return render_template('accountstations.html',title=name,pID=passengerID,sta_data=sta,data=result[0],x=0,info=info,notification=notification)

@app.route("/accountbook<passengerID>", methods=['GET', 'POST'])
def accountbook(passengerID):
	query = ('SELECT * from notify;')
	cursor.execute(query)
	notification = cursor.fetchall()
	query = ('SELECT PassengerId,Name,DOB,timestampdiff(YEAR,DOB,CURDATE()) AS Age,House_No,Street,City,PINCODE FROM Passenger where PassengerId="'+passengerID+'";')
	cursor.execute(query)
	result = cursor.fetchall()
	name = result[0][0]
	query = ('SELECT Station_ID,Name,Parking_Facility,Feeder_Bus_Availability,Distance_from_Rithala from Stations;')
	cursor.execute(query)
	sta = cursor.fetchall()
	if request.method=='POST':
		Station1 = request.form['stat_select']
		Station2 = request.form['stat_select2']
		query = ('SELECT Station_ID,Name,Parking_Facility,Feeder_Bus_Availability,Distance_from_Rithala from Stations WHERE Station_ID="'+Station1.strip()+'" OR Station_ID="'+Station2.strip()+'";')
		cursor.execute(query)
		Station = cursor.fetchall()
		print(Station)
		"""query = ('CALL TicketPrice('+str(Station[0][4])+','+str(Station[1][4])+');')
		print(query)
		cursor.execute(query,multi=True)
		print('cursor')
		#price = cursor.fetchall()
		#price = price[0][0]
		"""
		print(type(Station[0][4]))
		
		if(abs(Station[0][4]-Station[1][4])>=4):
			price=15+abs(Station[0][4]-Station[1][4]-4)*2
		else:
			price=15
		if result[0][3]>=60:
			price = price*0.75
		elif result[0][3]<=10:
			price = price*0.50
		
		#query = ('CALL Balance('+passengerID+');')
		#cursor.execute(query)
		
		query=("SELECT Balance FROM Wallet WHERE PassengerID="+passengerID+" ORDER BY transaction_time DESC LIMIT 1;")
		cursor.execute(query)
		B=cursor.fetchall()
		balance = B[0][0]
		newBalance = int(balance) + price
		query=("INSERT INTO Wallet(PassengerID,difference,Balance) values("+passengerID+","+str(price)+","+str(newBalance)+");")
		cursor.execute(query)
		connection.commit()

		return render_template('accountbook.html',title=name,pID=passengerID,sta_Data=sta,data=result[0],notification=notification,price=price,x=1)
	return render_template('accountbook.html',title=name,pID=passengerID,sta_data=sta,data=result[0],notification=notification,x=0)

@app.route("/accountwallet<passengerID>", methods=['GET', 'POST'])
def wallet(passengerID):
	query = ('SELECT * from notify;')
	cursor.execute(query)
	notification = cursor.fetchall()
	query = ("SELECT PassengerID,difference,Balance,transaction_time from Wallet where PassengerID="+passengerID+" order by transaction_time desc;")
	cursor.execute(query)
	details=cursor.fetchall()
	return render_template('Wallet.html',title='wallet',pID=passengerID,details=details,notification=notification)


@app.route("/register", methods=['GET', 'POST'])
def register():
	query = ('SELECT * from notify;')
	cursor.execute(query)
	notification = cursor.fetchall()
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
	return render_template('register.html', title="Register", form=form, notification=notification)




@app.route("/login", methods=['GET', 'POST'])
def login():
	query = ('SELECT * from notify;')
	cursor.execute(query)
	notification = cursor.fetchall()
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
	return render_template('login.html', title="Login", form=form, notification=notification)


@app.route("/notification<adminID>", methods=['GET', 'POST'])
def notify(adminID):
	query = ('SELECT * from notify;')
	cursor.execute(query)
	notification = cursor.fetchall()
	form = NotifyPosts()
	if form.validate_on_submit():
		notify=form.notify.data
		query = ('INSERT into notifications(Post,Admin_ID) VALUES("'+notify+'","'+adminID+'");')
		print(query)
		cursor.execute(query)
		connection.commit()
		flash(f'Post created!', 'success')
		return redirect(url_for('notify',adminID=adminID))
	return render_template('notification.html', title="Notification", form=form,adminID=adminID, notification=notification)

@app.route("/adminlogin", methods=['GET', 'POST'])
def Adminlogin():
	query = ('SELECT * from notify;')
	cursor.execute(query)
	notification = cursor.fetchall()
	form = AdminLogin()
	if form.validate_on_submit():
		query = ('SELECT Admin_ID, password FROM adminlogin WHERE Admin_ID="'+form.adminID.data+'";')
		cursor.execute(query)
		result=cursor.fetchall()
		print(query)
		if result:
			if result[0][1]==form.password.data:
				#flash('Welcome user!', 'success')
				#return accounthome(form.passengerID.data)
				return redirect(url_for('adminhome', adminID=form.adminID.data))
			else:
				flash('Incorrect Password!', 'danger')	
		else:
			flash('This admin is not registered!', 'danger')
	return render_template('adminlogin.html', form=form, title="Admin Login", notification=notification)




if __name__=='__main__':
	app.run(debug=True)