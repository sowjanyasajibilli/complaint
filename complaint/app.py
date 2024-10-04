from flask import Flask, render_template, request, session, redirect, url_for, flash
import mysql.connector
import datetime
import smtplib
app=Flask(__name__)
app.secret_key="chandra"
@app.route("/",methods=['GET','POST'])
def hello():
    if request.method=='POST':
        email = request.form.get("email")
        complaint = request.form.get("complaint")
        try:
            server=smtplib.SMTP('smtp.gmail.com',587)
            server.starttls()
            server.login('SENDER G-MAIL','SENDER G-MAIL APP PASSWORD')
            server.sendmail('SENDER G-MAIL',email,f'Hello your complaint has recieved as.......\n {complaint}')
        except:
            flash("The given Gmail was incorrect please enter a valid Gmail",'danger')
            return redirect(url_for('hello'))
        print(email)
        print(complaint)
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="chandrakiran",
            database="complaint"
        )
        mycursor = mydb.cursor()
        sql = "INSERT INTO complaint(email,complaint,date) VALUES (%s, %s,%s)"
        val = (email,complaint,datetime.date.today())
        mycursor.execute(sql, val)
        mydb.commit()
        flash(f'Your complaint has been submited', 'success')
        return redirect(url_for('hello'))
    return render_template('send.html')
@app.route("/admin",methods=['GET','POST'])
def admin():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="chandrakiran",
        database="complaint"
    )
    cursor = mydb.cursor()
    query = "SELECT * FROM complaint"
    cursor.execute(query)
    data1 = cursor.fetchall()
    cursor.close()
    #print(data)
    return render_template('admin.html',data=data1)
@app.route("/inprogress/<int:complaint_id>,<string:email>,<string:complaint>",methods=['GET','POST'])
def inprogress(complaint_id,email,complaint):
    server=smtplib.SMTP('smtp.gmail.com',587)
    server.starttls()
    server.login('SENDER G-MAIL','SENDER G-MAIL APP PASSWORD')
    server.sendmail('SENDER G-MAIL',email,f'Hello.....The complaint you sent was now under progress.......\n {complaint}')
    flash("Update sent as the complaint is in progress",'success')
    return redirect(url_for('admin'))
@app.route("/solved/<int:complaint_id>,<string:email>,<string:complaint>",methods=['GET','POST'])
def solved(complaint_id,email,complaint):
    mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="chandrakiran",
            database="complaint"
        )
    mycursor = mydb.cursor()
    sql = "delete from complaint where id=(%s)"
    val = (complaint_id,)
    mycursor.execute(sql, val)
    mydb.commit()
    server=smtplib.SMTP('smtp.gmail.com',587)
    server.starttls()
    server.login('SENDER G-MAIL','SENDER G-MAIL APP PASSWORD')
    server.sendmail(f'SENDER G-MAIL',email,f'Hello........The complaint you sent was solved now.......\n {complaint}')
    flash("Update sent as the complaint has solved",'success')
    return redirect(url_for('admin'))
if __name__ == "__main__":
    app.run(debug=True)