# Store this code in 'app.py' file
import pandas as pd
from flask import *
from flask_mysqldb import MySQL
import MySQLdb.cursors
import random
import smtplib
from datetime import datetime
app = Flask(__name__)

Dict={}
app.secret_key = '12345678'
db = MySQLdb.connect("aashay26.mysql.pythonanywhere-services.com","aashay26","Aashay123#2002","aashay26$login_data" )
mycursor = db.cursor()
app.config['MYSQL_HOST'] = 'aashay26.mysql.pythonanywhere-services.com'
app.config['MYSQL_USER'] = 'aashay26'
app.config['MYSQL_PASSWORD'] = 'Aashay123#2002'
app.config['MYSQL_DB'] = 'aashay26$login_data'
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


			try:
			    mycursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
			    x=mycursor.execute('INSERT INTO `student` ( `Scholar_No`, `DOB`, `Student_Name`, `Branch`, `YOG`) VALUES (%s,%s,%s, %s, %s)',(schno,dob,sname,branch,yog,))
			    mysql.connection.commit()
			    flash("Successful")


			except (MySQLdb.Error) as e:
			    flash("Invalid Entry !!!")




			return render_template('information.html')











		else:
			return render_template('information.html')

	else:
		return render_template('login.html')


@app.route('/records',methods=['GET','POST'])
def records():

	if session.get('loggedin')==True:

	    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
	    cursor.execute('SELECT * FROM student')
	    records=cursor.fetchall()
	    if request.method == 'POST':
	        sname = request.form['sname']
	        scno=request.form['scno']
	        branch=request.form['branch']
	        yog=request.form['yog']

	        if not scno=="":
	            cursor.execute('SELECT * FROM student where Scholar_No=%s',(scno,))
	            y=cursor.fetchall()
	            records=[x for x in records if x in y]

	        if not sname=="":
	            cursor.execute('SELECT * FROM student where Student_Name=%s',(sname,))
	            y=cursor.fetchall()
	            records=[x for x in records if x in y]

	        if not branch=="":
	            cursor.execute('SELECT * FROM student where Branch=%s',(branch,))
	            y=cursor.fetchall()
	            records=[x for x in records if x in y]

	        if not yog=="":
	            cursor.execute('SELECT * FROM student where yog=%s',(yog,))
	            y=cursor.fetchall()
	            records=[x for x in records if x in y]


	    return render_template('records.html',records=records)

	else:

	    return redirect('/login')
















@app.route("/update",methods=['GET','POST'])
def update():
    if session.get('loggedin')!=True:
        return redirect('/login')

    else:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        if request.method=='POST':
            dict={}
            i=0
            for x in request.form.getlist('sno[]'):
                dict[x]=i
                i=i+1

            schno=request.form.getlist('scholarno[]')
            dob=request.form.getlist('dob[]')
            sname=request.form.getlist('studentname[]')
            branch=request.form.getlist('branch[]')
            yog=request.form.getlist('yog[]')
            for x in request.form.getlist('sno[]'):

                i=dict[x]
                try:
                    f=cursor.execute('UPDATE student SET Scholar_No=%s,DOB=%s,Student_Name=%s,Branch=%s,YOG=%s where sno=%s',(schno[i],dob[i],sname[i],branch[i],yog[i],x,))
                    if f:
                        mysql.connection.commit()

                except (MySQLdb.Error) as e:
                    flash("An error occured !!")




            return redirect("/update")

        cursor.execute('SELECT * FROM student')
        records=cursor.fetchall()
        return render_template("update.html",records=records)













@app.route('/delete',methods=['GET','POST'])
def delete():
    if session.get('loggedin')!=True:
        return redirect('/login')

    else:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        if request.method=='POST':
            for x in request.form.getlist('id'):
                x=x.replace('/','')
                p=cursor.execute('DELETE FROM student WHERE sno = %s',(x,))

                if p:
                    mysql.connection.commit()


            return redirect('/records')

        cursor.execute('SELECT * FROM student')
        records=cursor.fetchall()
        return render_template('delete.html',records=records)



@app.route('/information/uploadData', methods=['GET', 'POST'])
def upload_file():
    if session.get('loggedin')!=True:
        return redirect('/login')

    df=pd.DataFrame()
    if request.method == 'POST':
        f = request.files['file']
        df=pd.read_csv(f)

        df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
        df=df.replace('\\n',' ')
        if df.columns.isin(['DOB']).any():
            df['DOB']=pd.to_datetime(df['DOB'])
            df['DOB']=df['DOB'].dt.strftime('%Y-%m-%d')


        if request.form['action']=='View Data':

            return render_template('file.html',df=df)


        elif request.form['action']=='Add Data':

            if df.columns.isin(['Scholar No']).any() and df.columns.isin(['DOB']).any() and df.columns.isin(['Student Name']).any() and df.columns.isin(['YOG']).any() and df.columns.isin(['Branch']).any():
                if not df.isnull().values.any():
                    flag=True
                    for index in df.index:
                        schno=df['Scholar No'][index]
                        dob=df['DOB'][index]
                        sname=df['Student Name'][index]
                        yog=df['YOG'][index]
                        branch=df['Branch'][index]
                        try:
                            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                            cursor.execute('INSERT INTO `student` ( `Scholar_No`, `DOB`, `Student_Name`, `Branch`, `YOG`) VALUES (%s,%s,%s, %s, %s)',(schno,dob,sname,branch,yog,))
                            mysql.connection.commit()


                        except (MySQLdb.Error) as e:

                            flag=False

                    if flag:
                        mysql.connection.commit()


            else:
                flash("Invalid data")
                df1=pd.DataFrame()
                df=df1




    return render_template('file.html',df=df)

