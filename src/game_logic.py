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

    def player_hit(self, equipment_shooter_code: int, equipment_hit_code: int) -> None:
        # Attributing points to a green user
        for user in self.green_users:
            # Check if id matches, and if player doesn't hit own teammate
            if user.equipment_id == equipment_shooter_code and equipment_hit_code not in self.green_user_equipment_ids:
                user.game_score += POINTS_PER_TAG
                self.green_team_score += POINTS_PER_TAG
                for victim_user in self.red_users:
                    if victim_user.equipment_id == equipment_hit_code:
                        shot_user: User = victim_user
                self.game_event_list.append(f"{user.username} hit {shot_user.username}")
        
        # Attributing points to a red user
        for user in self.red_users:
            # Check if id matches, and if player doesn't hit own teammate
            if user.equipment_id == equipment_shooter_code and equipment_hit_code not in self.red_user_equipment_ids:
                user.game_score += POINTS_PER_TAG
                self.red_team_score += POINTS_PER_TAG
                for victim_user in self.green_users:
                    if victim_user.equipment_id == equipment_hit_code:
                        shot_user: User = victim_user
                self.game_event_list.append(f"{user.username} hit {shot_user.username}")

    def red_base_hit(self, equipment_shooter_code: int) -> None:
        for user in self.green_users:
            # Check if id matches, and then add 100 points to the green player and team
            if user.equipment_id == equipment_shooter_code:
                user.game_score += POINTS_PER_BASE_HIT
                self.green_team_score += POINTS_PER_BASE_HIT
                self.game_event_list.append(f"{user.username} hit red base")

    def green_base_hit(self, equipment_shooter_code: int) -> None:
        for user in self.red_users:
            # Check if id matches, and then add 100 points to the red player and team
            if user.equipment_id == equipment_shooter_code:
                user.game_score += POINTS_PER_BASE_HIT
                self.red_team_score += POINTS_PER_BASE_HIT
                self.game_event_list.append(f"{user.username} hit green base")
