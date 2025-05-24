"""
Combat Analysis - Analyze monster and character stats
"""
from artifactsmmo_wrapper import wrapper, logger
from config import config

wrapper.token = config.token
api = wrapper.character(config.character_name)
logger.setLevel("INFO")

# Get Yellow Slime stats - api.monsters.get() returns a single Monster, not a list
monster = api.monsters.get(code='yellow_slime')
if monster:
    print("🐉 YELLOW SLIME STATS:")
    print(f"   Name: {monster.name}")
    print(f"   Level: {monster.level}")
    print(f"   HP: {monster.hp}")
    print(f"   Attack Fire: {monster.attack_fire}")
    print(f"   Attack Earth: {monster.attack_earth}")
    print(f"   Attack Water: {monster.attack_water}")
    print(f"   Attack Air: {monster.attack_air}")
    print(f"   Resistance Fire: {monster.res_fire}")
    print(f"   Resistance Earth: {monster.res_earth}")
    print(f"   Resistance Water: {monster.res_water}")
    print(f"   Resistance Air: {monster.res_air}")
    print(f"   Min Gold: {monster.min_gold}")
    print(f"   Max Gold: {monster.max_gold}")

print(f"\n⚔️ CHARACTER STATS:")
print(f"   Name: {api.char.name}")
print(f"   Level: {api.char.level}")
print(f"   HP: {api.char.hp}/{api.char.max_hp}")
print(f"   Attack Fire: {api.char.attack_fire}")
print(f"   Attack Earth: {api.char.attack_earth}")
print(f"   Attack Water: {api.char.attack_water}")
print(f"   Attack Air: {api.char.attack_air}")
print(f"   Damage Fire: {api.char.dmg_fire}")
print(f"   Damage Earth: {api.char.dmg_earth}")
print(f"   Damage Water: {api.char.dmg_water}")
print(f"   Damage Air: {api.char.dmg_air}")
print(f"   Resistance Fire: {api.char.res_fire}")
print(f"   Resistance Earth: {api.char.res_earth}")
print(f"   Resistance Water: {api.char.res_water}")
print(f"   Resistance Air: {api.char.res_air}")
print(f"   Critical Strike: {api.char.critical_strike}")
print(f"   Haste: {api.char.haste}")
print(f"   Total Damage: {api.char.dmg}")

if monster:
    print(f"\n📊 COMBAT ANALYSIS:")
    
    # Calculate character's total attack vs monster's resistances
    char_attacks = {
        'fire': api.char.attack_fire + api.char.dmg_fire,
        'earth': api.char.attack_earth + api.char.dmg_earth,
        'water': api.char.attack_water + api.char.dmg_water,
        'air': api.char.attack_air + api.char.dmg_air
    }
    
    monster_resistances = {
        'fire': monster.res_fire,
        'earth': monster.res_earth,
        'water': monster.res_water,
        'air': monster.res_air
    }
    
    monster_attacks = {
        'fire': monster.attack_fire,
        'earth': monster.attack_earth,
        'water': monster.attack_water,
        'air': monster.attack_air
    }
    
    char_resistances = {
        'fire': api.char.res_fire,
        'earth': api.char.res_earth,
        'water': api.char.res_water,
        'air': api.char.res_air
    }
    
    print(f"   Character vs Monster Damage Analysis:")
    total_char_damage = 0
    for element, attack in char_attacks.items():
        resistance = monster_resistances[element]
        effective_damage = max(1, attack - resistance)  # Minimum 1 damage
        total_char_damage += effective_damage
        print(f"     {element.capitalize()}: {attack} attack - {resistance} resistance = {effective_damage} damage")
    
    print(f"   Total Character Damage per Turn: ~{total_char_damage}")
    
    print(f"\n   Monster vs Character Damage Analysis:")
    total_monster_damage = 0
    for element, attack in monster_attacks.items():
        resistance = char_resistances[element]
        effective_damage = max(1, attack - resistance)  # Minimum 1 damage
        total_monster_damage += effective_damage
        print(f"     {element.capitalize()}: {attack} attack - {resistance} resistance = {effective_damage} damage")
    
    print(f"   Total Monster Damage per Turn: ~{total_monster_damage}")
    
    # Estimate turns to kill
    char_turns_to_kill = max(1, monster.hp // total_char_damage) if total_char_damage > 0 else 999
    monster_turns_to_kill = max(1, api.char.hp // total_monster_damage) if total_monster_damage > 0 else 999
    
    print(f"\n🎯 BATTLE PREDICTION:")
    print(f"   Character needs ~{char_turns_to_kill} turns to kill monster")
    print(f"   Monster needs ~{monster_turns_to_kill} turns to kill character")
    
    if char_turns_to_kill < monster_turns_to_kill:
        win_probability = "HIGH (Character wins!)"
        color = "🟢"
    elif char_turns_to_kill == monster_turns_to_kill:
        win_probability = "MEDIUM (Close fight!)"
        color = "🟡"
    else:
        win_probability = "LOW (Character loses!)"
        color = "🔴"
    
    print(f"   Win Probability: {color} {win_probability}")
    
    # Additional factors
    print(f"\n🔍 ADDITIONAL FACTORS:")
    print(f"   Character Critical Strike: {api.char.critical_strike}% (increases damage)")
    print(f"   Character Haste: {api.char.haste} (affects turn order)")
    print(f"   HP Advantage: Character {api.char.hp} vs Monster {monster.hp}")
else:
    print("❌ Could not find Yellow Slime data") 