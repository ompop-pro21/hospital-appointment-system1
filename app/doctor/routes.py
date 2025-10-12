from flask import Blueprint, render_template, abort
from flask_login import login_required, current_user
from functools import wraps
from ..models import Appointment

doctor_bp = Blueprint('doctor', __name__)

# This is our new security decorator for doctors
def doctor_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'doctor':
            abort(403) # Forbidden
        return f(*args, **kwargs)
    return decorated_function

@doctor_bp.route('/doctor/dashboard')
@login_required
@doctor_required
def dashboard():
    # Fetch all appointments where the doctor_id matches the current logged-in doctor
    appointments = Appointment.query.filter_by(doctor_id=current_user.id).order_by(Appointment.date.asc()).all()
    return render_template('doctor_dashboard.html', user=current_user, appointments=appointments)

