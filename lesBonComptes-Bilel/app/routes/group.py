from flask import Blueprint, request, jsonify
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

    try:

        group = Group(name=name, members=[current_user], creator=current_user)
        group.save()
        return jsonify({'msg': f'Group "{name}" created successfully', 'group_id': str(group.id)}), 201

    except ValidationError as e:

        return jsonify({'msg': str(e)}), 400
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
    """
    Renvoie les soldes de tous les membres du groupe spécifié.
    """
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
        try:
            creator_username = group.creator.username if group.creator else 'Inconnu'
            members_usernames = []
            for member in group.members:
                try:
                    members_usernames.append(member.username)
                except DoesNotExist:
                    continue
        except DoesNotExist:
            creator_username = 'Inconnu'

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
    """
    Recupere un groupe specifique par son ID.

    """
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
    """
    Supprime un groupe spécifique par son ID.

    """

    try:
        # on recupere l'identite de l'utilisateur connecté.
        current_user_username = get_jwt_identity()
        current_user = User.objects.get(username=current_user_username)
        group = Group.objects.get(id=group_id)

        # on verifie  si l'utilisateur courant est le createur du groupe

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
    """
    Modifie un groupe spécifique par son ID.
    """
    try:
        current_user_username = get_jwt_identity()
        current_user = User.objects.get(username=current_user_username)
        group = Group.objects.get(id=group_id)

        # On  vérifie si l'utilisateur courant est le créateur du groupe
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


@group_blueprint.route('/<group_id>/invite', methods=['POST'])
@jwt_required()
def invite_members(group_id):
    """inviter des membres dans le groupe"""
    current_user = get_jwt_identity()
    group = Group.objects.get(id=group_id)

    if group.creator.username != current_user:
        return jsonify({'message': 'Seul le créateur du groupe peut inviter des membres'}), 403

    data = request.json
    usernames = data.get('usernames', [])
    invited_users = User.objects.filter(username__in=usernames)

    for user in invited_users:
        group.members.append(user)
    group.save()

    return jsonify({'message': 'Membres invités avec succès'}), 200
