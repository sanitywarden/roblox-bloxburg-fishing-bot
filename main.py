import random
import time
import cv2
import numpy
import mss
import yaml
import platform
import numpy as np
import pyautogui

# Get the operating system
# Windows: 'Windows'
# Linux:   'Linux'
# macOS:   'Darwin'
def os():
    return platform.system()

# System specific libraries
# Windows clicking is done with Windows system API
if os() == "Windows":
    import win32api
    import win32con
    import ctypes
    import keyboard

# macOS clicking is done with native Quartz framework
elif os() == "Darwin":
    import Quartz.CoreGraphics as CG

# Attempt to load the config.yaml file in the project folder
# Returns the config or None
def load_yaml_settings():
    try:
        with open('./config.yaml', 'r') as file:
            config = yaml.safe_load(file)
            return config 
    except:
        return None
    return None

# Attempt to load the version.txt file in the project folder
# Returns version or error string
def load_version(): 
    try:
        with open('./version.txt', 'r') as file:
            version = file.read()
            return version
    except:
        return "error reading version.txt file"
    return "version.txt file not found"

config = load_yaml_settings()
if config is None:
    print_with_time("Roblox bloxburg fishing bot requires the 'config.yaml' file but it doesn't exist")
    exit(1)

debug_mode               = int(config['debug_mode'])
start_script_countdown_s = int(config['start_script_countdown_s'])
quit_script_hotkey       = config['quit_script_hotkey']
pause_script_hotkey      = config['pause_script_hotkey']
catch_fish_click_min_s   = float(config['catch_fish_click_min_s'])
catch_fish_click_max_s   = float(config['catch_fish_click_max_s'])

# macOS with it's Retina screen has some shenanigans going on
# and when detecting stuff on screen it's required to adjust scale
# because of that 
def get_screenshot_scale():
    with mss.mss() as screenshot:
        monitor = screenshot.monitors[1]

        test_image = np.array(screenshot.grab(monitor))
        scale = test_image.shape[1] / monitor['width']
        return scale
    return 1

def get_screen_size():
    return pyautogui.size()

    if os() == "Windows":
        user32 = ctypes.windll.user32
        return user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
    else:
        return pyautogui.size()

def get_key_code(key):
    key = key.upper()

    # Key codes that are important for us
    mac_codes = { 'Q': 12, 'P': 35 }

    if os() == "Windows":
        # This doesn't support special keys
        if len(key) == 1:
            return ord(key)
        return 0

    elif os() == "Darwin":
        return mac_codes.get(key, -1)
    
    return 0

def is_key_pressed(key_name):
    if os() == "Windows":
        return keyboard.is_pressed(key_name)

    elif os() == "Darwin":
        return CG.CGEventSourceKeyState(CG.kCGEventSourceStateCombinedSessionState, get_key_code(key_name))

    return False

def use_rod():
    if os() == "Windows":
        # Pressing enter has to be very low level for Roblox to recognise it as legit
        MapVirtualKey      = ctypes.windll.user32.MapVirtualKeyW
        KEYEVENTF_SCANCODE = 0x0008
        KEYEVENTF_KEYUP    = 0x0002
        scancode           = 0x1C

        ctypes.windll.user32.keybd_event(0, scancode, KEYEVENTF_SCANCODE, 0)
        time.sleep(random.uniform(catch_fish_click_min_s, catch_fish_click_max_s))
        ctypes.windll.user32.keybd_event(0, scancode, KEYEVENTF_SCANCODE | KEYEVENTF_KEYUP, 0)
        time.sleep(0.1)

    elif os() == "Darwin":
        ENTER_CODE = 36

        src = CG.CGEventSourceCreate(CG.kCGEventSourceStateHIDSystemState)
        push = CG.CGEventCreateKeyboardEvent(src, ENTER_CODE, True)
        release = CG.CGEventCreateKeyboardEvent(src, ENTER_CODE, False)
        CG.CGEventPost(CG.kCGHIDEventTap, push)
        time.sleep(random.uniform(catch_fish_click_min_s, catch_fish_click_max_s))
        CG.CGEventPost(CG.kCGHIDEventTap, release)
        time.sleep(0.1)

def print_with_time(message):
    print(f"[{time.strftime('%H:%M:%S')}] {message}")

def print_with_time_debug(message):
    if debug_mode: 
        print_with_time(f"[debug] {message}")

is_fishing = False
paused_script = False

width, height = get_screen_size()
search_area = { 
    "top":    int(height * float(config['align_window_top'])), 
    "left":   int(width  * float(config['align_window_left'])), 
    "width":  int(width  * float(config['align_window_width'])), 
    "height": int(height * float(config['align_window_height']))
}

if debug_mode:
    print_with_time_debug(f"roblox-bloxburg-fishing debug automation script {load_version()} by Vivit")
else:
    print_with_time(f"roblox-bloxburg-fishing automation script {load_version()} by Vivit")

print_with_time(f"This script averages at about 300-360 fish/hour or 1 fish/10-12s")
print_with_time(f"Press and hold '{quit_script_hotkey}' to stop the script")
print_with_time(f"Press and hold '{pause_script_hotkey}' to pause the script")
print_with_time(f"You have {start_script_countdown_s} seconds to prepare the Roblox Bloxburg game\n")
time.sleep(3)

# Countdown to start
for second in range(0, start_script_countdown_s):
    time_left = start_script_countdown_s - second
    if time_left <= 5:
        print_with_time(f"Starting script in {time_left} seconds")
    time.sleep(1)

# For pretty terminal formatting
print("")

while True:
    if cv2.waitKey(1) & 0xFF == ord(quit_script_hotkey.lower()):
        cv2.destroyAllWindows()
        time.sleep(1)
        break

    if is_key_pressed(quit_script_hotkey):
        cv2.destroyAllWindows()
        time.sleep(1)
        break

    if is_key_pressed(pause_script_hotkey):
        paused_script = not paused_script
        print_with_time("Paused the script" if paused_script else "Unpaused the script")
        time.sleep(1)
        continue

    if paused_script:
        time.sleep(1)
        continue

    else:
        if not is_fishing:
            is_fishing = True
            use_rod()

        with mss.mss() as screenshot:
            image = np.array(screenshot.grab(search_area))
            cv2.imshow("Place the hook in the image", image)

            # Create nice day/night vision eyes of the bot 
            hls = cv2.cvtColor(image, cv2.COLOR_BGR2HLS)
            lightness = hls[:, :, 1]
            clahe = cv2.createCLAHE(clipLimit=4.0, tileGridSize=(8, 8))
            light = clahe.apply(lightness)
            
            # Blur it to increase the change of detecting the floating bob 
            blur = cv2.GaussianBlur(light, (5, 5), 0)
            canny = blur

            if os() == "Windows":
                # Clean up the image a bit
                # This removes the fishing rod line and stray pixels
                kernel = np.ones((5, 5), np.uint8)
                cleaned = cv2.morphologyEx(blur, cv2.MORPH_OPEN, kernel)
                canny = cv2.Canny(cleaned, 225, 255)

            elif os() ==  "Darwin":
                # Something breaks with macOS and we can't really further process the screenshot
                # without losing valuable pixels of the hook
                # so we just do the detection on the blur
                canny = cv2.Canny(blur, 225, 255)

            # If the image is dark on average,
            # then the float is probably under water
            # which means that a fish is caught
            average_brightness = np.mean(canny)

            if not paused_script and is_fishing and average_brightness == 0:                    
                if not paused_script:
                    is_fishing = False
                    use_rod()
