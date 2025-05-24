"""
Combat Calculator - Evaluate fight outcomes before engaging
Calculates win probability based on attack/defense stats, not just level
"""
from artifactsmmo_wrapper import wrapper, logger
from config import config

class CombatCalculator:
    """Calculate combat outcomes and win probabilities"""
    
    def __init__(self, api):
        self.api = api
    
    def calculate_damage(self, attacker_stats, defender_resistances):
        """Calculate total damage per turn"""
        elements = ['fire', 'earth', 'water', 'air']
        total_damage = 0
        
        for element in elements:
            attack_key = f'attack_{element}' if 'attack_' in str(attacker_stats.__dict__.keys()) else element
            resist_key = f'res_{element}'
            
            # Get attack value (character has both attack_X and dmg_X)
            if hasattr(attacker_stats, f'attack_{element}'):
                attack = getattr(attacker_stats, f'attack_{element}', 0)
                if hasattr(attacker_stats, f'dmg_{element}'):
                    attack += getattr(attacker_stats, f'dmg_{element}', 0)
            else:
                attack = getattr(attacker_stats, attack_key, 0)
            
            # Get resistance value
            resistance = getattr(defender_resistances, resist_key, 0)
            
            # Calculate effective damage (minimum 1)
            effective_damage = max(1, attack - resistance)
            total_damage += effective_damage
        
        return total_damage
    
    def analyze_combat(self, monster_code):
        """Analyze combat outcome between character and monster"""
        # Get monster stats
        monster = self.api.monsters.get(code=monster_code)
        if not monster:
            return None
        
        # Calculate damage per turn
        char_damage = self.calculate_damage(self.api.char, monster)
        monster_damage = self.calculate_damage(monster, self.api.char)
        
        # Calculate turns to kill
        char_turns_to_kill = max(1, monster.hp // char_damage) if char_damage > 0 else 999
        monster_turns_to_kill = max(1, self.api.char.hp // monster_damage) if monster_damage > 0 else 999
        
        # Determine win probability
        if char_turns_to_kill < monster_turns_to_kill:
            win_prob = "HIGH"
            can_win = True
        elif char_turns_to_kill == monster_turns_to_kill:
            win_prob = "MEDIUM"
            can_win = True  # Could go either way, but allow it
        else:
            win_prob = "LOW" 
            can_win = False
        
        return {
            'monster': monster,
            'char_damage_per_turn': char_damage,
            'monster_damage_per_turn': monster_damage,
            'char_turns_to_kill': char_turns_to_kill,
            'monster_turns_to_kill': monster_turns_to_kill,
            'win_probability': win_prob,
            'can_win': can_win,
            'hp_ratio': self.api.char.hp / monster.hp if monster.hp > 0 else 1,
            'damage_ratio': char_damage / monster_damage if monster_damage > 0 else 999
        }
    
    def find_winnable_monsters(self, level_range=None, max_distance=20):
        """Find monsters the character can actually beat"""
        if level_range is None:
            min_level = max(1, self.api.char.level - 2)
            max_level = self.api.char.level + 1
        else:
            min_level, max_level = level_range
        
        # Get monsters in level range
        all_monsters = self.api.monsters.get(min_level=min_level, max_level=max_level)
        if not hasattr(all_monsters, '__iter__'):
            all_monsters = [all_monsters] if all_monsters else []
        
        winnable_monsters = []
        current_pos = (self.api.char.pos.x, self.api.char.pos.y)
        
        for monster in all_monsters:
            # Analyze combat
            analysis = self.analyze_combat(monster.code)
            if not analysis or not analysis['can_win']:
                continue
            
            # Find locations
            locations = self.api.maps.get(content_code=monster.code)
            if not locations:
                continue
            
            # Find closest location
            if not hasattr(locations, '__iter__'):
                locations = [locations]
            
            closest_location = None
            min_distance = float('inf')
            
            for location in locations:
                distance = abs(location.x - current_pos[0]) + abs(location.y - current_pos[1])
                if distance < min_distance and distance <= max_distance:
                    min_distance = distance
                    closest_location = location
            
            if closest_location:
                winnable_monsters.append({
                    'monster': monster,
                    'analysis': analysis,
                    'location': closest_location,
                    'distance': min_distance
                })
        
        # Sort by win probability and distance
        def sort_key(m):
            prob_weight = {'HIGH': 3, 'MEDIUM': 2, 'LOW': 1}[m['analysis']['win_probability']]
            return (prob_weight, -m['distance'])  # High prob first, then close distance
        
        winnable_monsters.sort(key=sort_key, reverse=True)
        return winnable_monsters
    
    def print_combat_analysis(self, monster_code):
        """Print detailed combat analysis"""
        analysis = self.analyze_combat(monster_code)
        if not analysis:
            print(f"❌ Could not analyze {monster_code}")
            return
        
        monster = analysis['monster']
        
        print(f"\n⚔️ COMBAT ANALYSIS: {monster.name}")
        print("="*50)
        print(f"📊 Character vs {monster.name}:")
        print(f"   Character Damage/Turn: {analysis['char_damage_per_turn']}")
        print(f"   Monster Damage/Turn: {analysis['monster_damage_per_turn']}")
        print(f"   Character needs {analysis['char_turns_to_kill']} turns to win")
        print(f"   Monster needs {analysis['monster_turns_to_kill']} turns to win")
        
        color = {"HIGH": "🟢", "MEDIUM": "🟡", "LOW": "🔴"}[analysis['win_probability']]
        print(f"   Win Probability: {color} {analysis['win_probability']}")
        print(f"   Recommended: {'✅ FIGHT' if analysis['can_win'] else '❌ AVOID'}")

# Global calculator instance
def get_combat_calculator():
    """Get a combat calculator instance"""
    wrapper.token = config.token
    api = wrapper.character(config.character_name)
    return CombatCalculator(api)

if __name__ == "__main__":
    print("⚔️ COMBAT CALCULATOR")
    print("="*50)
    
    calc = get_combat_calculator()
    
    # Analyze specific monsters
    test_monsters = ['yellow_slime', 'green_slime', 'blue_slime', 'red_slime']
    
    for monster_code in test_monsters:
        calc.print_combat_analysis(monster_code)
    
    print(f"\n🎯 FINDING WINNABLE MONSTERS")
    print("="*50)
    
    winnable = calc.find_winnable_monsters(max_distance=15)
    if winnable:
        print(f"Found {len(winnable)} winnable monsters:")
        for i, entry in enumerate(winnable[:5], 1):
            monster = entry['monster']
            analysis = entry['analysis']
            location = entry['location']
            distance = entry['distance']
            
            color = {"HIGH": "🟢", "MEDIUM": "🟡", "LOW": "🔴"}[analysis['win_probability']]
            print(f"{i}. {monster.name} (Lvl {monster.level}) {color}")
            print(f"   Location: ({location.x}, {location.y}) - Distance: {distance}")
            print(f"   Damage Ratio: {analysis['damage_ratio']:.1f}:1")
            print(f"   Win Probability: {analysis['win_probability']}")
    else:
        print("❌ No winnable monsters found nearby")
        print("💡 Try improving your equipment or finding weaker monsters") 