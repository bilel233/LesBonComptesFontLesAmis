from app import app
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from mongoengine import DoesNotExist, ValidationError, NotUniqueError
from ..models.group import Group
from ..models.user import User

group_blueprint = Blueprint('group_blueprint', __name__)

@group_blueprint.route('/create', methods=['POST'])
@jwt_required()
def create_group():
    current_user_username = get_jwt_identity()
    current_user = User.objects(username=current_user_username).first()

    if not current_user:
        return jsonify({"msg": "User not found"}), 404

    data = request.json
    name = data.get('name')

    if not name:
        return jsonify({'msg': 'Missing group name'}), 400


    if Group.objects(name=name, creator=current_user):
        return jsonify({'msg': 'Group name already used by this user'}), 400

    try:
        group = Group(name=name, members=[current_user], creator=current_user)
        group.save()
        return jsonify({
            'msg': f'Group "{name}" created successfully',
            'group_id': str(group.id),
            'name': group.name
        }), 201
    except ValidationError as e:
        return jsonify({'msg': str(e)}), 400
    except NotUniqueError:
        return jsonify({'msg': 'Group name must be unique'}), 400
    except Exception as e:
        return jsonify({'msg': 'An unexpected error occurred', 'error': str(e)}), 500
@group_blueprint.route('/join/<group_id>', methods=['POST'])
@jwt_required()
def join_group(group_id):
    current_user_username = get_jwt_identity()
    try:
        current_user = User.objects.get(username=current_user_username)
        group = Group.objects.get(id=group_id)

        if current_user in group.members:
            return jsonify({'msg': 'User already a member of the group'}), 400

        group.members.append(current_user)
        group.save()
        return jsonify({'msg': f'User {current_user_username} added to the group successfully'}), 200
    except DoesNotExist:
        return jsonify({'msg': 'Group or user not found'}), 404
    except ValidationError:
        return jsonify({'msg': 'Invalid group ID'}), 400
    except Exception as e:
        return jsonify({'msg': str(e)}), 500

@group_blueprint.route('/<group_id>/balances', methods=['GET'])
@jwt_required()
def get_group_balances(group_id):
    try:
        group = Group.objects.get(id=group_id)
        balances = group.calculate_balances()
        response = {
            'group_id': str(group.id),
            'balances': balances
        }
        return jsonify(response), 200
    except ValidationError:
        return jsonify({'message': 'ID de groupe invalide'}), 400
    except DoesNotExist:
        return jsonify({'message': 'Groupe non trouvé'}), 404
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@group_blueprint.route('/all', methods=['GET'])
@jwt_required()
def get_all_groups():
    groups = Group.objects.all()
    groups_data = []
    for group in groups:
        creator_username = group.creator.username if group.creator else 'Inconnu'
        members_usernames = [member.username for member in group.members]
        groups_data.append({
            'id': str(group.id),
            'name': group.name,
            'creator': creator_username,
            'members': members_usernames
        })
    return jsonify(groups_data), 200

@group_blueprint.route('/<group_id>', methods=['GET'])
@jwt_required()
def get_group_by_id(group_id):
    try:
        group = Group.objects.get(id=group_id)
        return jsonify({
            'id': str(group.id),
            'name': group.name,
            'creator': group.creator.username,
            'members': [{'username': member.username, 'id': str(member.id)} for member in group.members]
        }), 200
    except DoesNotExist:
        return jsonify({"message": " Groupe non trouve "}), 404
    except ValidationError:
        return jsonify({"message": "ID de groupe invalide"}), 400
    except Exception as e:
        return jsonify({"message": str(e)}), 500

@group_blueprint.route('/<group_id>', methods=['DELETE'])
@jwt_required()
def delete_group(group_id):
    try:
        current_user_username = get_jwt_identity()
        current_user = User.objects.get(username=current_user_username)
        group = Group.objects.get(id=group_id)

        if group.creator != current_user:
            return jsonify({'message': 'Seul le créateur du groupe peut le supprimer'}), 403

        group.delete()
        return jsonify({'message': 'Groupe supprimé avec succès'}), 200
    except DoesNotExist:
        return jsonify({'message': 'Groupe non trouvé'}), 404
    except ValidationError:
        return jsonify({'message': 'ID de groupe invalide'}), 400
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@group_blueprint.route('/<group_id>', methods=['PUT'])
@jwt_required()
def update_group(group_id):
    try:
        current_user_username = get_jwt_identity()
        current_user = User.objects.get(username=current_user_username)
        group = Group.objects.get(id=group_id)

        if group.creator != current_user:
            return jsonify({'message': 'Seul le créateur du groupe peut le modifier'}), 403

        data = request.json
        name = data.get('name', None)
        if name:
            group.name = name

        group.save()
        return jsonify({'message': 'Groupe modifié avec succès', 'group': {
            'id': str(group.id),
            'name': group.name,
            'creator': group.creator.username,
            'members': [{'username': member.username, 'id': str(member.id)} for member in group.members]
        }}), 200
    except DoesNotExist:
        return jsonify({'message': 'Groupe non trouvé'}), 404
    except ValidationError:
        return jsonify({'message': 'Données invalides ou ID de groupe invalide'}), 400
    except Exception as e:
        return jsonify({'message': str(e)}), 500


@group_blueprint.route('/invite', methods=['POST'])
@jwt_required()
def invite_members():
    current_user_username = get_jwt_identity()
    current_user = User.objects(username=current_user_username).first()

    if not current_user:
        return jsonify({"msg": "Utilisateur non trouvé"}), 404

    data = request.json


    if data is None:
        return jsonify({'msg': 'Aucun JSON reçu. Vérifiez que le corps de la requête est bien formaté.'}), 400

    group_id = data.get('group_id')
    usernames = data.get('usernames')


    if not group_id:
        return jsonify({'msg': "L'ID du groupe est requis."}), 400
    if not usernames:
        return jsonify({'msg': "Les noms d'utilisateur sont requis."}), 400

    if not isinstance(usernames, list) or not all(isinstance(username, str) for username in usernames):
        return jsonify({'msg': "Les noms d'utilisateur doivent être une liste de chaînes de caractères"}), 400

    try:
        group = Group.objects.get(id=group_id)

        if group.creator != current_user:
            return jsonify({'msg': 'Seul le créateur du groupe peut inviter des membres'}), 403

        invited_users = User.objects(username__in=usernames)
        existing_usernames = set(user.username for user in invited_users)
        non_existent_usernames = set(usernames) - existing_usernames

        if non_existent_usernames:
            return jsonify(
                {'msg': f"Les utilisateurs suivants n'existent pas: {', '.join(non_existent_usernames)}"}), 404

        for user in invited_users:
            if user not in group.members:
                group.members.append(user)

        group.save()
        return jsonify({'msg': 'Membres invités avec succès'}), 200
    except Group.DoesNotExist:
        return jsonify({'msg': 'Groupe non trouvé'}), 404
    except Exception as e:
        return jsonify({'msg': 'Une erreur s\'est produite', 'error': str(e)}), 500
@group_blueprint.route('/user/<username>', methods=['GET'])
@jwt_required()
def get_groups_by_user(username):
    try:
        user = User.objects.get(username=username)
        groups = Group.objects(members=user)
        groups_data = []
        for group in groups:
            members_data = []
            for member_ref in group.members:
                member = User.objects.with_id(member_ref.id)
                if member:
                    members_data.append({'username': member.username, 'id': str(member.id)})
            groups_data.append({
                'id': str(group.id),
                'name': group.name,
                'creator': group.creator.username if group.creator else 'Unknown',
                'members': members_data
            })
        return jsonify(groups_data), 200
    except DoesNotExist:
        return jsonify({'message': 'User not found'}), 404
    except ValidationError:
        return jsonify({'message': 'Invalid data'}), 400
    except Exception as e:
        current_app.logger.error(f'Unexpected error: {str(e)}')
        return jsonify({'message': str(e)}), 500

@group_blueprint.route('/user_groups', methods=['GET'])
@jwt_required()
def get_user_groups():
    """recupere les groupes de l'utilisateur """
    current_user_username = get_jwt_identity()
    try:
        current_user = User.objects.get(username=current_user_username)
        groups = Group.objects(members=current_user)
        groups_data = [{
            'id': str(group.id),
            'name': group.name,
            'creator': group.creator.username if group.creator else 'Unknown',
            'members': [{'username': member.username, 'id': str(member.id)} for member in group.members]
        } for group in groups]
        return jsonify(groups_data), 200
    except DoesNotExist:
        return jsonify({'message': 'User not found'}), 404
    except ValidationError:
        return jsonify({'message': 'Invalid data'}), 400
    except Exception as e:
        return jsonify({'message': str(e)}), 500
