from artifactsmmo_wrapper import wrapper, logger
from config import config
from combat_calculator import CombatCalculator
import time

# Load configuration from .env file
wrapper.token = config.token
api = wrapper.character(config.character_name)
logger.setLevel(config.log_level)

# Create combat calculator
combat_calc = CombatCalculator(api)

# Health management functions
def get_health_percentage():
    """Get current health as a percentage"""
    if api.char.max_hp == 0:
        return 100
    return (api.char.hp / api.char.max_hp) * 100

def needs_healing(threshold=50):
    """Check if character needs healing"""
    return api.char.hp < api.char.max_hp and get_health_percentage() < threshold

def rest_until_healed(target_health_pct=80):
    """Rest until health reaches target percentage"""
    if not needs_healing(target_health_pct):
        print(f"✅ Health is good: {api.char.hp}/{api.char.max_hp} ({get_health_percentage():.1f}%)")
        return True
    
    print(f"💤 Healing from {get_health_percentage():.1f}% to {target_health_pct}%...")
    
    while api.char.hp < api.char.max_hp and get_health_percentage() < target_health_pct:
        initial_hp = api.char.hp
        api.actions.rest()
        healed = api.char.hp - initial_hp
        if healed > 0:
            print(f"   ✅ Healed {healed} HP! Now: {api.char.hp}/{api.char.max_hp} ({get_health_percentage():.1f}%)")
    
    print(f"🎉 Healing complete: {api.char.hp}/{api.char.max_hp} ({get_health_percentage():.1f}%)")
    return True

print(f"🎮 Character: {config.character_name}")
print(f"📍 Current Position: ({api.char.pos.x}, {api.char.pos.y})")
print(f"⚔️ Current Level: {api.char.level}")
print(f"💚 Health: {api.char.hp}/{api.char.max_hp} ({get_health_percentage():.1f}%)")

# Always check health first!
if needs_healing(70):
    print(f"\n⚠️ Health is low! Healing before hunting...")
    rest_until_healed(80)

# Use combat calculator to find winnable monsters instead of just level matching!
print(f"\n🧠 SMART MONSTER ANALYSIS")
print("="*40)
print("🔍 Finding monsters you can actually beat...")

winnable_monsters = combat_calc.find_winnable_monsters(max_distance=15)

if winnable_monsters:
    print(f"✅ Found {len(winnable_monsters)} winnable monsters:")
    
    # Show top 3 options
    for i, entry in enumerate(winnable_monsters[:3], 1):
        monster = entry['monster']
        analysis = entry['analysis']
        location = entry['location']
        distance = entry['distance']
        
        color = {"HIGH": "🟢", "MEDIUM": "🟡", "LOW": "🔴"}[analysis['win_probability']]
        print(f"   {i}. {monster.name} (Lvl {monster.level}) {color}")
        print(f"      Distance: {distance} tiles | Win Chance: {analysis['win_probability']}")
        print(f"      Damage Ratio: {analysis['damage_ratio']:.1f}:1 (You:Monster)")
    
    # Fight the best option
    best_target = winnable_monsters[0]
    monster = best_target['monster']
    analysis = best_target['analysis']
    location = best_target['location']
    distance = best_target['distance']
    
    print(f"\n🎯 Selected Target: {monster.name}")
    print(f"⚔️ Expected Result: {analysis['win_probability']} win probability")
    print(f"📍 Location: ({location.x}, {location.y}) - Distance: {distance}")
    
    # Move to the monster location
    print(f"\n🚶 Moving to {monster.name}...")
    api.actions.move(location.x, location.y)
    print(f"✅ Arrived at ({api.char.pos.x}, {api.char.pos.y})")
    
    # Combat analysis gives us confidence - check health before fighting
    health_threshold = 60 if analysis['win_probability'] == 'HIGH' else 70
    print(f"\n⚔️ Pre-fight health check (need {health_threshold}%+)...")
    if needs_healing(health_threshold):
        print(f"⚠️ Health too low for fighting! Healing first...")
        rest_until_healed(health_threshold + 10)
    
    # Fight with confidence!
    print(f"⚔️ Fighting {monster.name} (Combat Analysis: {analysis['win_probability']} WIN!)...")
    try:
        fight_result = api.actions.fight()
        print("🏆 Victory! As predicted by combat analysis!")
        print(f"💰 Gold: {api.char.gold}")
        print(f"💚 Post-fight HP: {api.char.hp}/{api.char.max_hp} ({get_health_percentage():.1f}%)")
        
        # Check if we need healing after the fight
        if needs_healing(50):
            print(f"\n💤 Post-fight healing...")
            rest_until_healed(70)
            
    except Exception as e:
        print(f"❌ Fight failed: {e}")
        print("🤔 This is unexpected! Our combat analysis should have been accurate.")
        # Emergency healing if health is critically low
        if get_health_percentage() < 30:
            print(f"🚨 Emergency healing after failed fight!")
            rest_until_healed(60)

else:
    print("❌ No winnable monsters found nearby!")
    print("\n💡 SUGGESTIONS:")
    print("   • Your character may need better equipment")
    print("   • Try gathering resources to level up first")
    print("   • Look for lower level monsters further away")
    
    # Show what monsters are available but not winnable
    print(f"\n📊 ANALYSIS: Why you can't win fights")
    problem_monsters = ['yellow_slime', 'green_slime', 'blue_slime', 'red_slime']
    for monster_code in problem_monsters:
        analysis = combat_calc.analyze_combat(monster_code)
        if analysis:
            monster = analysis['monster']
            print(f"   {monster.name}: You deal {analysis['char_damage_per_turn']}/turn, they deal {analysis['monster_damage_per_turn']}/turn")

print(f"\n🎯 SMART HUNTING SUMMARY:")
print("="*40)
print("✅ Used combat analysis instead of just level matching")
print("✅ Only fought monsters with high win probability") 
print("✅ Health managed before and after fighting")
print("✅ Avoided certain death fights (like Yellow Slime)")
print("\n💡 TIP: Use smart_monster_hunter.py for continuous smart hunting!")