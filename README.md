# Discord Auto-Poster Bot

A simple automated tool for posting messages to Discord channels at specified intervals.

## Prerequisites
- modules such as: requests, sqlite3, time installed

## Getting Started

1. Run `start.bat`
2. Enter your Discord account token (see instructions below)
3. Configure the auto-poster settings as prompted

## How to Get Your Discord Token

1. Log in to your Discord account in a web browser
2. Open Developer Tools (Ctrl+Shift+I)
3. Go to the Network tab
4. Filter requests with `/api`
5. Look for the `science` request
6. Find the `authorization` parameter in the headers
7. Copy its value
8. Paste it into the program when prompted

**Warning:** Never share your token with anyone as it provides full access to your account.

## Configuration Steps in the Program
0. **Token** 
1. **Channel IDs**: Enter the channel IDs where the auto-poster should send messages
2. **Message Count**: Specify how many times the messages should be sent
3. **Interval**: Set the delay between messages in seconds (e.g., 60 for 1 minute)
   - Note: The bot will respect Discord's rate limits and skip sending if hitting cooldown
4. **Message Content**: Enter the message to be sent

## Persistent Configuration

- On subsequent runs, the program will detect and offer to restore settings from previous sessions
- Configuration data is stored in a local database file

## Disclaimer

**The creator of this auto-poster is not responsible for any misuse of this tool.**
- Use automation in compliance with Discord's Terms of Service
- This tool is provided for educational purposes only
