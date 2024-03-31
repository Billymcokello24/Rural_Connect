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


def login():
    # Output a message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM Auth WHERE username = %s AND password = %s', (username, password,))
        # Fetch one record and return result
        account = cursor.fetchone()
        # If account exists in accounts table in out database
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            msg = 'Logged in successfully !'
            return redirect(url_for('dashboard'))
        else:
            # Account doesn't exist or username/password incorrect
            msg = 'Incorrect username/password!'
    # Show the login form with message (if any)

    return render_template('login.html', success_message=msg)

