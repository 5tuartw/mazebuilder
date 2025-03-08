import json
import os

class ConfigManager:
    """
    A class to manage program configuration, saving and loading from a JSON file.
    """

    def __init__(self, config_file="config.json", default_config=None):
        """
        Initializes the ConfigManager.

        Args:
            config_file (str): The path to the configuration file.
            default_config (dict, optional): A dictionary containing default configuration values.
        """
        self.config_file = config_file
        self.config = {}
        self.default_config = default_config or {}
        self.load_config()

    def load_config(self):
        """
        Loads the configuration from the file, or initializes with defaults if the file doesn't exist.
        """
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, "r") as f:
                    self.config = json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                print(f"Error loading config from {self.config_file}. Using defaults.")
                self.config = self.default_config.copy() #important to copy, to avoid modifying the default object.
        else:
            print(f"Config file {self.config_file} not found. Using defaults.")
            self.config = self.default_config.copy()

    def save_config(self):
        """
        Saves the current configuration to the file.
        """
        try:
            with open(self.config_file, "w") as f:
                json.dump(self.config, f, indent=4)
        except IOError as e:
            print(f"Error saving config to {self.config_file}: {e}")

    def get(self, key, default=None):
        """
        Retrieves a configuration value by key.

        Args:
            key (str): The key of the configuration value.
            default (any, optional): The default value to return if the key is not found.

        Returns:
            any: The configuration value, or the default value if the key is not found.
        """
        return self.config.get(key, default)

    def set(self, key, value):
        """
        Sets a configuration value.

        Args:
            key (str): The key of the configuration value.
            value (any): The value to set.
        """
        self.config[key] = value

    def update(self, new_config):
        """
        Update the configuration with a dictionary.
        """
        self.config.update(new_config)

# Example Usage:
if __name__ == "__main__":
    default_config = {
        "api_key": "YOUR_API_KEY",
        "log_level": "INFO",
        "window_size": {"width": 800, "height": 600},
    }

    config_manager = ConfigManager(default_config=default_config)

    # Access configuration values
    api_key = config_manager.get("api_key")
    log_level = config_manager.get("log_level")
    window_size = config_manager.get("window_size")

    print(f"API Key: {api_key}")
    print(f"Log Level: {log_level}")
    print(f"Window Size: {window_size}")

    # Modify and save configuration
    config_manager.set("log_level", "DEBUG")
    config_manager.set("new_setting", "new value")
    config_manager.update({"api_key":"newKey"})

    config_manager.save_config()

    #reload and show the new config.
    config_manager2 = ConfigManager(default_config=default_config)
    print(config_manager2.get("log_level"))
    print(config_manager2.get("new_setting"))
    print(config_manager2.get("api_key"))