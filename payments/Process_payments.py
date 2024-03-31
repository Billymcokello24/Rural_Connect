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

from app import mysql, get_id


def process_payment():
    if request.method == 'POST':
        service_id = request.form['service_id']  # Assuming you have a way to get the service_id
        amount_payable = request.form['Amount_Payable']  # Assuming you have a way to get the Amount_Payable

        # Deduct Amount_Payable from the user's Amount in user_tokens table
        cur = mysql.connection.cursor()
        cur.execute(
            "UPDATE user_tokens SET Amount = Amount - %s WHERE id_number = %s",
            (amount_payable, get_id())
        )
        mysql.connection.commit()

        # Update received table with id_number and deducted amount
        cur.execute(
            "INSERT INTO received (id_number, service_id,Amount) VALUES (%s,%s, %s)",
            (get_id(), service_id, amount_payable)
        )
        mysql.connection.commit()

        cur.close()

    return redirect(url_for('dashboard'))  # Redirect to the dashboard after payment
