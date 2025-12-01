# Day 10 - Voice Improv Battle 🎭

A high-energy voice-first improv game show where players perform improvisation scenarios and receive real-time feedback from an AI host.

## 🎯 Overview

**Improv Battle** is a single-player improv performance game where:
- An AI game show host presents improvisation scenarios
- Players act out the scenarios using their voice
- The host provides varied, realistic reactions - sometimes supportive, sometimes critical
- The game runs through 3 rounds with different scenarios
- Players receive a personalized summary of their improv style at the end

## ✨ Features

### Game Flow
1. **Welcome & Introduction** - Host explains the game and asks for player's name
2. **3 Improv Rounds** - Each round presents a unique scenario
3. **Real-time Reactions** - Host comments on performance after each scene
4. **Closing Summary** - Personalized feedback on player's improv style

### AI Host Personality
- **Energetic & Witty** - Like a real game show host
- **Honest Reactions** - Not always supportive; provides constructive critique
- **Varied Feedback** - Sometimes amused, sometimes unimpressed, sometimes surprised
- **Respectful** - Light teasing but always fun and encouraging

### Improv Scenarios
15 diverse scenarios including:
- **Time-Travelling Tour Guide** - Explain smartphones to someone from the 1800s
- **Portal Barista** - Tell a customer their latte is a portal to another dimension
- **Motivational Ghost** - Haunt a house while motivating people to achieve their dreams
- **Sentient GPS** - Give directions while having an existential crisis
- **Dragon Real Estate** - Sell a house to a dragon with specific requirements
- And 10 more creative scenarios!

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- LiveKit Cloud account
- API keys for:
  - LiveKit
  - Google Gemini (LLM)
  - Deepgram (Speech-to-Text)
  - Murf AI (Text-to-Speech)

### Installation

1. **Navigate to backend directory:**
   ```bash
   cd "Day 10/backend"
   ```

2. **Install dependencies:**
   ```bash
   uv sync
   ```

3. **Configure environment:**
   Create a `.env` file with your API keys:
   ```env
   LIVEKIT_URL=wss://your-livekit-url.livekit.cloud
   LIVEKIT_API_KEY=your_api_key
   LIVEKIT_API_SECRET=your_api_secret
   MURF_API_KEY=your_murf_key
   GOOGLE_API_KEY=your_google_key
   DEEPGRAM_API_KEY=your_deepgram_key
   ```

4. **Start the backend:**
   ```bash
   uv run src/improv_agent.py dev
   ```

5. **Start the frontend:**
   ```bash
   cd "../../Day 7/frontend"
   pnpm dev
   ```

6. **Play the game:**
   - Open http://localhost:3000
   - Click "Start Improv Battle"
   - Follow the host's instructions!

## 🎮 How to Play

1. **Join the Game** - Click "Start Improv Battle" and introduce yourself
2. **Listen to the Scenario** - The host will present a creative improv scenario
3. **Perform!** - Act out the scenario in character
4. **End Your Scene** - Say "end scene" or pause when you're done
5. **Receive Feedback** - The host will comment on your performance
6. **Repeat** - Complete 3 rounds total
7. **Get Your Summary** - Hear what kind of improviser you are!

### Tips for Great Improv
- **Commit to the character** - Go all in!
- **Embrace the absurdity** - The weirder, the better
- **Don't rush** - Take your time to develop the scene
- **Have fun** - The host appreciates creativity and energy

## 🛠️ Technical Stack

- **Voice Agent Framework**: LiveKit Agents
- **LLM**: Google Gemini 2.0 Flash
- **Speech-to-Text**: Deepgram Nova-3
- **Text-to-Speech**: Murf AI (Terrell voice)
- **Frontend**: Next.js (from Day 7)
- **Backend**: Python with async/await

## 📁 Project Structure

```
Day 10/
├── backend/
│   ├── src/
│   │   ├── improv_agent.py      # Main agent with game logic
│   │   ├── scenarios.json       # 15 improv scenarios
│   │   └── __init__.py
│   ├── pyproject.toml           # Dependencies
│   └── .env                     # API keys (not in git)
└── README.md
```

## 🎭 Game State Management

The agent tracks:
- `player_name` - Player's name
- `current_round` - Which round (1-3)
- `max_rounds` - Total rounds (3)
- `rounds` - History of scenarios and reactions
- `phase` - Current game phase (intro/awaiting_improv/reacting/done)
- `used_scenario_ids` - Prevents scenario repetition

## 🔧 Function Tools

### `get_next_scenario()`
- Selects a random unused scenario
- Increments round counter
- Returns scenario description to present to player

### `end_game(reason)`
- Allows early exit if player wants to stop
- Provides graceful ending message

## 🎨 Customization

### Change Host Voice
Edit `improv_agent.py`:
```python
tts=murf.TTS(
    voice="en-US-terrell",  # Try other Murf voices
),
```

### Adjust Number of Rounds
Edit `improv_agent.py`:
```python
self.max_rounds = 3  # Change to 5, 10, etc.
```

### Add More Scenarios
Edit `scenarios.json` - add new scenarios with:
- `id` - Unique identifier
- `title` - Scenario name
- `description` - Full scenario description
- `character` - Who the player is
- `situation` - What's happening
- `tension` - The challenge/conflict

## 📝 License

Part of the "10 Days of Voice Agents" challenge.

## 🙏 Acknowledgments

- LiveKit for the amazing voice agent framework
- The improv community for inspiration
- All the creative scenarios that make this game fun!

---

**Ready to test your improv skills? Start the game and show us what you've got!** 🎭🎤✨

