from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        # minimal demo: accept any username for now
        session['user_id'] = 1
        session['username'] = username or 'operator'
        return redirect(url_for('dashboard.index'))
    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))

@auth_bp.route('/init-admin')
def init_admin():
    # placeholder endpoint (init scripts provided separately)
    return "init-admin placeholder"