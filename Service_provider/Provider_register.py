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

from app import mysql


def provider_register():
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'id_number' in request.form and 'name' in request.form and 'email' in request.form and 'service' in request.form and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        id_number = request.form['id_number']
        service = request.form['service']
        name = request.form['name']
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM provider_auth WHERE username = %s', (username,))
        account = cursor.fetchone()
        # If account exists show error and validation checks
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        else:
            # Hash the password
            # Account doesn't exist, and the form data is valid, so insert the new account into the accounts table
            cursor.execute(
                'INSERT INTO provider_auth (id_number, name, email, service, username, password) VALUES (%s,%s,%s,%s,%s, %s)',
                (id_number, name, email, service, username, password,))
            mysql.connection.commit()
            msg = 'You have successfully registered!, now login'
            return redirect(url_for('provider_login', msg=msg))


    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'

    return render_template('provider/provider_register.html', msg=msg)

