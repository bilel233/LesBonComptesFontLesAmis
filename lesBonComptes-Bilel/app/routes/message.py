from flask import Blueprint, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import jwt_required, get_jwt_identity
from mongoengine import Q, DoesNotExist, ValidationError
from ..models.user import User
from ..models.group import Group
from ..models.message import Message

messaging_blueprint = Blueprint('messaging_blueprint', __name__)
CORS(messaging_blueprint, resources={r"/*": {"origins": "*"}})

@messaging_blueprint.route('/send_group_message', methods=['POST'])
@jwt_required()
def send_group_message():
    sender_username = get_jwt_identity()
    sender = User.objects.get(username=sender_username)
    group_id = request.json.get('group_id')
    content = request.json.get('content')

    try:
        group = Group.objects.get(id=group_id)
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

    try:
        recipient = User.objects.get(username=recipient_username)
    except User.DoesNotExist:
        return jsonify({'error': 'Recipient not found'}), 404

    message = Message(content=content, sender=sender, recipient=recipient)
    message.save()
    return jsonify({'message': 'Private message sent successfully'}), 201

@messaging_blueprint.route('/group_messages/<group_id>', methods=['GET'])
@jwt_required()
def list_group_messages(group_id):
    try:
        messages = Message.objects(group=group_id).order_by('timestamp')
        return jsonify([
            {'sender': msg.sender.username, 'content': msg.content, 'timestamp': msg.timestamp}
            for msg in messages
        ]), 200
    except Group.DoesNotExist:
        return jsonify({'error': 'Group not found'}), 404

@messaging_blueprint.route('/private_messages/<recipient_username>', methods=['GET'])
@jwt_required()
def list_private_messages(recipient_username):
    current_user_username = get_jwt_identity()
    try:
        recipient = User.objects.get(username=recipient_username)
        current_user = User.objects.get(username=current_user_username)

        messages = Message.objects(
            (Q(sender=current_user) & Q(recipient=recipient)) |
            (Q(sender=recipient) & Q(recipient=current_user))
        ).order_by('timestamp')

        return jsonify([
            {'sender': msg.sender.username, 'content': msg.content, 'timestamp': msg.timestamp}
            for msg in messages
        ]), 200
    except User.DoesNotExist:
        return jsonify({'error': 'User not found'}), 404
    except ValidationError:
        return jsonify({'error': 'Invalid data'}), 400
