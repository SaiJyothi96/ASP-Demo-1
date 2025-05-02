import datetime
import re

from flask import Flask, request, render_template, redirect, session
import pymysql
import os
conn = pymysql.connect(host="localhost", user="root", password="root", db="modern_agriculture")
cursor = conn.cursor()
app = Flask(__name__)
app.secret_key = "modern_agriculture"
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
APP_ROOT = APP_ROOT+"/static"

username = "admin"
password = "admin"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/admin_login")
def admin_login():
    return render_template("admin_login.html")


@app.route("/admin_login_action", methods=['post'])
def admin_login1():
    username = request.form.get("username")
    password = request.form.get("password")
    if username == username and password == password:
        session['role'] = 'admin'
        return redirect("/admin_home")
    return render_template("msg.html", message="Invalid Login Details")


@app.route("/admin_home")
def admin_home():
    return render_template("admin_home.html")


@app.route("/machinery_provider_login")
def machinery_provider_login():
    return render_template("machinery_provider_login.html")


@app.route("/machinery_provider_login_action", methods=['post'])
def machinery_provider_login_action():
    email = request.form.get("email")
    password = request.form.get("password")
    count = cursor.execute("select * from machinery_providers where email='" + str(email) + "' and password='" + str(password) + "' ")
    if count > 0:
        machinery_providers = cursor.fetchall()
        session['machinery_provider_id'] = machinery_providers[0][0]
        session['role'] = 'machinery_provider'
        return redirect("/machinery_provider_home")
    else:
        return render_template("msg.html", message="invalid login details")



@app.route("/machinery_provider_registration")
def machinery_provider_registration():
    cursor.execute("select * from locations")
    locations = cursor.fetchall()
    return render_template("machinery_provider_registration.html",locations=locations)


@app.route("/machinery_provider_registration_action", methods=['post'])
def machinery_provider_registration_action():
    location_id = request.form.get("location_id")
    print(location_id)
    name = request.form.get("name")
    email = request.form.get("email")
    phone = request.form.get("phone")
    password = request.form.get("password")
    address = request.form.get("address")
    count = cursor.execute("select * from machinery_providers where email='"+str(email)+"' and phone='"+str(phone)+"'")
    if count > 0:
        return render_template("msg.html", message="Duplicate entry")
    else :
        cursor.execute("insert into machinery_providers (location_id,name, email, phone, password, address) values('"+str(location_id)+"','"+str(name)+"','"+str(email)+"','"+str(phone)+"','"+str(password)+"','"+str(address)+"')")
        conn.commit()
        return render_template("msg.html", message="Machinery provider registered successfully")



@app.route("/machinery_provider_home")
def machinery_provider_home():
    return render_template("machinery_provider_home.html")


@app.route("/farmer_login")
def farmer_login():
    return render_template("farmer_login.html")


@app.route("/farmer_login_action", methods=['post'])
def farmer_login_action():
    email = request.form.get("email")
    password = request.form.get("password")
    count = cursor.execute("select * from farmers where email='" + str(email) + "' and password='" + str(password) + "' ")
    if count > 0:
        farmers = cursor.fetchall()
        session['farmer_id'] = farmers[0][0]
        session['role'] = 'farmer'
        return redirect("/farmer_home")
    else:
        return render_template("msg.html", message="invalid login details")



@app.route("/farmer_registration")
def farmer_registration():

    return render_template("farmer_registration.html")


@app.route("/farmer_registration_action", methods=['post'])
def farmer_registration_action():
    name = request.form.get("name")
    email = request.form.get("email")
    phone = request.form.get("phone")
    password = request.form.get("password")
    address = request.form.get("address")
    count = cursor.execute("select * from farmers where email='"+str(email)+"' and phone='"+str(phone)+"'")
    if count > 0:
        return render_template("msg.html", message="Duplicate entry")
    else :
        cursor.execute("insert into farmers (name, email, phone, password, address) values('"+str(name)+"','"+str(email)+"','"+str(phone)+"','"+str(password)+"','"+str(address)+"')")
        conn.commit()
        return render_template("msg.html", message="Farmer registered successfully")



@app.route("/farmer_home")
def farmer_home():
    return render_template("farmer_home.html")


@app.route("/view_machinery_provider")
def view_machinery_provider():
    machinery_provider_id = request.args.get("machinery_provider_id")
    cursor.execute("select * from machinery_providers where machinery_provider_id='"+str(machinery_provider_id)+"'")
    machinery_providers = cursor.fetchall()
    return render_template("view_machinery_provider.html",machinery_providers=machinery_providers,machinery_provider_id=machinery_provider_id,get_location_by_location_id=get_location_by_location_id)

def get_location_by_location_id(location_id):
    cursor.execute("select * from locations where location_id ='"+str(location_id)+"' ")
    locations = cursor.fetchone()
    print(locations)
    return locations


@app.route("/add_location")
def add_location():
    cursor.execute("select * from locations")
    locations = cursor.fetchall()
    return render_template("add_location.html",locations=locations)


@app.route("/add_location_action", methods=['post'])
def add_location_action():
    location_name = request.form.get("location_name")
    zipcode = request.form.get("zipcode")
    count = cursor.execute("select * from locations where zipcode='"+str(zipcode)+"' and location_name='"+str(location_name)+"' ")
    if count > 0:
        return render_template("msg.html", message="Duplicate entry")
    else :
        cursor.execute("insert into locations (location_name, zipcode) values('"+str(location_name)+"','"+str(zipcode)+"')")
        conn.commit()
        return redirect("/add_location")


@app.route("/add_machinery_types")
def add_machinery_types():
    cursor.execute("select * from machinery_types")
    machinery_types = cursor.fetchall()
    return render_template("add_machinery_types.html",machinery_types=machinery_types)


@app.route("/add_machinery_types_action", methods=['post'])
def add_machinery_types_action():
    machinery_type = request.form.get("machinery_type")
    count = cursor.execute("select * from machinery_types where machinery_type='"+str(machinery_type)+"' ")
    if count > 0:
        return render_template("msg.html", message="Duplicate entry")
    else :
        cursor.execute("insert into machinery_types (machinery_type) values('"+str(machinery_type)+"')")
        conn.commit()
        return redirect("/add_machinery_types")



@app.route("/add_machinery")
def add_machinery():
    role = session['role']
    from_date_time = request.args.get("from_date_time")
    to_date_time = request.args.get("to_date_time")
    machinery_type_id = request.args.get("machinery_type_id")
    machinery_name = request.args.get("machinery_name")
    if machinery_type_id == None:
        machinery_type_id = ""
    if machinery_name == None:
        machinery_name=""

    query = ""
    if from_date_time ==None:
        from_date_time = datetime.datetime.now()
        to_date_time = from_date_time+datetime.timedelta(days=1)

        from_date_time = str(from_date_time).split(" ")
        from_date_time[-1] = from_date_time[-1][:8]
        from_date_time = " ".join(from_date_time)
        from_date_time = datetime.datetime.strptime(str(from_date_time), "%Y-%m-%d %H:%M:%S")
        to_date_time = str(to_date_time).split(" ")
        to_date_time[-1] = to_date_time[-1][:8]
        to_date_time = " ".join(to_date_time)
        to_date_time = datetime.datetime.strptime(str(to_date_time), "%Y-%m-%d %H:%M:%S")

    else:
        from_date_time = from_date_time.replace("T"," ")
        from_date_time = datetime.datetime.strptime(str(from_date_time), "%Y-%m-%d %H:%M:%S")
        to_date_time = to_date_time.replace("T", " ")
        to_date_time = datetime.datetime.strptime(str(to_date_time), "%Y-%m-%d %H:%M:%S")

    count = cursor.execute("select * from bookings  where  status ='Booked' and((from_date_time >= '" + str(
        from_date_time) + "' and from_date_time<= '" + str(
        to_date_time) + "' and to_date_time >='" + str(
        from_date_time) + "' and to_date_time >= '" + str(
        to_date_time) + "') or (from_date_time <= '" + str(
        from_date_time) + "' and from_date_time <= '" + str(
        to_date_time) + "' and to_date_time >= '" + str(
        from_date_time) + "' and to_date_time <= '" + str(
        to_date_time) + "') or (from_date_time <= '" + str(
        from_date_time) + "' and from_date_time <= '" + str(
        to_date_time) + "' and to_date_time >= '" + str(
        from_date_time) + "' and to_date_time >= '" + str(
        to_date_time) + "') or (from_date_time <= '" + str(
        to_date_time) + "' and from_date_time <= '" + str(
        to_date_time) + "' and to_date_time <= '" + str(
        from_date_time) + "' and to_date_time >= '" + str(to_date_time) + "'))")
    if role == 'machinery_provider':
        machinery_provider_id = session['machinery_provider_id']
        query = "select * from machineries where machinery_provider_id='" + str(machinery_provider_id) + "'"
    elif role == 'admin':
        status = 'Not Verified'
        query = "select * from machineries where status = '"+str(status)+"'"
    elif role == 'farmer':
        status = 'Verified'
        bookings = cursor.fetchall()
        if machinery_name=="" and machinery_type_id=="":
             if(len(bookings))==0:
                query = "select * from machineries where status = '" + str(status) + "' "
             else:
                for booking in bookings:
                   query = "select * from machineries where status = '"+str(status)+"' and machinery_id!='"+str(booking[8])+"'"
        elif machinery_name!="" and machinery_type_id=="":
            if (len(bookings)) == 0:
                query = "select * from machineries where status = '" + str(status) + "' and machinery_name like '%" + machinery_name + "%'"
            else:
                for booking in bookings:
                    query = "select * from machineries where status = '" + str(status) + "' and machinery_id!='" + str(
                        booking[8]) + "' and  machinery_name like '%" + machinery_name + "%'"
        elif machinery_name=="" and machinery_type_id!="":
            if (len(bookings)) == 0:
                query = "select * from machineries where status = '" + str(status) + "' and machinery_type_id='"+str(machinery_type_id)+"' "
            else:
                for booking in bookings:
                    query = "select * from machineries where status = '" + str(status) + "' and machinery_id!='" + str(
                        booking[8]) + "' and machinery_type_id='"+str(machinery_type_id)+"'"
    cursor.execute(query)
    machineries = cursor.fetchall()
    cursor.execute("select * from machinery_types")
    machinery_types = cursor.fetchall()
    return render_template("add_machinery.html",machineries=machineries,machinery_types=machinery_types,from_date_time=from_date_time,to_date_time=to_date_time,get_machinery_type_by_machinery_type_id=get_machinery_type_by_machinery_type_id,get_machinery_provider_by_machinery_provider_id=get_machinery_provider_by_machinery_provider_id)


def get_machinery_type_by_machinery_type_id(machinery_type_id):
    cursor.execute("select * from machinery_types where machinery_type_id ='"+str(machinery_type_id)+"' ")
    machinery_types = cursor.fetchone()
    print(machinery_types)
    return machinery_types

def get_machinery_provider_by_machinery_provider_id(machinery_provider_id):
    cursor.execute("select * from machinery_providers where machinery_provider_id ='"+str(machinery_provider_id)+"' ")
    machinery_providers = cursor.fetchone()
    print(machinery_providers)
    return machinery_providers



@app.route("/add_machinery1")
def add_machinery1():
    cursor.execute("select * from machinery_types")
    machinery_types = cursor.fetchall()
    return render_template("add_machinery1.html",machinery_types=machinery_types)


@app.route("/add_machinery1_action", methods=['post'])
def add_machinery1_action():
    machinery_provider_id = session['machinery_provider_id']
    machinery_type_id = request.form.get("machinery_type_id")
    print(machinery_type_id)
    machinery_name = request.form.get("machinery_name")
    picture = request.files['picture']
    path = APP_ROOT + "/" + picture.filename
    picture.save(path)
    price_per_hour = request.form.get("price_per_hour")
    description = request.form.get("description")
    status = request.form.get("status")
    cursor.execute("insert into machineries(machinery_provider_id,machinery_type_id, machinery_name, picture, price_per_hour, description,status) values('"+str(machinery_provider_id)+"','"+str(machinery_type_id)+"','"+str(machinery_name)+"','"+str(picture.filename)+"','"+str(price_per_hour)+"','"+str(description)+"','Not Verified')")
    conn.commit()
    return redirect("/add_machinery")


@app.route("/verify_machinery")
def verify_machinery():
    machinery_id = request.args.get("machinery_id")
    cursor.execute("update machineries set status = 'Verified' where machinery_id = '" + str(machinery_id) + "'")
    conn.commit()
    return redirect("/add_machinery")


@app.route("/book_machinery")
def book_machinery():
    machinery_id = request.args.get("machinery_id")
    cursor.execute("select * from machineries where machinery_id='"+str(machinery_id)+"'")
    machineries = cursor.fetchone()
    from_date_time = request.args.get("from_date_time")
    to_date_time = request.args.get("to_date_time")
    from_date_time = from_date_time.replace("T", " ")
    from_date_time = datetime.datetime.strptime(str(from_date_time), "%Y-%m-%d %H:%M:%S")
    to_date_time = to_date_time.replace("T", " ")
    to_date_time = datetime.datetime.strptime(str(to_date_time), "%Y-%m-%d %H:%M:%S")

    diff = to_date_time - from_date_time
    days = diff.days
    seconds = diff.seconds
    hours = days * 24 + seconds // 3600
    total_price = 0
    print(hours)
    if hours > 0:
      total_price = total_price +  float(machineries[3]) * float(hours)

    if hours <24:
        days = days+1

    cursor.execute(
        "insert into bookings(date,from_date_time,to_date_time,status,total_price,farmer_id,machinery_id) values('" + str(
            datetime.datetime.now()) + "','" + str(from_date_time) + "','" + str(to_date_time) + "','Payment Pending','" + str(
            total_price) + "','" + str(session['farmer_id']) + "','" + str(machinery_id) + "')")
    conn.commit()
    booking_id = cursor.lastrowid
    cursor.execute("select * from bookings where booking_id='"+str(cursor.lastrowid)+"'")
    booking = cursor.fetchone()
    return render_template("payment.html",days=days,booking=booking,booking_id=booking_id,stotal_price=total_price,machinery_id=machinery_id,machinery=machineries,get_farmer_by_farmer_id=get_farmer_by_farmer_id,get_machinery_by_machinery_id=get_machinery_by_machinery_id,int=int,float=float)



# @app.route("/book_machinery_action")
# def book_machinery_action():
#     machinery_id = request.args.get("machinery_id")
#     machinery = "select * from machineries where machinery_id='"+str(machinery_id)+"'"
#     farmer_id = session['farmer_id']
#     date = datetime.datetime.now()
#     from_date_time = request.args.get("from_date_time")
#     to_date_time = request.args.get("to_date_time")
#     from_date_time2 = datetime.datetime.strptime(from_date_time, "%Y-%m-%dT%H:%M")
#     to_date_time2 = datetime.datetime.strptime(to_date_time, "%Y-%m-%dT%H:%M")
#     diff = to_date_time2 - from_date_time2
#     days = diff.days
#     seconds = diff.seconds
#     hours = int(seconds/60)
#     if hours > 0:
#         days = days + 1
#     total_price = int(machinery[3]) * days
#     cursor.execute("insert into bookings(date,from_date_time,to_date_time,status,total_price,farmer_id,machinery_id) values('"+str(date)+"','"+str(from_date_time2)+"','"+str(to_date_time2)+"','Payment Pending','"+str(total_price)+"','"+str(farmer_id)+"','"+str(machinery_id)+"')")
#     conn.commit()
#     return render_template("payment.html",machinery_id=machinery_id,machinery=machinery,get_farmer_by_farmer_id=get_farmer_by_farmer_id,get_machinery_by_machinery_id=get_machinery_by_machinery_id,int=int,float=float)

def get_farmer_by_farmer_id(farmer_id):
    cursor.execute("select * from farmers where farmer_id ='"+str(farmer_id)+"' ")
    farmers = cursor.fetchall()
    return farmers[0]

def get_machinery_by_machinery_id(machinery_id):
    cursor.execute("select * from machineries where machinery_id ='"+str(machinery_id)+"' ")
    machineries = cursor.fetchall()
    return machineries[0]


@app.route("/payment_action")
def payment_action():
    farmer_id = session['farmer_id']
    booking_id = request.args.get("booking_id")
    card_type = request.args.get("card_type")
    card_number = request.args.get("card_number")
    date = datetime.datetime.now()
    card_holder_name = request.args.get("card_holder_name")
    cvv = request.args.get("cvv")
    expiry_date = request.args.get("expiry_date")
    amount = request.args.get("amount")
    cursor.execute("insert into payments(farmer_id, booking_id, card_type,card_number, date, card_holder_name, cvv, expiry_date, amount,status) values('" + str(farmer_id) + "','" + str(booking_id) + "','" + str(card_type) + "','" + str(card_number) + "','" + str(date) + "','" + str(card_holder_name) + "','" + str(cvv) + "','" + str(expiry_date) + "','" + str(amount) + "','Paid')")
    conn.commit()
    cursor.execute("update bookings set status = 'Booked' where booking_id='" + str(booking_id) + "'")
    conn.commit()
    return render_template("msg.html",message="payment Successful")


@app.route("/view_bookings")
def view_bookings():
    machinery_id =request.args.get("machinery_id")
    sql = ""
    if machinery_id==None:
        if session['role'] =='machinery_provider':
            sql = "select * from bookings where machinery_id in(select machinery_id from machineries where machinery_provider_id='"+str(session['machinery_provider_id'])+"')"
        elif session['role'] =='farmer':
         sql = "select * from bookings where farmer_id='"+str(session['farmer_id'])+"'"
    else:
        sql = "select * from bookings where machinery_id='"+str(machinery_id)+"'"
    cursor.execute(sql)
    bookings = cursor.fetchall()
    return render_template("view_bookings.html",bookings=bookings,get_farmer_by_farmer_id=get_farmer_by_farmer_id,get_machinery_by_machinery_id=get_machinery_by_machinery_id)


@app.route("/view_payments")
def view_payments():
    booking_id = request.args.get("booking_id")
    cursor.execute("select * from payments where booking_id= '"+str(booking_id)+"'")
    payments = cursor.fetchall()
    return render_template("view_payments.html",payments=payments)


@app.route("/pay_remaining_amount")
def pay_remaining_amount():
    booking_id = request.args.get("booking_id")
    cursor.execute("select * from bookings where booking_id= '" + str(booking_id) + "'")
    bookings = cursor.fetchall()
    return render_template("pay_remaining_amount.html",booking=bookings[0],int=int,float=float)


@app.route("/pay_remaining_amount_action")
def pay_remaining_amount_action():
    farmer_id = session['farmer_id']
    booking_id = request.args.get("booking_id")
    card_type = request.args.get("card_type")
    card_number = request.args.get("card_number")
    date = datetime.datetime.now()
    card_holder_name = request.args.get("card_holder_name")
    cvv = request.args.get("cvv")
    expiry_date = request.args.get("expiry_date")
    amount = request.args.get("amount")
    cursor.execute("insert into payments(farmer_id, booking_id, card_type,card_number, date, card_holder_name, cvv, expiry_date, amount,status) values('" + str(farmer_id) + "','" + str(booking_id) + "','" + str(card_type) + "','" + str(card_number) + "','" + str(date) + "','" + str(card_holder_name) + "','" + str(cvv) + "','" + str(expiry_date) + "','" + str(amount) + "','Paid')")
    conn.commit()
    cursor.execute("update bookings set status = 'Return' where booking_id='" + str(booking_id) + "'")
    conn.commit()
    return render_template("msg.html",message="payment Successful")

@app.route("/cancel_booking")
def cancel_booking():
    booking_id = request.args.get("booking_id")
    cursor.execute("update bookings set status = 'Cancelled' where booking_id = '" + str(booking_id) + "'")
    conn.commit()
    return redirect("/view_bookings")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


app.run(debug=True)

