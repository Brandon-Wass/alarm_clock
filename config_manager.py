import os
import configparser

CONFIG_FILE = "clock_config.ini"

class ConfigManager:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.load_config()

    def load_config(self):
        if os.path.exists(CONFIG_FILE):
            self.config.read(CONFIG_FILE)
        else:
            self.config['COLORS'] = {
                'second_color': 'purple',
                'minute_color': 'purple',
                'hour_color': 'purple',
                'border_color': 'purple',
                'bg_color': 'black',
                'markings_color': 'purple',
                'numbers_color': 'purple',
                'alarm_display_fg_color': 'purple',
                'hour_button_fg_color': 'purple',
                'minute_button_fg_color': 'purple',
                'hour_button_brdr_color': 'purple',
                'minute_button_brdr_color': 'purple',
                'dtdow_color': 'purple',
                'dtdat_color': 'purple',
                'dttim_color': 'purple'
            }
            self.config['SETTINGS'] = {
                'gpio_pin': '20',
                'snooze_time': '5',
                'alarm_hour': '',
                'alarm_minute': '',
                'alarm_sound_file': 'alarm.wav',
                'alarm_method': 'both'
            }
            self.save_config()

    def save_config(self):
        with open(CONFIG_FILE, 'w') as configfile:
            self.config.write(configfile)

    def get(self, section, key, fallback=None):
        return self.config.get(section, key, fallback=fallback)

    def set(self, section, key, value):
        self.config.set(section, key, value)
        self.save_config()
