from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models.expense import Expense
from ..models.user import User


statistics_blueprint = Blueprint('statistics_blueprint', __name__)

@statistics_blueprint.route('/user_statistics', methods=['GET'])
@jwt_required()
def user_statistics():
    current_user_username = get_jwt_identity()
    user = User.objects(username=current_user_username).first()

    if not user:
        return jsonify({'message': 'Utilisateur non trouvé'}), 404


    total_expenses = Expense.objects(payer=user).sum('amount')


    expenses_by_category = Expense.objects(payer=user).aggregate([
        {"$group": {"_id": "$category", "total": {"$sum": "$amount"}}}
    ])


    expenses_by_month = Expense.objects(payer=user).aggregate([
        {"$group": {
            "_id": {"month": {"$month": "$date"}, "year": {"$year": "$date"}},
            "total": {"$sum": "$amount"}
        }}
    ])

    return jsonify({
        'total_expenses': total_expenses,
        'expenses_by_category': list(expenses_by_category),
        'expenses_by_month': list(expenses_by_month)
    }), 200
