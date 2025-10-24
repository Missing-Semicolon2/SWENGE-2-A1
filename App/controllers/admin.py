from flask import jsonify
from App.models import Admin, Shift
from App.database import db
from sqlalchemy.exc import IntegrityError

