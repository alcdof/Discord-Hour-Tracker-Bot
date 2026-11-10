# 🤖 AI-Powered Discord Hour Tracker Bot

An AI-powered Discord bot built with Python, designed to provide server utilities, voice channel time tracking, and AI-powered interactions through Google's Gemini API.

## 🚀 Features

### ⏱️ Voice Channel Time Tracking
- Automatically detects when users join and leave voice channels.
- Tracks how long a user has been connected to a voice channel.
- Displays the elapsed time using the `/time` command.

### 🤖 AI Integration
- Interact with Google's Gemini AI directly through Discord.
- Ask questions and receive AI-generated responses using the `/ai` command.

### 🛠️ Server Utilities

| Command | Description |
|---|---|
| `/hello` | Greets the user. |
| `/ping` | Displays the bot's response latency. |
| `/counter` | Increments, decrements, or resets a shared counter. |
| `/clear` | Deletes a specified number of messages, optionally filtering by user. |
| `/join` | Makes the bot join the user's current voice channel. |
| `/leave` | Disconnects the bot from the voice channel. |
| `/time` | Displays the user's current voice session duration. |
| `/ai` | Sends a question to Google's Gemini AI. |

## 🧰 Technologies

- **Python** – Main programming language.
- **discord.py** – Discord API integration and bot functionality.
- **Google Gemini API** – AI-powered question answering.
- **python-dotenv** – Environment variable and API key management.
- **Discord Slash Commands** – Native command interface.

## ⚙️ Getting Started

### Prerequisites

Before running the project, make sure you have:

- Python 3.10 or newer.
- A Discord account and a Discord server.
- A Discord Bot Application.
- A Google Gemini API key.

### 1. Clone the repository

```bash
git clone https://github.com/alcdof/Discord-Hour-Tracker-Bot.git
cd Discord-Hour-Tracker-Bot
```

### 2. Install dependencies

```bash
pip install discord.py python-dotenv google-generativeai
```

### 3. Configure environment variables

Create a `.env` file in the project's root directory:

```env
DISCORD_TOKEN=your_discord_bot_token
GUILD_ID=your_discord_server_id
GEMINI_API_KEY=your_gemini_api_key
```

Replace the placeholder values with your actual credentials.

### 4. Configure your Discord Bot

In the [Discord Developer Portal](https://discord.com/developers/applications):

1. Create a new application.
2. Add a bot to your application.
3. Copy its token and add it to your `.env` file.
4. Enable the required Gateway Intents.
5. Invite the bot to your server with the necessary permissions, including message management and voice channel access.

### 5. Run the bot

```bash
python main.py
```

If everything is configured correctly, the terminal will display:

```text
Bot successfully initialized.
```

The bot's slash commands will then be available on the configured Discord server.

## 🧠 How It Works

The bot uses Discord's event-driven architecture to monitor user activity and respond to interactions.

For voice tracking, Discord voice state events are used to identify when a member joins or leaves a voice channel. The bot records the session's start time and calculates the elapsed duration when requested.

For AI interactions, user questions are sent to Google's Gemini model, which generates a response that is returned directly to the Discord server.

## ⚠️ Current Limitations

- Voice session data is stored in memory and is not persisted between bot restarts.
- Time tracking currently focuses on individual voice sessions rather than historical activity reports.
- Slash commands are synchronized with a configured Discord server through `GUILD_ID`.

## 📌 Future Improvements

- Persistent storage for voice activity and user statistics.
- Total time tracking across multiple sessions.
- Individual and server-wide activity reports.
- Leaderboards based on voice channel activity.
- Improved AI interaction and conversation context.

## 👨‍💻 Author

**André Caillot**

Computer Engineering Student | Python Developer

- GitHub: [@alcdof](https://github.com/alcdof)

---

*Developed as a personal project to explore Python, Discord bot development, event-driven programming, and AI API integration.*