import customtkinter as ctk
import tkinter as tk
import pygame
from tkinter import ttk
from PIL import Image

#using pygame mixer for sound
pygame.mixer.init()

#Global Variables
#Default times in minutes  
WORK_TIME = 25
SHORT_BREAK_TIME = 5
LONG_BREAK_TIME = 10

current_mode = "Pomodoro"
time_left = WORK_TIME * 60
is_running = False
timer_id = None
pomodoro_count = 0

# Purple theme colors
PRIMARY = "#5b2872"
HOVER = "#a064c9"
BACK_COLOR = "#2A1045"
LABEL_COLOR="#3c1e5d"
BORDER="#a855f7"

#converting time from seconds to minutes and second (format)
def format_time(seconds): 
    mins, secs = divmod(seconds, 60)
    return f"{mins:02d}:{secs:02d}"

#switching between modes
def switch_mode(mode): 
    global current_mode, time_left, is_running
    current_mode = mode
    is_running = False
    start_btn.configure(text="Start")
    update_timer_display()
    update_mode_indicator()
    if timer_id:
        root.after_cancel(timer_id)

#updates timer after every switch
def update_timer_display(): 
    global time_left
    if current_mode == "Pomodoro":
        time_left = WORK_TIME * 60
    elif current_mode == "Short Break":
        time_left = SHORT_BREAK_TIME * 60
    elif current_mode == "Long Break":
        time_left = LONG_BREAK_TIME * 60
    timer_label.configure(text=format_time(time_left))
    highlight_mode()

#for timer end sound
def play_sound(file):
    pygame.mixer.music.stop()  # Always stop before starting a new one
    pygame.mixer.music.load(file)
    pygame.mixer.music.play()

#The start button functionality (pauses or restarts)
def start_timer(): 
    global is_running
    if not is_running:
        is_running = True
        start_btn.configure(text="Pause")
        countdown()
    else:
        is_running = False
        start_btn.configure(text="Start")
        pygame.mixer.music.stop()

#decreases time by 1 sec per 1 sec
def countdown(): 
    global time_left, timer_id
    if is_running and time_left > 0:
        time_left -= 1
        timer_label.configure(text=format_time(time_left))
        #adding sound for pomodoro mode
        if time_left == 5: 
            if current_mode=="Pomodoro":
                play_sound("alarm.mp3")
        timer_id = root.after(1000, countdown)
    elif time_left == 0:
        start_btn.configure(text="Start")
        handle_completion()

#switching mode after time completion
def handle_completion(): 
    global pomodoro_count, time_left
    #adding sound for short and long breaks
    if current_mode=="Short Break": 
        play_sound("Twinkle.mp3")
    elif current_mode=="Long Break":
        play_sound("Twinkle.mp3")
    else:
        pygame.mixer.music.stop()
    #mode switching
    if current_mode == "Pomodoro":
        pomodoro_count += 1
        loop_label.configure(text=f"{pomodoro_count % 4}/4")
        if pomodoro_count % 4 == 0:
            switch_mode("Long Break")
        else:
            switch_mode("Short Break")
    else:
        switch_mode("Pomodoro")
    start_timer()

#skipping time
def skip_timer():
    global timer_id, is_running
    if timer_id:
        root.after_cancel(timer_id)
    is_running = False
    start_btn.configure(text="Start")
    handle_completion()

def open_settings(): #opens settings option
    def save_settings(event=None): #saves the times for different modes in the settings 
        global WORK_TIME, SHORT_BREAK_TIME, LONG_BREAK_TIME
        try:
            WORK_TIME = int(work_time_entry.get())
            SHORT_BREAK_TIME = int(short_break_time_entry.get())
            LONG_BREAK_TIME = int(long_break_time_entry.get())
            update_timer_display()
            settings_win.destroy()
        except ValueError:
            print("Please enter valid integer values")
    #the settungs page creation using ctk hehe
    settings_win = ctk.CTkToplevel(root)
    settings_win.title("Settings")
    settings_win.geometry("250x300")
    settings_win.configure(fg_color=BACK_COLOR)

    settings_win.bind("<Return>",save_settings) #saves time by pressing enter key.

    ctk.CTkLabel(settings_win, text="Pomodoro:").pack(pady=(10, 5))
    work_time_entry = ctk.CTkEntry(settings_win, fg_color=LABEL_COLOR,border_color=BORDER,width=100)
    work_time_entry.insert(0, str(WORK_TIME))
    work_time_entry.pack()

    ctk.CTkLabel(settings_win, text="Short Break:").pack(pady=(10, 5))
    short_break_time_entry = ctk.CTkEntry(settings_win, fg_color=LABEL_COLOR,border_color=BORDER,width=100)
    short_break_time_entry.insert(0, str(SHORT_BREAK_TIME))
    short_break_time_entry.pack()

    ctk.CTkLabel(settings_win, text="Long Break:").pack(pady=(10, 5))
    long_break_time_entry = ctk.CTkEntry(settings_win,fg_color=LABEL_COLOR,border_color=BORDER, width=100)
    long_break_time_entry.insert(0, str(LONG_BREAK_TIME))
    long_break_time_entry.pack()

    ctk.CTkButton(settings_win, text="Save", command=save_settings, fg_color=PRIMARY, hover_color=HOVER, border_color=BORDER).pack(pady=15)
    #keeps the settings on top (TopLevel)
    settings_win.lift()
    settings_win.attributes('-topmost', True)
    settings_win.after_idle(settings_win.attributes, '-topmost', False)
    settings_win.focus_force()

#color of the running mode button
def highlight_mode(): 
    for btn in [pomodoro_btn, short_break_btn, long_break_btn]:
        btn.configure(fg_color="transparent")
    if current_mode == "Pomodoro":
        pomodoro_btn.configure(fg_color=PRIMARY)
    elif current_mode == "Short Break":
        short_break_btn.configure(fg_color=PRIMARY)
    elif current_mode == "Long Break":
        long_break_btn.configure(fg_color=PRIMARY)

#color of the current mode indicator
def update_mode_indicator(): 
    if current_mode == "Pomodoro":
        mode_label.configure(text="Pomodoro Time ⏲", text_color="#be38e3",font=("Segoe UI", 20))
    elif current_mode == "Short Break":
        mode_label.configure(text="Short Break 💤", text_color="#d2afff",font=("Segoe UI", 20))
    elif current_mode == "Long Break":
        mode_label.configure(text="Long Break 😴", text_color="#38bbe3",font=("Segoe UI", 20))

#UI setup
ctk.set_appearance_mode("Dark")

root = ctk.CTk()
root.title("Timer")
root.iconbitmap("Timer.ico")
root.geometry("450x280")
root.configure(fg_color = BACK_COLOR)
image=  ctk.CTkImage(Image.open("refresh.png"), size=(22,22))
# Top controls
top_frame = ctk.CTkFrame(root, fg_color=LABEL_COLOR)
top_frame.pack(pady=10, fill="x", padx=10)

loop_label = ctk.CTkLabel(top_frame, text="0/4", font=("Segoe UI", 18))
loop_label.pack(side="left", padx=10)

ctk.CTkButton(top_frame, text="⚙", width=35, command=open_settings, fg_color=PRIMARY, hover_color= HOVER, border_color=BORDER).pack(side="right",padx=0)

# Mode Indicator Label
mode_label = ctk.CTkLabel(root, text="", font=("Segoe UI", 16))
mode_label.pack()
update_mode_indicator()

# Timer display
timer_label = ctk.CTkLabel(root, text=format_time(time_left), font=("Segoe UI", 48))
timer_label.pack(pady=10)

# Frame to hold Start and Skip side by side
button_frame = ctk.CTkFrame(root, fg_color="transparent")
button_frame.pack(pady=10)

#start and pause button
start_btn = ctk.CTkButton(button_frame, text="  Start", command=start_timer, width=140, fg_color=PRIMARY, hover_color=HOVER, border_color=BORDER)
start_btn.pack(side="left", padx=3)

#skip button
skip_btn = ctk.CTkButton(button_frame,text="",image=image, command=skip_timer, width=40, fg_color=PRIMARY, hover_color=HOVER, border_color=BORDER, font=("Segoe UI",20))
skip_btn.pack(side="left" , padx=2)

# Mode Buttons
mode_frame = ctk.CTkFrame(root, fg_color="transparent")
mode_frame.pack(pady=10)

pomodoro_btn = ctk.CTkButton(mode_frame, text="Pomodoro", command=lambda: switch_mode("Pomodoro"), width=90, fg_color="transparent", hover_color=HOVER, border_color=BORDER)
pomodoro_btn.grid(row=0, column=0, padx=5)

short_break_btn = ctk.CTkButton(mode_frame, text="Short Break", command=lambda: switch_mode("Short Break"), width=90, fg_color="transparent", hover_color=HOVER, border_color=BORDER)
short_break_btn.grid(row=0, column=1, padx=5)

long_break_btn = ctk.CTkButton(mode_frame, text="Long Break", command=lambda: switch_mode("Long Break"), width=90, hover_color=HOVER, border_color=BORDER)
long_break_btn.grid(row=0, column=2, padx=5)

highlight_mode()
root.mainloop()
