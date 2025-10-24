from flask import Blueprint, jsonify, request, redirect, url_for, flash
from flask_jwt_extended import jwt_required, current_user as jwt_current_user

from .index import index_views

from App.controllers import (
    create_staff,
    clock_in,
    clock_out,
    view_roster,
    get_current_shift_status
)

staff_views = Blueprint('staff_views', __name__, template_folder='../templates')


# ---------- REGISTER STAFF ----------
@staff_views.route('/create', methods=['POST'])
def create_staff_action():
    data = request.form
    flash(f"Staff {data['username']} created!")
    create_staff(data['username'], data['password'])
    return redirect(url_for('staff_views.get_user_page'))


# ---------- CLOCK IN ----------
@staff_views.route('/clock-in', methods=['POST'])
@jwt_required()
def clockin_staff_action():
    staff_id = jwt_current_user.id
    result = clock_in(staff_id)
    return jsonify(result), 200


# ---------- CLOCK OUT ----------
@staff_views.route('/clock-out', methods=['POST'])
@jwt_required()
def clockout_staff_action():
    staff_id = jwt_current_user.id
    result = clock_out(staff_id)
    return jsonify(result), 200


# ---------- VIEW COMBINED ROSTER ----------
@staff_views.route('/roster', methods=['GET'])
@jwt_required()
def view_combined_roster_action():
    roster = view_roster()
    return jsonify(roster), 200


# ---------- CHECK CURRENT SHIFT STATUS ----------
@staff_views.route('/shift-status', methods=['GET'])
@jwt_required()
def current_shift_status_action():
    staff_id = jwt_current_user.id
    status = get_current_shift_status(staff_id)
    return jsonify(status), 200