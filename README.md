# MOTD Dashboard

A system information dashboard that automatically displays in the terminal on SSH/local login. It shows ASCII art, weather, system resource usage, and last login info all on one screen.

## Features

- **ASCII Art**: Renders the distro name (from `/etc/os-release`) in a random color
- **Weather Info**: Looks up location from the public IP (via ipinfo.io), then fetches current weather/temperature/feels-like/humidity from the OpenWeatherMap API
- **System Info**: Uptime, CPU/memory/disk usage (color-coded by threshold), kernel version, hostname, username
- **Update Status**: Checks the number of pending package updates via `dnf check-update` (requires root)
- **Last Login**: Shows the most recent login time/user/IP using the `last` command

## File Structure

| File | Role |
|---|---|
| `main.py` | Entry point. Gathers data from each module and triggers rendering |
| `display.py` | Console output based on `rich` (ASCII art + info table) |
| `weather.py` | IP-based location lookup and OpenWeatherMap API calls |
| `system.py` | Collects uptime, resource usage, update status, login history, etc. |
| `setup.sh` | Installation script (creates deployment dir, sets up venv, registers login hook) |
| `.env` | Environment variables such as API keys (must be created manually) |

## Installation

1. Place the project files along with a `.env` file in the same directory.
2. Fill in the following values in `.env`:
   ```
   WEATHER_API_KEY=your_openweathermap_api_key
   IPINFO_TOKEN=your_ipinfo_token
   ```
3. Run the setup script as root:
   ```bash
   sudo bash setup.sh
   ```

The setup script performs the following:
- Deploys files to `/opt/motd-dashboard` and restricts `.env` permissions (creates a dedicated group, then sets 640)
- Creates an isolated Python virtual environment (venv) and installs dependencies (`rich`, `requests`, `python-dotenv`, `psutil`, `pyfiglet`)
- Registers a login hook at `/etc/profile.d/motd.sh` → runs automatically on login

## Requirements

- Python 3
- Root privileges (for installation)
- An OpenWeatherMap API key
- An ipinfo.io token

## Notes

- The update-check feature only runs when logged in as root (regular users are skipped).
- To access `.env`, a logging-in user must belong to the `motd-dashboard` group; re-login is required after being added to the group for the change to take effect.
