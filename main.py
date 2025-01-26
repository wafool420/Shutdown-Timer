import tkinter
import os
import random
import sys
import winsound
from tkinter import *
from tkinter import messagebox
from plyer import notification

countdown_task = None
roulette = False

def countdown(timer):
    global countdown_task, roulette
    if timer >= 0:
        days, remainder = divmod(timer, 86400)
        hours, remainder = divmod(remainder, 3600)
        mins, secs = divmod(remainder, 60)
        STRING.set(f"{days:02d}:{hours:02d}:{mins:02d}:{secs:02d}")

        if timer == 600:  
            show_notification("10 minutes left!")
            show_system_notification("10 minutes left!")
        elif timer == 300:  
            show_notification("5 minutes left!")
            show_system_notification("5 minutes left!")
        elif timer == 60:  
            show_notification("1 minute left!")
            show_system_notification("1 minute left!")

        countdown_task = window.after(1000, countdown, timer - 1)
    else:
        if roulette:
            gun_slot = random.randint(1, 5)
            if gun_slot == 4:
                display2.pack(pady=20)
                STRING2.set("DEAD")
                display2.config(fg="red")
                show_system_notification("YOU LOSE")
                os.system("shutdown /s /t 1")
            else:
                display2.pack(pady=20)
                STRING2.set("LIVE")
                display2.config(fg="green")
                print(gun_slot)
                start_countdown()
        else:
            show_system_notification("Time's up! Shutting down...")
            os.system("shutdown /s /t 1")
            

def show_notification(message):
    notification_window = Toplevel(window)
    notification_window.geometry("300x100")
    notification_window.title("Notification")

    label = Label(notification_window, text=message, font=("Arial", 14))
    label.pack(pady=10)

    ok_button = Button(notification_window, text="OK", font=("Arial", 12), command=notification_window.destroy)
    ok_button.pack(pady=10)

    notification_window.update_idletasks()
    x = window.winfo_x() + (window.winfo_width() // 2) - (300 // 2)
    y = window.winfo_y() + (window.winfo_height() // 2) - (100 // 2)
    notification_window.geometry(f"300x100+{x}+{y}")

def show_system_notification(message):
    notification.notify(
        title="Shutdown Roulette Notification",
        message=message,
        timeout=5  
    )
            
def stop_countdown():
    global countdown_task, roulette
    if countdown_task:
        window.after_cancel(countdown_task)
        STRING.set("00:00:00:00")
        countdown_task = None
        roulette = False
        display2.pack_forget()


def start_countdown():
    global countdown_task, roulette
    try:
        days = int(Entry_days.get())
        hours = int(Entry_hours.get())
        minutes = int(Entry_minutes.get())
        seconds = int(Entry_seconds.get())
        total_seconds = days * 86400 + hours * 3600 + minutes * 60 + seconds

        if countdown_task:
            window.after_cancel(countdown_task)

        countdown(total_seconds)

    except ValueError:
        STRING.set("Invalid input!")


def reset():
    stop_countdown()
    display2.pack_forget()
    roulette = False
    Entry_days.delete(0, END)
    Entry_hours.delete(0, END)
    Entry_minutes.delete(0, END)
    Entry_seconds.delete(0, END)
    Entry_days.insert(0, "0")
    Entry_hours.insert(0, "0")
    Entry_minutes.insert(0, "0")
    Entry_seconds.insert(0, "0")
    STRING.set("00:00:00:00")

def open_confirmation_window():
    confirmation_window = Toplevel(window)
    confirmation_window.geometry("250x100")
    confirmation_window.title("Confirmation")

    confirmation_window.update_idletasks()
    x = window.winfo_x() + (window.winfo_width() // 2) - (250 // 2)
    y = window.winfo_y() + (window.winfo_height() // 2) - (100 // 2)
    confirmation_window.geometry(f"250x100+{x}+{y}")

    def on_yes():
        global roulette
        print("Action confirmed!")
        days = int(Entry_days.get())
        hours = int(Entry_hours.get())
        minutes = int(Entry_minutes.get())
        seconds = int(Entry_seconds.get())
        total_seconds = days * 86400 + hours * 3600 + minutes * 60 + seconds
        print(f"Roulette will use {total_seconds} seconds")
        roulette = True
        start_countdown()
        confirmation_window.destroy()

    def on_no():
        print("Action canceled!")
        confirmation_window.destroy()
    
    label = Label(confirmation_window, text="Are you sure?", font=("Arial", 14))
    label.pack(pady=10)

    yes_button = Button(confirmation_window, text="Yes", font=("Arial", 15), command=on_yes)
    yes_button.pack(side=LEFT, padx=20, pady=10)

    no_button = Button(confirmation_window, text="No", font=("Arial", 15), command=on_no)
    no_button.pack(side=RIGHT, padx=20, pady=10)

def get_exe_directory():
    """Function to get the directory of the exe file."""
    return os.path.dirname(sys.argv[0])

window = Tk()
window.title("Shutdown Timer")
window.configure(bg="#0c192b")

title = Label(window, font=("Calibri", 50, "bold"), text="Shutdown Timer", fg="white")
title.pack(pady=20)
title.configure(bg="#0c192b")

exe_directory = get_exe_directory()
image_path = os.path.join(exe_directory, 'PC.png')
image = PhotoImage(file=image_path)
image_Label = Label(window, image=image)
image_Label.pack()
image_Label.configure(bg="#0c192b")
ico_image = os.path.join(exe_directory, 'icon.ico')
window.iconbitmap(ico_image)

STRING = StringVar()
STRING.set("00:00:00:00")
display = Label(window, font=("Arial", 50, "bold"), textvariable=STRING, fg="white")
display.pack(pady=20)
display.configure(bg="#0c192b")

STRING2 = StringVar()
STRING2.set("")
display2 = Label(window, font=("Arial", 50, "bold"), textvariable=STRING2)
display2.pack_forget()
display2.configure(bg="#0c192b")

entry_frame = Frame(window)
entry_frame.pack(pady=10)

Entry_days = Entry(entry_frame, font=("Arial", 30), width=7, justify=CENTER, fg="white", insertbackground="white")
Entry_days.pack(side=LEFT, padx=5)
Entry_days.configure(bg="#151617")

Entry_hours = Entry(entry_frame, font=("Arial", 30), width=7, justify=CENTER, fg="white", insertbackground="white")
Entry_hours.pack(side=LEFT, padx=5)
Entry_hours.configure(bg="#151617")

Entry_minutes = Entry(entry_frame, font=("Arial", 30), width=7, justify=CENTER, fg="white", insertbackground="white")
Entry_minutes.pack(side=LEFT, padx=5)
Entry_minutes.configure(bg="#151617")

Entry_seconds = Entry(entry_frame, font=("Arial", 30), width=7, justify=CENTER, fg="white", insertbackground="white")
Entry_seconds.pack(side=LEFT, padx=5)
Entry_seconds.configure(bg="#151617")

Entry_days.insert(0, "0")
Entry_hours.insert(0, "0")
Entry_minutes.insert(0, "0")
Entry_seconds.insert(0, "0")

button_frame = Frame(window)
button_frame.pack(pady=10)
button_frame.configure(bg="#151617")

start_button = Button(button_frame, font=('Arial', 15, "bold"), text="Start", command=start_countdown)
start_button.pack(side=LEFT, padx=5)

stop_button = Button(button_frame, font=('Arial', 15, "bold"), text="Stop", command=stop_countdown)
stop_button.pack(side=LEFT, padx=5)

reset_button = Button(button_frame, font=('Arial', 15, "bold"), text="Reset", command=reset)
reset_button.pack(side=LEFT, padx=5)

roulette_button = Button(button_frame, font=('Arial', 15, "bold"), text="Roulette", command=lambda: open_confirmation_window())
roulette_button.pack(side=LEFT, padx=5)

window.mainloop()
