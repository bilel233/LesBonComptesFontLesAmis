from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models.user import User
from ..services.stripe_service import save_payment_method

payment_blueprint = Blueprint('payment_blueprint', __name__)

@payment_blueprint.route('/save_payment_method', methods=['POST'])
@jwt_required()
def handle_payment_method():
    current_user_username = get_jwt_identity()
    user = User.objects(username=current_user_username).first()
    payment_method = request.form.get('payment_method')
    rib_file = request.files.get('rib_file')

    payment_info = save_payment_method(user, payment_method, rib_file)
    return jsonify({'message': 'Méthode de paiement sauvegardée avec succès'}), 200
