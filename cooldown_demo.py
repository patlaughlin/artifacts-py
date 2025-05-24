from artifactsmmo_wrapper import wrapper, logger
from config import config
import time

# Load configuration from .env file
wrapper.token = config.token
api = wrapper.character(config.character_name)
logger.setLevel("INFO")  # Override to INFO for cleaner output

def perform_action_with_timing(action_name, action_func):
    """Helper function to time actions and show cooldown management"""
    print(f"\n🚀 {action_name}")
    print(f"   Pre-action cooldown: {api.char.cooldown}s")
    print(f"   Time: {time.strftime('%H:%M:%S')}")
    
    start_time = time.time()
    try:
        result = action_func()
        end_time = time.time()
        duration = end_time - start_time
        
        print(f"   ✅ Completed in {duration:.2f}s")
        print(f"   Post-action cooldown: {api.char.cooldown}s")
        return result
    except Exception as e:
        end_time = time.time()
        duration = end_time - start_time
        print(f"   ❌ Failed after {duration:.2f}s: {str(e)[:50]}...")
        return None

print("🎮 COMPREHENSIVE COOLDOWN DEMO")
print("="*60)
print(f"🎮 Character: {config.character_name}")
print("This demo shows how different actions have different cooldowns")
print("and how the wrapper automatically manages them all!")

# Move actions (typically 10-50 second cooldowns depending on distance)
perform_action_with_timing(
    "Moving to (0, 0)", 
    lambda: api.actions.move(0, 0)
)

perform_action_with_timing(
    "Moving to (1, 1)", 
    lambda: api.actions.move(1, 1)
)

# Rest action (usually instant, no cooldown)
perform_action_with_timing(
    "Resting to restore energy", 
    lambda: api.actions.rest()
)

# Try to gather (might fail if no resource at location)
perform_action_with_timing(
    "Attempting to gather resources", 
    lambda: api.actions.gather()
)

# Try to fight (might fail if no monster at location)
perform_action_with_timing(
    "Attempting to fight", 
    lambda: api.actions.fight()
)

print(f"\n" + "="*60)
print("🔥 KEY COOLDOWN INSIGHTS:")
print("="*60)
print("🎯 Different actions have different cooldown lengths:")
print("   • Movement: 10-50+ seconds (based on distance & character speed)")
print("   • Combat: Variable (based on fight duration)")
print("   • Gathering: Variable (based on resource and skill)")
print("   • Rest: Usually instant (0 seconds)")
print("")
print("⚡ The @with_cooldown decorator automatically:")
print("   1. Checks current cooldown before each action")
print("   2. Waits for cooldown to expire if needed")
print("   3. Updates cooldown after each action completes")
print("   4. Logs waiting time for debugging")
print("")
print("🚀 You can chain actions without any manual timing:")
print("   api.actions.move(5, 5)")
print("   api.actions.gather()      # Waits for move cooldown automatically")
print("   api.actions.move(6, 6)    # Waits for gather cooldown automatically")
print("")
print("✨ No time.sleep(), no cooldown checking, no manual state management!")
print("")
print("🔧 CONFIGURATION MANAGEMENT:")
print("="*60)
print("✅ All settings loaded from .env file")
print("✅ Change CHARACTER_NAME in .env to switch characters")
print("✅ Change LOG_LEVEL in .env for different verbosity")
print("✅ Update ARTIFACTS_TOKEN in .env when needed") 