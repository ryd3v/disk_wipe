# Ryan Collins
# 2023
# @ryd3v
import os
import platform
import subprocess
import threading
import time
import tkinter as tk
from tkinter import messagebox

start_time = None


def wipe_disk():
    global start_time
    start_time = time.time()  # start timer
    threading.Thread(target=wipe_disk_thread).start()


# Wipe disk on Windows
def wipe_disk_windows(disk):
    subprocess.run(['cipher', '/w:' + disk], check=True)


# Wipe disk on Linux
def wipe_disk_linux(disk, num_passes):
    for i in range(num_passes):
        subprocess.run(['sudo', 'dc3dd', f'wipe={disk}', 'pat=0x00', f'hash=sha256', f'hlog=pass{i + 1}.log'],
                       check=True)


def wipe_disk_thread():
    disk = disk_entry.get()
    os_name = platform.system()
    if os_name == 'Windows':
        if not os.path.exists(disk):
            messagebox.showerror('Error', f'Disk {disk} does not exist.')
            return
        wipe_disk_windows(disk)
    elif os_name == 'Linux':
        num_passes = int(num_passes_entry.get())  # Convert to integer here
        if not os.path.exists(disk):
            messagebox.showerror('Error', f'Disk {disk} does not exist.')
            return
        try:
            wipe_disk_linux(disk, num_passes)
        except subprocess.CalledProcessError:
            messagebox.showerror('Error', f'Failed to wipe disk {disk}.')
    else:
        messagebox.showerror('Error', 'Unsupported operating system.')


# Timer
def update_timer():
    if start_time is not None:  # only update if timer has started
        elapsed_time = time.time() - start_time
        timer_label.config(text=f"Elapsed time: {int(elapsed_time)} seconds")
    root.after(1000, update_timer)  # schedule this function to run again after 1 second (1000 milliseconds)


# GUI
root = tk.Tk()
root.title("Disk Wipe")
root.configure(bg='#18181b')
root.geometry("500x300")
disk_label = tk.Label(root, text='Disk:', bg='black', fg='#f4f4f5')
disk_label.pack()
disk_entry = tk.Entry(root)
disk_entry.pack()
num_passes_label = tk.Label(root, text='Number of Passes:', bg='black', fg='#f4f4f5')
num_passes_label.pack()
num_passes_entry = tk.Entry(root)
num_passes_entry.pack()
timer_label = tk.Label(root, text="Elapsed time: 0 seconds", bg='#18181b', fg='#f4f4f5')
timer_label.pack(pady=10)
wipe_button = tk.Button(root, text='Wipe Disk', bg='#3b82f6', fg='#f4f4f5', command=wipe_disk)
wipe_button.pack(pady=5)
root.after(1000, update_timer)
root.mainloop()
