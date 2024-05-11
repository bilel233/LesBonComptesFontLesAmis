from flask import request, jsonify, Blueprint, url_for, current_app, flash, redirect
from flask_jwt_extended import create_access_token
from flask_jwt_extended import jwt_required
from flask_dance.contrib.facebook import make_facebook_blueprint, facebook
from ..models.user import User

auth_blueprint = Blueprint('auth_blueprint', __name__)

# Configuration du blueprint OAuth Facebook
facebook_blueprint = make_facebook_blueprint(
    client_id="1554210685119210",
    client_secret="66b0c16ed4ca5f1842d85641fe964a6b",
    redirect_to='facebook_login'
)



@auth_blueprint.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'message': 'Le nom d’utilisateur et le mot de passe sont requis'}), 400

    if len(password) < 8:
        return jsonify({'message': 'Le mot de passe doit contenir au moins 8 caractères'}), 400

    if User.objects(username=username).first() is not None:
        return jsonify({'message': "Nom d'utilisateur déjà pris"}), 400

    user = User.create_user(username, password)
    return jsonify({'message': f'Utilisateur {user.username} créé avec succès'}), 201


@auth_blueprint.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    user = User.objects(username=username).first()
    if user and user.check_password(password):
        # La creation du token jwt
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({'message': 'Identifiants invalides'}), 401


@auth_blueprint.route('/user/<username>', methods=['GET'])
@jwt_required()
def get_user(username):
    user = User.objects(username=username).first()
    if user:
        return jsonify({'username': user.username}), 200
    else:
        return jsonify({'message': 'Utilisateur non trouvé'}), 404


@auth_blueprint.route('/user/<username>', methods=['PUT'])
@jwt_required()
def update_user(username):
    user = User.objects(username=username).first()
    if not user:
        return jsonify({'message': 'Utilisateur non trouvé'}), 404

    data = request.json
    new_username = data.get('new_username')
    new_password = data.get('new_password')

    if new_username:
        user.username = new_username
    if new_password:
        user.password = User.hash_password(new_password)

    user.save()
    return jsonify({'message': f'Informations de {username} mises à jour'}), 200


@auth_blueprint.route('/user/<username>', methods=['DELETE'])
@jwt_required()
def delete_user(username):
    user = User.objects(username=username).first()
    if not user:
        return jsonify({'message': 'Utilisateur non trouvé'}), 404

    user.delete()
    return jsonify({'message': f'Utilisateur {username} supprimé'}), 200


@auth_blueprint.route('/users', methods=['GET'])
@jwt_required()
def get_all_users():
    """
    Route pour récupérer tous les utilisateurs.
    """
    # On recupere tous les utilisateurs de la BDD
    users = User.objects.all()

    users_list = [{'username': user.username} for user in users]

    return jsonify(users_list), 200


# Route pour la connexion via Facebook
@auth_blueprint.route('/facebook_login')
def facebook_login():
    if not facebook.authorized:
        return redirect(url_for('facebook.login'))
    try:
        resp = facebook.get('/me?fields=id,name,email')
        resp.raise_for_status()
        user_info = resp.json()
        return jsonify(user_info), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
