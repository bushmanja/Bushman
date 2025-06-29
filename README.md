# Bushman

# 🎓 YouTube View Simulator – PHD ADMIN PROTOCOL 22#

**A Human Emulation Framework for Educational Research on Anti-Bot Detection**
## Note: args are not yet implemented, this can be added easily 

---

## 🧠 About This Project

This simulator is part of a PhD-level research initiative focused on behavioral simulation, fingerprint evasion, and automated detection avoidance in browser-based systems. It is designed to simulate realistic user behavior on YouTube using dynamic profiles, rotating proxies, and anti-detection browser configurations.

The system supports:

- 🎛️ Fully interactive GUI
- 🌐 Authenticated proxy routing
- 🧬 Fingerprint spoofing
- 🧠 Human-like attention models
- 📊 Real-time view/session logging

> 🔬 **This project is strictly for academic, ethical, and educational use only.**

---

## 🧾 Key Features

- **Behavioral Profiles**: Casual, Engaged, Binge, and Distracted behavior engines simulate real attention spans and interaction patterns.
- **Proxy Support**: Load authenticated HTTP/SOCKS5 proxies from file. Rotates per session.
- **Advanced Fingerprint Randomization**: Modifies headers, timezones, hardwareConcurrency, platform, language, canvas and WebGL data.
- **GUI Frontend**: Built using `tkinter`, offers visual control of views, proxies, behaviors, and logs.
- **Modular & Threaded**: Each view runs in an isolated Chrome instance. Supports concurrency.
- **CAPTCHA & Stale Element Recovery**: Handles most common Selenium failures, recovers on DOM mutation.

---

## 🖥️ Platform Support

- ✅ Windows 10/11  
- ✅ Linux (Ubuntu, Debian, Fedora, Arch)
-  Mobile bushmanTmobile -

---

## ⚙️ Requirements

**Python 3.10+** is required.

Install required packages using pip or dont idk:

```bash
pip install selenium
pip install undetected-chromedriver
pip install fake-useragent
pip install requests
pip install webdriver-manager

📚 Acknowledgements & References
Selenium Project and continue work,

Undetected-Chromedriver by Ultrafunkamsterdam

Google Chrome DevTools Protocol

Research: arXiv:2506.10685v1 – CAPTCHA visual diffusion

Stack Overflow, GitHub, and OpenAI for shared anti-detection strategies
