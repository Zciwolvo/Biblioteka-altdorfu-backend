from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import Blueprint, jsonify
from random import randint

from character_data import Character

character_blueprint = Blueprint('character', __name__)


@character_blueprint.route('/create_character', methods=['POST'])
@jwt_required()
def create_character():
    current_user = get_jwt_identity()

    sample_character_data = {
        'name': 'Sample Character',
        'level': 1,
        'owner_id': current_user['username']
    }

    # Create a new character
    character: Character = Character(
        character_id=randint(10000000,99999999),
        data=sample_character_data,
        owner_id=current_user['username']
    )
    character.save_to_json()

    return jsonify({'message': 'Character created successfully'}), 201

# Example route to access a character
@character_blueprint.route('/character/<character_id>', methods=['GET'])
@jwt_required()
def get_character(character_id):
    current_user = get_jwt_identity()

    # Load the character
    character: Character = Character.load_from_json(character_id)

    # Check if the user is an admin (admin role)
    if current_user.get('role') == 'admin':
        return jsonify(character.to_dict())

    # Check if the user owns the character or has permission
    if character.owner_id == current_user.get('sub') or current_user.get('sub') in character.allowed_users:
        return jsonify(character.to_dict())

    return jsonify({'message': 'Access denied'}), 403