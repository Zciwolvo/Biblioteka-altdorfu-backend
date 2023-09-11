import json
import os

class Character:
    def __init__(self, character_id, data, owner_id, allowed_users=None):
        self.character_id = character_id
        self.data = data
        self.owner_id = owner_id
        self.allowed_users = allowed_users or []

    def to_dict(self):
        return {
            'character_id': self.character_id,
            'data': self.data,
            'owner_id': self.owner_id,
            'allowed_users': self.allowed_users
        }

    @classmethod
    def from_dict(cls, character_data):
        return cls(
            character_id=character_data['character_id'],
            data=character_data['data'],
            owner_id=character_data['owner_id'],
            allowed_users=character_data.get('allowed_users', [])
        )

    def save_to_json(self):
        character_file_path = os.path.join('characters', f'{self.character_id}.json')
        with open(character_file_path, 'w') as file:
            json.dump(self.to_dict(), file)

    @classmethod
    def load_from_json(cls, character_id):
        character_file_path = os.path.join('characters', f'{character_id}.json')
        if os.path.exists(character_file_path):
            with open(character_file_path, 'r') as file:
                character_data = json.load(file)
                return cls.from_dict(character_data)
        return None
