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

from app import mysql, socketio


def add_service():
    if request.method == 'POST':
        # Fetch form data
        service_id = request.form['service_id']
        image = request.files['image']
        name = request.form['name']
        category = request.form['category']
        description = request.form['description']
        Amt = request.form['Amount']
        email = request.form['email']
        phonenumber = request.form['phonenumber']
        location = request.form['location']
        status = request.form['status']

        # Save image to a location or store its path in the database
        # For simplicity, let's assume we're saving the image to a folder named "uploads" in the same directory
        image_path = f"templates/Pages/uploads/{image.filename}"
        image.save(image_path)

        try:
            cur = mysql.connection.cursor()
            cur.execute(
                "INSERT INTO services (service_id,image, name, category, description,Amount, email, phonenumber, location, status) VALUES (%s,%s,%s, %s, %s, %s, %s, %s, %s, %s)",
                (service_id, image_path, name, category, description, Amt, email, phonenumber, location, status))
            mysql.connection.commit()
            cur.close()

            socketio.emit('new_service_notification', {'message': 'A new service has been added!'})

            # Check if the category table exists, if not create it
            category = category.replace(' ', '_')
            cur = mysql.connection.cursor()
            cur.execute(f"SHOW TABLES LIKE '{category}'")
            result = cur.fetchone()
            if not result:
                # Create the category table
                cur.execute(
                    f"CREATE TABLE {category} (id INT AUTO_INCREMENT PRIMARY KEY, service_id VARCHAR(255), image BLOB, name VARCHAR(255),  description TEXT, Amount VARCHAR(255), email VARCHAR(255), phonenumber VARCHAR(255), location VARCHAR(255), status VARCHAR(255))")
            cur.close()

            # Insert data into the category table
            cur = mysql.connection.cursor()
            cur.execute(
                f"INSERT INTO {category} (service_id,image, name,  description,Amount, email, phonenumber, location, status) VALUES (%s,%s, %s, %s, %s, %s, %s, %s, %s)",
                (service_id, image_path, name, description, Amt, email, phonenumber, location, status))
            mysql.connection.commit()
            cur.close()

            return render_template("Pages/upload.html")
        except MySQLdb.Error as e:
            # Handle MySQL errors
            return str(e)
        except Exception as e:
            # Handle other exceptions
            return str(e)
    return render_template("Pages/upload.html")
