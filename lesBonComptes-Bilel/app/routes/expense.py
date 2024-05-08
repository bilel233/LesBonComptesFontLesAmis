import os
from datetime import datetime
from flask import request, jsonify, Blueprint, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from mongoengine import DoesNotExist, ValidationError
from werkzeug.utils import secure_filename
from ..models.expense import Expense
from ..models.group import Group
from ..models.user import User

# le blueprint expense
expenses_blueprint = Blueprint('expenses_blueprint', __name__)


def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@expenses_blueprint.route('/create_expense', methods=['POST'])
@jwt_required()
def create_expense():
    current_user_username = get_jwt_identity()
    payer = User.objects(username=current_user_username).first()

    if 'receipt' not in request.files:
        return jsonify({'message': 'Aucun fichier fourni'}), 400

    file = request.files['receipt']
    if file.filename == '':
        return jsonify({'message': 'Aucun fichier sélectionné'}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        expense_data = request.form
        expense_date = datetime.strptime(expense_data['date'], '%d-%m-%Y')
        group_id = expense_data.get('group_id')


        try:
            group = Group.objects.get(id=group_id)
        except Group.DoesNotExist:
            return jsonify({'message': 'Groupe non trouvé'}), 404


        involved_usernames = expense_data.getlist('involved_members')
        involved_members = User.objects(username__in=involved_usernames)

      #  if len(involved_members) != len(involved_usernames):
       #     return jsonify({'message': 'Un ou plusieurs membres spécifiés n\'existent pas'}), 400

        expense = Expense(
            title=expense_data['title'],
            amount=float(expense_data['amount']),
            date=expense_date,
            payer=payer,
            receipt=file_path,
            category=expense_data['category'],
            group=group,
            involved_members=involved_members,
            weights=[]
        )
        expense.save()

        return jsonify({'message': 'Dépense créée avec succès'}), 201
    else:
        return jsonify({'message': 'Type de fichier non autorisé'}), 400
@expenses_blueprint.route('/delete_expense/<expense_id>', methods=['DELETE'])
@jwt_required()
def delete_expense(expense_id):
    current_user_username = get_jwt_identity()
    current_user = User.objects(username=current_user_username).first()

    try:
        expense = Expense.objects.get(id=expense_id)
        expense.delete()
        return jsonify({'message': 'Dépense supprimée avec succès'}), 200
    except DoesNotExist:
        return jsonify({'message': 'Dépense non trouvée'}), 404
    except Exception as e:
        return jsonify({'message': str(e)}), 500


@expenses_blueprint.route('/get_expense/<expense_id>', methods=['GET'])
@jwt_required()
def get_expense(expense_id):
    """Recupere une depense selon son ID"""

    try:
        expense = Expense.objects.get(id=expense_id)

        expense_details = {
            'id': str(expense.id),
            'title': expense.title,
            'amount': expense.amount,
            'date': expense.date.strftime('%Y-%m-%d'),
            'payer': expense.payer.username,
            'group': expense.group.name if expense.group else None,
            'receipt': expense.receipt,
            'category': expense.category,
            'involved_members': [member.username for member in expense.involved_members],
            'weights': expense.weights
        }
        return jsonify(expense_details), 200
    except DoesNotExist:
        return jsonify({'message': 'Dépense non trouvée'}), 404

    except Exception as e:
        return jsonify({'message': str(e)}), 500

@expenses_blueprint.route('/get_all_expenses',methods=['GET'])
@jwt_required()
def get_all_expenses():
    """on recupere toute les depenses"""
    try:

        expenses = Expense.objects.all()  # On recupere toute les depenses

        expenses_list = []
        for expense in expenses:
            expenses_list.append({
                'id': str(expense.id),
                'title': expense.title,
                'amount': expense.amount,
                'date': expense.date.strftime('%Y-%m-%d'),
                'payer': expense.payer.username,
                'group': expense.group.name if expense.group else "N/A",
                'receipt': expense.receipt,
                'category': expense.category,
                'involved_members': [member.username for member in expense.involved_members],
                'weights': expense.weights
            })

        return jsonify(expenses_list), 200
    except Exception as e:
        return jsonify({'message': 'Erreur lors de la récupération des dépenses: {}'.format(str(e))}),


@expenses_blueprint.route('/update_expense/<expense_id>', methods=['PUT'])
@jwt_required()
def update_expense(expense_id):
    """ on met a jour la depense"""

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