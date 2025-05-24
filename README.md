# ArtifactsMmo Python Bot

A Python bot for interacting with the ArtifactsMmo game API, featuring automatic cooldown management, efficient caching, and secure configuration.

## 🚀 Features

- **Automatic Cooldown Management**: No need to manually handle API cooldowns
- **Smart Caching System**: Local SQLite cache for static game data (maps, items, monsters)
- **Secure Configuration**: Environment variables for API tokens and settings
- **Real-time Character State**: Automatic character state updates after actions
- **Comprehensive API Wrapper**: Full access to all game actions and data

## 📋 Prerequisites

- Python 3.8+
- pip package manager

## 🛠️ Setup

1. **Clone/Download the project**
   ```bash
   cd artifacts-py
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   ```bash
   # Copy the example file
   cp .env.example .env
   
   # Edit .env with your actual values
   nano .env
   ```

4. **Fill in your `.env` file:**
   ```env
   # Your ArtifactsMmo API token from artifactsmmo.com
   ARTIFACTS_TOKEN=your_actual_token_here
   
   # Your character name in the game
   CHARACTER_NAME=YourCharacterName
   
   # Log level (DEBUG, INFO, WARNING, ERROR)
   LOG_LEVEL=DEBUG
   ```

## 🎮 Usage

### Basic Usage
```python
from artifactsmmo_wrapper import wrapper, logger
from config import config

# Configuration is automatically loaded from .env
wrapper.token = config.token
api = wrapper.character(config.character_name)
logger.setLevel(config.log_level)

# All actions automatically handle cooldowns!
api.actions.move(10, 10)    # Moves character
api.actions.gather()        # Waits for move cooldown, then gathers
api.actions.move(5, 5)      # Waits for gather cooldown, then moves

# Character state is automatically updated
print(f"Position: ({api.char.pos.x}, {api.char.pos.y})")
print(f"Gold: {api.char.gold}")
```

### Getting World Map Data
```python
# Get entire world map (357 tiles, cached locally)
all_maps = api.maps.get()

# Get specific tile
tile = api.maps.get(x=10, y=10)

# Filter maps by content
monster_locations = api.maps.get(content_type="monster")
chicken_locations = api.maps.get(content_code="chicken")
```

## 🗄️ Cache System

The bot uses a smart caching system:

- **Static Game Data** → Cached in `db/artifacts.db` (maps, items, monsters)
- **Character Data** → Always fresh from API (position, stats, inventory)
- **Auto-Refresh** → Cache updates when game version changes

## ⏱️ Cooldown Management

The wrapper automatically handles all API cooldowns:

```python
# ❌ Don't do this manually:
# if api.char.cooldown > 0:
#     time.sleep(api.char.cooldown)

# ✅ Just call actions - cooldowns are automatic:
api.actions.move(1, 1)
api.actions.fight()  # Automatically waits for move cooldown
```

## 📁 Project Structure

```
artifacts-py/
├── .env                 # Your configuration (DO NOT COMMIT)
├── .env.example         # Template for configuration
├── config.py            # Configuration loader
├── main.py              # Basic demo
├── cooldown_demo.py     # Comprehensive cooldown demo
├── requirements.txt     # Python dependencies
├── db/                  # SQLite cache directory
│   └── artifacts.db     # Cached game data
└── logs/               # Log files
```

## 🔧 Configuration Options

| Variable | Description | Example |
|----------|-------------|---------|
| `ARTIFACTS_TOKEN` | Your API token from artifactsmmo.com | `eyJ0eXAi...` |
| `CHARACTER_NAME` | Your character name in-game | `MyCharacter` |
| `LOG_LEVEL` | Logging verbosity | `DEBUG`, `INFO`, `WARNING`, `ERROR` |

## 🛡️ Security

- **Never commit `.env` files** - they contain sensitive tokens
- The `.gitignore` automatically excludes `.env` files
- Use `.env.example` as a template for new setups
- Tokens are masked in log output for security

## 🎯 Examples

### Switch Characters
```bash
# Edit .env file
CHARACTER_NAME=AnotherCharacter
```

### Change Log Level
```bash
# Edit .env file  
LOG_LEVEL=INFO  # Less verbose output
```

### Bot Script Template
```python
from artifactsmmo_wrapper import wrapper, logger
from config import config

def main():
    # Setup
    wrapper.token = config.token
    api = wrapper.character(config.character_name)
    logger.setLevel(config.log_level)
    
    # Your bot logic here
    while True:
        # Move somewhere
        api.actions.move(5, 5)
        
        # Do something
        api.actions.gather()
        
        # Check character state
        if api.char.gold > 1000:
            break

if __name__ == "__main__":
    main()
```

## 🆘 Troubleshooting

**Config Error**: `ARTIFACTS_TOKEN not found`
- Check your `.env` file exists and has the correct variable names
- Make sure there are no spaces around the `=` in `.env`

**Character Not Found**: 
- Verify `CHARACTER_NAME` matches exactly (case-sensitive)
- Ensure character exists in your ArtifactsMmo account

**Cache Issues**:
- Delete `db/artifacts.db` to force cache refresh
- Check internet connection for API access

## 📚 API Reference

- [ArtifactsMmo Official API](https://artifactsmmo.com/api)
- [Wrapper Documentation](https://github.com/your-wrapper-repo)

---

**Happy Botting! 🤖⚔️** 