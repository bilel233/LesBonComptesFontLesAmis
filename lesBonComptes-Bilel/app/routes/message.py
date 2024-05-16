from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from mongoengine import Q

from ..models.user import User
from ..models.group import Group
from ..models.message import Message

messaging_blueprint = Blueprint('messaging_blueprint', __name__)

# Envoyer un message dans un groupe
@messaging_blueprint.route('/send_group_message', methods=['POST'])
@jwt_required()
def send_group_message():
    sender_username = get_jwt_identity()
    sender = User.objects.get(username=sender_username)
    group_name = request.json.get('group_name')
    content = request.json.get('content')

    try:
        group = Group.objects.get(name=group_name)
    except Group.DoesNotExist:
        return jsonify({'error': 'Group not found'}), 404

    if sender not in group.members:
        return jsonify({'error': 'Sender must be a member of the group'}), 403

    message = Message(content=content, sender=sender, group=group)
    message.save()
    return jsonify({'message': 'Message sent successfully'}), 201

@messaging_blueprint.route('/send_private_message', methods=['POST'])
@jwt_required()
def send_private_message():
    sender_username = get_jwt_identity()
    sender = User.objects.get(username=sender_username)
    recipient_username = request.json.get('recipient_username')
    content = request.json.get('content')

    recipient = User.objects.get(username=recipient_username)
    message = Message(content=content, sender=sender, recipient=recipient)
    message.save()
    return jsonify({'message': 'Private message sent successfully'}), 201

@messaging_blueprint.route('/group_messages/<group_id>', methods=['GET'])
@jwt_required()
def list_group_messages(group_id):
    messages = Message.objects(group=group_id)
    return jsonify([{'sender': msg.sender.username, 'content': msg.content, 'timestamp': msg.timestamp} for msg in messages]), 200

@messaging_blueprint.route('/private_messages/<recipient_username>', methods=['GET'])
@jwt_required()
def list_private_messages(recipient_username):
    current_user_username = get_jwt_identity()
    recipient = User.objects.get(username=recipient_username)
    current_user = User.objects.get(username=current_user_username)

    messages = Message.objects(
        (Q(sender=current_user) & Q(recipient=recipient)) |
        (Q(sender=recipient) & Q(recipient=current_user))
    ).order_by('timestamp')


@messaging_blueprint.route('/group_messages/delete/<message_id>', methods=['DELETE'])
@jwt_required()
def delete_group_message(message_id):
    """Route pour supprimer un message de groupe."""
    current_user_username = get_jwt_identity()
    try:
        # On trouve le message par son ID
        message = Message.objects.get(id=message_id)
    except Message.DoesNotExist:
        return jsonify({'message': 'Message non trouvé'}), 404

    # On vérifie si l'utilisateur courant est l'expéditeur du message ou un admin du groupe
    if message.sender.username != current_user_username and not current_user_username in [admin.username for admin in message.group.admins]:
        return jsonify({'message': 'Vous n\'avez pas l\'autorisation de supprimer ce message'}), 403

    # On supprime le message
    message.delete()
    return jsonify({'message': 'Message supprimé avec succès'}), 200

