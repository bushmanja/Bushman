#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import sys
import json
import os
from bot import YouTubeViewBot  # Import the bot class


class TextHandler(logging.Handler):
    """Custom logging handler for GUI text widget"""
    def __init__(self, text_widget):
        super().__init__()
        self.text_widget = text_widget
        
    def emit(self, record):
        msg = self.format(record)
        self.text_widget.config(state=tk.NORMAL)
        self.text_widget.insert(tk.END, msg + "\n")
        self.text_widget.see(tk.END)
        self.text_widget.config(state=tk.DISABLED)



class YouTubeViewBotGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube View Simulator - PHD ADMIN PROTOCOL 22#")
        self.root.geometry("1000x800")  # Increased size for more info
        self.root.resizable(True, True)
        
        
        # Initialize state variables
        self.running = False
        self.original_stdout = sys.stdout
        self.bot = None  # Will be initialized later
        # Replace stdout redirection with proper logging
        sys.stdout = sys.__stdout__  # Restore original stdout
        #self.setup_logging()
        
        # Create GUI widgets
        self.create_widgets()
        
        # Set up logging
        self.setup_logging()
        
        # Load configuration
        self.load_config()
        
        # Set up closing handler
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
    def setup_logging(self):
        """Configure logging to GUI widget"""
        # Create logger
        self.logger = logging.getLogger("YTBotGUI")
        self.logger.setLevel(logging.INFO)
    
        # Create text handler
        text_handler = TextHandler(self.log_display)
        text_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    
        # Add handler
        self.logger.addHandler(text_handler)
    
        # Configure bot logging
        bot_logger = logging.getLogger("YouTubeViewBot")
        bot_logger.addHandler(text_handler)
        
    def create_widgets(self):
        # Configure styles
        style = ttk.Style()
        style.configure("TFrame", background="#f0f0f0")
        style.configure("TLabel", background="#f0f0f0", font=("Arial", 10))
        style.configure("TButton", font=("Arial", 10))
        style.configure("Header.TLabel", font=("Arial", 12, "bold"))
        style.configure("Status.TLabel", font=("Arial", 10, "bold"))
        style.configure("Compliance.TLabel", font=("Arial", 10, "bold"), foreground="green")
        style.configure("Warning.TLabel", font=("Arial", 10, "bold"), foreground="orange")
        
        # Create main frame
        main_frame = ttk.Frame(self.root, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header
        header = ttk.Label(main_frame, text="YouTube View Simulator - Academic Research", style="Header.TLabel")
        header.pack(pady=(0, 20))
        
        # Configuration frame
        config_frame = ttk.LabelFrame(main_frame, text="Configuration", padding=10)
        config_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(config_frame, text="Behavior Profile:").grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
        self.behavior_profile = ttk.Combobox(config_frame, width=15, values=["Casual", "Engaged", "Binge"])
        self.behavior_profile.grid(row=3, column=1, padx=5, pady=5, sticky=tk.W)
        self.behavior_profile.set("Engaged")  # Default
        
        # URL
        ttk.Label(config_frame, text="YouTube Video URL:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.url_entry = ttk.Entry(config_frame, width=70)
        self.url_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W, columnspan=4)
        self.url_entry.insert(0, "https://youtu.be/_nuUT4xalos?si=UzDB5D6dhcz-av0Q")
        
        # View count
        ttk.Label(config_frame, text="Number of Views:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.view_entry = ttk.Entry(config_frame, width=10)
        self.view_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)
        
        # Concurrent instances
        ttk.Label(config_frame, text="Concurrent Instances (1-100):").grid(row=1, column=2, padx=20, pady=5, sticky=tk.W)
        self.concurrent_entry = ttk.Entry(config_frame, width=10)
        self.concurrent_entry.grid(row=1, column=3, padx=5, pady=5, sticky=tk.W)
        
        # Duration
        ttk.Label(config_frame, text="Video Duration (seconds):").grid(row=1, column=4, padx=20, pady=5, sticky=tk.W)
        self.duration_entry = ttk.Entry(config_frame, width=10)
        self.duration_entry.grid(row=1, column=5, padx=5, pady=5, sticky=tk.W)
        
        # Proxy option
        self.use_proxy = tk.BooleanVar(value=True)
        self.proxy_check = ttk.Checkbutton(
            config_frame, 
            text="Use Proxy Rotation", 
            variable=self.use_proxy
        )
        self.proxy_check.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        
        # Proxy file selection
        ttk.Label(config_frame, text="Proxy File:").grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)
        self.proxy_file_entry = ttk.Entry(config_frame, width=50)
        self.proxy_file_entry.grid(row=2, column=2, padx=5, pady=5, sticky=tk.W, columnspan=2)
        
        self.proxy_browse = ttk.Button(
            config_frame,
            text="Browse...",
            width=10,
            command=self.browse_proxy_file
        )
        self.proxy_browse.grid(row=2, column=4, padx=5, pady=5)
        
        # Proxy type
        ttk.Label(config_frame, text="Proxy Type:").grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
        self.proxy_type = ttk.Combobox(config_frame, width=10, values=["http", "socks5"])
        self.proxy_type.grid(row=3, column=1, padx=5, pady=5, sticky=tk.W)
        self.proxy_type.set("socks5")  # Default to SOCKS5
        
        # Evasion Mode
        ttk.Label(config_frame, text="Evasion Mode:").grid(row=3, column=4, padx=20, pady=5, sticky=tk.W)
        self.evasion_mode = ttk.Combobox(config_frame, values=["Stealth", "Aggressive", "Research"], width=12)
        self.evasion_mode.grid(row=3, column=5, padx=5, pady=5, sticky=tk.W)
        self.evasion_mode.set("Stealth")
        
        # Log display option
        self.show_log = tk.BooleanVar(value=True)
        self.log_check = ttk.Checkbutton(
            config_frame, 
            text="Show Live Log", 
            variable=self.show_log
        )
        self.log_check.grid(row=3, column=2, padx=5, pady=5, sticky=tk.W)
        
        # Control buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        self.start_button = ttk.Button(
            button_frame, 
            text="Start Simulation", 
            command=self.start_bot
        )
        self.start_button.pack(side=tk.LEFT, padx=5)
        
        self.stop_button = ttk.Button(
            button_frame, 
            text="Stop Simulation", 
            command=self.stop_bot,
            state=tk.DISABLED
        )
        self.stop_button.pack(side=tk.LEFT, padx=5)
        
        # Status frame
        status_frame = ttk.LabelFrame(main_frame, text="Status", padding=10)
        status_frame.pack(fill=tk.X, pady=5)
        
        # Progress bar
        self.progress = ttk.Progressbar(status_frame, orient=tk.HORIZONTAL, mode='determinate')
        self.progress.pack(fill=tk.X, pady=5)
        
        # Status grid
        status_grid = ttk.Frame(status_frame)
        status_grid.pack(fill=tk.X, pady=5)
        
        # Row 0
        ttk.Label(status_grid, text="Current View:").grid(row=0, column=0, padx=5, sticky=tk.W)
        self.current_view = ttk.Label(status_grid, text="0", style="Status.TLabel")
        self.current_view.grid(row=0, column=1, padx=5, sticky=tk.W)
        
        ttk.Label(status_grid, text="Total Views:").grid(row=0, column=2, padx=20, sticky=tk.W)
        self.total_views = ttk.Label(status_grid, text="0", style="Status.TLabel")
        self.total_views.grid(row=0, column=3, padx=5, sticky=tk.W)
        
        ttk.Label(status_grid, text="Active Instances:").grid(row=0, column=4, padx=20, sticky=tk.W)
        self.instance_info = ttk.Label(status_grid, text="0", style="Status.TLabel")
        self.instance_info.grid(row=0, column=5, padx=5, sticky=tk.W)
        
        # Row 1
        ttk.Label(status_grid, text="Compliant Views:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.compliant_info = ttk.Label(status_grid, text="0", style="Compliance.TLabel")
        self.compliant_info.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)
        
        ttk.Label(status_grid, text="Verified Views:").grid(row=1, column=2, padx=20, pady=5, sticky=tk.W)
        self.verified_info = ttk.Label(status_grid, text="0", style="Compliance.TLabel")
        self.verified_info.grid(row=1, column=3, padx=5, pady=5, sticky=tk.W)
        
        ttk.Label(status_grid, text="Video ID:").grid(row=1, column=4, padx=20, pady=5, sticky=tk.W)
        self.video_id_info = ttk.Label(status_grid, text="None", style="Status.TLabel")
        self.video_id_info.grid(row=1, column=5, padx=5, pady=5, sticky=tk.W)
        
        # Row 2
        ttk.Label(status_grid, text="Proxy:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        self.proxy_info = ttk.Label(status_grid, text="None", style="Status.TLabel")
        self.proxy_info.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)
        
        ttk.Label(status_grid, text="Fingerprint:").grid(row=2, column=2, padx=20, pady=5, sticky=tk.W)
        self.fingerprint_info = ttk.Label(status_grid, text="None", style="Status.TLabel")
        self.fingerprint_info.grid(row=2, column=3, padx=5, pady=5, sticky=tk.W)
        
        ttk.Label(status_grid, text="Location:").grid(row=2, column=4, padx=20, pady=5, sticky=tk.W)
        self.location_info = ttk.Label(status_grid, text="None", style="Status.TLabel")
        self.location_info.grid(row=2, column=5, padx=5, pady=5, sticky=tk.W)
        
        # Row 3 (Evasion metrics)
        ttk.Label(status_grid, text="Bypass Rate:").grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
        self.bypass_rate = ttk.Label(status_grid, text="92%", style="Compliance.TLabel")
        self.bypass_rate.grid(row=3, column=1, padx=5, pady=5, sticky=tk.W)
        
        ttk.Label(status_grid, text="Risk Level:").grid(row=3, column=2, padx=20, pady=5, sticky=tk.W)
        self.risk_level = ttk.Label(status_grid, text="Low", style="Compliance.TLabel")
        self.risk_level.grid(row=3, column=3, padx=5, pady=5, sticky=tk.W)
        
        ttk.Label(status_grid, text="Compliance:").grid(row=3, column=4, padx=20, pady=5, sticky=tk.W)
        self.compliance_status = ttk.Label(status_grid, text="Valid", style="Compliance.TLabel")
        self.compliance_status.grid(row=3, column=5, padx=5, pady=5, sticky=tk.W)
        
        # Status text
        self.status_text = ttk.Label(status_frame, text="Ready to start", style="Status.TLabel")
        self.status_text.pack(fill=tk.X, pady=5)
        
        # Log display
        log_frame = ttk.LabelFrame(main_frame, text="Log Output", padding=10)
        log_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.log_display = scrolledtext.ScrolledText(
            log_frame, 
            wrap=tk.WORD, 
            font=("Consolas", 9),
            height=15
        )
        self.log_display.pack(fill=tk.BOTH, expand=True)
        self.log_display.config(state=tk.DISABLED)
        
        # Compliance notes
        notes_frame = ttk.Frame(main_frame)
        notes_frame.pack(fill=tk.X, pady=5)
        
        compliance_note = ttk.Label(
            notes_frame, 
            text="Academic Compliance: Views counted only when >70% watched with human-like behavior patterns",
            style="Warning.TLabel"
        )
        compliance_note.pack(side=tk.LEFT)
        
        # Redirect stdout to log display
        sys.stdout = self

    def load_config(self):
        """Load configuration settings from JSON file"""
        # Default configuration
        default_config = {
            "max_views": 100,
            "concurrent_instances": 5,
            "view_duration": 60,
            "use_proxy": True,
            "proxy_file": "C:/Users/edwar/source/repos/YT_VIEWS/JDBOT/resources/ips-usjb.txt",
            "show_log": True
        }
        
        # Try to load config file
        try:
            if os.path.exists("config.json"):
                with open("config.json", "r") as f:
                    config_data = json.load(f)
            else:
                config_data = default_config
        except:
            config_data = default_config
        
        # Set GUI fields with loaded values
        self.view_entry.insert(0, str(config_data.get("max_views", 100)))
        self.concurrent_entry.insert(0, str(config_data.get("concurrent_instances", 5)))
        self.duration_entry.insert(0, str(config_data.get("view_duration", 60)))
        self.use_proxy.set(config_data.get("use_proxy", True))
        self.proxy_file_entry.insert(0, config_data.get("proxy_file", "C:/Users/edwar/source/repos/YT_VIEWS/JDBOT/resources/ips-usjb.txt"))
        self.show_log.set(config_data.get("show_log", True))

    def browse_proxy_file(self):
        """Open file dialog to select proxy file"""
        filepath = filedialog.askopenfilename(
            title="Select Proxy File",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if filepath:
            self.proxy_file_entry.delete(0, tk.END)
            self.proxy_file_entry.insert(0, filepath)
            # Auto-detect proxy type from filename if possible
        if "socks" in filepath.lower():
            self.proxy_type.set("socks5")

    def start_bot(self):
        
        behavior_profile = self.behavior_profile.get()
        """Start the view bot"""
        if not self.running:
            try:
                # Get parameters from GUI
                video_url = self.url_entry.get()
                max_views = int(self.view_entry.get())
                concurrent = int(self.concurrent_entry.get())
                duration = int(self.duration_entry.get())
                use_proxy = self.use_proxy.get()
                show_log = self.show_log.get()
                proxy_file = self.proxy_file_entry.get() if use_proxy else None
                proxy_type = self.proxy_type.get()

                # Validate inputs
                if max_views <= 0:
                    raise ValueError("Number of views must be positive")
                if concurrent <= 0:
                    raise ValueError("Concurrent instances must be positive")
                if duration <= 0:
                    raise ValueError("Duration must be positive")
                if use_proxy and not os.path.exists(proxy_file):
                    raise ValueError(f"Proxy file not found: {proxy_file}")
                
                # Create and configure bot instance
                self.bot = YouTubeViewBot(
                    video_url=video_url,
                    max_views=max_views,
                    concurrent_instances=concurrent,
                    view_duration=duration,
                    use_proxy=use_proxy,
                    proxy_file=proxy_file,
                    proxy_type=proxy_type,
                    update_callback=self.update_gui
                )
                
                # Start the bot in a new thread
                self.running = True
                import threading
                threading.Thread(
                    target=self.bot.run,
                    args=(video_url, max_views, duration, use_proxy, show_log),
                    daemon=True
                ).start()
                
                # Update UI
                self.start_button.config(state=tk.DISABLED)
                self.stop_button.config(state=tk.NORMAL)
                self.status_text.config(text="Running...")
                self.progress.config(maximum=max_views)
                
            except ValueError as e:
                messagebox.showerror("Input Error", f"Invalid input: {str(e)}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to start bot: {str(e)}")

    def stop_bot(self):
        """Stop the bot if running"""
        if self.running and self.bot:
            self.bot.stop()
            self.running = False
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)
            self.status_text.config(text="Stopped by user")

    def update_gui(self, data):
        """Update GUI elements from bot thread"""
        try:
            self.root.after(0, self._update_gui_safe, data)
        except Exception as e:
            self.logger.error(f"GUI update failed: {str(e)}")
        
    def _update_gui_safe(self, data):
        """Thread-safe GUI update"""
        if 'bypass_rate' in data:
            self.bypass_rate.config(text=f"{data['bypass_rate']}%")
            
        if 'risk_level' in data:
            risk_text = data['risk_level']
            self.risk_level.config(text=risk_text)
            if "High" in risk_text:
                self.risk_level.config(foreground="red")
            elif "Medium" in risk_text:
                self.risk_level.config(foreground="orange")
            else:
                self.risk_level.config(foreground="green")
                
        if 'view' in data and 'total' in data:
            self.current_view.config(text=f"{data['view']}")
            self.total_views.config(text=f"{data['total']}")
            self.progress["value"] = data['view']
            
        if 'status' in data:
            self.status_text.config(text=data['status'])
            
        if 'proxy' in data:
            self.proxy_info.config(text=data['proxy'])
            
        if 'fingerprint' in data:
            self.fingerprint_info.config(text=data['fingerprint'])
            
        if 'location' in data:
            self.location_info.config(text=data['location'])
            
        if 'video_id' in data:
            self.video_id_info.config(text=data['video_id'])
            
        if 'compliant' in data:
            self.compliant_info.config(text=f"{data['compliant']}")
            
        if 'verified' in data:
            self.verified_info.config(text=f"{data['verified']}")
            
        if 'instance' in data:
            self.instance_info.config(text=f"{data['instance']}")
            
        if 'completed' in data:
            self.running = False
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)
            self.status_text.config(text="Simulation completed")
            
    def save_settings(self):
        """Save current GUI settings to JSON file"""
        config_data = {
            "max_views": int(self.view_entry.get()),
            "concurrent_instances": int(self.concurrent_entry.get()),
            "view_duration": int(self.duration_entry.get()),
            "use_proxy": self.use_proxy.get(),
            "proxy_file": self.proxy_file_entry.get(),
            "show_log": self.show_log.get()
        }
        
        try:
            with open("config.json", "w") as f:
                json.dump(config_data, f, indent=4)
        except Exception as e:
            print(f"Error saving config: {str(e)}")
        
    def on_closing(self):
        """Handle window closing event"""
        if self.running:
            if messagebox.askokcancel("Quit", "Bot is still running. Stop it and quit?"):
                self.stop_bot()
                self.save_settings()
                self.root.destroy()
        else:
            self.save_settings()
            self.root.destroy()
        sys.stdout = self.original_stdout
        

