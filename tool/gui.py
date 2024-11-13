# frontend/gui.py

import tkinter as tk
from tkinter import filedialog, messagebox
import cv2
from app import retrieve_tracking_results, save_tracking_results_to_csv
from video_display import display_frame
from helpers import prompt_id_change

video_path = None
csv_path = None
results = []

root = tk.Tk()
root.title("Tracking Result Modifier Tool")
root.geometry("1600x1600")
root.configure(bg='black')

def load_video():
    global video_path
    video_path = filedialog.askopenfilename(
        title="Select Video File", 
        filetypes=[("Video files", "*.mp4;*.avi")]
    )
    if video_path:
        messagebox.showinfo("Video Selected", f"Video loaded from:\n{video_path}")

def load_csv():
    global csv_path
    csv_path = filedialog.askopenfilename(
        title="Select CSV File", 
        filetypes=[("CSV files", "*.csv")]
    )
    if csv_path:
        messagebox.showinfo("CSV Selected", f"CSV loaded from:\n{csv_path}")

def start_review_and_modify():
    """Start the video review and modification process."""
    global results
    if not video_path or not csv_path:
        messagebox.showwarning("Files Missing", "Please load both video and CSV files.")
        return
    
    results = retrieve_tracking_results(csv_path)
    cap = cv2.VideoCapture(video_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_idx = 0
    paused = True

    display_frame(cap, frame_idx, results)

    while True:
        key = cv2.waitKey(1) & 0xFF

        if key == ord(' '):  # Play/Pause
            paused = not paused

        elif key == ord('q'):  # Quit
            break

        elif key == ord('e'):  # Edit IDs
            if paused:
                old_id, new_id = prompt_id_change()
                if old_id is not None and new_id is not None:
                    for f_idx in range(frame_idx, len(results)):
                        for obj in results[f_idx]:
                            if obj["track_id"] == old_id:
                                obj["track_id"] = new_id
                    messagebox.showinfo("ID Updated", f"Track ID {old_id} changed to {new_id} from frame {frame_idx + 1} onwards.")
                    display_frame(cap, frame_idx, results)

        elif paused:
            if key == 83 or key == ord('d'):
                frame_idx = min(frame_idx + 1, total_frames - 1)
                display_frame(cap, frame_idx, results)
            elif key == 81 or key == ord('a'):
                frame_idx = max(frame_idx - 1, 0)
                display_frame(cap, frame_idx, results)

        elif not paused:
            frame_idx = min(frame_idx + 1, total_frames - 1)
            if not display_frame(cap, frame_idx, results):
                break

    cap.release()
    cv2.destroyAllWindows()

def export_results():
    output_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
    if output_path:
        save_tracking_results_to_csv(results, output_path)
        messagebox.showinfo("Export Complete", f"Results successfully saved to:\n{output_path}")

# Tkinter UI Buttons
tk.Button(root, text="Load Video", command=load_video, bg="green", fg="white", font=("Arial", 16)).pack(pady=10)
tk.Button(root, text="Load CSV", command=load_csv, bg="green", fg="white", font=("Arial", 16)).pack(pady=10)
tk.Button(root, text="Start Review and Modification", command=start_review_and_modify, bg="green", fg="white", font=("Arial", 16)).pack(pady=10)
tk.Button(root, text="Export Updated Results", command=export_results, bg="green", fg="white", font=("Arial", 16)).pack(pady=10)

root.mainloop()
