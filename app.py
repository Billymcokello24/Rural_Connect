# app.py
import base64
import io
from datetime import datetime
from decimal import Decimal

import yagmail
from PIL import Image
from africastalking.AfricasTalkingGateway import AfricasTalkingGateway, AfricasTalkingGatewayException
from flask import Flask, render_template, request, redirect, url_for, session, jsonify, json, flash
from flask_mail import Mail, Message
from flask_mysqldb import MySQL
from flask_socketio import SocketIO, emit

import MySQLdb.cursors
import MySQLdb.cursors, re, hashlib
from werkzeug.security import generate_password_hash

from Client import Register, Login, Client_payments, Book_service
from Service_provider import Provider_register, Provider_dashboard, My_payments, Provider_bookings, Add_service, \
    Provider_login, Mark_done
from Service_provider.Provider_login import providers_login
from payments import Process_payments

app = Flask(__name__)
app.secret_key = 'your secret key'
socketio = SocketIO(app)

# Enter your database connection details below
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Billy39016716...'
app.config['MYSQL_DB'] = 'RuralConnect'

mail = Mail(app)

username = "RuralConnect"
api_key = "d811c9c7b262a131121d328f5b5d36220f0da1c1034bc6e788cc410b1b6d9442"
phone_number = "+254759814390"

gmail_username = "cloudpioneercodinghub@gmail.com"
gmail_app_password = "eeip dvha lgwn qrtj"
yag = yagmail.SMTP(gmail_username, gmail_app_password)

# Intialize MySQL
mysql = MySQL(app)

from collections import defaultdict


@app.route('/')
def home():
    return render_template('index.html')


@socketio.on('service_added')
def handle_service_added(data):
    # Broadcast new service to all clients
    socketio.emit('new_service', data, broadcast=True)


@app.route("/client_dashboard/add_tokens", methods=["GET", "POST"])
def add_tokens():
    if request.method == 'POST':
        id_number = request.form[
            'id_number']  # Assuming you have a function to retrieve the id_number of the logged-in user
        phone_number = request.form['phonenumber']
        amount = request.form['Amount']

        # Create cursor
        cur = mysql.connection.cursor()

        # Insert data into the add_tokens table
        cur.execute(
            "INSERT INTO add_tokens (id_number, phonenumber, Amount) VALUES (%s, %s, %s)",
            (id_number, phone_number, amount)
        )
        mysql.connection.commit()

        # Retrieve all records from the add_tokens table for the logged-in user
        cur.execute(
            "SELECT id_number, SUM(Amount) FROM add_tokens GROUP BY id_number"
        )
        user_tokens_data = cur.fetchall()

        # Dictionary to store aggregated user token amounts
        aggregated_tokens = defaultdict(int)
        for row in user_tokens_data:
            aggregated_tokens[row[0]] += row[1]

        # Clear existing data from user_tokens table
        cur.execute("DELETE FROM user_tokens")

        # Insert aggregated data into user_tokens table
        for id_number, total_amount in aggregated_tokens.items():
            cur.execute(
                "INSERT INTO user_tokens (id_number, Amount) VALUES (%s, %s)",
                (id_number, total_amount)
            )
        mysql.connection.commit()

        # Close connection
        cur.close()

    return render_template("Pages/add_tokens.html")


@app.route("/client_dashboard/pay", methods=["POST"])
def process_payment():
    Process_payments.process_payment()


def count_bookings(id_number):
    try:
        # Connect to the database
        cursor = mysql.connection.cursor()

        # Query to count the number of bookings for the specific user
        cursor.execute("SELECT COUNT(*) FROM book_service WHERE id_number = %s", (id_number,))
        booking_count = cursor.fetchone()[0]

        # Close the cursor
        cursor.close()

        return booking_count
    except Exception as e:
        # Handle any exceptions, such as database errors
        print("Error counting bookings:", e)
        return 0  # Return 0 if an error occurs


def my_service_count(id_number):
    try:
        # Connect to the database
        cursor = mysql.connection.cursor()

        # Query to count the number of bookings for the specific user
        cursor.execute("SELECT COUNT(*) FROM services WHERE id_number = %s", (id_number,))
        booking_count = cursor.fetchone()[0]

        # Close the cursor
        cursor.close()

        return booking_count
    except Exception as e:
        # Handle any exceptions, such as database errors
        print("Error counting bookings:", e)
        return 0  # Return 0 if an error occurs


def service_counts():
    try:
        # Connect to the database
        cursor = mysql.connection.cursor()

        # Query to count available services
        cursor.execute("SELECT COUNT(*) FROM services")

        # Fetch the count
        service_count = cursor.fetchone()[0]

        # Close the cursor
        cursor.close()

        # Render the dashboard template with the service count
        return service_count
    except Exception as e:
        # Handle any exceptions, such as database errors
        return str(e)


def show_service():
    try:
        # Connect to the database
        cursor = mysql.connection.cursor()

        # Query to count available services
        cursor.execute("SELECT * FROM services")

        # Fetch the count
        services = cursor.fetchall()

        # Close the cursor
        cursor.close()

        # Render the dashboard template with the service count
        return services
    except Exception as e:
        # Handle any exceptions, such as database errors
        return str(e)


def booking_counts():
    try:
        # Connect to the database
        cursor = mysql.connection.cursor()

        # Query to count available services
        cursor.execute("SELECT COUNT(*) FROM book_service")

        # Fetch the count
        book_count = cursor.fetchone()[0]

        # Close the cursor
        cursor.close()

        # Render the dashboard template with the service count
        return book_count
    except Exception as e:
        # Handle any exceptions, such as database errors
        return str(e)


def send_sms_notification(to_phone_number):
    try:
        gateway = AfricasTalkingGateway(username, api_key)
        # Send notification to the service provider
        message = (
            f"Hello ! Someone is interested in your service. "
        )
        recipients = [to_phone_number]
        gateway.sendMessage(recipients, message)

        return True
    except AfricasTalkingGatewayException as e:
        print(f"Error sending SMS: {e}")
        return False


def send_email_notification(email):
    try:
        # Compose email
        subject = "New Booking Notification"
        body = f"Hello,\n\nYour Booking is successfully recieved. The service Provider will get to you shortly.\n\nRegards,\n RuralConnect Admin"

        # Send email
        yag.send(email, subject, body)

        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False


def send_email_notification_provider(email):
    try:
        # Compose email
        subject = "Confirmation Email"
        body = (f"Hello,\n\nThanks for booking a service with us. \n\n "
                f"It was nice service you.Keep connected to RuralConnect for more services\n\nRegards,\n RuralConnect Admin")

        # Send email
        yag.send(email, subject, body)

        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False


def client_screen():
    # Fetch uploaded service data from the database
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM services")
    services = cursor.fetchall()
    cursor.close()
    return render_template('services.html', services=services)


@app.route('/provider_screen')
def providers_screen():
    try:
        # Connect to the database
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        # Query to fetch all services
        cursor.execute("SELECT * FROM services")

        # Fetch all services
        services = cursor.fetchall()

        # Close the cursor
        cursor.close()

        # Convert images to base64 strings
        for service in services:
            image_path = service['image']
            if image_path:  # Ensure there is a valid image path
                with open(image_path, 'rb') as f:
                    img = Image.open(f)
                    img_byte_array = io.BytesIO()
                    img.save(img_byte_array, format=img.format)
                    img_base64 = base64.b64encode(img_byte_array.getvalue()).decode('utf-8')
                    service['image_base64'] = img_base64

        return render_template('Pages/my_services.html', services=services)

    except Exception as e:
        return str(e)


@socketio.on('service_added')
def handle_service_added(data):
    # Broadcast new service to all clients
    socketio.emit('new_service', data, broadcast=True)


@app.route('/upload_service')
def upload_service():
    return render_template('Pages/upload.html')


@app.route("/services/<category>")
def services_by_category(category):
    try:
        # Fetch services from the database based on the selected category
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT * FROM services WHERE category = %s", (category,))
        services = cur.fetchall()
        cur.close()

        for service in services:
            with open(service['image'], "rb") as img_file:
                service['image_base64'] = base64.b64encode(img_file.read()).decode('utf-8')

        # Render HTML template with the fetched services
        return render_template('Pages/services_by_category.html', services=services, category=category)
    except Exception as e:
        return str(e)


@app.route('/add_service', methods=['POST', 'GET'])
def add_service():
    Add_service.add_service()


@app.route('/provider/bookings')
def provider_bookings():
    Provider_bookings.provider_bookings()


@app.route('/client_dashboard/check_payments')
def client_payments():
    Client_payments.client_payments()


@app.route('/provider/check_payments')
def check_payments():
    return render_template("Pages/payments.html")


@app.route('/provider/payments')
def my_payments():
    My_payments.my_payments()


@app.route('/mark_done', methods=['POST', 'GET'])
def mark_done():
   Mark_done.mark_done()


@app.route('/book_service', methods=['POST', 'GET'])
def book_service():
    Book_service.book_service()


@app.route('/Available_bookings')
def available_bookings():
    return render_template('Pages/provider_booking.html')


@app.route('/my_services')
def my_services():
    return render_template('Pages/my_services.html')


@app.route('/delete_service', methods=['POST'])
def delete_service():
    if request.method == 'POST':
        # Fetch service ID from the form data
        service_id = request.form['service_id']

        try:
            # Create cursor
            cur = mysql.connection.cursor()

            # Delete associated records in the mark_done table
            cur.execute("DELETE FROM mark_done WHERE service_id = %s", (service_id,))

            # Then, delete the service from the services table
            cur.execute("DELETE FROM services WHERE service_id = %s", (service_id,))

            # Commit to DB
            mysql.connection.commit()

            # Close connection
            cur.close()

            # Redirect to the provider screen after deletion
            return redirect(url_for('providers_screen'))

        except Exception as e:
            # Handle any exceptions, such as database errors
            return str(e)


@app.route('/bookings_page')
def bookings():
    return render_template('Pages/bookings.html')


@app.route('/client_screen')
def client_screen():
    try:
        # Connect to the database
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        # Query to fetch all services
        cursor.execute("SELECT * FROM services")

        # Fetch all services
        services = cursor.fetchall()

        # Close the cursor
        cursor.close()

        # Convert images to base64 strings
        for service in services:
            image_path = service['image']
            if image_path:  # Ensure there is a valid image path
                with open(image_path, 'rb') as f:
                    img = Image.open(f)
                    img_byte_array = io.BytesIO()
                    img.save(img_byte_array, format=img.format)
                    img_base64 = base64.b64encode(img_byte_array.getvalue()).decode('utf-8')
                    service['image_base64'] = img_base64

        # Render the client screen template with the services data
        return render_template('Pages/services.html', services=services)

    except Exception as e:
        return str(e)


@app.route('/display_service_providers')
def display_service_providers():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM services')
        providers = cursor.fetchall()
        return render_template("services.html", providers=providers)
    return redirect(url_for('login'))


def get_username_from_db_client():
    if 'username' in session:
        cur = mysql.connection.cursor()
        cur.execute("SELECT username FROM Auth WHERE username = %s", (session['username'],))
        username = cur.fetchone()[0]  # Assuming username is unique
        cur.close()
        return username
    return None


@app.route('/book')
def book():
    return render_template("Pages/book_service.html")


@app.route('/client_sign_out')
def sign_out_client():
    session.pop('username')
    return redirect(url_for('login'))


@app.route('/provider_sign_out')
def sign_out_provider():
    session.pop('username')
    return redirect(url_for('provider_login'))


@app.route("/update", methods=['GET', 'POST'])
def updateClient():
    msg = ''
    if 'loggedin' in session:
        if request.method == 'POST' and 'name' in request.form and 'email' in request.form and 'username' in request.form and 'password' in request.form:
            username = request.form['username']
            password = request.form['password']
            email = request.form['email']
            name = request.form['name']
            profile_image = request.form['profile_image']
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute(
                'SELECT * FROM Auth WHERE username = % s',
                (username,))
            account = cursor.fetchone()
            if account:
                msg = 'Account already exists !'
            elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
                msg = 'Invalid email address !'
            elif not re.match(r'[A-Za-z0-9]+', username):
                msg = 'name must contain only characters and numbers !'
            else:
                cursor.execute('UPDATE accounts SET username =% s,\
                password =% s, email =% s, organisation =% s, \
                address =% s, city =% s, state =% s, \
                country =% s, postalcode =% s WHERE id =% s', (
                    username, password, email, name,
                    profile_image,
                    (session['id'],),))
                mysql.connection.commit()
                msg = 'You have successfully updated !'
                return render_template("Pages/userProfile.html", msg=msg)
        elif request.method == 'POST':
            msg = 'Please fill out the form !'
        return render_template("Pages/userProfile.html", msg=msg)
    return redirect(url_for('login'))


@app.route('/display_client')
def display1():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM Auth WHERE id = % s',
                       (session['id'],))
        Auth = cursor.fetchone()
        return render_template("Pages/userProfile.html", Auth=Auth)
    return redirect(url_for('login'))


@app.route('/display_provider')
def display2():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM provider_auth WHERE id = % s',
                       (session['id'],))
        provider = cursor.fetchone()
        return render_template("Pages/providerProfile.html", provider=provider)
    return redirect(url_for('provider_login'))


@app.route('/login/home')
def dashboard():
    return dashboard.dashboard()


def get_id_provider():
    if 'loggedin' in session:
        try:
            # Connect to the database
            cursor = mysql.connection.cursor()

            # Retrieve the id_number of the logged-in user using their username
            cursor.execute("SELECT id_number FROM provider_auth WHERE username = %s", (session['username'],))
            id_number = cursor.fetchone()[0]  # Assuming username is unique, fetch the first result

            # Close the cursor
            cursor.close()

            return id_number
        except Exception as e:
            # Handle any exceptions, such as database errors
            print("Error fetching id_number:", e)
            return None  # Return None if an error occurs


@app.route('/my_services')
def my_servicess():
    if 'loggedin' in session:
        try:
            # Get the id_number of the logged-in user
            id_number = get_id_provider()

            if id_number:
                # Connect to the database
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

                # Query to fetch bookings for the logged-in user
                cursor.execute("SELECT * FROM services WHERE id_number = %s", (id_number,))
                services = cursor.fetchall()

                # Close the cursor
                cursor.close()

                # Render the template with the bookings data
                return render_template('Pages/my_services.html', servicess=services)
            else:
                flash('Failed to retrieve user information.', 'error')
                return redirect(url_for('login'))
        except Exception as e:
            # Handle database errors
            flash('Error retrieving bookings: ' + str(e), 'error')
            return redirect(url_for('login'))
    else:
        # If user is not logged in, redirect to login page
        return redirect(url_for('login'))


@app.route('/my_bookings')
def my_bookings():
    if 'loggedin' in session:
        try:
            # Get the id_number of the logged-in user
            id_number = get_id()

            if id_number:
                # Connect to the database
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

                # Query to fetch bookings for the logged-in user
                cursor.execute("SELECT * FROM book_service WHERE id_number = %s", (id_number,))
                bookings = cursor.fetchall()

                # Close the cursor
                cursor.close()

                # Render the template with the bookings data
                return render_template('Pages/my_bookings.html', bookings=bookings)
            else:
                flash('Failed to retrieve user information.', 'error')
                return redirect(url_for('login'))
        except Exception as e:
            # Handle database errors
            flash('Error retrieving bookings: ' + str(e), 'error')
            return redirect(url_for('login'))
    else:
        # If user is not logged in, redirect to login page
        return redirect(url_for('login'))


@app.route('/delete_booking', methods=['POST'])
def delete_booking():
    if request.method == 'POST':
        # Fetch service ID from the form data
        service_id = request.form['service_id']

        try:
            # Create cursor
            cur = mysql.connection.cursor()

            # Delete associated records in the mark_done table
            cur.execute("DELETE FROM book_service WHERE service_id = %s", (service_id,))

            # Then, delete the service from the services table
            cur.execute("DELETE FROM book_service WHERE service_id = %s", (service_id,))

            # Commit to DB
            mysql.connection.commit()

            # Close connection
            cur.close()

            # Redirect to the provider screen after deletion
            return redirect(url_for('my_bookings'))

        except Exception as e:
            # Handle any exceptions, such as database errors
            return str(e)


def get_id():
    if 'loggedin' in session:
        try:
            # Connect to the database
            cursor = mysql.connection.cursor()

            # Retrieve the id_number of the logged-in user using their username
            cursor.execute("SELECT id_number FROM Auth WHERE username = %s", (session['username'],))
            id_number = cursor.fetchone()[0]  # Assuming username is unique, fetch the first result

            # Close the cursor
            cursor.close()

            return id_number
        except Exception as e:
            # Handle any exceptions, such as database errors
            print("Error fetching id_number:", e)
            return None  # Return None if an error occurs
    else:
        return None  # Return None if the user is not logged in


def get_username_from_db_client():
    if 'username' in session:
        cur = mysql.connection.cursor()
        cur.execute("SELECT username FROM Auth WHERE username = %s", (session['username'],))
        username = cur.fetchone()[0]  # Assuming username is unique
        cur.close()
        return username
    return None


def get_username_from_db_provider():
    if 'username' in session:
        cur = mysql.connection.cursor()
        cur.execute("SELECT username FROM provider_auth WHERE username = %s", (session['username'],))
        username = cur.fetchone()[0]  # Assuming username is unique
        cur.close()
        return username
    return None


@app.route("/provider_dashboard/Home")
def provider_dashboard():
    Provider_dashboard.provider_dashboard()


@app.route('/login/', methods=['GET', 'POST'])
def login():
    Login.login()


@app.route("/contact")
def contact():
    return render_template('contact.html')


@app.route("/login/register", methods=['GET', 'POST'])
def register():
    Register.register()


@app.route('/provider_login/', methods=['GET', 'POST'])
def provider_login():
    Provider_login.providers_login()


@app.route("/provider_login/provider_register", methods=['GET', 'POST'])
def provider_register():
   Provider_register.provider_register()


@app.route("/about/")
def about():
    return render_template('about.html')


@app.route("/services")
def services():
    return render_template('services.html')


@app.route("/Bookings")
def Bookings():
    return render_template('bookings.html')


@app.route("/details")
def details():
    return render_template('bookingsDetails.html')


@app.route("/Payments")
def Payments():
    return render_template('team.html')


@app.route("/blog")
def blog():
    return render_template('blog.html')


@app.route("/payment")
def payment():
    return render_template('payments.html')


@app.route("/beauty")
def beauty():
    return render_template('Services/beauty.html')


@app.route("/plumbing")
def plumbing():
    return render_template('Services/Plumbing.html')


@app.route("/Carpentry")
def carpentry():
    return render_template('Services/capentry.html')


@app.route("/education")
def education():
    return render_template('Services/education.html')


@app.route("/veterinary")
def veterinary():
    return render_template('Services/veterinary.html')


@app.route("/userProfile")
def userProfile():
    return render_template('Pages/userProfile.html')


@app.route("/providerProfile")
def providerProfile():
    return render_template('Pages/providerProfile.html')


@app.route("/available_services")
def available_services():
    return render_template('Pages/services.html')


if __name__ == '__main__':
    socketio.run(app, debug=True)
