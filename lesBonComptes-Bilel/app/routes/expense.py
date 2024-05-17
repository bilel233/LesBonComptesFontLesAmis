import os
from datetime import datetime
from flask import request, jsonify, Blueprint, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from mongoengine import DoesNotExist, ValidationError
from werkzeug.utils import secure_filename
from ..models.expense import Expense
from ..models.group import Group
from ..models.user import User
import logging

expenses_blueprint = Blueprint('expenses_blueprint', __name__)
logging.basicConfig(level=logging.DEBUG)

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@expenses_blueprint.route('/create_expense', methods=['POST'])
@jwt_required()
def create_expense():
    current_user_username = get_jwt_identity()
    payer = User.objects.get(username=current_user_username)

    if 'receipt' not in request.files:
        return jsonify({'message': 'No file part'}), 400

    file = request.files['receipt']
    if file.filename == '':
        return jsonify({'message': 'No selected file'}), 400

    if not allowed_file(file.filename):
        return jsonify({'message': 'File type not allowed'}), 400

    filename = secure_filename(file.filename)
    upload_folder = current_app.config['UPLOAD_FOLDER']

    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder, exist_ok=True)

    file_path = os.path.join(upload_folder, filename)
    file.save(file_path)

    expense_data = request.form
    expense_date = datetime.strptime(expense_data['date'], '%Y-%m-%d')
    group_id = expense_data.get('group_id')
    group = Group.objects.get(id=group_id)

    involved_usernames = expense_data.getlist('involved_members')
    involved_members = User.objects(username__in=involved_usernames)

    weights_input = expense_data.get('weights')
    weights = list(map(float, weights_input.split(','))) if weights_input else [1.0] * len(involved_members)

    # Création de l'objet Expense avec l'objet fichier
    with open(file_path, 'rb') as file_obj:
        expense = Expense(
            title=expense_data['title'],
            amount=float(expense_data['amount']),
            date=expense_date,
            payer=payer,
            receipt=file_obj,
            category=expense_data['category'],
            group=group,
            involved_members=involved_members,
            weights=weights
        )
        expense.save()

    return jsonify({'message': 'Expense created successfully'}), 201

@expenses_blueprint.route('/get_expense/<expense_id>', methods=['GET'])
@jwt_required()
def get_expense(expense_id):
    try:
        expense = Expense.objects.get(id=expense_id)
        expense_details = {
            'id': str(expense.id),
            'title': expense.title,
            'amount': expense.amount,
            'date': expense.date.strftime('%Y-%m-%d'),
            'payer': expense.payer.username,
            'category': expense.category,
            'receipt': expense.receipt,
            'involved_members': [member.username for member in expense.involved_members],
            'weights': expense.weights
        }
        return jsonify(expense_details), 200
    except DoesNotExist:
        return jsonify({'message': 'Expense not found'}), 404

@expenses_blueprint.route('/get_all_expenses', methods=['GET'])
@jwt_required()
def get_all_expenses():
    sort_by = request.args.get('sort_by', 'date')
    sort_order = request.args.get('sort_order', 'asc')
    expenses = Expense.objects().order_by(f"{'-' if sort_order == 'desc' else ''}{sort_by}")
    expenses_list = [{'id': str(exp.id), 'title': exp.title, 'amount': exp.amount,
                      'date': exp.date.strftime('%Y-%m-%d'), 'payer': exp.payer.username,
                      'category': exp.category, 'receipt': exp.receipt} for exp in expenses]
    return jsonify(expenses_list), 200

@expenses_blueprint.route('/update_expense/<expense_id>', methods=['PUT'])
@jwt_required()
def update_expense(expense_id):
    try:
        expense = Expense.objects.get(id=expense_id)
        data = request.json
        if 'title' in data:
            expense.title = data['title']
        if 'amount' in data:
            expense.amount = data['amount']
        if 'date' in data:
            expense.date = datetime.strptime(data['date'], '%d-%m-%Y')
        if 'category' in data:
            expense.category = data['category']
        if 'receipt' in data:
            expense.receipt = data['receipt']
        if 'weights' in data:
            expense.weights = data['weights']

        expense.save()
        return jsonify({'message': 'Dépense mise à jour avec succès'}), 200
    except DoesNotExist:
        return jsonify({'message': 'Dépense non trouvée'}), 404
    except ValidationError as e:
        return jsonify({'message': str(e)}), 400
    except Exception as e:
        return jsonify({'message': str(e)}), 500
