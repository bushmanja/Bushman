import bot
import sys
import tkinter as tk  # Moved to the top
from tkinter import ttk, scrolledtext, messagebox, filedialog
from gui import YouTubeViewBotGUI 
#import YouTubeViewBotGUI  # Now imports AFTER tkinter
from bot import YouTubeViewBot

if __name__ == "__main__":
    
    root = tk.Tk()
    app = YouTubeViewBotGUI(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()

