import os
import time
import math
import datetime
import tkinter as tk
from tkinter import filedialog
from popup_menu import PopupMenu
from config_manager import ConfigManager
from gpio_handler import GPIOHandler
import threading
import simpleaudio as sa

class Clock(tk.Tk):
    def __init__(self):
        super().__init__()
        self.config_manager = ConfigManager()
        self.gpio_handler = GPIOHandler(int(self.config_manager.get('SETTINGS', 'gpio_pin')))
        self.alarm_sound_file = self.config_manager.get('SETTINGS', 'alarm_sound_file', fallback="alarm.wav")
        self.alarm_method = self.config_manager.get('SETTINGS', 'alarm_method', fallback="both")
        self.alarm_playback = None

        self.init_colors()
        self.init_ui()
        self.alarm_time = None
        self.alarm_triggered = False
        self.snooze_time = int(self.config_manager.get('SETTINGS', 'snooze_time'))
        self.load_alarm_time()
        self.update_clock()

    def init_colors(self):
        self.second_color = self.config_manager.get('COLORS', 'second_color')
        self.minute_color = self.config_manager.get('COLORS', 'minute_color')
        self.hour_color = self.config_manager.get('COLORS', 'hour_color')
        self.border_color = self.config_manager.get('COLORS', 'border_color')
        self.bg_color = self.config_manager.get('COLORS', 'bg_color')
        self.markings_color = self.config_manager.get('COLORS', 'markings_color')
        self.numbers_color = self.config_manager.get('COLORS', 'numbers_color')
        self.alarm_display_fg_color = self.config_manager.get('COLORS', 'alarm_display_fg_color')
        self.hour_button_fg_color = self.config_manager.get('COLORS', 'hour_button_fg_color')
        self.minute_button_fg_color = self.config_manager.get('COLORS', 'minute_button_fg_color')
        self.hour_button_brdr_color = self.config_manager.get('COLORS', 'hour_button_brdr_color')
        self.minute_button_brdr_color = self.config_manager.get('COLORS', 'minute_button_brdr_color')
        self.dtdow_color = self.config_manager.get('COLORS', 'dtdow_color')
        self.dtdat_color = self.config_manager.get('COLORS', 'dtdat_color')
        self.dttim_color = self.config_manager.get('COLORS', 'dttim_color')

    def init_ui(self):
        self.attributes('-fullscreen', True)
        self.update_idletasks()
        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()

        self.title("Clock")
        self.canvas = tk.Canvas(self, width=self.screen_width, height=self.screen_height, bg=self.bg_color, highlightthickness=0, cursor="none")
        self.canvas.pack(fill=tk.BOTH, expand=1)

        self.canvas.bind("<Button-1>", self.show_menu)

        self.popup_menu = PopupMenu(self)
        self.alarm_display = tk.Label(self.canvas, text="--:--", font=('Arial', 20, 'bold'), bg=self.bg_color, fg=self.alarm_display_fg_color,
                                       activebackground=self.bg_color, activeforeground=self.alarm_display_fg_color, width=10, height=1)
        self.alarm_display.place(x=self.screen_width / 2, y=(self.screen_height / 2) + 50, anchor="n")
        self.alarm_display.bind("<Button-1>", self.destroy_alarm)

        self.hour_button = tk.Button(self.canvas, text="Set Hour", font=('Arial', 20, 'bold'), 
                                     fg=self.hour_button_fg_color, bg=self.bg_color, activebackground=self.bg_color, activeforeground=self.hour_button_fg_color, 
                                     width=8, height=4, highlightbackground=self.hour_button_brdr_color, relief=tk.FLAT)
        self.hour_button.place(x=0, y=self.screen_height, anchor="sw")
        self.hour_button.bind("<Button-1>", self.set_alarm_hour)

        self.minute_button = tk.Button(self.canvas, text="Set Minute", font=('Arial', 20, 'bold'), 
                                       fg=self.minute_button_fg_color, bg=self.bg_color, activebackground=self.bg_color, activeforeground=self.minute_button_fg_color, 
                                       width=8, height=4, highlightbackground=self.minute_button_brdr_color, relief=tk.FLAT)
        self.minute_button.place(x=self.screen_width, y=self.screen_height, anchor="se")
        self.minute_button.bind("<Button-1>", self.set_alarm_minute)

        script_directory = os.path.dirname(os.path.abspath(__file__))
        icon_path = os.path.join(script_directory, 'clockipy.png')

        self.icon_image = tk.PhotoImage(file=icon_path)
        self.iconphoto(False, self.icon_image)

    def load_alarm_time(self):
        alarm_hour = self.config_manager.get('SETTINGS', 'alarm_hour')
        alarm_minute = self.config_manager.get('SETTINGS', 'alarm_minute')
        if alarm_hour and alarm_minute:
            self.alarm_time = [int(alarm_hour), int(alarm_minute)]
            self.update_alarm_display()

    def update_canvas_colors(self):
        self.canvas.config(bg=self.bg_color)
        self.hour_button.config(bg=self.bg_color)
        self.minute_button.config(bg=self.bg_color)
        self.alarm_display.config(bg=self.bg_color)

    def update_clock(self):
        self.canvas.delete("all")

        center_x, center_y = self.screen_width / 2, self.screen_height / 2
        radius = min(center_x, center_y) - 50

        self.canvas.create_oval(center_x - 5, center_y - 5, center_x + 5, center_y + 5, fill=self.bg_color, outline=self.border_color)
        self.canvas.create_oval(center_x - radius, center_y - radius, center_x + radius, center_y + radius, fill=self.bg_color, outline=self.border_color)

        self.draw_marks(center_x, center_y, radius)
        self.draw_numbers(center_x, center_y, radius)
        self.draw_date_and_time()

        current_time = time.localtime(time.time())
        second_angle = math.radians(current_time.tm_sec * 6 - 90)
        minute_angle = math.radians(current_time.tm_min * 6 - 90 + current_time.tm_sec / 10.0)
        hour_angle = math.radians((current_time.tm_hour % 12) * 30 - 90 + current_time.tm_min / 2.0)

        second_hand_length = radius - 30
        minute_hand_length = radius - 60
        hour_hand_length = radius - 90

        second_x, second_y = center_x + second_hand_length * math.cos(second_angle), center_y + second_hand_length * math.sin(second_angle)
        minute_x, minute_y = center_x + minute_hand_length * math.cos(minute_angle), center_y + minute_hand_length * math.sin(minute_angle)
        hour_x, hour_y = center_x + hour_hand_length * math.cos(hour_angle), center_y + hour_hand_length * math.sin(hour_angle)

        self.canvas.create_line(center_x, center_y, second_x, second_y, fill=self.second_color, width=2)
        self.canvas.create_line(center_x, center_y, minute_x, minute_y, fill=self.minute_color, width=6)
        self.canvas.create_line(center_x, center_y, hour_x, hour_y, fill=self.hour_color, width=8)

        self.check_alarm(current_time)
        self.update_id = self.after(10, self.update_clock)

    def draw_marks(self, center_x, center_y, radius):
        mark_radius = radius - 5
        major_mark_length = 15
        minor_mark_length = 5

        for i in range(60):
            angle = math.radians(i * 6 - 90)
            length = major_mark_length if i % 5 == 0 else minor_mark_length
            start_x = center_x + (mark_radius - length) * math.cos(angle)
            start_y = center_y + (mark_radius - length) * math.sin(angle)
            end_x = center_x + mark_radius * math.cos(angle)
            end_y = center_y + mark_radius * math.sin(angle)
            width = 6 if i % 5 == 0 else 3
            self.canvas.create_line(start_x, start_y, end_x, end_y, width=width, fill=self.markings_color)

    def draw_numbers(self, center_x, center_y, radius):
        number_radius = radius - 30

        for i in range(1, 13):
            angle = math.radians(i * 30 - 90)
            x = center_x + number_radius * math.cos(angle)
            y = center_y + number_radius * math.sin(angle)
            self.canvas.create_text(x, y, text=str(i), font=('Arial', int(radius / 10), 'bold'), fill=self.numbers_color)

    def draw_date_and_time(self):
        now = datetime.datetime.now()
        day_of_week = now.strftime('%A')
        date = now.strftime('%d %B %Y')
        time_str = now.strftime('%I:%M:%S %p')
        padding = 10
        self.canvas.create_text(padding, padding, text=day_of_week, anchor='nw', font=('Arial', 20), fill=self.dtdow_color)
        self.canvas.create_text(padding, padding + 30, text=date, anchor='nw', font=('Arial', 20), fill=self.dtdat_color)
        self.canvas.create_text(padding, padding + 60, text=time_str, anchor='nw', font=('Arial', 20), fill=self.dttim_color)

    def show_menu(self, event):
        try:
            self.popup_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.popup_menu.grab_release()

    alarm_thread_running = threading.Event()

    def play_audio_alarm(self):
        while self.alarm_thread_running.is_set():
            wave_obj = sa.WaveObject.from_wave_file(self.alarm_sound_file)
            self.alarm_playback = wave_obj.play()
            self.alarm_playback.wait_done()

    def play_gpio_alarm(self):
        while self.alarm_thread_running.is_set():
            self.gpio_handler.activate_pin()
            time.sleep(0.125)
            self.gpio_handler.deactivate_pin()
            time.sleep(0.125)

    def start_alarm_sound(self):
        self.alarm_thread_running.set()
        if self.alarm_method in ['both', 'audio']:
            threading.Thread(target=self.play_audio_alarm, daemon=True).start()
        if self.alarm_method in ['both', 'gpio']:
            threading.Thread(target=self.play_gpio_alarm, daemon=True).start()

    def stop_alarm_sound(self):
        self.alarm_thread_running.clear()
        self.gpio_handler.deactivate_pin()
        if self.alarm_playback:
            self.alarm_playback.stop()

    def show_alarm_popup(self):
        self.start_alarm_sound()
        self.alarm_triggered = True

        def stop_alarm():
            self.stop_alarm_sound()
            self.delete_alarm()
            self.popup.destroy()
            self.focus_set()

        def reset_alarm():
            self.stop_alarm_sound()
            self.delete_alarm()
            self.alarm_time = None
            self.update_alarm_display()
            self.popup.destroy()
            self.focus_set()

        def snooze_alarm():
            self.stop_alarm_sound()
            self.delete_alarm()
            
            # Calculate the new minutes
            new_minutes = self.alarm_time[1] + self.snooze_time
            
            # If new minutes exceed 59, adjust hours and minutes
            if new_minutes >= 60:
                self.alarm_time[0] = (self.alarm_time[0] + new_minutes // 60) % 24
                self.alarm_time[1] = new_minutes % 60
            else:
                self.alarm_time[1] = new_minutes
            
            self.update_alarm_display()
            self.popup.destroy()
            self.focus_set()

        self.popup = tk.Toplevel(self, bg="black", cursor="none")
        self.popup.overrideredirect(True)
        self.popup.geometry("250x200+{}+{}".format(self.screen_width//2-100, self.screen_height//2-50))

        label = tk.Label(self.popup, text="Stop the alarm?\nSnooze the alarm?\nReset the alarm?", font=('Arial', 20, 'bold'), bg="black", fg="purple")
        label.grid(row=0, column=0, columnspan=3, pady=(10, 20))

        red_button = tk.Button(self.popup, text="STOP", bg="red", command=stop_alarm, width=5)
        red_button.grid(row=1, column=0, sticky=tk.W, padx=10)

        pink_button = tk.Button(self.popup, text="SNOOZE", bg="pink", command=snooze_alarm, width=5)
        pink_button.grid(row=1, column=1)

        yellow_button = tk.Button(self.popup, text="RESET", bg="yellow", command=reset_alarm, width=5)
        yellow_button.grid(row=1, column=2, sticky=tk.E, padx=10)

    def set_alarm_hour(self, event):
        if self.alarm_time is None:
            self.alarm_time = [0, 0]
        self.alarm_time[0] = (self.alarm_time[0] + 1) % 24
        self.update_alarm_display()
        self.save_alarm_time()

    def set_alarm_minute(self, event):
        if self.alarm_time is None:
            self.alarm_time = [0, 0]
        self.alarm_time[1] = (self.alarm_time[1] + 1) % 60
        self.update_alarm_display()
        self.save_alarm_time()

    def update_alarm_display(self):
        if self.alarm_time:
            hour = self.alarm_time[0]
            minute = self.alarm_time[1]
            period = "AM" if hour < 12 else "PM"
            hour = hour % 12
            if hour == 0:
                hour = 12
            self.alarm_display.config(text=f"{hour:02}:{minute:02} {period}")
        else:
            self.alarm_display.config(text="--:--")

    def check_alarm(self, current_time):
        if self.alarm_time and not self.alarm_triggered:
            if (current_time.tm_hour == self.alarm_time[0] and current_time.tm_min == self.alarm_time[1]
                    and current_time.tm_sec == 0):
                self.alarm_triggered = True
                self.show_alarm_popup()

    def destroy_alarm(self, event=None):
        self.alarm_time = None
        self.alarm_triggered = False
        self.alarm_display.config(text="--:--")
        self.config_manager.set('SETTINGS', 'alarm_hour', '')
        self.config_manager.set('SETTINGS', 'alarm_minute', '')

    def delete_alarm(self):
        self.alarm_triggered = False

    def save_alarm_time(self):
        if self.alarm_time:
            self.config_manager.set('SETTINGS', 'alarm_hour', str(self.alarm_time[0]))
            self.config_manager.set('SETTINGS', 'alarm_minute', str(self.alarm_time[1]))
        else:
            self.config_manager.set('SETTINGS', 'alarm_hour', '')
            self.config_manager.set('SETTINGS', 'alarm_minute', '')

    def change_alarm_sound(self):
        new_sound_file = filedialog.askopenfilename(filetypes=[("WAV files", "*.wav")])
        if new_sound_file:
            self.alarm_sound_file = new_sound_file
            self.config_manager.set('SETTINGS', 'alarm_sound_file', new_sound_file)

    def change_alarm_method(self, method):
        self.alarm_method = method
        self.config_manager.set('SETTINGS', 'alarm_method', method)

if __name__ == "__main__":
    app = Clock()
    app.mainloop()
