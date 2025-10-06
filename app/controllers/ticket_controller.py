from flask import Blueprint, render_template, request, jsonify, current_app, session

ticket_bp = Blueprint('ticket', __name__)

@ticket_bp.route('/')
def index():
    return render_template('tickets/index.html')

@ticket_bp.route('/create', methods=['GET','POST'])
def create():
    if request.method == 'POST':
        data = request.form.to_dict()
        # in production: create ticket via models
        return jsonify({'success': True, 'ticket': data})
    return render_template('tickets/create.html')