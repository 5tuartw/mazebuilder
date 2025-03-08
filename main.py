from window import Window
import sys
from config import ConfigManager

def main():

    default_config = {
        "api_key": "YOUR_API_KEY",
        "log_level": "INFO",
        "window_size": {"width": 800, "height": 600},
    }

    config_manager = ConfigManager("config.json", default_config)

    sys.setrecursionlimit(10000)
    win = Window(config_manager)
    config_manager.save_config()

    win.wait_for_close()


main()
