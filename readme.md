# Alarm Clock

A Python-based alarm clock application with a simple graphical user interface (GUI). This project allows users to set alarms, configure settings, and manage alarm sounds. It is designed to run on systems with a Raspberry Pi for GPIO-based buzzer functionality.

## Features

- Set and manage alarms
- Customizable alarm sounds
- Snooze functionality
- Configuration file for persistent settings
- Simple and intuitive GUI
- GPIO buzzer integration for Raspberry Pi
- Fullscreen mode for better visualization
- Customizable clock colors and appearance

## Getting Started

### Prerequisites

- Python 3.6 or higher
- Required libraries: `tkinter`, `configparser`, `pydub`, `simpleaudio`, `RPi.GPIO`

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/B-Boone/alarm_clock.git
   cd alarm_clock
   ```

2. Install the required libraries:
   ```bash
   pip install tkinter configparser pydub simpleaudio RPi.GPIO
   ```

### Usage

1. Run the `clock_ui.py` script to start the alarm clock application:
   ```bash
   python clock_ui.py
   ```

2. Use the GUI to set alarms and configure settings as needed.

## Project Structure

- `alarm_clock/`: Directory containing main application scripts
- `__pycache__/`: Directory for compiled Python files
- `alarm.wav` `TF006.wav` `TF048.wav`: Alarm sound files
- `clock_ui.py`: Main GUI application script
- `config_manager.py`: Script for managing configuration settings
- `gpio_handler`: Script for managing the GPIO Buzzer configuration
- `popup_menu.py`: Script for managing the customization menu
- `clock_config.ini`: Configuration file for storing settings
- `clockipy.png`: Image file for the application icon
Configuration
The clock_config.ini file stores the alarm clock settings, including alarm times and sound preferences. You can edit this file manually or through the GUI customization menu.

Example clock_config.ini:
```python
[COLORS]
second_color = #00ff00
minute_color = #0000ff
hour_color = #ff0000
border_color = #00ff00
bg_color = black
markings_color = #0000ff
numbers_color = #ff0000
alarm_display_fg_color = #d9d900
hour_button_fg_color = #ff0000
minute_button_fg_color = #0000ff
hour_button_brdr_color = #ff0000
minute_button_brdr_color = #0000ff
dtdow_color = #b09300
dtdat_color = #a85c84
dttim_color = #397c8c

[SETTINGS]
gpio_pin = 20
snooze_time = 5
alarm_hour = 12
alarm_minute = 30
alarm_method = both
alarm_sound_file = ~/alarm_clock/alarm_clock/TF006.wav
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
Contributing
Contributions are welcome! Please follow these steps:

Fork the repository
Create a new branch (git checkout -b feature-branch)
Commit your changes (git commit -am 'Add new feature')
Push to the branch (git push origin feature-branch)
Open a pull request
Please open an issue for any improvements or bug fixes.

## Contact

For any inquiries or feedback, please contact B-Boone at [brandon.boone1304@gmail.com].

---

© 2024 B-Boone. All rights reserved.
