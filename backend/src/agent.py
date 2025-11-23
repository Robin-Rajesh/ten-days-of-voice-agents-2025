import json
import logging
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
    RunContext,
    WorkerOptions,
    cli,
    function_tool,
    metrics,
    tokenize,
)
from livekit.plugins import murf, silero, google, deepgram, noise_cancellation
from livekit.plugins.turn_detector.multilingual import MultilingualModel

logger = logging.getLogger("agent")

load_dotenv(".env.local")

# Order state structure
ORDER_STATE = {
    "drinkType": None,
    "size": None,
    "milk": None,
    "extras": [],
    "name": None,
}


class BaristaAgent(Agent):
    def __init__(self) -> None:
        super().__init__(
            instructions="""You are Alex, a friendly barista at Brew & Bean Coffee Shop. Always mention you're from the cafe when greeting customers.

Collect: drinkType, size, milk, extras, name. Ask ONE question at a time. Keep responses SHORT - 5-10 words max. Be warm but brief.
Use tools immediately when customer provides information. Once complete, save the order.

When greeting, say something like "Hi, welcome to Brew & Bean Cafe" or "Hello from Brew & Bean Cafe".

CRITICAL: Respond FAST. Keep answers under 10 words. No explanations unless asked.""",
        )
        self.room = None  # Will be set when session starts
    
    async def _publish_order_update(self, context: RunContext) -> None:
        """Helper function to publish order state updates to the frontend."""
        if not self.room:
            return  # Can't publish without room
        
        try:
            payload = json.dumps({
                "type": "order_update",
                "data": {
                    "drinkType": ORDER_STATE["drinkType"],
                    "size": ORDER_STATE["size"],
                    "milk": ORDER_STATE["milk"],
                    "extras": ORDER_STATE["extras"],
                    "name": ORDER_STATE["name"],
                }
            })
            
            await self.room.local_participant.publish_data(
                payload=payload.encode('utf-8'),
                reliable=True,
            )
            logger.info("Published order update to frontend")
        except Exception as e:
            logger.error(f"Failed to publish order update: {e}")

    @function_tool
    async def update_drink_type(self, context: RunContext, drink_type: str) -> str:
        """Update the drink type in the order.
        
        Args:
            drink_type: The type of drink the customer wants (e.g., latte, cappuccino, americano, espresso, mocha)
        """
        ORDER_STATE["drinkType"] = drink_type
        logger.info(f"Updated drink type: {drink_type}")
        await self._publish_order_update(context)
        return f"{drink_type}. What size?"

    @function_tool
    async def update_size(self, context: RunContext, size: str) -> str:
        """Update the size of the drink in the order.
        
        Args:
            size: The size of the drink (small, medium, large, or tall, grande, venti)
        """
        ORDER_STATE["size"] = size
        logger.info(f"Updated size: {size}")
        await self._publish_order_update(context)
        return f"{size}. What milk?"

    @function_tool
    async def update_milk(self, context: RunContext, milk: str) -> str:
        """Update the milk type in the order.
        
        Args:
            milk: The type of milk (whole milk, skim milk, almond milk, oat milk, soy milk, coconut milk, or none)
        """
        ORDER_STATE["milk"] = milk
        logger.info(f"Updated milk: {milk}")
        await self._publish_order_update(context)
        return f"{milk}. Any extras?"

    @function_tool
    async def update_extras(self, context: RunContext, extras: list[str]) -> str:
        """Update the extras in the order.
        
        Args:
            extras: A list of extras the customer wants (e.g., ["whipped cream", "caramel"] or ["extra shot"])
        """
        ORDER_STATE["extras"] = extras
        logger.info(f"Updated extras: {extras}")
        await self._publish_order_update(context)
        return f"Added. Your name?"

    @function_tool
    async def update_name(self, context: RunContext, name: str) -> str:
        """Update the customer's name in the order.
        
        Args:
            name: The customer's name for the order
        """
        ORDER_STATE["name"] = name
        logger.info(f"Updated name: {name}")
        await self._publish_order_update(context)
        return f"Thanks {name}. Saving your order now."

    @function_tool
    async def check_order_complete(self, context: RunContext) -> str:
        """Check if the order has all required fields filled.
        
        Returns a message indicating which fields are still missing, or confirms the order is complete.
        """
        missing = []
        if not ORDER_STATE["drinkType"]:
            missing.append("drink type")
        if not ORDER_STATE["size"]:
            missing.append("size")
        if not ORDER_STATE["milk"]:
            missing.append("milk type")
        if not ORDER_STATE["name"]:
            missing.append("name")
        
        if missing:
            return f"I still need to know your {', '.join(missing)}. Let me ask you about that."
        else:
            return "Your order is complete! Let me save it for you."

    @function_tool
    async def save_order(self, context: RunContext) -> str:
        """Save the complete order to a JSON file. Only call this when all order fields are filled.
        
        The order will be saved to a file named with the customer's name and timestamp.
        """
        # Check if order is complete
        if not all([ORDER_STATE["drinkType"], ORDER_STATE["size"], ORDER_STATE["milk"], ORDER_STATE["name"]]):
            return "I can't save the order yet. I'm still missing some information. Let me check what we need."
        
        # Create orders directory if it doesn't exist
        orders_dir = Path("orders")
        orders_dir.mkdir(exist_ok=True)
        
        # Create filename with customer name and timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_name = "".join(c for c in ORDER_STATE["name"] if c.isalnum() or c in (' ', '-', '_')).strip()
        filename = orders_dir / f"order_{safe_name}_{timestamp}.json"
        
        # Prepare order data
        order_data = {
            "drinkType": ORDER_STATE["drinkType"],
            "size": ORDER_STATE["size"],
            "milk": ORDER_STATE["milk"],
            "extras": ORDER_STATE["extras"],
            "name": ORDER_STATE["name"],
            "timestamp": datetime.now().isoformat(),
        }
        
        # Save to JSON file
        with open(filename, "w") as f:
            json.dump(order_data, f, indent=2)
        
        logger.info(f"Order saved to {filename}")
        
        # Reset order state for next order
        ORDER_STATE["drinkType"] = None
        ORDER_STATE["size"] = None
        ORDER_STATE["milk"] = None
        ORDER_STATE["extras"] = []
        ORDER_STATE["name"] = None
        
        return f"Perfect! I've saved your order, {order_data['name']}. Your {order_data['size']} {order_data['drinkType']} with {order_data['milk']} is being prepared. Is there anything else I can help you with?"


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

    # Create the agent instance
    agent = BaristaAgent()
    
    # Store room reference in agent for data publishing
    agent.room = ctx.room
    
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
