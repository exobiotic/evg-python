# Simplified player logic: find and attack enemies
import random
from game import Action, is_empty


def get_actions(state):
    """Simplified AI: attack adjacent enemies, else move toward nearest enemy"""
    unit = state.unit
    
    # ===== ATTACK: Check all 4 adjacent positions =====
    for foe in state.foes:
        if foe.health <= 0:
            continue
        
        # Adjacent horizontally?
        if foe.y == unit.y and abs(foe.x - unit.x) == 1:
            direction = "Left" if foe.x < unit.x else "Right"
            return [Action("Attack", direction)]
        
        # Adjacent vertically?
        if foe.x == unit.x and abs(foe.y - unit.y) == 1:
            direction = "Up" if foe.y < unit.y else "Down"
            return [Action("Attack", direction)]
    
    # ===== MOVE: Find and chase nearest alive enemy =====
        
    # ===== DEFAULT: Random valid move =====
    directions = ["Up", "Down", "Left", "Right"]
    random.shuffle(directions)
    for direction in directions:
        x, y = unit.x, unit.y
        if direction == "Up":
            y -= 1
        elif direction == "Down":
            y += 1
        elif direction == "Left":
            x -= 1
        else:  # Right
            x += 1
        
        if is_empty(x, y, state):
            return [Action("Move", direction)]
    
    return []


def get_player_info():
    return {
        "id": "basic-ai-001",
        "name": "Basic AI"
    }


def game_end():
    pass
