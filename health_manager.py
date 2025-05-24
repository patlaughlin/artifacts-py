"""
Health Management Utility
Automatic health monitoring and healing for safe botting
"""
from artifactsmmo_wrapper import wrapper, logger
from config import config
import time

# Load configuration
wrapper.token = config.token
api = wrapper.character(config.character_name)
logger.setLevel(config.log_level)

def get_health_percentage():
    """Get current health as a percentage"""
    if api.char.max_hp == 0:
        return 100  # Avoid division by zero
    return (api.char.hp / api.char.max_hp) * 100

def is_health_low(threshold=50):
    """Check if health is below threshold percentage"""
    health_pct = get_health_percentage()
    return health_pct < threshold

def needs_healing(threshold=50):
    """Check if character needs healing"""
    return api.char.hp < api.char.max_hp and is_health_low(threshold)

def rest_until_healed(target_health_pct=80, max_rest_cycles=10):
    """Rest until health reaches target percentage or max cycles reached"""
    print(f"💤 HEALTH MANAGEMENT")
    print(f"   Current HP: {api.char.hp}/{api.char.max_hp} ({get_health_percentage():.1f}%)")
    
    if not needs_healing(target_health_pct):
        print(f"   ✅ Health is good, no rest needed")
        return True
    
    print(f"   ⚠️ Health low! Resting until {target_health_pct}% HP...")
    
    cycles = 0
    while api.char.hp < api.char.max_hp and cycles < max_rest_cycles:
        cycles += 1
        initial_hp = api.char.hp
        
        print(f"   🛌 Rest cycle {cycles}: {api.char.hp}/{api.char.max_hp} HP")
        
        try:
            api.actions.rest()
            healed = api.char.hp - initial_hp
            health_pct = get_health_percentage()
            
            if healed > 0:
                print(f"   ✅ Healed {healed} HP! Now at {api.char.hp}/{api.char.max_hp} ({health_pct:.1f}%)")
            else:
                print(f"   ⚠️ No healing occurred. Current: {health_pct:.1f}%")
            
            # Check if we've reached target
            if health_pct >= target_health_pct:
                print(f"   🎉 Target health reached! ({health_pct:.1f}%)")
                break
                
        except Exception as e:
            print(f"   ❌ Rest failed: {e}")
            break
    
    final_health_pct = get_health_percentage()
    if final_health_pct >= target_health_pct:
        print(f"   ✅ Healing complete: {api.char.hp}/{api.char.max_hp} ({final_health_pct:.1f}%)")
        return True
    else:
        print(f"   ⚠️ Healing incomplete: {api.char.hp}/{api.char.max_hp} ({final_health_pct:.1f}%)")
        return False

def safe_action(action_func, action_name="action", health_threshold=50, *args, **kwargs):
    """Safely perform an action with automatic health checking"""
    print(f"\n🛡️ SAFE {action_name.upper()}")
    
    # Check health before action
    if needs_healing(health_threshold):
        print(f"   ⚠️ Health too low for {action_name}! Healing first...")
        if not rest_until_healed(target_health_pct=health_threshold + 10):
            print(f"   ❌ Could not heal enough for {action_name}")
            return False
    
    # Perform the action
    print(f"   🚀 Performing {action_name}...")
    try:
        result = action_func(*args, **kwargs)
        print(f"   ✅ {action_name.capitalize()} completed!")
        
        # Check health after action
        health_pct = get_health_percentage()
        print(f"   💚 Post-action HP: {api.char.hp}/{api.char.max_hp} ({health_pct:.1f}%)")
        
        return result
    except Exception as e:
        print(f"   ❌ {action_name.capitalize()} failed: {e}")
        return False

def safe_fight():
    """Safely fight with automatic health management"""
    return safe_action(api.actions.fight, "fight", health_threshold=60)

def safe_gather():
    """Safely gather with automatic health management"""
    return safe_action(api.actions.gather, "gather", health_threshold=30)

def safe_move(x, y):
    """Safely move with automatic health management"""
    return safe_action(api.actions.move, "move", health_threshold=20, x=x, y=y)

def health_status_report():
    """Print detailed health status"""
    health_pct = get_health_percentage()
    print(f"\n💚 HEALTH REPORT")
    print(f"   HP: {api.char.hp}/{api.char.max_hp} ({health_pct:.1f}%)")
    
    if health_pct >= 80:
        print(f"   Status: 🟢 Excellent")
    elif health_pct >= 60:
        print(f"   Status: 🟡 Good")
    elif health_pct >= 40:
        print(f"   Status: 🟠 Fair")
    elif health_pct >= 20:
        print(f"   Status: 🔴 Low - Should heal!")
    else:
        print(f"   Status: ☠️ Critical - HEAL NOW!")
    
    return health_pct

if __name__ == "__main__":
    print("💚 HEALTH MANAGEMENT DEMO")
    print("="*40)
    
    # Show current health status
    health_status_report()
    
    # Demo health checking
    print(f"\n🔍 HEALTH CHECKS:")
    print(f"   Is health low (50%)? {is_health_low(50)}")
    print(f"   Needs healing (50%)? {needs_healing(50)}")
    
    # Demo safe actions
    print(f"\n🛡️ SAFE ACTIONS DEMO:")
    
    # Test safe movement
    print(f"\n1. Safe Movement Test:")
    safe_move(api.char.pos.x + 1, api.char.pos.y)
    
    # Test safe gathering 
    print(f"\n2. Safe Gathering Test:")
    safe_gather()
    
    # Test safe fighting
    print(f"\n3. Safe Fighting Test:")
    safe_fight()
    
    # Final health report
    print(f"\n" + "="*40)
    health_status_report() 