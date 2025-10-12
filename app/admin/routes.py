from flask import Blueprint, render_template, abort, request, jsonify
from flask_login import login_required, current_user
from functools import wraps
from ..models import Appointment, User
from .. import db

admin = Blueprint('admin', __name__)

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Check if the user is logged in and if their role is 'admin'
        if not current_user.is_authenticated or current_user.role != 'admin':
            abort(403) # Return a 'Forbidden' error if they are not an admin
        return f(*args, **kwargs)
    return decorated_function

@admin.route('/admin/dashboard')
@login_required
@admin_required
def dashboard():
    all_appointments = Appointment.query.order_by(Appointment.date.desc()).all()
    return render_template('admin_dashboard.html', appointments=all_appointments)

@admin.route('/admin/users')
@login_required
@admin_required
def manage_users():
    users = User.query.all()
    return render_template('manage_users.html', users=users)

@admin.route('/admin/user/<int:user_id>/set_role', methods=['POST'])
@login_required
@admin_required
def set_user_role(user_id):
    user = User.query.get_or_404(user_id)
    data = request.get_json()
    new_role = data.get('role')

    if new_role not in ['patient', 'doctor', 'admin']:
        return jsonify({'message': 'Invalid role specified.'}), 400

    user.role = new_role
    db.session.commit()
    
    return jsonify({'message': f"User {user.username}'s role updated to {new_role}."}), 200

