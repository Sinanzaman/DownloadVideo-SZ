import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
from datetime import datetime  # Bu satırı ekleyin

def browse_directory():
    folder_selected = filedialog.askdirectory()
    entry_video_location.delete(0, tk.END)
    entry_video_location.insert(0, folder_selected)

def insert_current_date():
    current_date = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    entry_video_name.delete(0, tk.END)
    entry_video_name.insert(0, current_date)

def run_command():
    base_command = "yt-dlp -o "
    
    video_name = entry_video_name.get()
    location = entry_video_location.get()
    video_link = entry_video_link.get()
    
    if not video_name or not location or not video_link:
        messagebox.showerror("Error", "Video Title, Location and Connection must be entered!")
        return
    
    output_path = f'"{location}/{video_name}.mp4"'
    
    try:
        start_hour = int(start_hour_spin.get())
        start_minute = int(start_minute_spin.get())
        start_second = int(start_second_spin.get())

        end_hour = int(end_hour_spin.get())
        end_minute = int(end_minute_spin.get())
        end_second = int(end_second_spin.get())

        if any(t < 0 for t in [start_hour, start_minute, start_second, end_hour, end_minute, end_second]):
            raise ValueError("Time cannot be negative!")

        start_time = start_hour * 3600 + start_minute * 60 + start_second
        end_time = end_hour * 3600 + end_minute * 60 + end_second

    except ValueError:
        messagebox.showerror("Error", "Start and end times must be a valid number!")
        return

    download_section = f'--download-sections "*{start_time}-{end_time}"'

    command = f'{base_command} {output_path} -f bestvideo+bestaudio[ext=m4a] --merge-output-format mp4 {download_section} "{video_link}"'

    try:
        subprocess.run(command, shell=True, check=True)
        messagebox.showinfo("Success", "Video has been downloaded successfully!")
    except subprocess.CalledProcessError:
        messagebox.showerror("Error", "The video could not be downloaded!")

def on_mouse_wheel(event, *spinboxes):
    for spinbox in spinboxes:
        if event.delta > 0:
            spinbox.invoke("buttonup")
        elif event.delta < 0:
            spinbox.invoke("buttondown")

root = tk.Tk()
root.title("DownloadVideo-SZ")

window_width = 480
window_height = 300
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

position_top = int(screen_height / 2 - window_height / 2)
position_left = int(screen_width / 2 - window_width / 2)

root.geometry(f'{window_width}x{window_height}+{position_left}+{position_top}')

main_frame = tk.Frame(root)
main_frame.pack(padx=10, pady=10, fill="both", expand=True)

label_video_name = tk.Label(main_frame, text="Video name:")
label_video_name.grid(row=0, column=0, pady=5, sticky="w")
entry_video_name = tk.Entry(main_frame, width=30)
entry_video_name.grid(row=0, column=1, pady=5)

date_button = tk.Button(main_frame, text="Add Date", command=insert_current_date)
date_button.grid(row=0, column=2, padx=5, pady=5)

insert_current_date()

label_video_location = tk.Label(main_frame, text="File Location:")
label_video_location.grid(row=1, column=0, pady=5, sticky="w")
entry_video_location = tk.Entry(main_frame, width=30)
entry_video_location.grid(row=1, column=1, pady=5)

browse_button = tk.Button(main_frame, text="Select Location", command=browse_directory)
browse_button.grid(row=1, column=2, padx=5, pady=5)

label_start_time = tk.Label(main_frame, text="Starter Time:\n(hh--mm-ss)")
label_start_time.grid(row=2, column=0, pady=5, sticky="w")

start_hour_spin = tk.Spinbox(main_frame, from_=0, to=23, width=5)
start_hour_spin.grid(row=2, column=1, padx=5, pady=5)

start_minute_spin = tk.Spinbox(main_frame, from_=0, to=59, width=5)
start_minute_spin.grid(row=2, column=2, padx=5, pady=5)

start_second_spin = tk.Spinbox(main_frame, from_=0, to=59, width=5)
start_second_spin.grid(row=2, column=3, padx=5, pady=5)

label_end_time = tk.Label(main_frame, text="Finish time:\n(hh--mm-ss)")
label_end_time.grid(row=3, column=0, pady=5, sticky="w")

end_hour_spin = tk.Spinbox(main_frame, from_=0, to=23, width=5)
end_hour_spin.grid(row=3, column=1, padx=5, pady=5)

end_minute_spin = tk.Spinbox(main_frame, from_=0, to=59, width=5)
end_minute_spin.grid(row=3, column=2, padx=5, pady=5)

end_second_spin = tk.Spinbox(main_frame, from_=0, to=59, width=5)
end_second_spin.grid(row=3, column=3, padx=5, pady=5)

start_hour_spin.bind("<MouseWheel>", lambda event, spinbox=start_hour_spin, end_spinbox=end_hour_spin: on_mouse_wheel(event, spinbox, end_spinbox))
start_minute_spin.bind("<MouseWheel>", lambda event, spinbox=start_minute_spin, end_spinbox=end_minute_spin: on_mouse_wheel(event, spinbox, end_spinbox))
start_second_spin.bind("<MouseWheel>", lambda event, spinbox=start_second_spin, end_spinbox=end_second_spin: on_mouse_wheel(event, spinbox, end_spinbox))

end_hour_spin.bind("<MouseWheel>", lambda event, spinbox=end_hour_spin: on_mouse_wheel(event, spinbox))
end_minute_spin.bind("<MouseWheel>", lambda event, spinbox=end_minute_spin: on_mouse_wheel(event, spinbox))
end_second_spin.bind("<MouseWheel>", lambda event, spinbox=end_second_spin: on_mouse_wheel(event, spinbox))

label_video_link = tk.Label(main_frame, text="Video URL:")
label_video_link.grid(row=4, column=0, pady=5, sticky="w")
entry_video_link = tk.Entry(main_frame, width=30)
entry_video_link.grid(row=4, column=1, pady=5)

run_button = tk.Button(main_frame, text="DOWNLOAD", command=run_command)
run_button.grid(row=5, column=0, columnspan=4, pady=10)

root.mainloop()
