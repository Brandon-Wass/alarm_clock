import tkinter as tk
import tkinter.colorchooser as colorchooser
import tkinter.simpledialog as simpledialog

class PopupMenu(tk.Menu):
    def __init__(self, parent):
        super().__init__(parent, tearoff=0)
        self.parent = parent

        # Adding a submenu for color options
        self.add_color_menu("Analog Clock Colors", [("Seconds Hand", self.seconds_hand_colors),
                                                   ("Minutes Hand", self.minutes_hand_colors),
                                                   ("Hours Hand", self.hours_hand_colors),
                                                   ("Clock Border", self.change_border_color),
                                                   ("Background", self.change_bg_color),
                                                   ("Markings", self.change_markings_color),
                                                   ("Clock Numbers", self.change_numbers_color)])
        self.add_separator()
        self.add_color_menu("Digital Clock Colors", [("Day of Week", self.change_dtdow_color),
                                                    ("Date", self.change_dtdat_color),
                                                    ("Time", self.change_dttim_color)])
        self.add_separator()
        self.add_color_menu("Hour Button Colors", [("Text", self.change_hour_button_fg_color),
                                                  ("Border", self.change_hour_button_brdr_color)])
        self.add_color_menu("Minute Button Colors", [("Text", self.change_minute_button_fg_color),
                                                    ("Border", self.change_minute_button_brdr_color)])
        self.add_separator()
        self.add_color_menu("Alarm Display Colors", [("Text", self.change_alarm_display_fg_color)])
        self.add_separator()
        self.add_command(label="Change Snooze Time", command=self.change_snooze_time)
        self.add_separator()
        self.add_color_menu("Alarm Sound", [("GPIO Buzzer Pin", self.change_gpio_pin),
                                            ("Change alarm Sound", self.parent.change_alarm_sound),
                                            ("Use GPIO Buzzer", lambda: self.parent.change_alarm_method("gpio")),
                                            ("Use Audio File", lambda: self.parent.change_alarm_method("audio")),
                                            ("Use Both", lambda: self.parent.change_alarm_method("both"))])
        self.add_separator()
        self.add_command(label="Minimize Program", command=self.minimize_program)  # New minimize button
        self.add_command(label="Close Menu", command=self.close_menu)
        self.add_command(label="Exit Program", command=self.exit_program)

    def add_color_menu(self, label, commands):
        menu = tk.Menu(self, tearoff=0)
        self.add_cascade(label=label, menu=menu)
        for cmd_label, cmd in commands:
            menu.add_command(label=cmd_label, command=cmd)

    def select_color(self, attribute):
        color = colorchooser.askcolor()[1]
        if color:
            setattr(self.parent, attribute, color)
            self.parent.config_manager.set('COLORS', attribute, color)
            self.parent.update_canvas_colors()
            self.parent.focus_set()

    def seconds_hand_colors(self):
        self.select_color("second_color")

    def minutes_hand_colors(self):
        self.select_color("minute_color")

    def hours_hand_colors(self):
        self.select_color("hour_color")

    def change_border_color(self):
        self.select_color("border_color")

    def change_bg_color(self):
        color = colorchooser.askcolor()[1]
        if color:
            self.parent.bg_color = color
            self.parent.config_manager.set('COLORS', 'bg_color', color)
            self.parent.update_canvas_colors()
        self.parent.focus_set()

    def change_markings_color(self):
        self.select_color("markings_color")

    def change_numbers_color(self):
        self.select_color("numbers_color")

    def change_dtdow_color(self):
        self.select_color("dtdow_color")

    def change_dtdat_color(self):
        self.select_color("dtdat_color")

    def change_dttim_color(self):
        self.select_color("dttim_color")

    def change_hour_button_fg_color(self):
        color = colorchooser.askcolor()[1]
        if color:
            self.parent.hour_button.config(fg=color)
            self.parent.config_manager.set('COLORS', 'hour_button_fg_color', color)
        self.parent.focus_set()

    def change_hour_button_brdr_color(self):
        color = colorchooser.askcolor()[1]
        if color:
            self.parent.hour_button.config(highlightbackground=color)
            self.parent.config_manager.set('COLORS', 'hour_button_brdr_color', color)
        self.parent.focus_set()

    def change_minute_button_fg_color(self):
        color = colorchooser.askcolor()[1]
        if color:
            self.parent.minute_button.config(fg=color)
            self.parent.config_manager.set('COLORS', 'minute_button_fg_color', color)
        self.parent.focus_set()

    def change_minute_button_brdr_color(self):
        color = colorchooser.askcolor()[1]
        if color:
            self.parent.minute_button.config(highlightbackground=color)
            self.parent.config_manager.set('COLORS', 'minute_button_brdr_color', color)
        self.parent.focus_set()

    def change_alarm_display_fg_color(self):
        color = colorchooser.askcolor()[1]
        if color:
            self.parent.alarm_display.config(fg=color)
            self.parent.config_manager.set('COLORS', 'alarm_display_fg_color', color)
        self.parent.focus_set()

    def change_gpio_pin(self):
        gpio_pin = simpledialog.askinteger("GPIO Pin", "Enter a new GPIO pin number:")
        if gpio_pin is not None:
            self.parent.gpio_handler.change_gpio_pin(gpio_pin)
            self.parent.config_manager.set('SETTINGS', 'gpio_pin', str(gpio_pin))

    def change_snooze_time(self):
        time = simpledialog.askinteger("Snooze Time", "Enter the snooze time in minutes:", parent=self.parent)
        if time:
            self.parent.snooze_time = time
            self.parent.config_manager.set('SETTINGS', 'snooze_time', str(time))
        self.parent.focus_set()

    def minimize_program(self):
        self.parent.iconify()  # Minimize the main window

    def close_menu(self):
        self.unpost()
        self.parent.focus_set()

    def exit_program(self):
        self.parent.gpio_handler.deactivate_pin()
        self.parent.gpio_handler.cleanup()
        self.parent.destroy()
