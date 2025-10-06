from flask import Blueprint, render_template, request, jsonify, current_app

subscriber_bp = Blueprint('subscriber', __name__)

@subscriber_bp.route('/')
def index():
    return render_template('subscribers/index.html')

@subscriber_bp.route('/create', methods=['GET','POST'])
def create():
    if request.method == 'POST':
        data = request.form.to_dict()
        return jsonify({'success': True, 'subscriber': data})
    return render_template('subscribers/create.html')