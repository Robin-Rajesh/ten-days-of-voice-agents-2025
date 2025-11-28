# Day 8 – Stranger Things Voice Game Master

A D&D-style voice adventure game set in the Stranger Things universe (Hawkins, Indiana, 1985).

## Overview

Experience an interactive voice-driven adventure where you play as a teenager in Hawkins discovering strange happenings. The AI Game Master guides you through a suspenseful story inspired by Stranger Things, complete with mystery, danger, and 80s nostalgia.

## Features Implemented

### ✅ Primary Goal (MVP)

1. **Game Master Persona**
   - Clear GM role with Stranger Things universe setting
   - Dramatic, suspenseful tone with 80s atmosphere
   - Set in Hawkins, Indiana, summer of 1985
   - References to Starcourt Mall, Hawkins Lab, the arcade, and the Upside Down

2. **Interactive Voice Story**
   - GM describes vivid scenes with sensory details
   - Each turn ends with "What do you do?" or similar prompt
   - Player responds via voice, GM continues the story
   - Dynamic storytelling based on player choices

3. **Continuity with Chat History**
   - GM remembers past player decisions
   - Tracks locations visited, items found, NPCs met
   - References previous events in the narrative
   - Maintains story coherence throughout the session

4. **Complete Story Arc**
   - Sessions last 8-15 exchanges
   - Mini-arc structure: discovery → investigation → resolution
   - Encounters with strange phenomena or creatures
   - Satisfying conclusion (finding clues, escaping danger, making discoveries)

5. **Session Persistence**
   - Game sessions saved to JSON files
   - Tracks player name, story log, locations, items, NPCs
   - Turn count and timestamps for each action
   - Saved to `sessions/session_[PlayerName]_[Timestamp].json`

### 🎮 Game Master Features

- **Vivid Scene Descriptions** - Atmospheric storytelling with sensory details
- **Player Choice** - Multiple paths and creative solutions encouraged
- **Dice Rolls** - GM determines when to use dice for uncertain outcomes
- **Mystery & Tension** - Builds suspense through investigation and discovery
- **Concise Responses** - 2-4 sentences per turn for smooth voice interaction
- **Story Tracking** - Logs all player actions and GM responses

## Project Structure

```
Day 8/
├── backend/
│   ├── src/
│   │   ├── __init__.py
│   │   └── game_master.py          # Main Game Master agent
│   ├── sessions/                    # Game session JSON files (generated)
│   │   └── .gitkeep
│   ├── pyproject.toml              # Python dependencies
│   ├── .env.example                # Environment variables template
│   └── .env.local                  # API keys (not in repo)
├── frontend/                        # Next.js frontend (shared with Day 7)
└── README.md                       # This file
```

## Setup Instructions

### Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd "Day 8/backend"
   ```

2. **Install dependencies:**
   ```bash
   pip install livekit-agents livekit-plugins-deepgram livekit-plugins-google livekit-plugins-murf livekit-plugins-silero python-dotenv
   ```

3. **Create `.env.local` file:**
   ```env
   LIVEKIT_URL=wss://your-livekit-url
   LIVEKIT_API_KEY=your-api-key
   LIVEKIT_API_SECRET=your-api-secret
   DEEPGRAM_API_KEY=your-deepgram-key
   GOOGLE_API_KEY=your-google-key
   MURF_API_KEY=your-murf-key
   ```

4. **Run the Game Master:**
   ```bash
   python src/game_master.py dev
   ```

### Frontend Setup

Use the shared frontend from Day 7:

1. **Navigate to frontend directory:**
   ```bash
   cd "../Day 7/frontend"
   ```

2. **Install dependencies (if not already done):**
   ```bash
   pnpm install
   ```

3. **Create `.env.local` file (if not already done):**
   ```env
   LIVEKIT_URL=wss://your-livekit-url
   LIVEKIT_API_KEY=your-api-key
   LIVEKIT_API_SECRET=your-api-secret
   ```

4. **Run the frontend:**
   ```bash
   pnpm dev
   ```

5. **Open browser:**
   Navigate to http://localhost:3000

## How to Play

### Starting Your Adventure

1. **Connect** to the agent at http://localhost:3000
2. **Say:** "Start adventure" or "My name is [Your Name]"
3. **Listen** to the GM's opening scene
4. **Respond** with what you want to do

### Example Gameplay

```
GM: "Welcome, Mike. It's the summer of 1985 in Hawkins, Indiana. 
     The sun is setting as you ride your bike past the new Starcourt Mall. 
     Suddenly, the streetlights flicker and die. In the distance, you hear 
     a strange, low humming sound coming from the direction of the old 
     Hawkins Lab. What do you do?"

You: "I ride my bike toward the sound to investigate"

GM: "You pedal faster, your heart racing. As you approach the abandoned lab, 
     the humming grows louder. The chain-link fence has a hole torn in it, 
     big enough to squeeze through. Through the fence, you see a faint blue 
     glow coming from one of the basement windows. What do you do?"

You: "I go through the fence and look in the window"

GM: "You squeeze through the fence, your jacket catching on the wire. 
     Peering into the basement window, you see strange vines covering the 
     walls, pulsing with that eerie blue light. Roll for perception... 
     You notice a walkie-talkie on the ground near the window, still working. 
     What do you do?"
```

### Voice Commands

- **"Start adventure"** - Begin a new game
- **"Save session"** - Save your current progress
- Describe your actions naturally - the GM will respond to your choices

### Tips for Playing

- **Be specific** - "I search the room" vs "I look under the desk"
- **Be creative** - The GM rewards creative solutions
- **Ask questions** - "What do I see?" "Is there anyone nearby?"
- **Make choices** - The story adapts to your decisions
- **Have fun** - Embrace the 80s Stranger Things atmosphere!

## Session Data Structure

Sessions are saved as JSON files in `backend/sessions/`:

```json
{
  "player_name": "Mike",
  "start_time": "2025-11-28T22:45:00.123456",
  "end_time": "2025-11-28T23:15:00.654321",
  "turn_count": 12,
  "story_log": [
    {
      "turn": 0,
      "type": "gm",
      "text": "Welcome, Mike. It's the summer of 1985...",
      "timestamp": "2025-11-28T22:45:00.123456"
    },
    {
      "turn": 1,
      "type": "player",
      "text": "I ride my bike toward the sound",
      "timestamp": "2025-11-28T22:46:15.789012"
    }
  ],
  "locations_visited": ["Starcourt Mall", "Hawkins Lab"],
  "items_found": ["walkie-talkie"],
  "npcs_met": []
}
```

## Technical Stack

- **Framework:** LiveKit Agents (Python)
- **STT:** Deepgram Nova-3
- **LLM:** Google Gemini 2.5 Flash
- **TTS:** Murf Falcon (en-US-matthew voice)
- **VAD:** Silero
- **Frontend:** Next.js with React (shared from Day 7)

## Game Master Instructions

The GM follows these principles:

1. **Universe:** Hawkins, Indiana, 1985 (Stranger Things setting)
2. **Tone:** Mysterious, suspenseful, with 80s nostalgia
3. **Story Structure:** Discovery → Investigation → Resolution
4. **Response Format:** 2-4 sentences + "What do you do?"
5. **Memory:** Tracks locations, items, NPCs, and past decisions
6. **Dice Rolls:** Used for uncertain outcomes
7. **Player Agency:** Responds to creative choices and solutions

## Resources

- [LiveKit Agents Documentation](https://docs.livekit.io/agents/)
- [Prompting Guide](https://docs.livekit.io/agents/build/prompting/)
- [Function Tools](https://docs.livekit.io/agents/build/tools/)
- [Stranger Things Wiki](https://strangerthings.fandom.com/) - For lore and references

## License

MIT

