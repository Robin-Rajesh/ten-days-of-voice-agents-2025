import json
import logging
import os
from pathlib import Path
from typing import Any, Dict, List, Optional

from dotenv import load_dotenv
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
    inference,
    metrics,
    tokenize,
)
from livekit.plugins import deepgram, google, murf, noise_cancellation, silero
from livekit.plugins.turn_detector.multilingual import MultilingualModel

logger = logging.getLogger("agent")

load_dotenv(".env.local")

CONTENT_FILE = Path("shared-data/day4_tutor_content.json")
DEFAULT_CONTENT = [
    {
        "id": "variables",
        "title": "Variables",
        "summary": "Variables store values so you can reuse or update them later. Give them clear names, assign a value, and reference that label instead of repeating the literal value.",
        "sample_question": "What is a variable and why is it useful?",
    },
    {
        "id": "loops",
        "title": "Loops",
        "summary": "Loops let you repeat an action multiple times. For loops are great when you know how many steps you need, while while-loops keep running until a condition changes.",
        "sample_question": "Explain the difference between a for loop and a while loop.",
    },
]

LEARNING_STATE: Dict[str, Any] = {
    "mode": None,
    "concept_id": None,
    "mastery": {},
}


def load_course_content() -> List[Dict[str, str]]:
    if not CONTENT_FILE.exists():
        logger.warning("Course content file missing, writing default sample.")
        CONTENT_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(CONTENT_FILE, "w", encoding="utf-8") as f:
            json.dump(DEFAULT_CONTENT, f, indent=2)
    try:
        with open(CONTENT_FILE, "r", encoding="utf-8") as f:
            content = json.load(f)
            if isinstance(content, list) and content:
                return content
            raise ValueError("Content file is empty or malformed.")
    except Exception as exc:
        logger.error("Failed to load course content: %s", exc)
        return DEFAULT_CONTENT


COURSE_CONTENT = load_course_content()
CONTENT_BY_ID = {concept["id"]: concept for concept in COURSE_CONTENT}
VOICE_BY_MODE = {
    "learn": "en-US-matthew",
    "quiz": "en-US-alicia",
    "teach_back": "en-US-ken",
}


def get_concept(concept_id: Optional[str]) -> Optional[Dict[str, str]]:
    if not concept_id:
        return None
    return CONTENT_BY_ID.get(concept_id)


class TeachTheTutorAgent(Agent):
    def __init__(self) -> None:
        concept_list = ", ".join(f"{c['title']} ({c['id']})" for c in COURSE_CONTENT)
        super().__init__(
            instructions=f"""You are Teach-the-Tutor, an active recall coach. You are not a wellness companion.

MISSION:
- Greet with "Hi, I'm your Teach-the-Tutor coach" and briefly explain the three modes.
- Modes: learn (voice Matthew), quiz (voice Alicia), teach_back (voice Ken).
- Invite the user to pick a concept and mode. Concepts available: {concept_list}.
- Use the JSON content via tools. Never fabricate content.
- Let the user switch modes or concepts at any time.

MODE GUIDELINES:
- LEARN: Call `get_concept_summary` for the selected concept. Explain clearly and invite follow-up.
- QUIZ: Use `get_sample_question`. Ask one question, listen, then provide concise feedback.
- TEACH_BACK: Ask the user to explain the concept, listen fully, then use `record_teach_back_feedback` to log mastery notes and give qualitative scoring (strong / developing / needs work).

STATE:
- Track the active concept and mode with the provided tools (`set_active_concept`, `set_learning_mode`).
- Encourage the user to cover all concepts eventually; mention mastery progress from `get_mastery_snapshot` when relevant.

TONE:
- Enthusiastic coach, concise, no medical or wellness talk.
- Always reference which mode you're in so the learner stays oriented.
- Never mention Cult.fit or wellness check-ins.
""",
        )

    @function_tool
    async def list_concepts(self, context: RunContext) -> str:
        """List the available concept IDs and titles from the JSON content file."""
        lines = [f"{c['id']}: {c['title']}" for c in COURSE_CONTENT]
        return "Available concepts:\n" + "\n".join(lines)

    @function_tool
    async def set_active_concept(self, context: RunContext, concept_id: str) -> str:
        """Set the concept to focus on (must exist in the JSON file)."""
        concept = CONTENT_BY_ID.get(concept_id)
        if not concept:
            return f"I couldn't find a concept named '{concept_id}'. Please choose one of: {', '.join(CONTENT_BY_ID)}."
        LEARNING_STATE["concept_id"] = concept_id
        return f"Great, we'll focus on {concept['title']}."

    @function_tool
    async def set_learning_mode(self, context: RunContext, mode: str) -> str:
        """Switch between learn, quiz, and teach_back modes."""
        mode = mode.lower()
        if mode not in VOICE_BY_MODE:
            return "Please choose learn, quiz, or teach_back."
        LEARNING_STATE["mode"] = mode
        return f"Mode locked to {mode.upper()} (voice hint: {VOICE_BY_MODE[mode]})."

    @function_tool
    async def get_concept_summary(self, context: RunContext, concept_id: Optional[str] = None) -> str:
        """Fetch the summary text for the active concept (or a provided concept id)."""
        concept = get_concept(concept_id or LEARNING_STATE.get("concept_id"))
        if not concept:
            return "No concept selected yet. Call `set_active_concept` with one of the available IDs."
        return concept["summary"]

    @function_tool
    async def get_sample_question(self, context: RunContext, concept_id: Optional[str] = None) -> str:
        """Return the sample question for quiz or teach_back prompts."""
        concept = get_concept(concept_id or LEARNING_STATE.get("concept_id"))
        if not concept:
            return "No concept selected yet. Call `set_active_concept` before quizzing."
        return concept["sample_question"]

    @function_tool
    async def record_teach_back_feedback(
        self,
        context: RunContext,
        concept_id: str,
        mastery_note: str,
        mastery_level: str,
    ) -> str:
        """Store mastery feedback for a concept after teach_back (levels: strong / developing / needs work)."""
        if mastery_level not in {"strong", "developing", "needs work"}:
            return "Mastery level must be 'strong', 'developing', or 'needs work'."
        concept = CONTENT_BY_ID.get(concept_id)
        if not concept:
            return f"Concept '{concept_id}' is not in the syllabus."
        LEARNING_STATE["mastery"][concept_id] = {
            "title": concept["title"],
            "level": mastery_level,
            "note": mastery_note,
        }
        return f"Logged teach-back feedback for {concept['title']} as {mastery_level}."

    @function_tool
    async def get_mastery_snapshot(self, context: RunContext) -> str:
        """Summarize current mastery notes for the learner."""
        mastery = LEARNING_STATE["mastery"]
        if not mastery:
            return "No mastery notes saved yet."
        lines = [
            f"{data['title']} → {data['level']} (note: {data['note']})"
            for data in mastery.values()
        ]
        return "Mastery log:\n" + "\n".join(lines)


def prewarm(proc: JobProcess):
    proc.userdata["vad"] = silero.VAD.load()


async def entrypoint(ctx: JobContext):
    # Logging setup
    # Add any other context you want in all log entries here
    ctx.log_context_fields = {
        "room": ctx.room.name,
    }

    # Set up a voice AI pipeline using OpenAI, Cartesia, AssemblyAI, and the LiveKit turn detector
    session = AgentSession(
        # Speech-to-text (STT) is your agent's ears, turning the user's speech into text that the LLM can understand
        # See all available models at https://docs.livekit.io/agents/models/stt/
        stt=deepgram.STT(model="nova-3"),
        # A Large Language Model (LLM) is your agent's brain, processing user input and generating a response
        # See all available models at https://docs.livekit.io/agents/models/llm/
        # Allow selecting the default LLM model via env var `DEFAULT_LLM_MODEL`.
        # Example to enable Claude Haiku 4.5 for all clients:
        # DEFAULT_LLM_MODEL=anthropic/claude-haiku-4.5
        llm=(
            inference.LLM(model=os.getenv("DEFAULT_LLM_MODEL"))
            if os.getenv("DEFAULT_LLM_MODEL")
            else google.LLM(model="gemini-2.5-flash")
        ),
        # Text-to-speech (TTS) is your agent's voice, turning the LLM's text into speech that the user can hear
        # See all available models as well as voice selections at https://docs.livekit.io/agents/models/tts/
        tts=murf.TTS(
                voice="en-US-matthew", 
                style="Conversation",
                tokenizer=tokenize.basic.SentenceTokenizer(min_sentence_len=2),
                text_pacing=True
            ),
        # VAD and turn detection are used to determine when the user is speaking and when the agent should respond
        # See more at https://docs.livekit.io/agents/build/turns
        turn_detection=MultilingualModel(),
        vad=ctx.proc.userdata["vad"],
        # allow the LLM to generate a response while waiting for the end of turn
        # See more at https://docs.livekit.io/agents/build/audio/#preemptive-generation
        preemptive_generation=True,
    )

    # To use a realtime model instead of a voice pipeline, use the following session setup instead.
    # (Note: This is for the OpenAI Realtime API. For other providers, see https://docs.livekit.io/agents/models/realtime/))
    # 1. Install livekit-agents[openai]
    # 2. Set OPENAI_API_KEY in .env.local
    # 3. Add `from livekit.plugins import openai` to the top of this file
    # 4. Use the following session setup instead of the version above
    # session = AgentSession(
    #     llm=openai.realtime.RealtimeModel(voice="marin")
    # )

    # Metrics collection, to measure pipeline performance
    # For more information, see https://docs.livekit.io/agents/build/metrics/
    usage_collector = metrics.UsageCollector()

    @session.on("metrics_collected")
    def _on_metrics_collected(ev: MetricsCollectedEvent):
        metrics.log_metrics(ev.metrics)
        usage_collector.collect(ev.metrics)

    async def log_usage():
        summary = usage_collector.get_summary()
        logger.info(f"Usage: {summary}")

    ctx.add_shutdown_callback(log_usage)

    # # Add a virtual avatar to the session, if desired
    # # For other providers, see https://docs.livekit.io/agents/models/avatar/
    # avatar = hedra.AvatarSession(
    #   avatar_id="...",  # See https://docs.livekit.io/agents/models/avatar/plugins/hedra
    # )
    # # Start the avatar and wait for it to join
    # await avatar.start(session, room=ctx.room)

    # Create the agent instance
    agent = TeachTheTutorAgent()
    
    # Start the session, which initializes the voice pipeline and warms up the models
    await session.start(
        agent=agent,
        room=ctx.room,
        room_input_options=RoomInputOptions(
            # For telephony applications, use `BVCTelephony` for best results
            noise_cancellation=noise_cancellation.BVC(),
        ),
    )

    # Join the room and connect to the user
    await ctx.connect()


if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint, prewarm_fnc=prewarm))
