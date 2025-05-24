from artifactsmmo_wrapper import wrapper, logger
from config import config
import time

# Load configuration from .env file
wrapper.token = config.token
api = wrapper.character(config.character_name)
logger.setLevel(config.log_level)

print("🔄 AUTOMATIC COOLDOWN MANAGEMENT DEMO")
print("="*50)
print(f"🎮 Character: {config.character_name}")
print(f"📊 Log Level: {config.log_level}")

# Check initial cooldown status
print(f"Initial cooldown: {api.char.cooldown} seconds")
print(f"Cooldown expires: {api.char.cooldown_expiration}")

# Perform action 1 - this will put us on cooldown
print(f"\n⏰ Current time: {time.strftime('%H:%M:%S')}")
print("🚀 Action 1: Moving to (6, 6)...")
start_time = time.time()
api.actions.move(6, 6)
end_time = time.time()
print(f"✅ Move completed in {end_time - start_time:.2f} seconds")
print(f"New cooldown: {api.char.cooldown} seconds")

# Perform action 2 immediately - wrapper will automatically wait for cooldown!
print(f"\n⏰ Current time: {time.strftime('%H:%M:%S')}")
print("🚀 Action 2: Moving to (7, 7) - will auto-wait for cooldown...")
start_time = time.time()
api.actions.move(7, 7)
end_time = time.time()
print(f"✅ Move completed in {end_time - start_time:.2f} seconds (including cooldown wait!)")

# Perform action 3 immediately again
print(f"\n⏰ Current time: {time.strftime('%H:%M:%S')}")
print("🚀 Action 3: Moving to (8, 8) - will auto-wait again...")
start_time = time.time()
api.actions.move(8, 8)
end_time = time.time()
print(f"✅ Move completed in {end_time - start_time:.2f} seconds (including cooldown wait!)")

print("\n" + "="*50)
print("🎉 COOLDOWN MANAGEMENT SUMMARY:")
print("="*50)
print("✅ No manual cooldown checking needed")
print("✅ No manual time.sleep() required")
print("✅ Wrapper automatically waits for cooldowns")
print("✅ Actions are queued and executed when ready")
print("✅ You can call actions back-to-back safely")
print("⚡ The @with_cooldown decorator handles everything!")
print("\n🔧 CONFIGURATION MANAGEMENT:")
print("="*50)
print("✅ Token and character loaded from .env file")
print("✅ No hardcoded credentials in source code")
print("✅ Easy to change characters or tokens")
print("✅ Secure credential management")