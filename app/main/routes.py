from flask import Blueprint, render_template, request, jsonify, abort
from flask_login import login_required, current_user
from .. import db
from ..models import Appointment, User
from datetime import datetime

main = Blueprint('main', __name__)

@main.route('/dashboard')
@login_required
def dashboard():
    # We will update this later to show the doctor's name
    appointments = Appointment.query.filter_by(user_id=current_user.id).order_by(Appointment.date.asc()).all()
    return render_template('dashboard.html', user=current_user, appointments=appointments)

@main.route('/book_appointment', methods=['GET', 'POST'])
@login_required
def book_appointment():
    if request.method == 'POST':
        data = request.get_json()
        title = data.get('title')
        date_str = data.get('date')
        doctor_id = data.get('doctor_id')

        if not all([title, date_str, doctor_id]):
            return jsonify({'message': 'All fields are required.'}), 400

        date_obj = datetime.strptime(date_str, '%Y-%m-%dT%H:%M')

        if date_obj < datetime.now():
            return jsonify({'message': 'Cannot book an appointment in the past.'}), 400

        # --- THIS IS THE CORRECTED LINE ---
        # Instead of 'booker', we use the actual column name 'user_id'
        new_appointment = Appointment(title=title, 
                                      date=date_obj, 
                                      user_id=current_user.id, 
                                      doctor_id=doctor_id)
        db.session.add(new_appointment)
        db.session.commit()
        return jsonify({'message': 'Appointment booked successfully!'}), 201
    
    doctors = User.query.filter_by(role='doctor').all()
    return render_template('book_appointment.html', doctors=doctors)


@main.route('/delete_appointment/<int:appointment_id>', methods=['DELETE'])
@login_required
def delete_appointment(appointment_id):
    appointment = Appointment.query.get_or_404(appointment_id)
    if appointment.booker != current_user and current_user.role != 'admin':
        abort(403)
    db.session.delete(appointment)
    db.session.commit()
    return jsonify({'message': 'Appointment deleted successfully'}), 200

