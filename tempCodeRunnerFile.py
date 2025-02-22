from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Database connection settings for flask_mysqldb
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'krishna@1411'
app.config['MYSQL_DB'] = 'electricity_billing_system'

mysql = MySQL(app)

# Correct route for customer

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/customer', methods=['GET', 'POST'])
def customer():
    if request.method == 'POST':
        customer_id = request.form['customer_id']
        customer_name = request.form['customer_name']
        dob = request.form['dob']
        password = request.form['password']
        email_id = request.form['email_id']
        contact_details = request.form['contact_details']
        address = request.form['address']
        
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('INSERT INTO customer (customer_id, customer_name, dob, password, email_id, contact_details, address) VALUES (%s, %s, %s, %s, %s, %s, %s)', 
                       (customer_id, customer_name, dob, password, email_id, contact_details, address))
        mysql.connection.commit()
        
        flash('Customer added successfully!', 'success')
        return redirect(url_for('customer_login'))  # Use url_for for proper redirection
        
    return render_template('customer.html')

# Add an index route to handle redirection

@app.route('/customer_login')
def customer_login():
    if request.method == 'POST':
        email_id = request.form['email_id']
        password = request.form['password']
        
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM customer WHERE email_id = %s AND password = %s', (email_id, password))
        account = cursor.fetchone()

        # Check if customer account exists in the database
        if account:
            session['loggedin'] = True
            session['customer_id'] = account['customer_id']
            session['email_id'] = account['email_id']
            flash('Login successful!', 'success')
            return redirect(url_for('customer_dashboard')) # Redirect to the customer dashboard
        else:
            flash('Incorrect email or password!', 'danger')

    return render_template('customer_login.html')

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        admin_id = request.form['admin_id']
        email = request.form['email']
        password = request.form['password']
        
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('INSERT INTO admin (admin_id, email, password) VALUES (%s, %s, %s)', 
                       (admin_id, email, password))
        mysql.connection.commit()
        
        flash('Admin added successfully!', 'success')
        return render_template('admin_login.html')  # Use url_for for proper redirection
        
    return render_template('admin.html') 

@app.route('/admin_login')
def admin_login():
    return render_template('admin_login.html')

@app.route('/service_provider', methods=['GET', 'POST'])
def service_provider():
    if request.method == 'POST':
        reader_id = request.form['reader_id']
        name = request.form['name']
        address = request.form['address']
        contact_details = request.form['contact_details']
        email = request.form['email']
        password = request.form['password']
        
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('INSERT INTO service_provider (reader_id, name, address, contact_details, email, password) VALUES (%s, %s, %s, %s, %s, %s)', 
                       (reader_id, name, address, contact_details, email, password))
        mysql.connection.commit()
        
        flash('Service Provider added successfully!', 'success')
        return render_template('service_provider_login.html')  # Use url_for for proper redirection
        
    return render_template('service_provider.html')

@app.route('/service_provider_login')
def service_provider_login():
    return render_template('service_provider_login.html')


if __name__ == '__main__':
    app.run(debug=True)
