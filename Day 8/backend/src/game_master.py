#!/usr/bin/env python3
"""
Day 8 - Stranger Things Voice Game Master
A D&D-style voice adventure set in the Stranger Things universe (Hawkins, 1985)
"""

import json
import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv

# Load environment variables FIRST, before any LiveKit imports
SCRIPT_DIR = Path(__file__).parent.parent
env_path = SCRIPT_DIR / ".env.local"
load_dotenv(env_path)

# Verify environment variables are loaded
livekit_url = os.getenv("LIVEKIT_URL")
if not livekit_url:
    raise RuntimeError(f"LIVEKIT_URL not found! Tried loading from: {env_path.absolute()}")
print(f"[OK] Loaded LIVEKIT_URL: {livekit_url}")
from livekit.agents import (
    Agent,
    AgentSession,
    JobContext,
    JobProcess,
    MetricsCollectedEvent,
    RoomInputOptions,
    RunContext,
    WorkerOptions,
    cli,
    function_tool,
    metrics,
    tokenize,
)
from livekit.plugins import (
    murf,
    silero,
    google,
    deepgram,
    noise_cancellation,
)
from livekit.plugins.turn_detector.multilingual import MultilingualModel

logger = logging.getLogger("game-master")
logger.setLevel(logging.INFO)

# Sessions directory
SESSIONS_DIR = SCRIPT_DIR / "sessions"
SESSIONS_DIR.mkdir(exist_ok=True)


class StrangerThingsGM(Agent):
    """Stranger Things Game Master - runs D&D-style adventures in Hawkins, 1985"""
    
    def __init__(self) -> None:
        super().__init__(
            instructions=(
                "You are the Game Master for a Stranger Things adventure set in Hawkins, Indiana, 1985. "
                "You run an interactive D&D-style story where the player is a teenager in Hawkins who discovers strange happenings. "
                "\n\n"
                "STARTING THE GAME:\n"
                "- When the player first connects, greet them warmly and ask for their name\n"
                "- Once you have their name, immediately begin the adventure with a vivid opening scene\n"
                "- The opening should place them in Hawkins in summer 1985 and present something mysterious\n"
                "\n\n"
                "UNIVERSE & TONE:\n"
                "- Setting: Hawkins, Indiana, summer of 1985\n"
                "- Atmosphere: Mysterious, suspenseful, with 80s nostalgia\n"
                "- Tone: Dramatic with moments of friendship and courage, inspired by the Stranger Things series\n"
                "- The Upside Down exists, and strange things are happening in Hawkins\n"
                "- References to Starcourt Mall, Hawkins Lab, the arcade, and familiar locations are encouraged\n"
                "\n\n"
                "YOUR ROLE AS GM:\n"
                "- Describe scenes vividly with sensory details (sights, sounds, atmosphere)\n"
                "- Present the player with choices and challenges\n"
                "- ALWAYS end each response with a question asking what the player does next\n"
                "- Remember the player's past decisions and reference them\n"
                "- Keep the story moving forward with mystery and tension\n"
                "- Use dice rolls for uncertain outcomes (you decide when to roll)\n"
                "\n\n"
                "STORY STRUCTURE:\n"
                "- Start with the player discovering something strange in Hawkins\n"
                "- Build tension through investigation and discovery\n"
                "- Include encounters with strange phenomena or creatures\n"
                "- Create a mini-arc that reaches some resolution (finding a clue, escaping danger, making a discovery)\n"
                "- Aim for 8-15 exchanges to complete a session\n"
                "\n\n"
                "IMPORTANT:\n"
                "- Keep responses concise (2-4 sentences per turn)\n"
                "- Always ask 'What do you do?' or similar at the end\n"
                "- Track important story elements (locations visited, items found, NPCs met)\n"
                "- Be responsive to player creativity and choices\n"
                "- Start the adventure immediately after getting the player's name - don't wait for them to ask\n"
            )
        )
        self.room = None
        self.session_data = {
            "player_name": None,
            "start_time": datetime.now().isoformat(),
            "story_log": [],
            "locations_visited": [],
            "items_found": [],
            "npcs_met": [],
            "turn_count": 0,
        }

    async def on_enter(self):
        """Called when the agent enters the session - greet the user immediately"""
        await self.session.say("Welcome, adventurer! I'm your Game Master for today's Stranger Things adventure. What's your name?")

    @function_tool
    async def start_adventure(self, context: RunContext, player_name: str) -> str:
        """Start a new Stranger Things adventure with the player's name."""
        self.session_data["player_name"] = player_name
        self.session_data["turn_count"] = 0
        
        opening = (
            f"Welcome, {player_name}. It's the summer of 1985 in Hawkins, Indiana. "
            f"The sun is setting as you ride your bike past the new Starcourt Mall. "
            f"Suddenly, the streetlights flicker and die. In the distance, you hear a strange, "
            f"low humming sound coming from the direction of the old Hawkins Lab. "
            f"What do you do?"
        )
        
        self.session_data["story_log"].append({
            "turn": 0,
            "type": "gm",
            "text": opening,
            "timestamp": datetime.now().isoformat()
        })
        
        return opening
    
    @function_tool
    async def log_player_action(self, context: RunContext, action: str) -> str:
        """Log the player's action and continue the story."""
        self.session_data["turn_count"] += 1
        
        self.session_data["story_log"].append({
            "turn": self.session_data["turn_count"],
            "type": "player",
            "text": action,
            "timestamp": datetime.now().isoformat()
        })
        
        return f"Logged: {action}"
    
    @function_tool
    async def save_session(self, context: RunContext) -> str:
        """Save the current game session to a JSON file."""
        if not self.session_data["player_name"]:
            return "No active session to save."
        
        filename = SESSIONS_DIR / f"session_{self.session_data['player_name']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        self.session_data["end_time"] = datetime.now().isoformat()
        
        with open(filename, 'w') as f:
            json.dump(self.session_data, f, indent=2)
        
        return f"Session saved! You completed {self.session_data['turn_count']} turns. Thanks for playing!"


def prewarm(proc: JobProcess):
    proc.userdata['vad'] = silero.VAD.load()


async def entrypoint(ctx: JobContext):
    ctx.log_context_fields = {'room': ctx.room.name}

    session = AgentSession(
        stt=deepgram.STT(model='nova-3'),
        llm=google.LLM(model='gemini-2.5-flash'),
        tts=murf.TTS(
            voice='en-US-matthew',
            style='Conversation',
            tokenizer=tokenize.basic.SentenceTokenizer(min_sentence_len=2),
            text_pacing=True,
        ),
        turn_detection=MultilingualModel(),
        vad=ctx.proc.userdata['vad'],
        preemptive_generation=True,
    )

    usage_collector = metrics.UsageCollector()

    @session.on('metrics_collected')
    def _on_metrics_collected(ev: MetricsCollectedEvent):
        metrics.log_metrics(ev.metrics)
        usage_collector.collect(ev.metrics)

    async def log_usage():
        summary = usage_collector.get_summary()
        logger.info(f"Usage: {summary}")

    ctx.add_shutdown_callback(log_usage)

    agent = StrangerThingsGM()
    agent.room = ctx.room

    await session.start(agent=agent, room=ctx.room, room_input_options=RoomInputOptions(noise_cancellation=noise_cancellation.BVC()))

    await ctx.connect()


if __name__ == '__main__':
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint, prewarm_fnc=prewarm))

