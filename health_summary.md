# 💚 Health Management System

## 🎯 **Overview**
The ArtifactsMmo bot now includes automatic health management to ensure your character never dies from low health. The system automatically monitors health and heals when needed.

## 🚨 **Health Thresholds**

| Threshold | Default | Description |
|-----------|---------|-------------|
| **Critical** | 30% | Emergency healing required |
| **Low** | 50% | Should heal soon |
| **Fight Minimum** | 60% | Minimum health to start fighting |

Configure these in your `.env` file:
```env
HEALTH_CRITICAL=30
HEALTH_LOW=50  
HEALTH_FIGHT_MIN=60
```

## 🛡️ **Automatic Safety Features**

### ✅ **Pre-Action Health Checks**
- **Before Fighting**: Requires 60%+ health
- **Before Gathering**: Requires 30%+ health  
- **Before Moving**: Requires 20%+ health

### ✅ **Post-Action Health Management**
- **After Fighting**: Heals if below 50%
- **After Any Action**: Emergency heal if below 30%

### ✅ **Smart Healing Logic**
- **Automatic Rest Cycles**: Rests until target health reached
- **Health Percentage Tracking**: Monitors health as percentage
- **Configurable Targets**: Set different healing goals per action

## 🔧 **Usage Examples**

### Basic Health Functions
```python
from config import config

# Check if health is low
if needs_healing(config.health_low):
    rest_until_healed(80)

# Get health percentage
health_pct = get_health_percentage()
print(f"Health: {health_pct:.1f}%")
```

### Safe Actions
```python
# These automatically check/heal before performing action
safe_fight()      # Heals to 70% if below 60%
safe_gather()     # Heals to 40% if below 30% 
safe_move(x, y)   # Heals to 30% if below 20%
```

### Monster Hunting with Health Management
```python
# Automatically handles all health checks
hunt_monster(auto_heal=True)

# Continuous hunting with healing between hunts
continuous_hunt(hunt_count=5, rest_between_hunts=True)
```

## 📊 **Health Status Indicators**

| Health % | Status | Indicator |
|----------|--------|-----------|
| 80-100% | Excellent | 🟢 |
| 60-79% | Good | 🟡 |
| 40-59% | Fair | 🟠 |
| 20-39% | Low | 🔴 |
| 0-19% | Critical | ☠️ |

## 🎮 **Integration Examples**

### 1. **Updated main.py**
- Pre-hunt health check
- Pre-fight health check  
- Post-fight healing
- Emergency healing on critical health

### 2. **Safe Monster Hunter**
- Automatic healing before each hunt
- Health checks before fighting
- Rest between hunts
- Emergency healing on failures

### 3. **Health Manager Utility**
- Comprehensive health monitoring
- Safe action wrappers
- Detailed health reporting

## ⚙️ **Configuration**

Add to your `.env` file:
```env
# Health management thresholds (percentages)
HEALTH_CRITICAL=30      # Emergency healing threshold
HEALTH_LOW=50          # General low health threshold  
HEALTH_FIGHT_MIN=60    # Minimum health to fight
```

## 🔄 **How It Works**

1. **Health Monitoring**: Continuously tracks `api.char.hp / api.char.max_hp`
2. **Threshold Checking**: Compares current health % to configured thresholds
3. **Automatic Resting**: Calls `api.actions.rest()` until target health reached
4. **Action Gating**: Prevents dangerous actions when health is too low
5. **Emergency Healing**: Forces healing when health becomes critical

## ⚠️ **Safety Features**

- **Maximum Rest Cycles**: Prevents infinite rest loops
- **Health Validation**: Handles edge cases (0 max HP, etc.)
- **Action Failure Handling**: Emergency healing after failed fights
- **Configurable Thresholds**: Adjust safety levels per your character

## 🚀 **Quick Start**

1. **Basic Health Check**: 
   ```python
   if needs_healing(50):
       rest_until_healed(80)
   ```

2. **Safe Fighting**:
   ```python
   safe_fight()  # Automatically heals if needed
   ```

3. **Continuous Hunting**:
   ```python
   continuous_hunt(hunt_count=5)  # Handles all health management
   ```

## 💡 **Best Practices**

- ✅ Use `safe_fight()` instead of `api.actions.fight()`
- ✅ Check health before dangerous activities
- ✅ Configure thresholds based on your character's level
- ✅ Use `auto_heal=True` in hunting functions
- ✅ Monitor health status during long bot runs

---

**🎉 Your character will never die from low health again!** 💚 