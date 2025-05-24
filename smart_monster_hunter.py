"""
Smart Monster Hunter - Only fights monsters you can actually beat!
Uses combat analysis instead of just level matching
"""
from artifactsmmo_wrapper import wrapper, logger
from config import config
from combat_calculator import CombatCalculator
import time

# Load configuration
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

def rest_until_healed(target_health_pct=80, max_rest_cycles=10):
    """Rest until health reaches target percentage"""
    if not needs_healing(target_health_pct):
        return True
    
    print(f"💤 Healing: {api.char.hp}/{api.char.max_hp} ({get_health_percentage():.1f}%) -> {target_health_pct}%")
    
    cycles = 0
    while api.char.hp < api.char.max_hp and cycles < max_rest_cycles:
        cycles += 1
        initial_hp = api.char.hp
        
        try:
            api.actions.rest()
            healed = api.char.hp - initial_hp
            health_pct = get_health_percentage()
            
            if healed > 0:
                print(f"   ✅ Rest {cycles}: +{healed} HP ({health_pct:.1f}%)")
            
            if health_pct >= target_health_pct:
                print(f"   🎉 Healing complete!")
                break
                
        except Exception as e:
            print(f"   ❌ Rest failed: {e}")
            break
    
    return get_health_percentage() >= target_health_pct

def smart_hunt(max_distance=15, hunt_count=5):
    """Intelligently hunt monsters using combat analysis"""
    print(f"🧠 SMART MONSTER HUNTER")
    print("="*50)
    print(f"🎮 Character: {config.character_name} (Level {api.char.level})")
    print(f"💚 Health: {api.char.hp}/{api.char.max_hp} ({get_health_percentage():.1f}%)")
    print(f"📍 Position: ({api.char.pos.x}, {api.char.pos.y})")
    
    # Initial health check
    if needs_healing(80):
        print(f"\n💚 PRE-HUNT HEALING")
        if not rest_until_healed(85):
            print("❌ Could not heal enough for hunting")
            return False
    
    successful_hunts = 0
    
    for hunt_num in range(hunt_count):
        print(f"\n🎯 HUNT {hunt_num + 1}/{hunt_count}")
        print("-" * 30)
        
        # Find winnable monsters
        print("🔍 Analyzing available monsters...")
        winnable_monsters = combat_calc.find_winnable_monsters(max_distance=max_distance)
        
        if not winnable_monsters:
            print("❌ No winnable monsters found nearby!")
            print("💡 Suggestions:")
            print("   • Try increasing max_distance")
            print("   • Improve equipment")
            print("   • Level up by gathering resources first")
            break
        
        # Select best target
        best_target = winnable_monsters[0]
        monster = best_target['monster']
        analysis = best_target['analysis']
        location = best_target['location']
        distance = best_target['distance']
        
        color = {"HIGH": "🟢", "MEDIUM": "🟡", "LOW": "🔴"}[analysis['win_probability']]
        print(f"🎯 Selected Target: {monster.name} (Level {monster.level}) {color}")
        print(f"   Win Probability: {analysis['win_probability']}")
        print(f"   Damage Ratio: {analysis['damage_ratio']:.1f}:1 (Character:Monster)")
        print(f"   Location: ({location.x}, {location.y}) - Distance: {distance}")
        print(f"   Expected Turns: {analysis['char_turns_to_kill']} to win")
        
        # Pre-fight health check
        health_threshold = 70 if analysis['win_probability'] == 'HIGH' else 80
        if needs_healing(health_threshold):
            print(f"💚 Pre-fight healing to {health_threshold}%...")
            if not rest_until_healed(health_threshold + 5):
                print("❌ Could not heal enough for this fight")
                continue
        
        # Move to target
        print(f"🚶 Moving to {monster.name}...")
        api.actions.move(location.x, location.y)
        print(f"✅ Arrived at ({api.char.pos.x}, {api.char.pos.y})")
        
        # Fight with confidence!
        print(f"⚔️ Fighting {monster.name} (PREDICTED WIN!)...")
        try:
            fight_result = api.actions.fight()
            print("🏆 Victory! As predicted by combat analysis!")
            print(f"💰 Gold: {api.char.gold}")
            print(f"💚 Post-fight HP: {api.char.hp}/{api.char.max_hp} ({get_health_percentage():.1f}%)")
            
            successful_hunts += 1
            
            # Post-fight healing if needed
            if needs_healing(60):
                print(f"💚 Post-fight healing...")
                rest_until_healed(75)
                
        except Exception as e:
            print(f"❌ Fight failed unexpectedly: {e}")
            print("🤔 This shouldn't happen with our combat analysis!")
            
            # Emergency healing
            if get_health_percentage() < 40:
                print(f"🚨 Emergency healing...")
                rest_until_healed(70)
        
        # Rest between fights for multi-hunt
        if hunt_num < hunt_count - 1:
            print("💤 Resting between hunts...")
            rest_until_healed(80)
    
    print(f"\n🏆 SMART HUNT SUMMARY")
    print("="*50)
    print(f"   Successful Hunts: {successful_hunts}/{hunt_count}")
    print(f"   Success Rate: {(successful_hunts/hunt_count)*100:.1f}%")
    print(f"   Final Level: {api.char.level}")
    print(f"   Final Gold: {api.char.gold}")
    print(f"   Final HP: {api.char.hp}/{api.char.max_hp} ({get_health_percentage():.1f}%)")
    
    if successful_hunts == hunt_count:
        print("🎉 Perfect hunting session!")
    elif successful_hunts > 0:
        print("✅ Good hunting session!")
    else:
        print("😔 No successful hunts - need better equipment or lower level monsters")

def analyze_current_options():
    """Analyze what monsters are available to fight"""
    print(f"🔍 CURRENT COMBAT OPTIONS")
    print("="*50)
    
    print("📊 Combat Analysis for Nearby Monsters:")
    
    # Test all slimes
    slime_types = ['yellow_slime', 'green_slime', 'blue_slime', 'red_slime']
    for slime in slime_types:
        combat_calc.print_combat_analysis(slime)
    
    print(f"\n🎯 RECOMMENDED TARGETS:")
    winnable = combat_calc.find_winnable_monsters(max_distance=20)
    
    if winnable:
        for i, entry in enumerate(winnable[:3], 1):
            monster = entry['monster']
            analysis = entry['analysis']
            location = entry['location']
            distance = entry['distance']
            
            color = {"HIGH": "🟢", "MEDIUM": "🟡", "LOW": "🔴"}[analysis['win_probability']]
            print(f"{i}. {monster.name} (Lvl {monster.level}) {color}")
            print(f"   Distance: {distance} tiles")
            print(f"   Win Chance: {analysis['win_probability']}")
            print(f"   Your Damage: {analysis['char_damage_per_turn']}/turn")
            print(f"   Their Damage: {analysis['monster_damage_per_turn']}/turn")
    else:
        print("❌ No winnable monsters found!")
        print("💡 You need better equipment or to find weaker monsters")

if __name__ == "__main__":
    print("🧠 SMART MONSTER HUNTER")
    print("Combat Analysis + Health Management = Safe Hunting!")
    print("="*60)
    
    # First, analyze current options
    analyze_current_options()
    
    print(f"\n" + "="*60)
    
    # Then do smart hunting
    print("\n🎯 STARTING SMART HUNT SESSION")
    smart_hunt(max_distance=20, hunt_count=3) 