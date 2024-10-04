from flask import Flask, render_template, request, session, redirect, url_for, flash
import mysql.connector
import datetime
import smtplib
app=Flask(__name__)
app.secret_key="chandra"
@app.route("/",methods=['GET','POST'])
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
    data = cursor.fetchall()
    cursor.close()
    #print(data)
    return render_template('admin.html',data=data)
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
    server.sendmail('SENDER G-MAIL',email,f'Hello........The complaint you sent was solved now.......\n {complaint}')
    flash("Update sent as the complaint has solved",'success')
    return redirect(url_for('admin'))
if __name__ == "__main__":
    app.run(debug=True)