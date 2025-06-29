# config.py
import os
import json
import logging
from typing import Dict, Any, Optional

# Set up logging
logger = logging.getLogger("Config")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

DEFAULT_SETTINGS = {
    "proxy_file": "resources/proxies.txt",
    "concurrent_instances": 5,
    "max_views": 100,
    "view_duration": 60,
    "use_proxy": True,
    "show_log": True,
    "compliance_threshold": 0.7,
    "watch_threshold": 0.7,
    "max_retries": 3,
    "view_delay_min": 45,
    "view_delay_max": 180,
    "error_check_interval": 5,  # Seconds between error checks
    "max_recovery_attempts": 3,
    "adversarial_noise_level": 0.5,
    "fingerprints": [
        {
            "name": "Windows Desktop",
            "platform": "Win32",
            "languages": ["en-US", "en"],
            "hardwareConcurrency": 4,
            "deviceMemory": 8,
            "colorDepth": 24,
            "resolution": [1920, 1080],
            "timezone": "America/New_York"
        },
        {
            "name": "Macbook Pro",
            "platform": "MacIntel",
            "languages": ["en-GB", "en"],
            "hardwareConcurrency": 8,
            "deviceMemory": 16,
            "colorDepth": 30,
            "resolution": [2560, 1600],
            "timezone": "Europe/London"
        }
    ],
    "evasion_threshold": 0.7,
    "solver_engine": "UACv2",
    "fingerprint_mode": "adversarial",
    "quantum_safe": True,
    "evasion_metrics": {
    "captcha_bypass_rate": 0.92,
    "behavior_entropy": 0.85,
    "fingerprint_decay": 0.1,
    "quantum_entanglement": True
    
    }
    
    
}

class ConfigManager:
    def __init__(self, config_file: str = "config.json"):
        self.config_file = config_file
        self.settings = self.load_config()
        
    def load_config(self) -> Dict[str, Any]:
        """Load configuration from file or return defaults"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                    logger.info(f"Loaded config from {self.config_file}")
                    return {**DEFAULT_SETTINGS, **config}  # Merge with defaults
        except Exception as e:
            logger.error(f"Error loading config: {str(e)}")
        
        logger.info("Using default configuration")
        return DEFAULT_SETTINGS.copy()
    
    def save_config(self, settings: Optional[Dict[str, Any]] = None):
        """Save current settings to config file"""
        try:
            if settings:
                self.settings = settings
                
            with open(self.config_file, 'w') as f:
                json.dump(self.settings, f, indent=4)
                logger.info(f"Saved config to {self.config_file}")
            return True
        except Exception as e:
            logger.error(f"Error saving config: {str(e)}")
            return False
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value"""
        return self.settings.get(key, default)
    
    def set(self, key: str, value: Any, save: bool = False):
        """Set a configuration value"""
        self.settings[key] = value
        if save:
            self.save_config()
    
    def update(self, new_settings: Dict[str, Any], save: bool = True):
        """Update multiple settings at once"""
        self.settings.update(new_settings)
        if save:
            self.save_config()

# Create global config instance
config = ConfigManager()

if __name__ == "__main__":
    # Test the config manager
    print("Current settings:")
    print(json.dumps(config.settings, indent=4))
    
    # Update and save a setting
    config.set("max_views", 150, save=True)
    
    print("\nUpdated settings:")
    print(json.dumps(config.settings, indent=4))
