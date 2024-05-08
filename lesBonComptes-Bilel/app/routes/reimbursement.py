from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
from mongoengine import DoesNotExist
from ..services.reimbursement_service import save_reimbursements
from ..models.group import Group
from ..services.reimbursement_service import calculate_optimal_reimbursements

reimbursement_blueprint = Blueprint('reimbursement_blueprint', __name__)


@reimbursement_blueprint.route('/<group_id>/reimbursements/optimize', methods=['GET'])
@jwt_required()
def get_optimized_reimbursements(group_id):
    try:
        # On récupère le groupe et on calcule les soldes
        group = Group.objects.get(id=group_id)
        balances = group.calculate_balances()

        # On calcule les remboursements optimisés
        reimbursements = calculate_optimal_reimbursements(balances)

        # On enregistre les remboursements optimisés dans la base de données
        save_reimbursements(group_id, reimbursements)

        # On prépare la réponse
        formatted_reimbursements = [
            {"sender": sender, "recipient": recipient, "amount": amount}
            for sender, recipient, amount in reimbursements
        ]

        return jsonify(formatted_reimbursements), 200
    except DoesNotExist:
        return jsonify({'message': 'Groupe non trouvé'}), 404
    except Exception as e:
        return jsonify({'message': str(e)}), 500