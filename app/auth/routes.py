from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from .. import db, mail
from ..models import User, Appointment
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from flask_mail import Message

auth = Blueprint('auth', __name__)

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('auth.reset_token', token=token, _external=True)}

If you did not make this request then simply ignore this email and no changes will be made.
'''
    try:
        mail.send(msg)
        print("--- MAIL SENT SUCCESSFULLY ---")
    except Exception as e:
        print(f"!!! MAIL SENDING FAILED: {e}")

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        email, password = data.get('email'), data.get('password')
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            
            # This logic now handles all three roles
            if user.role == 'admin':
                redirect_url = '/admin/dashboard'
            elif user.role == 'doctor':
                redirect_url = '/doctor/dashboard'
            else: # This covers the 'patient' role
                redirect_url = '/dashboard'
            
            return jsonify({'message': 'Logged in successfully', 'redirect_url': redirect_url}), 200
        return jsonify({'message': 'Invalid credentials'}), 401
    return render_template('login.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.get_json()
        username, email, password = data.get('username'), data.get('email'), data.get('password')
        if User.query.filter_by(email=email).first() or User.query.filter_by(username=username).first():
            return jsonify({'message': 'User already exists'}), 409
        hashed_password = generate_password_hash(password, 'pbkdf2:sha256')
        new_user = User(username=username, email=email, password_hash=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'User created successfully'}), 201
    return render_template('register.html')

@auth.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if request.method == 'POST':
        data = request.get_json()
        user = User.query.filter_by(email=data.get('email')).first()
        if user:
            send_reset_email(user)
        return jsonify({'message': 'An email has been sent with instructions to reset your password.'}), 200
    return render_template('reset_request.html')

@auth.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    user = User.verify_reset_token(token)
    if user is None:
        return jsonify({'message': 'That is an invalid or expired token'}), 400
    if request.method == 'POST':
        data = request.get_json()
        password = data.get('password')
        hashed_password = generate_password_hash(password, 'pbkdf2:sha256')
        user.password_hash = hashed_password
        db.session.commit()
        return jsonify({'message': 'Your password has been updated! You are now able to log in.'}), 200
    return render_template('reset_token.html', token=token)

@auth.route('/delete_account', methods=['DELETE'])
@login_required
def delete_account():
    Appointment.query.filter_by(user_id=current_user.id).delete()
    db.session.delete(current_user)
    db.session.commit()
    logout_user()
    return jsonify({'message': 'Your account has been permanently deleted.'}), 200

