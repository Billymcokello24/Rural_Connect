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

from app import mysql, send_sms_notification, send_email_notification_provider


def mark_done():
    if request.method == 'POST':
        # Fetch form data

        service_id = request.form['service_id']
        name = request.form['name']
        email = request.form['email']
        phone_number = request.form['phonenumber']

        try:
            # Create cursor
            cur = mysql.connection.cursor()

            # Insert data into the database
            cur.execute(
                "INSERT INTO mark_done (service_id,name,email, phonenumber) VALUES ( %s, %s, %s, %s)",
                (service_id, name, email, phone_number))

            cur.execute("DELETE FROM book_service WHERE service_id = %s", (service_id,))

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
            send_sms_notification(phone_number)
            send_sms_notification(service_provider_phonenumber)
            # Send email notification to both client and service provider
            send_email_notification_provider(email)
            send_email_notification_provider(service_provider_email)

            return "Booking successful! You will receive a confirmation soon."
        except Exception as e:
            return str(e)

    return render_template("Pages/mark_done.html")
