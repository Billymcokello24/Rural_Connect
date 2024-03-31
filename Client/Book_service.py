import base64
import io
import re
from datetime import datetime
from decimal import Decimal

import MySQLdb
import yagmail
from PIL import Image
from africastalking.AfricasTalkingGateway import AfricasTalkingGateway, AfricasTalkingGatewayException
from flask import Flask, render_template, request, redirect, url_for, session, jsonify, json, flash
from flask_mail import Mail, Message
from flask_mysqldb import MySQL
from flask_socketio import SocketIO, emit

from app import mysql, send_sms_notification, send_email_notification


def book_service():
    if request.method == 'POST':
        # Fetch form data
        id_no = request.form['id_number']
        service_id = request.form['service_id']
        service_name = request.form['service_booked']
        amount_payable = request.form['Amount_Payable']
        name = request.form['name']
        client_email = request.form['email']
        client_phonenumber = request.form['phonenumber']
        location = request.form['location']
        urgency = request.form['urgency']

        try:
            # Create cursor
            cur = mysql.connection.cursor()

            # Insert data into the database
            cur.execute(
                "INSERT INTO book_service (id_number,service_id,service_booked,Amount_Payable,name, email, phonenumber, location, urgency) VALUES (%s,%s,%s,%s,%s, %s, %s, %s, %s)",
                (id_no, service_id, service_name, amount_payable, name, client_email, client_phonenumber, location,
                 urgency))

            # Commit to DB
            mysql.connection.commit()

            # Fetch service provider's email and phone number from the database
            # Fetch service provider's email and phone number from the database
            # Fetch service provider's email and phone number from the database
            cur.execute("SELECT email, phonenumber FROM services")
            service_provider_info = cur.fetchone()
            service_provider_email = service_provider_info[0]  # Access email by index 0
            service_provider_phonenumber = service_provider_info[1]  # Access phone number by index 1

            # Close connection
            cur.close()

            # Send SMS notification to both client and service provider
            send_sms_notification(client_phonenumber)
            send_sms_notification(service_provider_phonenumber)
            # Send email notification to both client and service provider
            send_email_notification(client_email)
            send_email_notification(service_provider_email)

        except Exception as e:
            return str(e)

    return render_template("Pages/book_service.html")
