import json
import logging
import os
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
from livekit.agents import (
    Agent,
    AgentSession,
    JobContext,
    JobProcess,
    MetricsCollectedEvent,
    RoomInputOptions,
    WorkerOptions,
    cli,
    metrics,
    tokenize,
    function_tool,
    RunContext
)
from livekit.plugins import murf, silero, google, deepgram, noise_cancellation
from livekit.plugins.turn_detector.multilingual import MultilingualModel

logger = logging.getLogger("agent")

load_dotenv(".env.local")


class Assistant(Agent):
    def __init__(self, faq_data: dict) -> None:
        super().__init__(
            instructions="""You are a friendly and professional Sales Development Representative (SDR) for Razorpay.
            
            Your role is to:
            1. Warmly greet visitors and introduce yourself as a Razorpay SDR
            2. Ask what brought them here and what they're working on
            3. Understand their business needs and pain points
            4. Answer their questions about Razorpay's products, features, and pricing using the FAQ tool
            5. Naturally collect lead information during the conversation (name, company, email, role, use case, team size, timeline)
            6. Keep the conversation focused on understanding their needs and how Razorpay can help
            
            Important guidelines:
            - Be conversational and natural, not robotic
            - Ask one question at a time, don't overwhelm the user
            - Use the lookup_faq tool whenever they ask about Razorpay's products, features, pricing, or capabilities
            - Use the save_lead_info tool to store information as you learn about them
            - Don't make up information - if you don't know something, check the FAQ or admit you need to find out
            - Keep responses concise and avoid complex formatting
            - When the user indicates they're done (says goodbye, thanks, that's all, etc.), use the generate_summary tool to wrap up
            
            Your goal is to qualify leads and understand if Razorpay is a good fit for their business.""",
        )
        self.faq_data = faq_data
        self.lead_data = {
            "name": None,
            "company": None,
            "email": None,
            "role": None,
            "use_case": None,
            "team_size": None,
            "timeline": None,
            "conversation_notes": []
        }

    @function_tool
    async def lookup_faq(self, context: RunContext, query: str):
        """Look up information about Razorpay from the company FAQ database.
        
        Use this tool whenever the user asks about:
        - What Razorpay does
        - Who Razorpay is for
        - Pricing and plans
        - Features and capabilities
        - Integration details
        - Security and compliance
        - Payment methods
        - Any other product-related questions
        
        Args:
            query: The user's question or topic they're asking about (e.g. "pricing", "payment methods", "who is this for")
        """
        logger.info(f"Looking up FAQ for query: {query}")
        
        # Simple keyword-based search through FAQs
        query_lower = query.lower()
        relevant_faqs = []
        
        # Search through all FAQs
        for faq in self.faq_data.get("faqs", []):
            question_lower = faq["question"].lower()
            answer_lower = faq["answer"].lower()
            
            # Check if query keywords appear in question or answer
            if any(word in question_lower or word in answer_lower for word in query_lower.split()):
                relevant_faqs.append(faq)
        
        if not relevant_faqs:
            return f"I don't have specific information about '{query}' in our FAQ. Let me provide general information: {self.faq_data.get('description', '')}"
        
        # Return the most relevant FAQs (up to 2)
        response = "\n\n".join([f"Q: {faq['question']}\nA: {faq['answer']}" for faq in relevant_faqs[:2]])
        return response

    @function_tool
    async def save_lead_info(self, context: RunContext, field: str, value: str):
        """Save information about the lead/prospect as you learn it during the conversation.
        
        Use this tool to store lead information as the user shares it naturally in conversation.
        
        Args:
            field: The type of information (must be one of: name, company, email, role, use_case, team_size, timeline)
            value: The actual information shared by the user
        """
        valid_fields = ["name", "company", "email", "role", "use_case", "team_size", "timeline"]
        
        if field not in valid_fields:
            logger.warning(f"Invalid field: {field}. Must be one of {valid_fields}")
            return f"Error: Invalid field. Must be one of: {', '.join(valid_fields)}"
        
        self.lead_data[field] = value
        logger.info(f"Saved lead info - {field}: {value}")
        
        return f"Got it, I've noted down your {field}: {value}"

    @function_tool
    async def generate_summary(self, context: RunContext, conversation_summary: str):
        """Generate and save a summary of the conversation when the user is ready to end the call.
        
        Use this tool when the user indicates they're done (says goodbye, thanks, that's all, I'm done, etc.).
        
        Args:
            conversation_summary: A brief summary of what was discussed, the user's needs, and key points from the conversation
        """
        logger.info("Generating end-of-call summary")
        
        # Add conversation summary to lead data
        self.lead_data["conversation_summary"] = conversation_summary
        self.lead_data["timestamp"] = datetime.now().isoformat()
        
        # Save to JSON file
        leads_dir = Path("leads")
        leads_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = leads_dir / f"lead_{timestamp}.json"
        
        with open(filename, "w") as f:
            json.dump(self.lead_data, f, indent=2)
        
        logger.info(f"Lead data saved to {filename}")
        
        # Generate verbal summary
        name = self.lead_data.get("name", "the prospect")
        company = self.lead_data.get("company", "their company")
        use_case = self.lead_data.get("use_case", "their business needs")
        timeline = self.lead_data.get("timeline", "to be determined")
        
        summary = f"Thank you for your time! To recap, I spoke with {name} from {company}. "
        summary += f"They're interested in {use_case}. "
        summary += f"Timeline: {timeline}. "
        summary += "I've saved all the details and someone from our team will follow up soon."
        
        return summary


def prewarm(proc: JobProcess):
    proc.userdata["vad"] = silero.VAD.load()
    
    # Load FAQ data
    faq_path = Path(__file__).parent / "company_faq.json"
    with open(faq_path, "r") as f:
        proc.userdata["faq_data"] = json.load(f)
    
    logger.info("FAQ data loaded successfully")


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
        llm=google.LLM(
                model="gemini-2.5-flash",
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

    # Get FAQ data from prewarm
    faq_data = ctx.proc.userdata.get("faq_data", {})
    
    # Start the session, which initializes the voice pipeline and warms up the models
    await session.start(
        agent=Assistant(faq_data=faq_data),
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
