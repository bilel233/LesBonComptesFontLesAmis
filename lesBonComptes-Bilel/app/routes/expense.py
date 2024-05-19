from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
import os
from mongoengine import DoesNotExist, ValidationError
from ..models.expense import Expense
from ..models.group import Group
from ..models.user import User
from datetime import datetime
import json

expenses_blueprint = Blueprint('expenses_blueprint', __name__)

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS




@expenses_blueprint.route('/create_expense', methods=['POST'])
@jwt_required()
def create_expense():
    current_user_username = get_jwt_identity()
    payer = User.objects.get(username=current_user_username)

    file = request.files.get('receipt')

    if file and file.filename:
        if not allowed_file(file.filename):
            return jsonify({'message': 'File type not allowed'}), 400

        filename = secure_filename(file.filename)
        upload_folder = current_app.config['UPLOAD_FOLDER']

        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder, exist_ok=True)

        file_path = os.path.join(upload_folder, filename)
        file.save(file_path)
        with open(file_path, 'rb') as file_obj:
            file_data = file_obj.read()
    else:
        file_data = None

    expense_data = request.form
    expense_date = datetime.strptime(expense_data['date'], '%Y-%m-%d')  # Correction ici
    group_id = expense_data.get('group_id')
    group = Group.objects.get(id=group_id)

    involved_usernames = expense_data.getlist('involved_members')
    involved_members = User.objects(username__in=involved_usernames)

    weights_input = expense_data.get('weights')
    weights = list(map(float, weights_input.split(','))) if weights_input else [1.0] * len(involved_members)

    expense = Expense(
        title=expense_data['title'],
        amount=float(expense_data['amount']),
        date=expense_date,
        payer=payer,
        receipt=file_data,
        category=expense_data['category'],
        group=group,
        involved_members=involved_members,
        weights=weights
    )
    expense.save()

    return jsonify({'message': 'Expense created successfully'}), 201

@expenses_blueprint.route('/get_all_expenses_by_group/<group_id>', methods=['GET'])
@jwt_required()
def get_all_expenses_by_group(group_id):
    try:
        group = Group.objects.get(id=group_id)
        expenses = Expense.objects(group=group)
        expenses_list = [{
            'id': str(exp.id),
            'title': exp.title,
            'amount': exp.amount,
            'date': exp.date.strftime('%Y-%m-%d'),
            'payer': exp.payer.username,
            'category': exp.category,
            'involved_members': [member.username for member in exp.involved_members],
            'weights': exp.weights
        } for exp in expenses]
        return jsonify(expenses_list), 200
    except DoesNotExist:
        return jsonify({'message': 'Group or expenses not found'}), 404
    except Exception as e:
        return jsonify({'message': str(e)}), 500
