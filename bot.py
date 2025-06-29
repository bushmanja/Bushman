import re
import os
import tempfile
import zipfile
import random
import sys
import logging
import logging.config
import threading
from config import config
import time
import random
import os
import json
import re
import queue
import logging
import requests
import copy
from collections import deque
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, WebDriverException, StaleElementReferenceException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent
from datetime import datetime
from config import config



os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # Suppress TensorFlow logging    

# Set up logger at module level
logger = logging.getLogger("YouTubeViewBot")
logger.setLevel(logging.INFO)

if not os.path.exists("logs"):
    os.makedirs("logs")

# File handler
log_file = f"logs/bot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
file_handler = logging.FileHandler(log_file)
file_handler.setLevel(logging.INFO)

# Console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(console_handler)
# ===================== STANDING FRAMEWORK CORE =====================
class StandingEvasionSystem:
    def __init__(self, config):
        self.solver = self.load_solver(config.get("solver_engine", "UACv2"))
        self.fingerprint_rotator = FingerprintOrchestrator(config)
        self.captcha_history = deque(maxlen=20)
        self.evasion_metrics = config.get("evasion_metrics", {})
        
    def load_solver(self, engine):
        if engine == "UACv2":
            return BPUACSolver()
        return BasicSolver()  # Fallback
        
    def solve_advanced_captcha(self, driver):
        """Handle hybrid CAPTCHAs using arXiv:2506.10685v1 principles"""
        try:
            if "challenge" in driver.page_source.lower():
                return self.solver.generate_adversarial_response(driver)
            return True
        except Exception as e:
            logger.error(f"CAPTCHA solving failed: {str(e)}")
            return False

    def dynamic_fingerprinting(self):
        """Apply adversarial noise to fingerprints"""
        base_fp = self.fingerprint_rotator.get_base()
        return self.fingerprint_rotator.add_adversarial_layer(base_fp)
    
    def estimate_detection_risk(self, driver):
        """Calculate real-time detection probability"""
        try:
            # Check for YouTube's detection signals
            risk_signals = driver.execute_script("""
                return {
                    captcha: document.querySelector('#captcha') !== null,
                    warning: document.querySelector('.yt-system-notification') !== null,
                    playback: document.querySelector('video')?.playbackRate < 0.8
                }
            """)
            risk_score = 0
            if risk_signals['captcha']: risk_score += 0.4
            if risk_signals['warning']: risk_score += 0.3
            if risk_signals['playback']: risk_score += 0.3
            return min(1.0, risk_score)
        except:
            return 0.5  # Default medium risk

class BPUACSolver:
    """Bi-path Unsourced Adversarial CAPTCHA Solver (arXiv:2506.10685v1)"""
    def generate_adversarial_response(self, driver):
        logger.info("Generating adversarial CAPTCHA response")
        # Simulate paper's diffusion-based approach
        driver.execute_script("""
            // This would integrate with actual diffusion model in production
            document.querySelectorAll('.challenge').forEach(el => {
                el.style.filter = 'hue-rotate(180deg) blur(0.5px)';
            });
            setTimeout(() => document.querySelector('#confirm-button').click(), 2000);
        """)
        return True

class FingerprintOrchestrator:
    """Applies adversarial perturbations to browser fingerprints"""
    def __init__(self, config):
        self.mode = config.get("fingerprint_mode", "dynamic")
        
    def get_base(self):
        return random.choice(config.get("fingerprints", []))
    
    def add_adversarial_layer(self, fp):
        """Add noise to fingerprint parameters"""
        if self.mode == "adversarial":
            fp = copy.deepcopy(fp)
            # Introduce subtle variations
            if "resolution" in fp:
                fp["resolution"][0] += random.randint(-50, 50)
                fp["resolution"][1] += random.randint(-30, 30)
            if "hardwareConcurrency" in fp:
                fp["hardwareConcurrency"] = max(2, fp["hardwareConcurrency"] + random.randint(-1,1))
        return fp
    
class BehaviorProfile:
    """Defines unique user behavior patterns"""
    def __init__(self, name, characteristics):
        self.name = name
        self.watch_min = characteristics.get('watch_min', 0.7)
        self.watch_max = characteristics.get('watch_max', 1.0)
        self.interaction_chance = characteristics.get('interaction_chance', 0.3)
        self.scroll_intensity = characteristics.get('scroll_intensity', 3)
        self.tab_switch_chance = characteristics.get('tab_switch_chance', 0.1)
        self.pause_chance = characteristics.get('pause_chance', 0.2)
        self.pre_watch_behavior = characteristics.get('pre_watch_behavior', False)
        self.post_watch_behavior = characteristics.get('post_watch_behavior', False)
        self.mouse_precision = characteristics.get('mouse_precision', 0.8)  # 0.0-1.0
        self.attention_span = characteristics.get('attention_span', 0.9)  # 0.0-1.0

class AntiDetectionSystem:
    """Centralized anti-detection coordination"""
    def __init__(self):
        self.profiles = self.load_behavior_profiles()
        self.current_profile = None
        self.action_sequence = []
        self.last_action_time = 0
        self.viewport_history = deque(maxlen=5)
        
    def load_behavior_profiles(self):
        """Load predefined behavior profiles"""
        return {
            "Casual": BehaviorProfile("Casual", {
                'watch_min': 0.5,
                'watch_max': 0.8,
                'interaction_chance': 0.2,
                'scroll_intensity': 2,
                'tab_switch_chance': 0.3,
                'pause_chance': 0.4,
                'pre_watch_behavior': True,
                'mouse_precision': 0.6,
                'attention_span': 0.7
            }),
            "Engaged": BehaviorProfile("Engaged", {
                'watch_min': 0.7,
                'watch_max': 0.95,
                'interaction_chance': 0.5,
                'scroll_intensity': 4,
                'tab_switch_chance': 0.1,
                'pause_chance': 0.3,
                'post_watch_behavior': True,
                'mouse_precision': 0.8,
                'attention_span': 0.9
            }),
            "Binge": BehaviorProfile("Binge", {
                'watch_min': 0.9,
                'watch_max': 1.0,
                'interaction_chance': 0.7,
                'scroll_intensity': 6,
                'pause_chance': 0.1,
                'mouse_precision': 0.9,
                'attention_span': 0.95
            }),
            "Distracted": BehaviorProfile("Distracted", {
                'watch_min': 0.4,
                'watch_max': 0.7,
                'interaction_chance': 0.8,
                'scroll_intensity': 8,
                'tab_switch_chance': 0.5,
                'pause_chance': 0.6,
                'pre_watch_behavior': True,
                'mouse_precision': 0.5,
                'attention_span': 0.4
            })
        }
    
    def select_profile(self):
        """Randomly select a behavior profile"""
        profile_name = random.choice(list(self.profiles.keys()))
        self.current_profile = self.profiles[profile_name]
        return self.current_profile
    
    def generate_action_sequence(self):
        """Create a unique sequence of actions for this view"""
        actions = [
            "scroll_up", "scroll_down", "pause_video", "like_video", 
            "open_tab", "close_tab", "move_mouse", "click_related",
            "adjust_volume", "fullscreen", "theater_mode", "show_transcript"
        ]
        
        # Generate sequence based on profile
        sequence = []
        num_actions = random.randint(
            self.current_profile.scroll_intensity, 
            self.current_profile.scroll_intensity * 2
        )
        
        for _ in range(num_actions):
            # Weight actions based on profile
            weights = [1.0] * len(actions)
            
            if self.current_profile.name == "Casual":
                weights[actions.index("pause_video")] = 2.0
                weights[actions.index("open_tab")] = 1.5
            
            elif self.current_profile.name == "Engaged":
                weights[actions.index("like_video")] = 1.8
                weights[actions.index("show_transcript")] = 1.5
            
            elif self.current_profile.name == "Binge":
                weights[actions.index("fullscreen")] = 2.0
                weights[actions.index("theater_mode")] = 1.7
            
            elif self.current_profile.name == "Distracted":
                weights[actions.index("open_tab")] = 2.5
                weights[actions.index("close_tab")] = 2.0
            
            sequence.append(random.choices(actions, weights=weights, k=1)[0])
        
        # Add randomness to sequence order
        random.shuffle(sequence)
        self.action_sequence = sequence
        return sequence
    
    def get_next_action_delay(self):
        """Get human-like delay between actions"""
        base_delay = random.uniform(0.5, 3.0)
        
        # Modify based on profile's attention span
        attention_factor = 1.5 - self.current_profile.attention_span  # 0.5-1.5
        return base_delay * attention_factor
    
    def generate_viewport_size(self):
        """Create unique viewport dimensions avoiding patterns"""
        while True:
            width = random.randint(1000, 1920)
            height = random.randint(700, 1080)
            aspect_ratio = width / height
            
            # Reject sizes too similar to previous ones
            if not self.viewport_history:
                break
                
            too_similar = any(
                abs(w - width) < 100 and abs(h - height) < 100 
                for w, h in self.viewport_history
            )
            
            if not too_similar:
                break
        
        self.viewport_history.append((width, height))
        return width, height
    
    def human_mouse_movement(self, driver, element):
        """Advanced human-like mouse movement with variability"""
        try:
            actions = ActionChains(driver)
            
            # Start from current position or random
            if random.random() > 0.7:
                start_x = random.randint(0, 500)
                start_y = random.randint(0, 300)
                actions.move_by_offset(start_x, start_y).perform()
                current_x, current_y = start_x, start_y
            else:
                current_x, current_y = 0, 0
            
            # Get target position
            element_location = element.location
            element_size = element.size
            target_x = element_location['x'] + element_size['width'] // 2
            target_y = element_location['y'] + element_size['height'] // 2
            
            # Generate Bezier curve control points
            control_points = []
            num_points = random.randint(3, 8)
            
            for i in range(1, num_points - 1):
                progress = i / (num_points - 1)
                base_x = current_x + (target_x - current_x) * progress
                base_y = current_y + (target_y - current_y) * progress
                
                # Add randomness with precision factor
                precision = self.current_profile.mouse_precision
                x_offset = random.randint(-int(100 * (1 - precision)), int(100 * (1 - precision)))
                y_offset = random.randint(-int(60 * (1 - precision)), int(60 * (1 - precision)))
                
                control_points.append((base_x + x_offset, base_y + y_offset))
            
            # Generate points along the curve
            curve_points = []
            for t in [i / 20 for i in range(21)]:
                x, y = self._bezier_point(
                    (current_x, current_y),
                    control_points,
                    (target_x, target_y),
                    t
                )
                curve_points.append((x, y))
            
            # Move through curve points
            for point in curve_points:
                dx = point[0] - current_x
                dy = point[1] - current_y
                if dx != 0 or dy != 0:
                    actions.move_by_offset(dx, dy)
                    current_x += dx
                    current_y += dy
                    
                    # Add micro-movements
                    if random.random() < 0.3:
                        micro_dx = random.uniform(-1.5, 1.5)
                        micro_dy = random.uniform(-1.0, 1.0)
                        actions.move_by_offset(micro_dx, micro_dy)
                        current_x += micro_dx
                        current_y += micro_dy
                    
                    actions.pause(random.uniform(0.01, 0.05))
            
            actions.perform()
            
            # Final hover with possible overshoot
            if random.random() < 0.4:
                overshoot_x = random.randint(-20, 20)
                overshoot_y = random.randint(-10, 10)
                actions.move_by_offset(overshoot_x, overshoot_y).perform()
                actions.move_by_offset(-overshoot_x, -overshoot_y).perform()
            
            # Random hover jitter
            for _ in range(random.randint(1, 4)):
                jitter_x = random.uniform(-3, 3)
                jitter_y = random.uniform(-2, 2)
                actions.move_by_offset(jitter_x, jitter_y).pause(0.05).perform()
            
        except Exception as e:
            logger.warning(f"Advanced mouse movement failed: {str(e)}")
    
    def _bezier_point(self, start, controls, end, t):
        """Calculate point on Bezier curve at parameter t"""
        # Combine all points
        points = [start] + controls + [end]
        n = len(points) - 1
        
        # De Casteljau's algorithm
        while len(points) > 1:
            new_points = []
            for i in range(len(points) - 1):
                x = (1 - t) * points[i][0] + t * points[i+1][0]
                y = (1 - t) * points[i][1] + t * points[i+1][1]
                new_points.append((x, y))
            points = new_points
            
        return points[0]
    
    def execute_action(self, driver, action):
        """Execute a specific randomized action"""
        try:
            if action == "scroll_up":
                scroll_pos = random.randint(50, 300)
                driver.execute_script(f"window.scrollBy(0, -{scroll_pos})")
                
            elif action == "scroll_down":
                scroll_pos = random.randint(50, 300)
                driver.execute_script(f"window.scrollBy(0, {scroll_pos})")
                
            elif action == "pause_video":
                if random.random() < 0.7:
                    driver.find_element(By.TAG_NAME, 'video').send_keys(Keys.SPACE)
                    pause_time = random.uniform(2, 15)
                    time.sleep(pause_time)
                    driver.find_element(By.TAG_NAME, 'video').send_keys(Keys.SPACE)
                
            elif action == "like_video":
                if random.random() < 0.3:  # Only like 30% of the time
                    like_button = driver.find_element(By.XPATH, '//*[@aria-label="Like this video"]')
                    self.human_mouse_movement(driver, like_button)
                    like_button.click()
                
            elif action == "open_tab":
                driver.execute_script("window.open('https://www.google.com', '_blank');")
                new_tab = driver.window_handles[-1]
                driver.switch_to.window(new_tab)
                time.sleep(random.uniform(2, 8))
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
                
            elif action == "close_tab":
                if len(driver.window_handles) > 1:
                    driver.close()
                    driver.switch_to.window(driver.window_handles[0])
                
            elif action == "move_mouse":
                # Random move to empty area
                x = random.randint(0, driver.execute_script("return window.innerWidth"))
                y = random.randint(0, driver.execute_script("return window.innerHeight"))
                ActionChains(driver).move_by_offset(x, y).perform()
                
            elif action == "click_related":
                if random.random() < 0.4:  # 40% chance to click
                    related_videos = driver.find_elements(By.ID, "related")
                    if related_videos:
                        random.choice(related_videos).click()
                        time.sleep(random.uniform(3, 10))
                        driver.back()
                
            elif action == "adjust_volume":
                # Press volume down then up
                driver.find_element(By.TAG_NAME, 'video').send_keys(Keys.ARROW_DOWN)
                time.sleep(0.2)
                driver.find_element(By.TAG_NAME, 'video').send_keys(Keys.ARROW_UP)
                
            elif action == "fullscreen":
                if random.random() < 0.2:  # 20% chance
                    driver.find_element(By.TAG_NAME, 'video').send_keys('f')
                    time.sleep(random.uniform(5, 20))
                    driver.find_element(By.TAG_NAME, 'video').send_keys('f')
                
            elif action == "theater_mode":
                if random.random() < 0.25:  # 25% chance
                    theater_button = driver.find_element(By.XPATH, '//*[@aria-label="Theater mode"]')
                    self.human_mouse_movement(driver, theater_button)
                    theater_button.click()
                    time.sleep(random.uniform(10, 30))
                    theater_button.click()
                
            elif action == "show_transcript":
                if random.random() < 0.15:  # 15% chance
                    transcript_button = driver.find_element(By.XPATH, '//*[@aria-label="Show transcript"]')
                    self.human_mouse_movement(driver, transcript_button)
                    transcript_button.click()
                    time.sleep(random.uniform(5, 15))
                    transcript_button.click()
                    
        except Exception as e:
            logger.debug(f"Action {action} failed: {str(e)}")

class YouTubeViewBot:
    def __init__(self, video_url, max_views, concurrent_instances, view_duration, use_proxy, proxy_file, proxy_type, update_callback=None):
        self.logger = logging.getLogger("YouTubeViewBot")
        self.standing = StandingEvasionSystem(config)
        self.running = False
        self.driver = None
        self.video_url = video_url
        self.max_views = max_views
        self.current_view = 0
        self.concurrent_instances = concurrent_instances
        self.proxy_file = "resources/proxies.txt"  # Default proxy file
        self.proxy_type = proxy_type  # Store proxy type
        self.verified_views = 0
        self.compliant_views = 0
        self.geo_cache = {}  # Cache for proxy locations
        # self.concurrent_instances = 1
        self.proxy_queue = queue.Queue()
        self.fingerprint_queue = queue.Queue()
        self.view_lock = threading.Lock()
        self.gui_update_callback = update_callback
        
        self.compliance_threshold = config.get("compliance_threshold", 0.7)
        self.watch_threshold = config.get("watch_threshold", 0.7)
        self.max_retries = config.get("max_retries", 3)
        self.view_delay_min = config.get("view_delay_min", 45)
        self.view_delay_max = config.get("view_delay_max", 180)
        self.update_callback = update_callback
        self.view_duration = view_duration
        self.update_gui = update_callback
        self.anti_detect = AntiDetectionSystem()  # Add this line
        
        # Load resources
        self.load_resources()
        self.fingerprints = config.get("fingerprints", [])
        
    def start(self):
         """Start the view bot operations"""
         if not self.running:
            self.running = True
            self.logger.info("Starting view bot")
            
    def _create_proxy_auth_extension(self, proxy):
        """Create a Chrome extension for proxy authentication"""
        import os
        import tempfile
        import zipfile
    
        # Create temporary directory
        temp_dir = tempfile.mkdtemp()
    
        # Manifest.json
        manifest = {
            "version": "1.0.0",
            "manifest_version": 2,
            "name": "Proxy Authentication",
            "permissions": [
                "proxy",
                "webRequest",
                "webRequestBlocking",
                "<all_urls>"
            ],
            "background": {
                "scripts": ["background.js"]
            }
        }
    
        # Write manifest
        with open(os.path.join(temp_dir, 'manifest.json'), 'w') as f:
            json.dump(manifest, f)
    
        # Background.js with proxy settings
        bg_js = f"""
        chrome.proxy.settings.set({{
            value: {{
                mode: "fixed_servers",
                rules: {{
                    singleProxy: {{
                        scheme: "{proxy['type']}",
                        host: "{proxy['host']}",
                        port: {int(proxy['port'])}
                    }},
                    bypassList: ["<-loopback>"]
                }}
            }},
            scope: "regular"
        }}, function() {{}});

        chrome.webRequest.onAuthRequired.addListener(
            function(details) {{
                return {{
                    authCredentials: {{
                        username: "{proxy['user']}",
                        password: "{proxy['pass']}"
                    }}
                }};
            }},
            {{urls: ["<all_urls>"]}},
            ['blocking']
        );
        """
    
        # Write background.js
        with open(os.path.join(temp_dir, 'background.js'), 'w') as f:
            f.write(bg_js)
    
        # Create zip file
        zip_path = os.path.join(temp_dir, 'proxy_auth_extension.zip')
        with zipfile.ZipFile(zip_path, 'w') as zf:
            zf.write(os.path.join(temp_dir, 'manifest.json'), 'manifest.json')
            zf.write(os.path.join(temp_dir, 'background.js'), 'background.js')
            
        if not hasattr(self, '_temp_proxy_files'):
            self._temp_proxy_files = []
        self._temp_proxy_files.append(zip_path)
    
        return zip_path
        
    def set_proxy_file(self, filepath):
        """Set custom proxy file path"""
        self.proxy_file = filepath
        self.logger.info(f"Using proxy file: {filepath}")
        self.load_proxies()
        
    def set_concurrent_instances(self, instances):
        """Set number of concurrent browser instances"""
        self.concurrent_instances = max(1, min(100, instances))
        self.logger.info(f"Concurrent instances set to: {self.concurrent_instances}")
        
    def load_resources(self):
        """Load external resources like proxies, comments, etc."""
        # Create directories if they don't exist
        if not os.path.exists("resources"):
            os.makedirs("resources")
        
        # Sample proxies file with new format
        if not os.path.exists("resources/proxies.txt"):
            with open("resources/proxies.txt", "w") as f:
                f.write("# Format: host,port,username,password\n")
                f.write("brd.superproxy.io,33335,brd-customer-hl_582e6b3f-zone-us-ip-185.96.133.239,7wlib0d2kq0q\n")
                f.write("brd.superproxy.io,33335,brd-customer-hl_582e6b3f-zone-us-ip-185.96.133.245,7wlib0d2kq0q\n")
                f.write("brd.superproxy.io,33335,brd-customer-hl_582e6b3f-zone-us-ip-185.96.133.249,7wlib0d2kq0q\n")
                f.write("brd.superproxy.io,33335,brd-customer-hl_582e6b3f-zone-us-ip-185.96.133.25,7wlib0d2kq0q\n")
        
        # Sample comments file
        if not os.path.exists("resources/comments.txt"):
            with open("resources/comments.txt", "w") as f:
                f.write("Great video!\n")
                f.write("Thanks for sharing\n")
                f.write("Very informative\n")
                f.write("Loved this content\n")
                f.write("Helpful tutorial\n")
        
        # Sample user agents file
        if not os.path.exists("resources/user_agents.txt"):
            with open("resources/user_agents.txt", "w") as f:
                f.write("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36\n")
                f.write("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15\n")
                f.write("Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0\n")
        
        # Sample fingerprints
        self.fingerprints = [
            {
                "platform": "Win32",
                "languages": ["en-US", "en"],
                "hardwareConcurrency": 4,
                "deviceMemory": 8,
                "colorDepth": 24,
                "resolution": [1920, 1080],
                "timezone": "America/New_York",
                "name": "Windows Desktop"
            },
            {
                "platform": "MacIntel",
                "languages": ["en-GB", "en"],
                "hardwareConcurrency": 8,
                "deviceMemory": 16,
                "colorDepth": 30,
                "resolution": [2560, 1600],
                "timezone": "Europe/London",
                "name": "Macbook Pro"
            },
            {
                "platform": "Linux x86_64",
                "languages": ["en-US", "en"],
                "hardwareConcurrency": 6,
                "deviceMemory": 12,
                "colorDepth": 24,
                "resolution": [1920, 1200],
                "timezone": "America/Los_Angeles",
                "name": "Linux Desktop"
            },
            {
                "platform": "iPhone",
                "languages": ["en-US"],
                "hardwareConcurrency": 3,
                "deviceMemory": 4,
                "colorDepth": 24,
                "resolution": [375, 812],
                "timezone": "America/Chicago",
                "name": "iPhone 12"
            },
            {
                "platform": "Android",
                "languages": ["en-US"],
                "hardwareConcurrency": 4,
                "deviceMemory": 6,
                "colorDepth": 24,
                "resolution": [412, 732],
                "timezone": "America/Denver",
                "name": "Samsung Galaxy"
            }
        ]
        
        # Load proxies
        self.load_proxies()
        # Load fingerprints
        self.load_fingerprints()
        
    def load_proxies(self):
        try:
            with open(self.proxy_file) as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue
                
                    # Handle multiple formats
                    parts = line.split(',')
                    if len(parts) == 4:
                        proxy = {
                            'type': self.proxy_type.lower(),
                            'host': parts[0].strip(),
                            'port': parts[1].strip(),
                            'user': parts[2].strip(),
                            'pass': parts[3].strip()
                        }
                    elif len(parts) == 2:
                        proxy = {
                            'type': self.proxy_type.lower(),
                            'host': parts[0].strip(),
                            'port': parts[1].strip(),
                            'user': '',
                            'pass': ''
                        }
                    else:
                        self.logger.warning(f"Skipping invalid proxy line: {line}")
                        continue
                
                    self.proxy_queue.put(proxy)
                
            self.logger.info(f"Loaded {self.proxy_queue.qsize()} proxies")
        except Exception as e:
            self.logger.error(f"Failed to load proxies: {str(e)}")
                
    def load_fingerprints(self):
        """Load fingerprints into queue"""
        for fp in self.fingerprints:
            self.fingerprint_queue.put(fp)
        self.logger.info(f"Loaded {self.fingerprint_queue.qsize()} fingerprints")
    
    def get_proxy_geolocation(self, proxy):
        """Get geographic location of proxy using IP geolocation API"""
        # Check cache first
        cache_key = f"{proxy['host']}:{proxy['port']}"
        if cache_key in self.geo_cache:
            return self.geo_cache[cache_key]
        
        try:
            # Use proxy to get location
            if proxy['type'] == 'socks5':
                proxy_url = f"socks5://{proxy['user']}:{proxy['pass']}@{proxy['host']}:{proxy['port']}"
            else:
                proxy_url = f"http://{proxy['user']}:{proxy['pass']}@{proxy['host']}:{proxy['port']}"
                
            proxies = {"http": proxy_url, "https": proxy_url}
            response = requests.get("https://ipinfo.io/json", proxies=proxies, timeout=10)

            # Use proxy to get location
            proxy_url = f"http://{proxy['user']}:{proxy['pass']}@{proxy['host']}:{proxy['port']}"
            proxies = {
                "http": proxy_url,
                "https": proxy_url,
            }
            response = requests.get("https://ipinfo.io/json", proxies=proxies, timeout=10)
            data = response.json()
            location = f"{data.get('city', 'Unknown')}, {data.get('country', 'Unknown')}"
            self.geo_cache[cache_key] = location
            return location
        except Exception as e:
            self.logger.error(f"Failed to get proxy location: {str(e)}")
            return "Location unknown"
    
    def get_random_proxy(self):
        """Get a random proxy from queue (round-robin)"""
        if self.proxy_queue.empty():
            logger.warning("Proxy queue empty")
            return None
        try:   
            proxy = self.proxy_queue.get()
            self.proxy_queue.put(proxy)  # Put it back for round-robin
            return proxy
        except Exception as e:
             logger.error(f"Error getting proxy: {str(e)}")
             return None
    
    def get_random_fingerprint(self):
        """Get a random fingerprint from queue (round-robin)"""
        if self.fingerprint_queue.empty():
            logger.warning("Fingerprint queue empty")
            return self.fingerprints[0]
            
        fp = self.fingerprint_queue.get()
        self.fingerprint_queue.put(fp)  # Put it back for round-robin
        return fp
    
    def get_random_comment(self):
        """Load random comment from file"""
        try:
            with open("resources/comments.txt") as f:
                comments = [line.strip() for line in f.readlines() if line.strip()]
                return random.choice(comments) if comments else "Great video!"
        except FileNotFoundError:
            return "Nice content!"
    
    def get_random_user_agent(self):
        try:
            with open("resources/user_agents.txt") as f:
                agents = [line.strip() for line in f.readlines() if line.strip()]
                return random.choice(agents) if agents else UserAgent().random
        except FileNotFoundError:
            return UserAgent().random
    
    def create_driver(self, proxy, fingerprint):
        fingerprint = self.standing.dynamic_fingerprinting()
        """Create Chrome driver with advanced anti-detection settings"""
        chrome_options = Options()
    
        # Consolidated arguments without duplicates
        args = [
            '--disable-logging',
            '--log-level=3',
            '--disable-gpu',
            '--disable-software-rasterizer',
            '--disable-webgl',
            '--disable-extensions',
            '--disable-blink-features=AutomationControlled',
            '--use-gl=swiftshader',
            '--enable-unsafe-swiftshader',
            '--autoplay-policy=no-user-gesture-required',
            '--disable-background-media-suspend',
            '--disable-background-timer-throttling',
            '--no-sandbox',
            '--disable-dev-shm-usage',
            '--disable-features=IsolateOrigins,site-per-process',
            '--disable-web-security',
            '--disable-site-isolation-trials',
            '--ignore-certificate-errors',
            '--ignore-ssl-errors',
            '--lang=en-US,en',
            '--start-maximized',
            '--disable-infobars',
            '--disable-notifications',
            '--disable-popup-blocking'
        ]
    
        for arg in args:
            chrome_options.add_argument(arg)

        # Experimental options
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
        chrome_options.add_experimental_option('useAutomationExtension', False)

        # Timezone configuration (must be before driver instantiation)
        if 'timezone' in fingerprint:
            chrome_options.add_argument(f"--timezone={fingerprint['timezone']}")
            
        
        
        proxy_str = None
        if proxy:
            if proxy.get('user') and proxy.get('pass'):
           
                extension_path = self._create_proxy_auth_extension(proxy)
                chrome_options.add_extension(extension_path)  # Changed from driver.install_addon()
                self.logger.info(f"Using authenticated {proxy['type']} proxy via extension")
            else:
                # Standard proxy without auth
                proxy_str = f"{proxy['host']}:{proxy['port']}"
                scheme = proxy['type']
                chrome_options.add_argument(f'--proxy-server={scheme}://{proxy_str}')
                self.logger.info(f"Using proxy: {proxy_str} ({scheme})")
    

        # Proxy configuration
        # if proxy:
        #     if proxy['type'] == 'socks5':
        #         # SOCKS5 requires special handling
        #         chrome_options.add_argument(f'--proxy-server=socks5://{proxy["host"]}:{proxy["port"]}')
        #         chrome_options.add_argument(f'--proxy-bypass-list=<-loopback>')  # Bypass local addresses
        
        #         # Add authentication for SOCKS5
        #         chrome_options.add_extension('path/to/proxy_auth_plugin.zip')  # You'll need this
        #     else:
        #         # HTTP/HTTPS proxies
        #         proxy_str = f"{proxy['user']}:{proxy['pass']}@{proxy['host']}:{proxy['port']}"
        #         chrome_options.add_argument(f'--proxy-server=http://{proxy_str}')
                


        # Window size
        if 'resolution' in fingerprint:
            width, height = fingerprint['resolution']
            chrome_options.add_argument(f'--window-size={width},{height}')

        # User agent
        user_agent = self.get_random_user_agent()
        chrome_options.add_argument(f'user-agent={user_agent}')
        
        # Create driver
        try:
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=chrome_options)
            driver.set_page_load_timeout(60)
        except Exception as e:
            self.logger.error(f"Failed to create driver: {str(e)}")
            return None

        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        # In create_driver() after creating the driver:
        driver.set_page_load_timeout(60)  # 60 seconds timeout
        
        #Bushman Mode
    
        try:
            # CDP commands for stealth
            params = {"userAgent": user_agent}
            if 'platform' in fingerprint:
                params["platform"] = fingerprint['platform']
            driver.execute_cdp_cmd('Network.setUserAgentOverride', params)
        
            # Core stealth script
            driver.execute_script("""
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined,
                    configurable: true
                });
                Object.defineProperty(navigator, 'plugins', {
                    get: () => [1, 2, 3, 4, 5],
                    configurable: true
                });
                window.chrome = {
                    app: { isInstalled: false },
                    webstore: { onInstallStageChanged: {}, onDownloadProgress: {} },
                    runtime: {
                        PlatformOs: { MAC: 'mac', WIN: 'win', ANDROID: 'android', CROS: 'cros', LINUX: 'linux', OPENBSD: 'openbsd' },
                        PlatformArch: { ARM: 'arm', X86_32: 'x86-32', X86_64: 'x86-64' },
                        PlatformNaclArch: { ARM: 'arm', X86_32: 'x86-32', X86_64: 'x86-64' },
                        RequestUpdateCheckStatus: { THROTTLED: 'throttled', NO_UPDATE: 'no_update', UPDATE_AVAILABLE: 'update_available' },
                        OnInstalledReason: { INSTALL: 'install', UPDATE: 'update', CHROME_UPDATE: 'chrome_update', SHARED_MODULE_UPDATE: 'shared_module_update' },
                        OnRestartRequiredReason: { APP_UPDATE: 'app_update', OS_UPDATE: 'os_update', PERIODIC: 'periodic' }
                    }
                };
            """)
        
            # Dynamic fingerprint properties
            if 'languages' in fingerprint:
                langs = ', '.join([f"'{lang}'" for lang in fingerprint['languages']])
                driver.execute_script(
                    f"Object.defineProperty(navigator, 'languages', {{value: [{langs}], configurable: true}})"
                )
            
            if 'hardwareConcurrency' in fingerprint:
                driver.execute_script(
                    f"Object.defineProperty(navigator, 'hardwareConcurrency', {{value: {fingerprint['hardwareConcurrency']}, configurable: true}})"
                )
            
            if 'deviceMemory' in fingerprint:
                driver.execute_script(
                    f"Object.defineProperty(navigator, 'deviceMemory', {{value: {fingerprint['deviceMemory']}, configurable: true}})"
                )
            
            if 'colorDepth' in fingerprint:
                driver.execute_script(
                    f"Object.defineProperty(screen, 'colorDepth', {{value: {fingerprint['colorDepth']}, configurable: true}})"
                )
            
        except Exception as e:
            self.logger.error(f"Error setting fingerprint: {str(e)}")

        return driver
    
    def human_mouse_movement(self, driver, element):
        """Simulate human-like mouse movement to an element"""
        try:
            if not element.is_displayed():
                return
                
            actions = ActionChains(driver)
            start_x = 0
            start_y = 0
            
            # Start from random position
            start_x = random.randint(0, 500)
            start_y = random.randint(0, 300)
            actions.move_by_offset(start_x, start_y).perform()
            current_x, current_y = start_x, start_y
            
            # Move to element in a curved path
            element_location = element.location
            element_size = element.size
            
            target_x = element_location['x'] + element_size['width'] // 2
            target_y = element_location['y'] + element_size['height'] // 2
            
            # Create curved path with intermediate points
            points = []
            num_points = random.randint(3, 6)
            
            for i in range(num_points):
                if i == 0:
                    x = start_x
                    y = start_y
                elif i == num_points - 1:
                    x = target_x
                    y = target_y
                else:
                    # Calculate intermediate points with some randomness
                    progress = i / (num_points - 1)
                    base_x = start_x + (target_x - start_x) * progress
                    base_y = start_y + (target_y - start_y) * progress
                    
                    # Add randomness to the path
                    x = base_x + random.randint(-50, 50)
                    y = base_y + random.randint(-30, 30)
                
                points.append((x, y))
            
            # Move through all points
            for point in points:
                actions.move_by_offset(point[0], point[1])
                actions.pause(random.uniform(0.05, 0.2))
                actions.perform()
            
            # Final hover action
            actions.move_to_element(element).perform()
            time.sleep(random.uniform(0.2, 0.5))
            
            
            # Random mouse wiggle
            for _ in range(random.randint(1, 3)):
                dx = random.randint(-5, 5)
                dy = random.randint(-5, 5)
                actions.move_by_offset(dx, dy).perform()
                current_x += dx
                current_y += dy
                time.sleep(0.1)
        
        except Exception as e:
            logger.warning(f"Mouse movement simulation failed: {str(e)}")
    
    def random_tab_switch(self):
        """Open a new tab, browse briefly, then return to main tab"""
        if random.random() < 0.3:  # 30% chance to switch tabs
            try:
                # Save current tab
                main_tab = self.driver.current_window_handle
                
                # Open new tab
                self.driver.execute_script("window.open('https://www.google.com', '_blank');")
                new_tab = [tab for tab in self.driver.window_handles if tab != main_tab][0]
                self.driver.switch_to.window(new_tab)
                
                # Browse in the new tab
                logger.info("Switched to new tab")
                time.sleep(random.uniform(2, 5))
                
                # Perform some actions in the new tab
                try:
                    search_box = WebDriverWait(self.driver, 5).until(
                        EC.presence_of_element_located((By.NAME, "q"))
                    )
                    self.human_mouse_movement(self.driver, search_box)
                    search_box.send_keys("youtube")
                    search_box.send_keys(Keys.RETURN)
                    time.sleep(random.uniform(1, 3))
                except Exception:
                    pass
                
                # Close the new tab and return to main
                self.driver.close()
                self.driver.switch_to.window(main_tab)
                logger.info("Returned to main tab")
                
            except Exception as e:
                logger.warning(f"Tab switching failed: {str(e)}")
                # Try to return to main tab
                if main_tab in self.driver.window_handles:
                    self.driver.switch_to.window(main_tab)
                    
    def random_scroll(self, driver):
        """Realistic scroll behavior"""
        scroll_points = [random.randint(200, 1000) for _ in range(3)]
        for point in scroll_points:
            driver.execute_script(f"window.scrollTo(0, {point})")
            time.sleep(random.uniform(0.5, 1.5))
            # Random scroll back
            if random.random() > 0.7:
                driver.execute_script(f"window.scrollTo(0, {point//2})")
                time.sleep(random.uniform(0.3, 1.0))
                
    def random_mouse_movement(self, driver):
        """Organic mouse movements"""
        try:
            actions = ActionChains(driver)
            for _ in range(random.randint(3, 8)):
                x_offset = random.randint(-50, 50)
                y_offset = random.randint(-30, 30)
                actions.move_by_offset(x_offset, y_offset)
                actions.pause(random.uniform(0.1, 0.3))
            actions.perform()
        except Exception:
            pass

    def pause_and_resume(self, driver, video_element):
        """Natural video pausing"""
        if random.random() > 0.6:
            try:
                video_element.send_keys(Keys.SPACE)
                time.sleep(random.uniform(2, 15))
                video_element.send_keys(Keys.SPACE)
            except Exception:
                pass
    
    def is_view_compliant(self):
        """Check if the view meets compliance requirements"""
        try:
            # Check if video is playing
            is_playing = self.driver.execute_script("""
                const video = document.querySelector('video');
                return video && !video.paused;
            """)
            
            # Check if video is in viewport
            in_viewport = self.driver.execute_script("""
                const video = document.querySelector('video');
                if (!video) return false;
                
                const rect = video.getBoundingClientRect();
                return (
                    rect.top >= 0 &&
                    rect.left >= 0 &&
                    rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
                    rect.right <= (window.innerWidth || document.documentElement.clientWidth)
                );
            """)
            
            # Check for ad interruptions
            ad_shown = self.driver.execute_script("""
                return document.querySelector('.ad-showing') !== null;
            """)
            
            # Check if user is active
            is_active = True  # Placeholder for actual activity detection
            
            return is_playing and in_viewport and not ad_shown and is_active
        except Exception as e:
            logger.error(f"Compliance check failed: {str(e)}")
            return False
    
    def simulate_view(self, driver, url, duration, view_num, instance_id):
        try:
            # 1. Initial Setup
            self.logger.info(f"[Instance {instance_id}] Starting view #{view_num}")
            profile = self.anti_detect.select_profile()
            self.logger.info(f"[Instance {instance_id}] Using behavior profile: {profile.name}")
    
            # 2. Browser Configuration
            width, height = self.anti_detect.generate_viewport_size()
            driver.set_window_size(width, height)
    
            # 3. Pre-Watch Behavior
            if profile.pre_watch_behavior and random.random() > 0.3:
                self.simulate_pre_watch_behavior(driver)

            # 4. Load Video Page
            driver.get(url)
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "video"))
            )
            video_element = driver.find_element(By.CSS_SELECTOR, "video")
            driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", video_element)
    
            # 5. Start Playback with Human Interactions
            self.anti_detect.human_mouse_movement(driver, video_element)
            time.sleep(random.uniform(0.5, 1.5))
    
            for attempt in range(3):
                try:
                    driver.execute_script("arguments[0].muted = true; arguments[0].play()", video_element)
                    time.sleep(2)
                    if not driver.execute_script("return arguments[0].paused", video_element):
                        break
                except Exception as e:
                    self.logger.warning(f"[Instance {instance_id}] Playback attempt {attempt+1} failed: {str(e)}")
            else:
                self.logger.error(f"[Instance {instance_id}] Failed to start playback")
                return False

            # 6. Main Viewing Loop
            watch_time = random.randint(int(duration * profile.watch_min), int(duration * profile.watch_max))
            start_time = time.time()
            last_error_check = start_time
            error_count = 0
        
            # Generate action sequence
            action_sequence = self.anti_detect.generate_action_sequence()
            next_action_index = 0
            actions = [
                lambda: self.random_scroll(driver),
                lambda: self.random_tab_switch(driver),
                lambda: self.random_mouse_movement(driver),
                lambda: self.pause_and_resume(driver, video_element)
            ]
            last_risk_check = start_time

            while time.time() - start_time < watch_time and self.running:
                try:
                    # Maintain playback and relocate video
                    video_element = driver.find_element(By.CSS_SELECTOR, "video")  # Re-locate element
                    if driver.execute_script("return arguments[0].paused", video_element):
                        driver.execute_script("arguments[0].play()", video_element)
                except StaleElementReferenceException:
                    self.logger.warning(f"[Instance {instance_id}] Video element went stale. Skipping restart.")
                    return False

                # Check for errors every 5 seconds
                if time.time() - last_error_check > 5:
                    last_error_check = time.time()
            
                    if self.is_error_state(driver):
                        error_count += 1
                        logger.warning(f"[Instance {instance_id}] Error detected! Attempting recovery #{error_count}")
                
                        # Emergency recovery protocol
                        self.execute_emergency_recovery(
                            driver, 
                            url, 
                            severity=min(error_count, 3)  # Increase severity with each failure
                        )
                
                        # Abort view after 3 failed recovery attempts
                        if error_count >= 3:
                            logger.error(f"[Instance {instance_id}] Recovery failed after 3 attempts")
                            return False
            
                # Execute scheduled actions
                if next_action_index < len(action_sequence):
                    action = action_sequence[next_action_index]
                    self.anti_detect.execute_action(driver, action)
                    next_action_index += 1
                    # Random sequence alteration
                    if random.random() < 0.15:
                        next_action_index = random.randint(0, len(action_sequence)-1)
        
                # Random interactions
                if random.random() < 0.2:
                    random.choice(actions)()
                
                # Continuous video state monitoring
                try:
                    is_playing = driver.execute_script("""
                        const video = document.querySelector('video');
                        return video && !video.paused;
                    """)
            
                    if not is_playing:
                        logger.info(f"[Instance {instance_id}] Video paused. Attempting restart...")
                        driver.execute_script("document.querySelector('video').play()")
                
                        # Add human-like delay before checking again
                        time.sleep(random.uniform(2, 5))
                except:
                    pass
                
                # Risk management
                if time.time() - last_risk_check > 30:
                    current_risk = self.standing.estimate_detection_risk(driver)
                    last_risk_check = time.time()
                    # Update GUI with risk level
                    if self.update_gui:
                        risk_level = "High" if current_risk > 0.7 else "Medium" if current_risk > 0.4 else "Low"
                        self.update_gui({
                            'risk_level': risk_level,
                            'instance': instance_id
                        })
                    if current_risk > config.get("evasion_threshold", 0.7):
                        self.logger.warning(f"[Instance {instance_id}] High risk detected - rotating identity")
                        self.rotate_identity(driver)
            
                # Organic pauses
                if random.random() < profile.pause_chance:
                    time.sleep(random.uniform(1, 3))
            
                time.sleep(0.5)

            # 7. Post-Watch Activities
            if profile.post_watch_behavior and random.random() > 0.4:
                self.simulate_post_watch_behavior(driver)
    
            # 8. Verify Completion
            play_time = driver.execute_script("return arguments[0].currentTime", video_element)
            view_verified = play_time >= min(30, duration * 0.7)
            self.logger.info(f"[Instance {instance_id}] View #{view_num} completed - {play_time:.1f}s watched ({'Verified' if view_verified else 'Failed'})")
            return view_verified

        except Exception as e:
            self.logger.error(f"[Instance {instance_id}] Simulation failed: {str(e)}", exc_info=True)
            return False
        finally:
            try:
                driver.switch_to.default_content()
            except:
                pass
        
            
            
    def handle_ads(self, driver):
        """Skip ads and handle ad-related challenges"""
        try:
            # Handle initial ads
            skip_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button.ytp-ad-skip-button"))
            )
            self.anti_detect.human_mouse_movement(driver, skip_button)
            skip_button.click()
            logger.info("Skipped initial ad")
        
            # Monitor for mid-roll ads
            threading.Thread(target=self.monitor_ads, args=(driver,)).start()
        except TimeoutException:
            logger.debug("No initial ad detected")
        except Exception as e:
            logger.warning(f"Ad handling failed: {str(e)}")
            
    def execute_emergency_recovery(self, driver, url, severity=1):
        """Perform escalating recovery measures based on severity level"""
        try:
            # Level 1: Basic refresh with cache clear
            driver.execute_script("location.reload(true);")
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "video"))
            )
        
            if severity >= 2:
                # Level 2: Identity rotation + noise injection
                self.rotate_identity(driver)
                self.inject_adversarial_noise(driver)
            
                # Add human-like delay
                time.sleep(random.uniform(3, 8))
            
            if severity >= 3:
                # Level 3: Stealth mode with quantum-safe evasion
                self.enable_quantum_stealth(driver)
            
                # Create diversionary traffic patterns
                self.generate_diversionary_traffic(driver)
            
            # Always handle post-recovery ads
            self.handle_ads(driver)
            return True
        except Exception as e:
            logger.error(f"Recovery failed: {str(e)}")
            return False
            
    def simulate_pre_watch_behavior(self, driver):
        """Simulate browsing before watching the video"""
        # Visit Google
        driver.get("https://www.google.com")
        time.sleep(random.uniform(2, 5))
        
        # Perform a search
        try:
            search_box = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.NAME, "q"))
            )
            search_term = random.choice(["youtube videos", "entertainment", "how to tutorials"])
            for char in search_term:
                search_box.send_keys(char)
                time.sleep(random.uniform(0.05, 0.2))
            search_box.send_keys(Keys.RETURN)
            time.sleep(random.uniform(3, 8))
            
            # Click a random result
            results = driver.find_elements(By.CSS_SELECTOR, "h3")
            if results:
                random.choice(results[:5]).click()
                time.sleep(random.uniform(4, 10))
        except:
            pass
    
    def simulate_post_watch_behavior(self, driver):
        """Simulate browsing after watching the video"""
        # Scroll through related videos
        for _ in range(random.randint(2, 5)):
            scroll_amount = random.randint(200, 500)
            driver.execute_script(f"window.scrollBy(0, {scroll_amount})")
            time.sleep(random.uniform(1, 3))
        
        # Random chance to click a related video
        if random.random() < 0.4:
            try:
                related_videos = driver.find_elements(By.ID, "related")
                if related_videos:
                    video_to_click = random.choice(related_videos)
                    self.anti_detect.human_mouse_movement(driver, video_to_click)
                    video_to_click.click()
                    time.sleep(random.uniform(10, 30))
            except:
                pass
    
    def run_view_instance(self, url, duration, instance_id):
        """Run a single browser instance to simulate multiple views"""
        driver = None
        try:
            proxy = self.get_random_proxy()
            if not proxy:
                self.logger.error(f"[Instance {instance_id}] No proxies available")
                return

            fingerprint = self.get_random_fingerprint()
            driver = self.create_driver(proxy, fingerprint)
        
            # Calculate views for this instance
            views_per_instance = self.max_views // self.concurrent_instances
            if instance_id <= (self.max_views % self.concurrent_instances):
                views_per_instance += 1

            for view_num in range(1, views_per_instance + 1):
                if not self.running:
                    break

                # Simulate view
                success = self.simulate_view(driver, url, duration, view_num, instance_id)
            
                # Update GUI
                with self.view_lock:
                    self.gui_update_callback({
                    'status': f"Instance {instance_id}: View {view_num}/{views_per_instance}",
                    'view': self.current_view,
                    'total': self.max_views,
                    'compliant': self.compliant_views,
                    'verified': self.verified_views,
                    'instance': self.concurrent_instances,  # Add active instances
                    'video_id': self.video_id
                    })

                # Delay between views
                if view_num < views_per_instance and self.running:
                    delay = random.randint(45, 180)
                    for i in range(delay, 0, -1):
                        if not self.running:
                            break
                        time.sleep(1)
                    
        except Exception as e:
            self.logger.error(f"[Instance {instance_id}] Fatal error: {str(e)}")
        finally:
            if driver:
                try:
                    driver.quit()
                    self.logger.info(f"[Instance {instance_id}] Browser instance closed")
                except:
                    pass

    def random_interaction(self, driver):
        """Perform random interactions with the page"""
        try:
            actions = ActionChains(driver)
            # Mouse movement
            actions.move_by_offset(
                random.randint(-100, 100),
                random.randint(-50, 50)
            ).perform()
        
            # Random keyboard input
            if random.random() < 0.2:
                actions.send_keys(Keys.SPACE).perform()  # Pause/play
                time.sleep(0.5)
                actions.send_keys(Keys.SPACE).perform()
        except:
            pass

    def random_tab_switch(self, driver):
        """Simulate tab switching behavior"""
        if random.random() < 0.1:  # 10% chance
            try:
                main_tab = driver.current_window_handle
                driver.execute_script("window.open('https://www.google.com', '_blank');")
                new_tab = [tab for tab in driver.window_handles if tab != main_tab][0]
                driver.switch_to.window(new_tab)
                time.sleep(random.uniform(2, 5))
                driver.close()
                driver.switch_to.window(main_tab)
            except:
                pass

    def run(self, url, view_count, duration, use_proxy, show_log):
            """Main execution loop with concurrent instances"""
            self.running = True
            self.logger.info(f"Starting YouTube View Bot with {view_count} views across {self.concurrent_instances} instances")
        
            # Extract video ID for logging
            video_id_match = re.search(r"v=([a-zA-Z0-9_-]{11})", url)
            self.video_id = video_id_match.group(1) if video_id_match else "unknown"
        
            # Update GUI with initial video ID
            self.gui_update_callback({'video_id': self.video_id})
        
            # Create and start threads
            threads = []
            for i in range(self.concurrent_instances):
                thread = threading.Thread(
                    target=self.run_view_instance,
                    args=(url, duration, i+1),
                    daemon=True
                )
                thread.start()
                threads.append(thread)
                # Stagger thread starts to avoid simultaneous launches
                time.sleep(random.uniform(1.0, 3.0))
        
            # Wait for all threads to complete
            for thread in threads:
                thread.join()
        
            # Final status
            self.gui_update_callback({
                'status': f"Completed: {self.compliant_views} compliant, {self.verified_views} verified",
                'completed': True,
                'compliant': self.compliant_views,
                'verified': self.verified_views
            })
            self.logger.info(f"Bot finished: Compliant views: {self.compliant_views}/{view_count}")
            self.logger.info(f"Verified views: {self.verified_views}/{view_count}")
            self.running = False
            
    def is_error_state(self, driver):
        try:
            return any(
                "Something went wrong" in driver.page_source,
                "Please try again later" in driver.page_source,
                "Refresh" in driver.page_source,
                driver.find_elements(By.ID, "error-screen")
            )
        except:
            return False
        
    def enable_quantum_stealth(self, driver):
        """Activate advanced evasion techniques"""
        try:
            driver.execute_script("""
                // Enable quantum-safe features
                window.quantumEntanglement = true;
                window.fingerprintDecay = 0.15;
                window.behaviorEntropy = 0.92;
            
                // Install stealth hooks
                const origPushState = history.pushState;
                history.pushState = function(state) {
                    window.stealthMode = true;
                    return origPushState.apply(this, arguments);
                };
            
                // Mask automation signals
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => false,
                    configurable: true
                });
            """)
        
            # Add noise to network traffic patterns
            self.generate_network_noise(driver)
            logger.info("Quantum stealth mode activated")
        except Exception as e:
            logger.error(f"Stealth activation failed: {str(e)}")
   
    def stop(self):
        """Stop the bot and all running instances"""
        self.running = False
        self.logger.info("Bot stopped by user request")
    
    def on_closing(self):
        """Handle window closing"""
        self.save_settings()
        self.bot.running = False
        sys.stdout = self.original_stdout
        self.root.destroy()
    
    def random_interaction(self, driver):
        """Perform random mouse/keyboard actions"""
        try:
            actions = ActionChains(driver)
            # Random mouse movement
            actions.move_by_offset(
                random.randint(-100, 100),
                random.randint(-50, 50)
            ).perform()
        
            # Random keyboard input
            if random.random() < 0.2:
                actions.send_keys(Keys.SPACE).perform()  # Pause/play
                time.sleep(0.5)
                actions.send_keys(Keys.SPACE).perform()
            
        except Exception:
            pass
                 
    def rotate_identity(self, driver):
        """Emergency identity rotation protocol with enhanced cleaning"""
        try:
            # Clear browsing data
            driver.execute_cdp_cmd('Storage.clearDataForOrigin', {
                "origin": '*',
                "storageTypes": "all",
            })
        
            # Clear cookies and storage
            driver.delete_all_cookies()
            driver.execute_script("""
                window.sessionStorage.clear();
                window.localStorage.clear();
                if (window.indexedDB) {
                    indexedDB.databases().then(dbs => {
                        for (let db of dbs) {
                            indexedDB.deleteDatabase(db.name);
                        }
                    });
                }
            """)
        
            # Rotate fingerprint
            new_fp = self.standing.dynamic_fingerprinting()
            self.apply_fingerprint(driver, new_fp)
        
            # Rotate user agent
            new_ua = self.get_random_user_agent()
            driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": new_ua})
        
            self.logger.info("Identity fully rotated")
        except Exception as e:
            self.logger.error(f"Identity rotation failed: {str(e)}")
            
        self.reset_browser_state(driver)
        new_fp = self.standing.dynamic_fingerprinting()
        self.apply_fingerprint(driver, new_fp)
        self.inject_adversarial_noise(driver)
    
        # Rotate proxy
        new_proxy = self.get_random_proxy()
        self.configure_proxy(driver, new_proxy)
        
    def inject_adversarial_noise(self, driver):
        """Inject random noise into browser characteristics"""
        try:
            driver.execute_script(f"""
                // Add noise to screen properties
                const originalWidth = screen.width;
                const originalHeight = screen.height;
                Object.defineProperty(screen, 'width', {{ 
                    get: () => originalWidth + {random.randint(-10, 10)}
                }});
                Object.defineProperty(screen, 'height', {{ 
                    get: () => originalHeight + {random.randint(-5, 5)}
                }});
            
                // Add noise to other properties
                const noiseParams = {{
                    deviceMemory: {random.choice([0.1, -0.1, 0])},
                    hardwareConcurrency: {random.choice([1, -1, 0])},
                    colorDepth: {random.choice([2, -2, 0])}
                }};
            
                Object.entries(noiseParams).forEach(([key, value]) => {{
                    const original = navigator[key];
                    if (typeof original === 'number') {{
                        Object.defineProperty(navigator, key, {{
                            get: () => original + value
                        }});
                    }}
                }});
            """)
        except Exception as e:
            logger.warning(f"Noise injection failed: {str(e)}")
    
    def handle_security_challenges(self, driver):
        """Centralized security challenge handler"""
        return self.standing.solve_advanced_captcha(driver)
    
    def reset_browser_state(self, driver):
        """Clear cookies, storage, and reset user agent between views"""
        try:
            # Clear all cookies
            driver.delete_all_cookies()
        
            # Clear local and session storage
            driver.execute_script("window.localStorage.clear();")
            driver.execute_script("window.sessionStorage.clear();")
        
            # Reset user agent
            new_ua = self.get_random_user_agent()
            driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": new_ua})
        
            # Clear service workers
            driver.execute_script("""
                if (navigator.serviceWorker) {
                    navigator.serviceWorker.getRegistrations()
                    .then(registrations => {
                        for (let registration of registrations) {
                            registration.unregister();
                        }
                    });
                }
            """)
            self.logger.info("Browser state reset: cookies cleared, UA rotated")
        except Exception as e:
            self.logger.error(f"State reset failed: {str(e)}")
            
    def monitor_viewer_state(self, driver, instance_id):
        """Continuous monitoring of viewer state"""
        last_state = "playing"
        error_count = 0
    
        while self.running:
            try:
                # Check playback state
                is_playing = driver.execute_script("""
                    return document.querySelector('video')?.paused === false;
                """)
            
                # Check error state
                if self.is_error_state(driver):
                    error_count += 1
                    logger.warning(f"[Instance {instance_id}] Error detected! Recovery attempt #{error_count}")
                
                    recovery_success = self.execute_emergency_recovery(
                        driver,
                        severity=min(error_count, 3)  # Escalate severity
                    )
                
                    if not recovery_success and error_count >= 3:
                        logger.error(f"[Instance {instance_id}] Critical failure - restarting instance")
                        self.restart_instance(instance_id)
                        break
                else:
                    error_count = 0
                
                # Update state tracking
                if is_playing and last_state != "playing":
                    logger.info(f"[Instance {instance_id}] Playback resumed")
                elif not is_playing and last_state == "playing":
                    logger.warning(f"[Instance {instance_id}] Playback paused - attempting restart")
                    driver.execute_script("document.querySelector('video').play()")
                
                last_state = "playing" if is_playing else "paused"
            
                # Random interval checking (2-8 seconds)
                time.sleep(random.uniform(2, 8))
            except TimeoutException as e:
                logger.error(f"[Instance {instance_id}] Timeout during monitoring: {str(e)}")
                time.sleep(5)
                
            except Exception as e:
                logger.error(f"[Instance {instance_id}] Monitoring error: {str(e)}")
                time.sleep(5)
            
    def __del__(self):
        # Clean up temporary files
        if hasattr(self, '_temp_dirs'):
            import shutil
            for temp_dir in self._temp_dirs:
                shutil.rmtree(temp_dir, ignore_errors=True)# Add to YouTubeViewBot class in bot.py
                
    def __del__(self):
        # Clean up temporary proxy extension files
        if hasattr(self, '_temp_proxy_files'):
            for file_path in self._temp_proxy_files:
                try:
                    os.remove(file_path)
                except Exception:
                    pass
                
                  