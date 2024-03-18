from typing import Dict, List
from user_info import User

POINTS_PER_TAG: int = 10
POINTS_PER_BASE_HIT: int = 100

class GameState:
    def __init__(self, users_dict: Dict[str, List[User]]) -> None:
        # User references
        self.green_users = users_dict["green"]
        self.red_users = users_dict["red"]

        # Red equipment IDs
        self.red_user_equipment_ids = []
        for user in self.red_users:
            self.red_user_equipment_ids.append(user.equipment_id)

       # Green equipment IDs
        self.green_user_equipment_ids = []
        for user in self.green_users:
            self.green_user_equipment_ids.append(user.equipment_id)

        # Team scores, set to default of zero
        self.red_team_score: int = 0
        self.green_team_score: int = 0

        # If bases are scored
        self.red_base_scored: bool = False
        self.green_base_scored: bool = False
        self.game_event_list: [str] = []
