from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models.user import User
from ..models.group import Group
from ..models.message import Message

messaging_blueprint = Blueprint('messaging_blueprint', __name__)

@messaging_blueprint.route('/send_group_message', methods=['POST'])
@jwt_required()
def send_group_message():
    """Route pour envoyer un message au groupe."""
    sender_username = get_jwt_identity()
    sender = User.objects(username=sender_username).first()


    data = request.json
    content = data.get('content')
    group_id = data.get('group_id')


    if not content or not group_id:
        return jsonify({'message': 'Le contenu et l\'identifiant du groupe sont requis'}), 400


    group = Group.objects(id=group_id).first()
    if not group:
        return jsonify({'message': 'Groupe non trouvé'}), 404


    if sender not in group.members:
        return jsonify({'message': 'L\'expéditeur doit être membre du groupe'}), 403


    message = Message(content=content, sender=sender, group=group)
    message.save()

    return jsonify({'message': 'Message envoyé au groupe avec succès'}), 201

@messaging_blueprint.route('/group_messages/<group_id>', methods=['GET'])
@jwt_required()
def list_group_messages(group_id):
    """lister les messages de groupes"""
    messages = Message.objects(group=group_id).order_by('timestamp')
    return jsonify([{
        'content': message.content,
        'sender': message.sender.username,
        'timestamp': message.timestamp
    } for message in messages]), 200

@messaging_blueprint.route('/send_private_message', methods=['POST'])
@jwt_required()
def send_private_message():
    """Route pour envoyer un message privé."""
    sender_username = get_jwt_identity()
    sender = User.objects(username=sender_username).first()


    data = request.json
    content = data.get('content')
    recipient_username = data.get('recipient')


    if not content or not recipient_username:
        return jsonify({'message': 'Le contenu et le destinataire sont requis'}), 400


    recipient = User.objects(username=recipient_username).first()
    if not recipient:
        return jsonify({'message': 'Destinataire non trouvé'}), 404


    message = Message(content=content, sender=sender, recipient=recipient)
    message.save()

    return jsonify({'message': 'Message privé envoyé avec succès'}), 201


@messaging_blueprint.route('/all_group_messages', methods=['GET'])
@jwt_required()
def list_all_group_messages():
    """Lister tous les messages de groupes."""
    messages = Message.objects.filter(group__ne=None).order_by(
        'timestamp')

    messages_list = []
    for message in messages:
        messages_list.append({
            'content': message.content,
            'sender': message.sender.username,
            'group_id': str(message.group.id) if message.group else None,
            'timestamp': message.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        })

    return jsonify(messages_list), 200

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

@messaging_blueprint.route('/send_message', methods=['POST'])
@jwt_required()
def send_message():
    data = request.get_json()
    sender_id = get_jwt_identity()
    group_id = data.get('group_id')
    recipient_id = data.get('recipient_id', None)
    content = data.get('content')

    if not content:
        return jsonify({"message": "Content is required"}), 400

    message = Message(
        sender=sender_id,
        group=group_id if not recipient_id else None,
        recipient=recipient_id,
        content=content
    )
    message.save()
    return jsonify({"message": "Message sent successfully"}), 201
