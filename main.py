# Store this code in 'app.py' file

from flask import *
from flask_mysqldb import MySQL
import MySQLdb.cursors
import random
import smtplib
from datetime import datetime
app = Flask(__name__,static_url_path='/static')

Dict={}
app.secret_key = '12345678'
db = MySQLdb.connect("localhost","root","","login_data" )
mycursor = db.cursor()
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'login_data'
app.config["SESSION_PERMANENT"] = False
mysql = MySQL(app)



@app.route('/',methods=["GET","POST"])
def home():
	if request.method=="POST":
		name=request.form['name']
		email=request.form['email']
		msg=request.form['msg']
		s = smtplib.SMTP("smtp.gmail.com", 587)  # 587 is a port number
		s.starttls()
		ssender = "aashay1000@gmail.com"
		spass = "frwe dkwc sbgr jpgz"
		s.login(ssender, spass)	
		s.sendmail(ssender, "jainaashay123@gmail.com", msg+"     email="+email)
		
        

	if session.get('loggedin')==True:
		
		return render_template('index.html',data="Sign Out")
	else:
		return render_template('index.html',data="Login/SignUp")

	







@app.route('/login', methods =['GET', 'POST'])
def login():
	msg = ''
	if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
		username = request.form['username']
		password = request.form['password']
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM login WHERE email = % s AND password = % s', (username, password, ))
		account = cursor.fetchone()
		if account:
			session['loggedin'] = True
			session['username'] = account['email']
			msg = 'Logged in successfully !'
			
			return redirect(url_for('home'))
		else:
			flash('Invalid Credentials !!')
			return render_template('login.html')

	return render_template('login.html', msg = msg)

@app.route('/logout')
def logout():
	
	session.pop('loggedin', None)
	
	session.pop('username', None)
	return redirect(url_for('home'))


@app.route('/New',methods=["GET","POST"])
def New():
	#if not session.get('loggedin'):
	#	return 'Access Denied'

	if request.method=="POST":
		emaill=request.form['email']
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM login WHERE email = % s ', (emaill,))
		account = cursor.fetchone()
		if not account:
			s = smtplib.SMTP("smtp.gmail.com", 587)  # 587 is a port number
			s.starttls()
			ssender = "aashay1000@gmail.com"
			spass = "frwe dkwc sbgr jpgz"
			s.login(ssender, spass)
			otp = random.randint(1000, 9999)
			otp=str(otp)
			s.sendmail(ssender, emaill, otp)
			Dict[emaill]=otp
			return redirect(url_for('Enter',email=emaill))
		else:
			flash("Account already Exists !!")
	
	return render_template('New.html')
     
	      
 
@app.route('/Enter/<email>',methods=["POST","GET"])
def Enter(email):
	if request.method=="POST":
		otp=request.form['otp']
		
		
		if Dict[email]==otp:
			return redirect(url_for('setpassword',email=email))
		else:
			flash('incorrect OTP!! Try Again !!')
		
		
	return render_template('Enter.html')



@app.route('/password/<email>',methods=["POST","GET"])
def setpassword(email):
	if request.method=="POST":
		password=request.form['pass']
		#cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		mycursor.execute('INSERT INTO `login` (`email`, `password`) VALUES ( %s, %s)', (email,password,))
		db.commit()
		flash('Registration Successful')
		
	return render_template('password.html')


@app.route('/information',methods=["POST","GET"])
def information():
	if session.get('loggedin')==True:
		if request.method=="POST":
			schno=request.form['scno']
			dob=str(request.form['dob'])
			sname=request.form['Student_Name']
			branch=request.form['branch']
			yog=request.form['YOG']
			x=mycursor.execute('INSERT INTO `student` ( `Scholar_No`, `DOB`, `Student_Name`, `Branch`, `YOG`) VALUES (%s,%s,%s, %s, %s)',(schno,dob,sname,branch,yog,))
			if x:
				db.commit()
				flash("Successful")
				return render_template('information.html')
			else:
				flash('invalid entry !!')
		else:
			return render_template('information.html')

	else:
		return render_template('login.html')
	

@app.route('/records')
def show():
	if session.get('loggedin')==True:
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM student')
		records=cursor.fetchall()
		return render_template('records.html',records=records)
	else:
		return "Access Denied !! Please Login first"


	

	    
			
	    
	    
	    
	    

		


		

			








        
			
	




			
			
			
	
	
		


app.run()

#INSERT INTO `login` (`sno`, `email`, `password`) VALUES (NULL, 'ahdhshj', 'sds')