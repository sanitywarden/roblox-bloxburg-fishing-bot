#### README in other languages
[Polski](https://github.com/sanitywarden/roblox-bloxburg-fishing-bot/blob/main/pl_README.md#readme)

# roblox-bloxburg-fishint-bot
This is the repository for a simple Windows/MacOS Python bot/script which automates the fishing job in a Roblox game called Bloxburg.

>This is a project developed out of my own curiosity and for educational purposes only. Using bots and/or automation scripts makes the experience worse for the gaming community and should be avoided.

>Using this script is most likely against Roblox guideliness and could get you banned if caught. Use at your own risk and always respect the terms of service of the game and platform.

## Features

* Works on Windows and MacOS
* Automatically catches fish
* Ability to stop (default `q`) or pause (default `p`) the script

## Rates and efficiency
I measured that the bot averages at about a fish per 10 to 12 seconds. That makes it catch about 300 to 360 fish per hour.

The higher job level you have in Bloxburg the more money you will earn per hour.

## Prerequisites
- Roblox
- Python (tested on 3.12)

## How to install it
### Using `git`

1. Clone/download this repository
```
git clone https://github.com/sanitywarden/roblox-bloxburg-fishing-bot
```

2. Open the `roblox-bloxburg-fishing-bot` folder in your terminal and depending on your OS install appropriate packages.

#### Windows
```
pip install -r windows_requirements.txt
```

Once the packages install, prepare your Roblox, join Bloxburg and you can run the scipt with `python main.py` or `python3 main.py`. If none of those work it means you don't have a `python` interpreter installed on your system. Install it, and come back to this step later.

#### MacOS
```
pip install -r macos_requirements.txt
```

Once the packages install, your Mac will most likely not let you run this script yet. You have to first give it some permissions, as the OS is more restrictive of what it lets you run.

Go to `Settings > Privacy & Security > Accessibility` and add the `Terminal` app to the list. Do the same in `Screen & System Audio Recording`.

Once the packages install and you configure your Mac, prepare your Roblox, join Bloxburg and you can run the scipt with `python main.py` or `python3 main.py`. If none of those work it means you don't have a `python` interpreter installed on your system. Install it, and come back to this step later.

### How to use the bot?

After running the script with `python main.py` you should see two windows open. One is a terminal with the running script and the second is a preview camera. For the bot to work and automatically fish the hook has to be visible in the preview window. If the preview window is too small and doesn't fit your display, you can configure it in `config.yaml`.