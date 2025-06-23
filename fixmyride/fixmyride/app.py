from flask import Flask, render_template, request, redirect, url_for, flash, session
import mysql.connector
import os
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename  # ✅ Import secure_filename


app = Flask(__name__)
app.secret_key = "secret_key"

# ✅ Database Connection Function
def connect_db():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="fixmyride",
            port=3306
        )
        
        if conn.is_connected():
            print("✅ Database connected successfully!")
        return conn  # Ensure the connection is returned correctly
    except mysql.connector.Error as err:
        print(f"❌ MySQL Connection Error: {err}")
        return None  # Return None if the connection fails

@app.route('/')
def index():
    return render_template('index.html')
@app.route('/home')
def home(): 
        return render_template('home.html') 
    
    
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password'].encode('utf-8')

        hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())

        db = connect_db()
        cursor = db.cursor()

        try:
            cursor.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)", 
                           (username, email, hashed_password))
            db.commit()
            flash("✅ Registration successful! Please login.", "success")
            return redirect(url_for('login'))
        except mysql.connector.Error as err:
            db.rollback()
            flash(f"❌ Error: {err}", "danger")
        finally:
            cursor.close()
            db.close()

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password'].encode('utf-8')

        db = connect_db()
        cursor = db.cursor()
        cursor.execute("SELECT username, password FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()

        if user and bcrypt.checkpw(password, user[1].encode('utf-8')):  # Using bcrypt to verify the password
            session['user'] = user[0]  # Store username in session
            flash("✅ Login successful!", "success")
            return redirect(url_for('home'))
        else:
            flash("❌ Invalid email or password!", "danger")

        cursor.close()
        db.close()

    return render_template('login.html')
@app.route('/logout')
def logout():
    session.pop('user', None)  # Use 'user' instead of 'user_id'
    flash("You have been logged out.", "info")
    return redirect(url_for('login'))

@app.route('/compare_services')
def compare_services():
    return render_template('compare_services.html')

@app.route('/spare_parts')
def spare_parts():
    return render_template('spare_parts.html')

@app.route('/forum')
def forum():
    return render_template('forum.html')

@app.route('/payment')
def payment():
    return render_template('payment.html')
@app.route('/success')
def success():
    return "Payment Successful! Thank you for your purchase."


@app.route('/diagnose')
def diagnose():
    return render_template('diagnose.html')
if __name__ == "__main__":
    app.run(port=5001, debug=True)

