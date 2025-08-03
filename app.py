from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
from config import Config

# Initialize Flask app and configuration
app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

# Import models
from models import Staff, Payroll

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


# ================= HOME PAGE ===================
@app.route('/')
def home():
    return render_template('index.html')


# ================= STAFF LISTING ===================
@app.route('/staff')
def list_staff():
    staff_members = Staff.query.all()
    return render_template('staff_list.html', staff=staff_members)


# ================= GENERATE PAYROLL ===================
@app.route('/generate-payroll', methods=['GET', 'POST'])
def generate_payroll():
    if request.method == 'POST':
        staff_id = request.form['staff_id']
        amount = float(request.form['amount'])
        month = request.form['month']

        staff = Staff.query.get(staff_id)
        if not staff:
            flash('Invalid staff selected.', 'danger')
            return redirect(url_for('generate_payroll'))

        # Create payroll record
        payroll = Payroll(
            staff_id=staff.id,
            amount=amount,
            month=month,
            generated_on=datetime.utcnow()
        )
        db.session.add(payroll)
        db.session.commit()

        flash(f'Payroll generated for {staff.fullname} successfully.', 'success')
        return redirect(url_for('list_staff'))

    staff_members = Staff.query.all()
    return render_template('generate_payroll.html', staff=staff_members)


# ================= VIEW PAYSLIP ===================
@app.route('/payslip/<int:payroll_id>')
def view_payslip(payroll_id):
    payslip = Payroll.query.get_or_404(payroll_id)
    staff = Staff.query.get_or_404(payslip.staff_id)
    return render_template('payslip.html', staff=staff, payslip=payslip)


# ================= STATIC FILE SERVING (Payslip/Upload) ===================
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


# ================= ERROR HANDLER ===================
@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404


# ================= MAIN ===================
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
