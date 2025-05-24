"""
Monster Hunter Utility
Advanced monster location and hunting functions for ArtifactsMmo
Now with automatic health management!
"""
from artifactsmmo_wrapper import wrapper, logger
from config import config
import time

# Load configuration
wrapper.token = config.token
api = wrapper.character(config.character_name)
logger.setLevel(config.log_level)

# Import health management functions
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

def safe_fight():
    """Safely fight with health checking"""
    # Check health before fighting
    if needs_healing(60):
        print("   ⚠️ Health too low for fighting! Healing first...")
        if not rest_until_healed(70):
            print("   ❌ Could not heal enough for fighting")
            return False
    
    try:
        result = api.actions.fight()
        health_pct = get_health_percentage()
        print(f"   💚 Post-fight HP: {api.char.hp}/{api.char.max_hp} ({health_pct:.1f}%)")
        return result
    except Exception as e:
        print(f"   ❌ Fight failed: {e}")
        return False

def calculate_distance(pos1, pos2):
    """Calculate Manhattan distance between two positions"""
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

def find_monster_locations(monster_code):
    """Find all map locations where a specific monster appears"""
    locations = api.maps.get(content_code=monster_code)
    return locations

def find_closest_monster_location(monster_code, current_pos=None):
    """Find the closest location of a specific monster"""
    if current_pos is None:
        current_pos = (api.char.pos.x, api.char.pos.y)
    
    locations = find_monster_locations(monster_code)
    if not locations:
        return None
    
    closest = min(locations, key=lambda loc: calculate_distance(current_pos, (loc.x, loc.y)))
    return closest

def find_monsters_by_level_range(min_level=None, max_level=None):
    """Find monsters within a level range"""
    if min_level is None:
        min_level = max(1, api.char.level - 1)
    if max_level is None:
        max_level = api.char.level + 1
    
    monsters = api.monsters.get(min_level=min_level, max_level=max_level)
    return monsters

def find_all_nearby_monsters(radius=10):
    """Find all monsters within a certain radius of current position"""
    current_pos = (api.char.pos.x, api.char.pos.y)
    nearby_monsters = []
    
    # Get all monster locations
    monster_tiles = api.maps.get(content_type="monster")
    
    for tile in monster_tiles:
        distance = calculate_distance(current_pos, (tile.x, tile.y))
        if distance <= radius:
            nearby_monsters.append({
                'location': tile,
                'distance': distance,
                'code': tile.content_code
            })
    
    # Sort by distance
    nearby_monsters.sort(key=lambda x: x['distance'])
    return nearby_monsters

def hunt_monster(monster_code=None, level_range=None, auto_heal=True):
    """Complete monster hunting workflow with health management"""
    print(f"🎮 Character: {config.character_name}")
    print(f"📍 Position: ({api.char.pos.x}, {api.char.pos.y})")
    print(f"⚔️ Level: {api.char.level} | HP: {api.char.hp}/{api.char.max_hp} ({get_health_percentage():.1f}%)")
    
    # Pre-hunt health check
    if auto_heal and needs_healing(70):
        print(f"\n💚 PRE-HUNT HEALING")
        if not rest_until_healed(80):
            print("❌ Could not heal enough for hunting")
            return False
    
    if monster_code:
        # Hunt specific monster
        print(f"\n🎯 Hunting specific monster: {monster_code}")
        location = find_closest_monster_location(monster_code)
        if not location:
            print(f"❌ No {monster_code} found on the map")
            return False
    else:
        # Find suitable monsters by level
        if level_range:
            min_level, max_level = level_range
        else:
            min_level = max(1, api.char.level - 1)
            max_level = api.char.level + 1
        
        monsters = find_monsters_by_level_range(min_level, max_level)
        if not monsters:
            print(f"❌ No monsters found in level range {min_level}-{max_level}")
            return False
        
        print(f"\n🐉 Available monsters (Level {min_level}-{max_level}):")
        monster_options = []
        
        for monster in monsters:
            locations = find_monster_locations(monster.code)
            if locations:
                closest_loc = find_closest_monster_location(monster.code)
                distance = calculate_distance((api.char.pos.x, api.char.pos.y), (closest_loc.x, closest_loc.y))
                monster_options.append({
                    'monster': monster,
                    'location': closest_loc,
                    'distance': distance
                })
                print(f"   • {monster.name} (Lvl {monster.level}) - Closest at ({closest_loc.x}, {closest_loc.y}) - Distance: {distance}")
        
        if not monster_options:
            print("❌ No monsters found with available locations")
            return False
        
        # Choose closest monster
        best_option = min(monster_options, key=lambda x: x['distance'])
        location = best_option['location']
        monster_code = best_option['monster'].code
        
        print(f"\n🎯 Selected: {best_option['monster'].name} (Level {best_option['monster'].level})")
    
    # Move to monster
    distance = calculate_distance((api.char.pos.x, api.char.pos.y), (location.x, location.y))
    print(f"\n🚶 Moving to {monster_code} at ({location.x}, {location.y}) - Distance: {distance}")
    
    api.actions.move(location.x, location.y)
    print(f"✅ Arrived at ({api.char.pos.x}, {api.char.pos.y})")
    
    # Fight with health management!
    print(f"\n⚔️ Fighting {monster_code}...")
    fight_success = safe_fight()
    
    if fight_success:
        print("🏆 Hunt successful!")
        print(f"💰 Gold: {api.char.gold}")
        
        # Post-fight health management
        if auto_heal and needs_healing(50):
            print(f"\n💚 POST-FIGHT HEALING")
            rest_until_healed(70)
        
        return True
    else:
        print("❌ Hunt failed")
        # Emergency healing if needed
        if get_health_percentage() < 30:
            print(f"\n🚨 EMERGENCY HEALING")
            rest_until_healed(60)
        return False

def continuous_hunt(hunt_count=5, monster_code=None, rest_between_hunts=True):
    """Hunt multiple monsters with automatic health management"""
    print(f"🔄 CONTINUOUS HUNT - {hunt_count} hunts")
    print("="*50)
    
    successful_hunts = 0
    for i in range(hunt_count):
        print(f"\n🎯 HUNT {i+1}/{hunt_count}")
        print("-" * 30)
        
        # Always check health before each hunt
        if get_health_percentage() < 70:
            print("💚 Pre-hunt healing...")
            rest_until_healed(80)
        
        success = hunt_monster(monster_code=monster_code, auto_heal=True)
        
        if success:
            successful_hunts += 1
            
        # Rest between hunts if requested
        if rest_between_hunts and i < hunt_count - 1:
            print("💤 Resting between hunts...")
            rest_until_healed(80)
    
    print(f"\n🏆 HUNT SUMMARY")
    print(f"   Successful hunts: {successful_hunts}/{hunt_count}")
    print(f"   Final HP: {api.char.hp}/{api.char.max_hp} ({get_health_percentage():.1f}%)")
    print(f"   Final Gold: {api.char.gold}")

if __name__ == "__main__":
    print("🗡️ SAFE MONSTER HUNTER")
    print("="*50)
    print("Now with automatic health management!")
    
    # Example 1: Single hunt with health management
    print("\n1. 🎯 SAFE SINGLE HUNT")
    hunt_monster(auto_heal=True)
    
    print("\n" + "="*50)
    
    # Example 2: Continuous hunting
    print("\n2. 🔄 CONTINUOUS SAFE HUNTING (3 hunts)")
    continuous_hunt(hunt_count=3, rest_between_hunts=True) 