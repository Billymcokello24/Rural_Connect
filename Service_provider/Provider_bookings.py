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


def provider_bookings():
    try:

        # Fetch all bookings from the book_service table
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT * FROM book_service")
        bookings = cur.fetchall()
        cur.close()

        # Render the provider's bookings screen with the fetched data
        return render_template('Pages/provider_booking.html', bookingss=bookings)
    except Exception as e:
        return str(e)
