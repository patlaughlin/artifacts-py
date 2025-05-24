"""
Simple Monster Location Example
Shows the key concepts for finding and moving to monsters
"""
from artifactsmmo_wrapper import wrapper, logger
from config import config

# Setup
wrapper.token = config.token
api = wrapper.character(config.character_name)
logger.setLevel("INFO")

print("🔍 MONSTER LOCATION LOOKUP GUIDE")
print("="*40)

# CONCEPT 1: Monster data vs Monster locations are separate
print("\n1️⃣ UNDERSTANDING THE DATA STRUCTURE:")
print("   • api.monsters.get() = Monster stats (name, level, HP, etc.)")
print("   • api.maps.get()     = Map tiles with locations (x, y, content)")

# CONCEPT 2: Get monster by level
monsters_at_my_level = api.monsters.get(min_level=api.char.level, max_level=api.char.level)
print(f"\n2️⃣ MONSTERS AT MY LEVEL ({api.char.level}):")
for monster in monsters_at_my_level[:3]:
    print(f"   • {monster.name} (Level {monster.level}) - Code: '{monster.code}'")

# CONCEPT 3: Find where monsters appear on the map
if monsters_at_my_level:
    target_monster = monsters_at_my_level[0]
    print(f"\n3️⃣ FINDING LOCATIONS FOR '{target_monster.code}':")
    
    # This is the key - use the monster's CODE to find map locations
    monster_locations = api.maps.get(content_code=target_monster.code)
    print(f"   Found {len(monster_locations)} locations:")
    
    for i, location in enumerate(monster_locations):
        # Calculate simple distance (Manhattan distance)
        distance = abs(location.x - api.char.pos.x) + abs(location.y - api.char.pos.y)
        print(f"   {i+1}. ({location.x}, {location.y}) - Distance: {distance}")

# CONCEPT 4: Find closest location
print(f"\n4️⃣ FINDING CLOSEST LOCATION:")
if monsters_at_my_level and monster_locations:
    def get_distance(location):
        return abs(location.x - api.char.pos.x) + abs(location.y - api.char.pos.y)
    
    closest = min(monster_locations, key=get_distance)
    distance = get_distance(closest)
    
    print(f"   Closest {target_monster.name}: ({closest.x}, {closest.y}) - Distance: {distance}")
    
    # CONCEPT 5: Move and fight
    print(f"\n5️⃣ HUNT THE MONSTER:")
    print(f"   Moving to ({closest.x}, {closest.y})...")
    api.actions.move(closest.x, closest.y)
    print(f"   ✅ Arrived! Now fighting...")
    try:
        api.actions.fight()
        print(f"   🏆 Victory!")
    except Exception as e:
        print(f"   ❌ Fight error: {e}")

print(f"\n🎯 KEY TAKEAWAY:")
print("   1. Get monster stats: api.monsters.get()")
print("   2. Get monster locations: api.maps.get(content_code=monster.code)")
print("   3. Calculate distances and pick closest")
print("   4. Move and fight!")

print(f"\n🔧 QUICK FUNCTIONS YOU CAN USE:")
print("   # Find all chicken locations")
print("   chicken_spots = api.maps.get(content_code='chicken')")
print("   ")
print("   # Find all monster tiles nearby")
print("   nearby_monsters = api.maps.get(content_type='monster')")
print("   ")
print("   # Filter by distance")
print("   close_ones = [loc for loc in nearby_monsters if abs(loc.x - my_x) + abs(loc.y - my_y) <= 10]") 