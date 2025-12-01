#!/usr/bin/env python3
"""
Day 10 - Voice Improv Battle
Single-player improv game show with AI host
"""

import logging
import os
import json
import random
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv

# Load environment variables FIRST
SCRIPT_DIR = Path(__file__).parent.parent
env_path = SCRIPT_DIR / ".env"
if not env_path.exists():
    env_path = SCRIPT_DIR / ".env.local"
load_dotenv(env_path)

# Verify environment variables
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

# Load scenarios
SCENARIOS_FILE = Path(__file__).parent / "scenarios.json"
with open(SCENARIOS_FILE, 'r') as f:
    SCENARIOS_DATA = json.load(f)
    SCENARIOS = SCENARIOS_DATA['scenarios']

print(f"[OK] Loaded {len(SCENARIOS)} improv scenarios")

logger = logging.getLogger("improv-agent")
logger.setLevel(logging.INFO)


class ImprovBattleAgent(Agent):
    """Voice Improv Battle Game Show Host"""
    
    def __init__(self) -> None:
        super().__init__(
            instructions=(
                "You are the host of 'IMPROV BATTLE', a high-energy TV improv game show!\n"
                "\n"
                "YOUR PERSONALITY:\n"
                "- Energetic, witty, and charismatic like a game show host\n"
                "- You give HONEST reactions - not always supportive\n"
                "- Sometimes amused, sometimes unimpressed, sometimes pleasantly surprised\n"
                "- You can tease players lightly, but stay respectful and fun\n"
                "- You're encouraging but also give constructive critique\n"
                "\n"
                "GAME FLOW:\n"
                "1. INTRO: Welcome the player, explain the game briefly\n"
                "2. ROUNDS: Run 3 improv scenarios\n"
                "   - Present the scenario clearly\n"
                "   - Tell the player to start improvising\n"
                "   - Listen to their performance\n"
                "   - When they finish (pause, say 'done', 'end scene', or after ~30 seconds), react\n"
                "3. REACTIONS: After each scene, comment on their performance\n"
                "   - Mix positive and critical feedback\n"
                "   - Be specific about what worked or didn't\n"
                "   - Vary your tone: supportive, neutral, or mildly critical\n"
                "   - Examples:\n"
                "     * 'That was hilarious! I loved how you committed to the character!'\n"
                "     * 'Hmm, that felt a bit rushed. You could have leaned more into the absurdity.'\n"
                "     * 'Interesting choice, but I'm not sure the energy was quite there.'\n"
                "     * 'WOW! That was unexpected and brilliant!'\n"
                "4. CLOSING: After 3 rounds, summarize their improv style and thank them\n"
                "\n"
                "IMPORTANT RULES:\n"
                "- Keep scenarios clear and concise\n"
                "- Don't interrupt during their performance\n"
                "- React naturally - don't force positivity\n"
                "- If they say 'stop game' or 'end show', gracefully end\n"
                "- Track which round you're on (1, 2, or 3)\n"
                "- After round 3, give a closing summary\n"
                "\n"
                "Use the get_next_scenario() function to get scenarios for each round.\n"
                "Use the end_game() function if the player wants to quit early.\n"
            ),
        )
        self.room = None
        self.player_name = None
        self.current_round = 0
        self.max_rounds = 3
        self.rounds = []  # Store {scenario, reaction} for each round
        self.phase = "intro"  # "intro" | "awaiting_improv" | "reacting" | "done"
        self.used_scenario_ids = set()
        
    async def on_enter(self):
        """Called when agent session starts - greet the player"""
        logger.info("Agent entered - starting Improv Battle")
        self.phase = "intro"

        greeting = (
            "Welcome to IMPROV BATTLE! "
            "I'm your host, and we're about to test your improvisation skills! "
            "Here's how it works: I'll give you three different scenarios, "
            "and you'll act them out. I'll react to each performance. "
            "Ready to show me what you've got? What's your name?"
        )

        await self.session.say(greeting, allow_interruptions=True)

    @function_tool
    async def get_next_scenario(self) -> str:
        """
        Get the next improv scenario for the current round.
        Call this when you're ready to present a new scenario to the player.

        Returns:
            The scenario description to present to the player
        """
        if self.current_round >= self.max_rounds:
            return "All rounds complete! Time for the closing summary."

        # Get a random scenario that hasn't been used
        available_scenarios = [s for s in SCENARIOS if s['id'] not in self.used_scenario_ids]

        if not available_scenarios:
            # Reset if we've used all scenarios
            self.used_scenario_ids.clear()
            available_scenarios = SCENARIOS

        scenario = random.choice(available_scenarios)
        self.used_scenario_ids.add(scenario['id'])

        # Increment round
        self.current_round += 1

        # Store scenario info
        self.rounds.append({
            "round": self.current_round,
            "scenario": scenario,
            "reaction": None
        })

        self.phase = "awaiting_improv"

        logger.info(f"Round {self.current_round}: {scenario['title']}")

        # Return the scenario description
        return (
            f"Round {self.current_round} of {self.max_rounds}! "
            f"Here's your scenario: {scenario['description']} "
            f"Take it away!"
        )

    @function_tool
    async def end_game(self, reason: str = "Player requested") -> str:
        """
        End the game early.

        Args:
            reason: Why the game is ending

        Returns:
            Confirmation message
        """
        self.phase = "done"
        logger.info(f"Game ended early: {reason}")

        return (
            f"Understood! Thanks for playing Improv Battle. "
            f"You completed {self.current_round} out of {self.max_rounds} rounds. "
            f"Hope to see you again soon!"
        )


def prewarm(proc: JobProcess):
    """Prewarm function to load VAD model"""
    proc.userdata['vad'] = silero.VAD.load()


async def entrypoint(ctx: JobContext):
    """Main entrypoint for the improv battle agent"""

    # Initialize session with Google Gemini LLM
    session = AgentSession(
        llm=google.LLM(
            model="gemini-2.5-flash",
        ),
        stt=deepgram.STT(
            model="nova-3",
        ),
        tts=murf.TTS(
            voice="en-US-terrell",  # Energetic male voice for game show host
            style="Conversation",
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

    agent = ImprovBattleAgent()
    agent.room = ctx.room

    await session.start(agent=agent, room=ctx.room, room_input_options=RoomInputOptions(noise_cancellation=noise_cancellation.BVC()))
    await ctx.connect()


if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint, prewarm_fnc=prewarm))

