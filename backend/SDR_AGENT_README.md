# SDR Agent Implementation

## Overview
This implementation creates a Sales Development Representative (SDR) voice agent for **Razorpay**, an Indian fintech company. The agent can answer questions about the company, collect lead information, and generate summaries.

## What's Been Implemented

### 1. Company FAQ Data (`src/company_faq.json`)
- Comprehensive information about Razorpay
- 12 detailed FAQs covering:
  - Product features
  - Pricing details
  - Integration information
  - Security and compliance
  - Payment methods
  - Customer support
- Structured pricing information
- Key features list

### 2. SDR Persona
The agent acts as a professional Razorpay SDR with the following behavior:
- Warmly greets visitors
- Asks about their business and needs
- Focuses on understanding pain points
- Naturally collects lead information
- Provides accurate information from the FAQ
- Wraps up with a summary when done

### 3. Three Function Tools

#### a) `lookup_faq(query)`
- Searches the FAQ database using keyword matching
- Returns relevant FAQs based on user questions
- Handles questions about:
  - Products and features
  - Pricing
  - Integration
  - Security
  - Payment methods
  - And more

#### b) `save_lead_info(field, value)`
- Stores lead information as the conversation progresses
- Tracks 7 key fields:
  - Name
  - Company
  - Email
  - Role
  - Use case
  - Team size
  - Timeline

#### c) `generate_summary(conversation_summary)`
- Triggered when user indicates they're done
- Saves all collected lead data to JSON file
- Generates a verbal summary for the user
- Stores data in `leads/lead_TIMESTAMP.json`

## Files Modified/Created

1. **`src/company_faq.json`** (NEW)
   - Contains all Razorpay company information

2. **`src/agent.py`** (MODIFIED)
   - Added imports: `json`, `os`, `datetime`, `Path`, `function_tool`, `RunContext`
   - Updated `Assistant` class with SDR persona and three function tools
   - Modified `prewarm()` to load FAQ data
   - Modified `entrypoint()` to pass FAQ data to Assistant
   - Maintains lead data state during conversation

3. **`leads/`** (AUTO-CREATED)
   - Directory where lead JSON files are saved
   - Each conversation creates a timestamped file

## How to Use

### 1. Start the Agent
```bash
cd backend
uv run python src/agent.py dev
```

### 2. Start the Frontend
In another terminal:
```bash
cd frontend
pnpm dev
```

### 3. Connect to the Agent
- Open http://localhost:3000
- Start a voice conversation

### 4. Sample Conversation Flow

**Agent:** "Hi! I'm calling from Razorpay. What brought you here today?"

**User:** "I'm looking for a payment solution for my startup"

**Agent:** *Uses lookup_faq* "Great! Let me tell you about Razorpay..."

**Agent:** "Can I get your name and company?"

**User:** "I'm John from TechStartup"

**Agent:** *Uses save_lead_info to store name and company*

**User:** "What's your pricing?"

**Agent:** *Uses lookup_faq to answer about pricing*

**User:** "Thanks, that's all I needed"

**Agent:** *Uses generate_summary* "Thank you for your time! To recap, I spoke with John from TechStartup..."

### 5. Check Saved Leads
After the conversation, check:
```bash
backend/leads/lead_YYYYMMDD_HHMMSS.json
```

Example lead data:
```json
{
  "name": "John Doe",
  "company": "TechStartup",
  "email": "john@techstartup.com",
  "role": "CTO",
  "use_case": "payment gateway for ecommerce",
  "team_size": "10-20",
  "timeline": "next quarter",
  "conversation_notes": [],
  "conversation_summary": "Discussed payment gateway needs...",
  "timestamp": "2025-11-25T19:04:56.123456"
}
```

## Features Implemented

✅ **Primary Goal Complete:**
- SDR persona with proper greeting and conversation flow
- FAQ lookup with keyword search
- Lead information collection (7 fields)
- End-of-call summary generation
- Lead data saved to JSON

## Testing the Agent

1. **Test FAQ Lookup:**
   - Ask: "What does Razorpay do?"
   - Ask: "What are your pricing details?"
   - Ask: "Do you have a free tier?"

2. **Test Lead Collection:**
   - Share your name, company, email
   - Mention your role and use case
   - Discuss team size and timeline

3. **Test Summary:**
   - Say "That's all" or "Thanks, goodbye"
   - Check that lead file is created in `leads/` directory

## Architecture

```
User Voice Input
    ↓
Deepgram STT (Speech-to-Text)
    ↓
Google Gemini LLM (Brain)
    ↓
Function Tools (lookup_faq, save_lead_info, generate_summary)
    ↓
Murf Falcon TTS (Text-to-Speech)
    ↓
User Voice Output
```

## Next Steps (Optional Advanced Goals)

The implementation can be extended with:
1. **Mock Meeting Scheduler** - Book demo slots
2. **CRM-Style Notes** - Add qualification scoring
3. **Persona-Aware Pitching** - Tailor pitch based on role
4. **Follow-up Email Draft** - Auto-generate emails
5. **Return Visitor Recognition** - Remember previous conversations

## Notes

- The agent uses keyword-based FAQ search (simple but effective)
- All lead data is stored locally in JSON files
- The conversation is natural and doesn't force information collection
- The agent only uses information from the FAQ, doesn't hallucinate

## Troubleshooting

**Issue:** FAQ not loading
- **Solution:** Ensure `company_faq.json` exists in `backend/src/`

**Issue:** Lead files not being created
- **Solution:** Check write permissions in backend directory

**Issue:** Agent not using tools
- **Solution:** Ensure the instructions clearly guide when to use tools

**Issue:** Tools not working
- **Solution:** Check that `function_tool` and `RunContext` are imported

---

**Built for Day 5 of the Murf AI Voice Agents Challenge**
