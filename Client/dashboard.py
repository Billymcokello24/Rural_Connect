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

from app import mysql, count_bookings, get_id, get_username_from_db_client, service_counts


def dashboard():
    if 'loggedin' in session:
        id_number = get_id()
        username = get_username_from_db_client()
        count = service_counts()  # Assuming this function fetches the total count of services

        # Fetch sum of tokens for the logged-in user from user_tokens table
        if id_number:
            cur = mysql.connection.cursor()
            cur.execute("SELECT Amount FROM user_tokens WHERE id_number = %s", (id_number,))
            token_sum = cur.fetchone()
            cur.close()
            if token_sum:
                token_sum = token_sum[0]
            else:
                token_sum = 0
            booking_count = count_bookings(id_number)
            return render_template('dashboard/index.html', Username=username, booking_count=booking_count,
                                   service_count=count, token_sum=token_sum)
        else:
            flash('Failed to retrieve user information.', 'error')
            return render_template('dashboard/index.html', Username=username, service_count=count)
    else:
        # User is not logged in, redirect to the login page
        return redirect(url_for('login'))
