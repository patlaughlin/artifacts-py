"""
Continuous Smart Hunter - Infinite hunting loop with safety features
Keeps hunting winnable monsters until manually stopped or no targets found
"""
from artifactsmmo_wrapper import wrapper, logger
from config import config
from combat_calculator import CombatCalculator
import time
import signal
import sys

# Load configuration
wrapper.token = config.token
api = wrapper.character(config.character_name)
logger.setLevel(config.log_level)

# Create combat calculator
combat_calc = CombatCalculator(api)

# Global flag for graceful shutdown
running = True

def signal_handler(sig, frame):
    """Handle Ctrl+C gracefully"""
    global running
    print(f"\n\n🛑 GRACEFUL SHUTDOWN REQUESTED")
    print("🔄 Finishing current hunt, then stopping...")
    running = False

# Register signal handler for Ctrl+C
signal.signal(signal.SIGINT, signal_handler)

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
    while api.char.hp < api.char.max_hp and cycles < max_rest_cycles and running:
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

def continuous_hunt(max_distance=20, rest_between_hunts=True, no_target_limit=5):
    """Continuously hunt monsters until stopped"""
    global running
    
    print(f"🔄 CONTINUOUS SMART HUNTER")
    print("="*60)
    print(f"🎮 Character: {config.character_name} (Level {api.char.level})")
    print(f"💚 Health: {api.char.hp}/{api.char.max_hp} ({get_health_percentage():.1f}%)")
    print(f"📍 Position: ({api.char.pos.x}, {api.char.pos.y})")
    print(f"🎯 Max Distance: {max_distance} tiles")
    print(f"⚠️  Press Ctrl+C to stop gracefully")
    
    # Track statistics
    total_hunts = 0
    successful_hunts = 0
    failed_hunts = 0
    no_target_count = 0
    starting_gold = api.char.gold
    starting_level = api.char.level
    
    # Initial health check
    if needs_healing(80):
        print(f"\n💚 INITIAL HEALING")
        if not rest_until_healed(85):
            print("❌ Could not heal enough for hunting")
            return False
    
    print(f"\n🚀 STARTING CONTINUOUS HUNT...")
    print(f"   🛑 Will stop after {no_target_limit} consecutive 'no targets found'")
    
    while running:
        total_hunts += 1
        print(f"\n🎯 HUNT #{total_hunts}")
        print("-" * 40)
        
        # Check if we should stop
        if not running:
            print("🛑 Stopping due to shutdown request...")
            break
        
        # Find winnable monsters
        print("🔍 Analyzing available monsters...")
        winnable_monsters = combat_calc.find_winnable_monsters(max_distance=max_distance)
        
        if not winnable_monsters:
            no_target_count += 1
            print(f"❌ No winnable monsters found! ({no_target_count}/{no_target_limit})")
            
            if no_target_count >= no_target_limit:
                print(f"\n🛑 STOPPING: No winnable targets found {no_target_limit} times in a row")
                print("💡 Suggestions:")
                print("   • Increase max_distance parameter")
                print("   • Improve equipment/level up")
                print("   • Try gathering resources first")
                break
            
            # Wait a bit before trying again
            print("⏳ Waiting 10 seconds before trying again...")
            for i in range(10):
                if not running:
                    break
                time.sleep(1)
            continue
        
        # Reset no target counter since we found something
        no_target_count = 0
        
        # Select best target
        best_target = winnable_monsters[0]
        monster = best_target['monster']
        analysis = best_target['analysis']
        location = best_target['location']
        distance = best_target['distance']
        
        color = {"HIGH": "🟢", "MEDIUM": "🟡", "LOW": "🔴"}[analysis['win_probability']]
        print(f"🎯 Target: {monster.name} (Level {monster.level}) {color}")
        print(f"   Win Probability: {analysis['win_probability']}")
        print(f"   Location: ({location.x}, {location.y}) - Distance: {distance}")
        print(f"   Expected Turns: {analysis['char_turns_to_kill']} to win")
        
        # Pre-fight health check
        health_threshold = 70 if analysis['win_probability'] == 'HIGH' else 80
        if needs_healing(health_threshold):
            print(f"💚 Pre-fight healing to {health_threshold}%...")
            if not rest_until_healed(health_threshold + 5):
                print("❌ Could not heal enough for this fight")
                failed_hunts += 1
                continue
        
        # Move to target
        print(f"🚶 Moving to {monster.name}...")
        try:
            api.actions.move(location.x, location.y)
            print(f"✅ Arrived at ({api.char.pos.x}, {api.char.pos.y})")
        except Exception as e:
            if "already at destination" in str(e).lower():
                print(f"✅ Already at destination ({api.char.pos.x}, {api.char.pos.y})")
            else:
                print(f"❌ Move failed: {e}")
                failed_hunts += 1
                continue
        
        # Fight with confidence!
        print(f"⚔️ Fighting {monster.name} (PREDICTED WIN!)...")
        try:
            fight_result = api.actions.fight()
            print("🏆 Victory! As predicted by combat analysis!")
            print(f"💰 Gold: {api.char.gold} (+{api.char.gold - starting_gold} total)")
            
            # Check for level up
            if api.char.level > starting_level:
                print(f"🎉 LEVEL UP! Now Level {api.char.level}")
                starting_level = api.char.level
            
            print(f"💚 Post-fight HP: {api.char.hp}/{api.char.max_hp} ({get_health_percentage():.1f}%)")
            
            successful_hunts += 1
            
            # Post-fight healing if needed
            if needs_healing(60):
                print(f"💚 Post-fight healing...")
                rest_until_healed(75)
                
        except Exception as e:
            print(f"❌ Fight failed unexpectedly: {e}")
            print("🤔 This shouldn't happen with our combat analysis!")
            failed_hunts += 1
            
            # Emergency healing
            if get_health_percentage() < 40:
                print(f"🚨 Emergency healing...")
                rest_until_healed(70)
        
        # Rest between fights if requested
        if rest_between_hunts and running:
            print("💤 Quick rest between hunts...")
            rest_until_healed(80)
        
        # Show running statistics every 5 hunts
        if total_hunts % 5 == 0:
            success_rate = (successful_hunts / total_hunts) * 100 if total_hunts > 0 else 0
            print(f"\n📊 RUNNING STATS (Hunt #{total_hunts}):")
            print(f"   ✅ Successful: {successful_hunts}")
            print(f"   ❌ Failed: {failed_hunts}")
            print(f"   📈 Success Rate: {success_rate:.1f}%")
            print(f"   💰 Gold Gained: {api.char.gold - starting_gold}")
            print(f"   ⚔️ Current Level: {api.char.level}")
    
    # Final summary
    print(f"\n🏁 CONTINUOUS HUNT COMPLETE!")
    print("="*60)
    print(f"📊 FINAL STATISTICS:")
    print(f"   Total Hunts: {total_hunts}")
    print(f"   Successful: {successful_hunts}")
    print(f"   Failed: {failed_hunts}")
    
    success_rate = (successful_hunts / total_hunts) * 100 if total_hunts > 0 else 0
    print(f"   Success Rate: {success_rate:.1f}%")
    print(f"   Gold Gained: {api.char.gold - starting_gold}")
    print(f"   Final Level: {api.char.level}")
    print(f"   Final HP: {api.char.hp}/{api.char.max_hp} ({get_health_percentage():.1f}%)")
    
    if success_rate >= 90:
        print("🎉 EXCELLENT hunting session!")
    elif success_rate >= 70:
        print("✅ GOOD hunting session!")
    elif success_rate >= 50:
        print("🟡 DECENT hunting session!")
    else:
        print("🔴 POOR hunting session - check equipment/targeting")

if __name__ == "__main__":
    print("🔄 CONTINUOUS SMART HUNTER")
    print("Infinite hunting with combat analysis + health management!")
    print("="*65)
    print("⚠️  CONTROLS:")
    print("   • Press Ctrl+C to stop gracefully")
    print("   • The bot will finish current hunt then stop")
    print("   • Statistics shown every 5 hunts")
    
    try:
        # Start continuous hunting
        continuous_hunt(max_distance=25, rest_between_hunts=True, no_target_limit=5)
    except KeyboardInterrupt:
        print(f"\n🛑 MANUAL STOP REQUESTED")
    except Exception as e:
        print(f"\n❌ UNEXPECTED ERROR: {e}")
        print("🔄 Try restarting the script")
    
    print(f"\n👋 Continuous hunting stopped. Character is safe!") 