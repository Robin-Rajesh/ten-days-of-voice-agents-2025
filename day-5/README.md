# Day 5 - SDR Voice Agent

## Challenge: Sales Development Representative (SDR) Agent

This implementation creates a voice-based Sales Development Representative that can:
- Answer questions about Razorpay (Indian fintech company)
- Collect lead information naturally during conversation
- Generate summaries and save lead data

## What's Implemented

### ✅ Primary Goal Complete

1. **Company Selection**: Razorpay - Indian payment gateway and banking platform
2. **SDR Persona**: Professional, conversational sales representative
3. **FAQ System**: 12 comprehensive FAQs covering products, pricing, features
4. **Lead Collection**: Captures 7 fields (name, company, email, role, use case, team size, timeline)
5. **End-of-Call Summary**: Verbal summary + JSON file with all lead data

### 🎨 Frontend Customization

- Khan Academy branding with banner image
- Custom accent colors
- Modified welcome screen with large centered banner

## Key Features

### Backend (`backend/src/agent.py`)

Three custom function tools:

1. **`lookup_faq(query)`** - Searches Razorpay FAQ database
2. **`save_lead_info(field, value)`** - Stores lead information
3. **`generate_summary(conversation_summary)`** - Saves data and provides summary

### Frontend

- Large centered banner on welcome screen
- Khan Academy themed interface
- "Start learning session" button

## Files Structure

```
day-5/
├── backend/
│   ├── src/
│   │   ├── agent.py                 # SDR agent implementation
│   │   └── company_faq.json         # Razorpay FAQ database
│   ├── leads/                       # Generated lead files
│   └── SDR_AGENT_README.md          # Detailed documentation
├── frontend/
│   ├── app-config.ts                # Khan Academy branding
│   ├── components/
│   │   └── app/welcome-view.tsx     # Custom welcome screen
│   └── public/
│       └── banner-772x250.png       # Banner image
└── README.md                        # This file
```

## How to Run

### 1. Start Backend

```powershell
cd day-5/backend
$env:LIVEKIT_URL="wss://voice-agents-dx87aoa8.livekit.cloud"
$env:LIVEKIT_API_KEY="APIAsmKErmZ6Y8q"
$env:LIVEKIT_API_SECRET="rHCTV3K9GDHDrJ560SMQwnAletvfdkfrpKzfYtbXyf5A"
uv run python src/agent.py dev
```

### 2. Start Frontend

```powershell
cd day-5/frontend
pnpm dev
```

### 3. Test the Agent

Open http://localhost:3000 (or 3004) and:

1. Click "Start learning session"
2. Ask about Razorpay:
   - "What does Razorpay do?"
   - "What's your pricing?"
   - "Do you have a free tier?"
3. Share your information:
   - Name, company, email
   - Role and use case
   - Team size and timeline
4. Say "That's all" or "Thanks, goodbye" to trigger summary
5. Check `backend/leads/` for saved lead JSON

## Sample Conversation

```
Agent: Hi! I'm calling from Razorpay. What brought you here today?
User: I need a payment solution for my startup
Agent: [Uses lookup_faq] Great! Let me tell you about Razorpay...
Agent: Can I get your name and company?
User: I'm John from TechStartup
Agent: [Uses save_lead_info] Got it, I've noted down your name: John
User: What's your pricing?
Agent: [Uses lookup_faq] Razorpay charges 2% for domestic transactions...
User: Thanks, that's all
Agent: [Uses generate_summary] Thank you! I spoke with John from TechStartup...
```

## Lead Data Output

Saved in `backend/leads/lead_TIMESTAMP.json`:

```json
{
  "name": "John Doe",
  "company": "TechStartup",
  "email": "john@techstartup.com",
  "role": "CTO",
  "use_case": "payment gateway for ecommerce",
  "team_size": "10-20",
  "timeline": "next quarter",
  "conversation_summary": "Discussed payment needs...",
  "timestamp": "2025-11-25T19:00:00.000000"
}
```

## Technologies Used

- **LiveKit Agents** - Voice AI framework
- **Deepgram** - Speech-to-text
- **Google Gemini** - LLM brain
- **Murf Falcon** - Ultra-fast text-to-speech
- **Next.js** - Frontend framework

## Challenge Completion

✅ SDR persona with warm greeting  
✅ FAQ-based question answering  
✅ Natural lead information collection  
✅ End-of-call summary generation  
✅ Lead data saved to JSON  
✅ Custom branding and UI  

---

**Built for Day 5 of the Murf AI Voice Agents Challenge**  
**Agent Demos:** #MurfAIVoiceAgentsChallenge #10DaysofAIVoiceAgents
