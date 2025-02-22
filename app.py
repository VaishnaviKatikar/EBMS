from flask import Flask, render_template, request, redirect, url_for, flash, session
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
        email_id = request.form['email_id']
        password = request.form['password']
        contact_details = request.form['contact_details']
        address = request.form['address']
        
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('INSERT INTO customer (customer_id, customer_name, dob, email_id, password, contact_details, address) VALUES (%s, %s, %s, %s, %s, %s, %s)', 
                       (customer_id, customer_name, dob, email_id, password, contact_details, address))
        mysql.connection.commit()
        
        flash('Customer added successfully!', 'success')
        return redirect(url_for('customer_login'))  # Use url_for for proper redirection
        
    return render_template('customer.html')

# Add an index route to handle redirection

@app.route('/customer_login', methods=['GET', 'POST'])
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

@app.route('/customer_dashboard')
def customer_dashboard():
    if 'loggedin' in session:
        return render_template('customer_dashboard.html', email=session['email_id'])
    return redirect(url_for('customer_login'))


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
        return redirect(url_for('admin_login'))  # Use url_for for proper redirection
        
    return render_template('admin.html') 

@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM admin WHERE email = %s AND password = %s', (email, password))
        account = cursor.fetchone()

        # Check if customer account exists in the database
        if account:
            session['loggedin'] = True
            session['admin_id'] = account['admin_id']
            session['email'] = account['email']
            flash('Login successful!', 'success')
            return redirect(url_for('admin_dashboard')) # Redirect to the customer dashboard
        else:
            flash('Incorrect email or password!', 'danger')
    return render_template('admin_login.html')

@app.route('/admin_dashboard')
def admin_dashboard():
    if 'loggedin' in session:
        return render_template('admin_dashboard.html', email=session['email'])
    return redirect(url_for('admin_login'))

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
        return redirect(url_for('service_provider_login'))  # Use url_for for proper redirection
        
    return render_template('service_provider.html')

@app.route('/service_provider_login', methods=['GET', 'POST'])
def service_provider_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM service_provider WHERE email = %s AND password = %s', (email, password))
        account = cursor.fetchone()

        # Check if customer account exists in the database
        if account:
            session['loggedin'] = True
            session['reader_id'] = account['reader_id']
            session['email'] = account['email']
            flash('Login successful!', 'success')
            return redirect(url_for('service_provider_dashboard')) # Redirect to the customer dashboard
        else:
            flash('Incorrect email or password!', 'danger')
    return render_template('service_provider_login.html')

@app.route('/service_provider_dashboard')
def service_provider_dashboard():
    if 'loggedin' in session:
        return render_template('service_provider_dashboard.html')
    else:
        flash('Please log in first', 'danger')
        return redirect(url_for('service_provider_login'))

@app.route('/bill_calculation', methods=['GET', 'POST'])
def bill_calculation():
    if request.method == 'POST':
        # Get form data
        customer_id = request.form['customer_id']
        previous_meter_reading = request.form['previous_meter_reading']
        current_meter_reading = request.form['current_meter_reading']
        tariff_rate = request.form['tariff_rate']
        payment_due_date = request.form['payment_due_date']
        
        # Calculate total bill
        units_consumed = float(current_meter_reading) - float(previous_meter_reading)
        total_bill = units_consumed * float(tariff_rate)
        
        # Handle the case where 'is_late' might not be provided
        is_late = request.form.get('is_late')  # Use .get() to avoid KeyError
        late_fee = total_bill * 0.10 if is_late == 'true' else 0
        final_bill = total_bill + late_fee

        # Insert the bill data into the database
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        # Ensure that is_late is either 0 (false) or 1 (true)
        cursor.execute('''
    INSERT INTO bill_calculation 
    (customer_id, previous_meter_reading, current_meter_reading, tariff_rate, payment_due_date, is_late, final_bill)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    ''', (customer_id, previous_meter_reading, current_meter_reading, tariff_rate, payment_due_date, 0 if is_late == 'false' else 1, final_bill)
)
        mysql.connection.commit()

        flash('Bill added successfully!', 'success')
        return redirect(url_for('admin_dashboard'))  # Redirect to the admin dashboard

    return render_template('bill_calculation.html')

@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if request.method == 'POST':
        customer_id = request.form['customer_id']
        feedback = request.form['feedback']

        # Insert the feedback into the database
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('INSERT INTO feedback (customer_id, feedback) VALUES (%s, %s)', (customer_id, feedback))
        mysql.connection.commit()

        flash('Feedback submitted successfully!', 'success')
        return redirect(url_for('customer_dashboard'))  # Redirect back to the dashboard after feedback

    return render_template('feedback.html')  # Render the feedback form

# Add this route to serve the bill estimation page
@app.route('/bill_estimate', methods=['GET'])
def bill_estimate():
    return render_template('bill_estimate.html')  # Render the HTML form

@app.route('/view_bills', methods=['GET'])
def view_bills():
    # Get the logged-in customer's ID
    customer_id = session.get('customer_id')
    
    if customer_id:  # Only proceed if the customer is logged in
        try:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            # Fetch the bills for the customer
            query = '''SELECT 
                            bc.customer_id,
                            bc.previous_meter_reading,
                            bc.current_meter_reading,
                            bc.tariff_rate,
                            bc.payment_due_date,
                            bc.is_late,
                            bc.bill_amount,
                            bc.final_bill,
                            bc.created_at,
                            CASE 
                                WHEN bc.is_late = 1 THEN 'Unpaid' 
                                ELSE 'Paid' 
                            END AS status
                        FROM 
                            bill_calculation AS bc 
                        WHERE 
                            bc.customer_id = %s'''
            cursor.execute(query, (customer_id,))
            bills = cursor.fetchall()  # Retrieve all bills for this customer
            
            cursor.close()  # Close the cursor
            
            # Render the template with the fetched bills
            return render_template('view_bills.html', bills=bills)

        except MySQLdb.Error as e:
            flash(f"An error occurred while fetching bills: {e}", "danger")
            return redirect(url_for('customer_dashboard'))  # Redirect to dashboard on error

    else:
        return redirect(url_for('customer_login'))  # Redirect to login if not logged in

@app.route('/pay_bill/<int:bill_id>', methods=['POST'])
def pay_bill(bill_id):
    # Get the logged-in customer's ID
    customer_id = session.get('customer_id')
    
    if customer_id:
        try:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

            # Update the bill status to 'Paid' and record the payment
            update_query = '''UPDATE bill_calculation 
                              SET is_late = 0, final_bill = bill_amount 
                              WHERE customer_id = %s AND bill_id = %s'''
            cursor.execute(update_query, (customer_id, bill_id))
            mysql.connection.commit()

            # Retrieve transaction details
            transaction_query = '''SELECT 
                                        previous_meter_reading,
                                        current_meter_reading,
                                        tariff_rate,
                                        payment_due_date,
                                        bill_amount,
                                        final_bill,
                                        created_at 
                                   FROM 
                                        bill_calculation 
                                   WHERE 
                                        customer_id = %s AND bill_id = %s'''
            cursor.execute(transaction_query, (customer_id, bill_id))
            transaction = cursor.fetchone()

            cursor.close()  # Close the cursor

            if transaction:
                # Render the transaction details page
                return render_template('transaction_details.html', transaction=transaction)

            else:
                flash('Transaction not found.', 'danger')
                return redirect(url_for('view_bills'))

        except MySQLdb.Error as e:
            flash(f"An error occurred while processing payment: {e}", "danger")
            return redirect(url_for('view_bills'))  # Redirect on error

    else:
        return redirect(url_for('customer_login'))  # Redirect to login if not logged in

@app.route('/transaction_details')
def transaction_details():
    return render_template('transaction_details.html')

@app.route('/pay_bill/<int:bill_id>', methods=['POST'])
def process_payment(bill_id):
    # Here you would typically process the payment.
    # For this example, we'll assume the payment is successful.

    # Update the database if necessary to mark the bill as paid.
    cursor = mysql.connection.cursor()
    
    # Update the bill status to 'Paid' in the bill_calculation table
    cursor.execute("UPDATE bill_calculation SET is_late = 0 WHERE bill_id = %s", (bill_id,))
    mysql.connection.commit()
    
    cursor.close()
    
    # Optionally, you could add a flash message here
    flash("Transaction completed successfully!", "success")
    
    return redirect(url_for('transaction_completed'))

@app.route('/transaction_completed')
def transaction_completed():
    return render_template('transaction_completed.html')

@app.route('/logout')
def logout():
    # Clear the session
    session.clear()
    # Redirect to the login page (or any other page)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
