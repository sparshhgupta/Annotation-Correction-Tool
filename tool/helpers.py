# frontend/helpers.py

import tkinter as tk
from tkinter import simpledialog

def prompt_id_change():
    """Prompts user to enter old and new track IDs."""
    old_id = simpledialog.askinteger("Old ID", "Enter the track ID you want to change:")
    new_id = simpledialog.askinteger("New ID", "Enter the new track ID to replace it with:")
    return old_id, new_id
