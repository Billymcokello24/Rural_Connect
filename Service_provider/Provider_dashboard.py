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

from app import mysql, booking_counts, service_counts, get_username_from_db_provider


def provider_dashboard():
    # Get counts and username
    counts = booking_counts()
    service_countsss = service_counts()
    username = get_username_from_db_provider()

    if username:
        # Fetch the sum of received amounts from the database
        cur = mysql.connection.cursor()
        cur.execute("SELECT SUM(Amount) FROM received")
        total_received = cur.fetchone()[0]
        cur.close()

        # Pass the total_received to the template
        return render_template('provider/provider_dashboard.html',
                               Username=session['username'],
                               counts=counts,
                               service_countsss=service_countsss,
                               total_received=total_received)
    else:
        return redirect(url_for('provider_login'))

    return redirect(url_for('provider_login'))