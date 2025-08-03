from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


# ========== USER (Admin login) ==========
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)


# ========== DEPARTMENT ==========
class Department(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

    def __repr__(self):
        return f"<Department {self.name}>"


# ========== POSITION ==========
class Position(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    base_salary = db.Column(db.Float, nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'), nullable=True)

    department = db.relationship('Department', backref='positions')

    def __repr__(self):
        return f"<Position {self.title}>"


# ========== STAFF ==========
class Staff(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    position_id = db.Column(db.Integer, db.ForeignKey('position.id'), nullable=False)
    date_employed = db.Column(db.Date, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)

    position = db.relationship('Position', backref='staff_members')

    def __repr__(self):
        return f"<Staff {self.full_name}>"


# ========== PAYROLL ==========
class Payroll(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    staff_id = db.Column(db.Integer, db.ForeignKey('staff.id'), nullable=False)
    salary_amount = db.Column(db.Float, nullable=False)
    month = db.Column(db.String(20), nullable=False)  # e.g., "July"
    year = db.Column(db.Integer, nullable=False)
    paid_on = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(50), default="Paid")  # Pending, Processing, Paid

    staff = db.relationship('Staff', backref='payrolls')

    def __repr__(self):
        return f"<Payroll {self.month} {self.year} - {self.staff.full_name}>"
