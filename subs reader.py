import tkinter as tk
from datetime import timedelta
import time
import threading

def parse_srt(srt_text):
    subtitles = []
    for block in srt_text.strip().split('\n\n'):
        lines = block.split('\n')
        if len(lines) >= 3:
            start_end = lines[1]
            start, end = start_end.split(' --> ')
            subtitle = ' '.join(lines[2:])
            subtitles.append({'start': str_to_timedelta(start), 'end': str_to_timedelta(end), 'text': subtitle})
    return subtitles

def str_to_timedelta(time_str):
    h, m, s_ms = time_str.split(':')
    s, ms = s_ms.split(',')
    return timedelta(hours=int(h), minutes=int(m), seconds=int(s), milliseconds=int(ms))

def update_subtitle():
    global current_time, running
    while running:
        subtitle = get_subtitle_for_time(subtitles, current_time)
        subtitle_label.config(text=subtitle)
        time.sleep(1)
        current_time += timedelta(seconds=1)

def get_subtitle_for_time(subtitles, time):
    for subtitle in subtitles:
        if subtitle['start'] <= time <= subtitle['end']:
            return subtitle['text']
    return ""

# Initialize Tkinter
root = tk.Tk()
root.title("SRT Subtitle Viewer")

# Change window size
root.geometry("600x200+500-10")
# Configure widget Label
subtitle_label = tk.Label(root, text="", wraplength=550, fg="white", bg="black", font=("Arial", 20))
subtitle_label.pack(pady=20, fill="both", expand=True)

# Configure the background colour of the window
root.configure(background='black')

# Load SRT file
filesrt = "path/to/file.srt"
with open(filesrt, 'r') as file:
    srt_text = file.read()
# Parse SRT
subtitles = parse_srt(srt_text)

# Start time: n minutes, m seconds
# Manually adjust these values for aligning subtitles and video
# The reason being that when the video starts, the user may have a lag for running the app. Therefore, wait until the selected time (m and n) for running the app.
# E.g. when video starts, wait until sec 30 to run it. Then the subtitles will start at sec 30, which is where the video is at. The subs and video are aligned.
n,m=0,30
current_time = timedelta(minutes=n, seconds=m)
running = True
thread = threading.Thread(target=update_subtitle)
thread.start()

# Eliminate menu bar
# root.overrideredirect(True)

# Run
root.mainloop()
running = False
