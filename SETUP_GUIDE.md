# Setup Guide for Day 1 Challenge

This guide will help you complete the Day 1 challenge by setting up all required API keys and getting your voice agent running.

## ✅ Completed Steps

1. ✅ Environment files created (`.env.example` and `.env.local` in both backend and frontend)
2. ✅ Backend dependencies installed
3. ✅ Frontend dependencies installed  
4. ✅ Required models downloaded (Silero VAD, LiveKit turn detector)

## 🔑 Required API Keys

You need to obtain the following API keys and add them to your `.env.local` files:

### 1. LiveKit Credentials
**Location:** `backend/.env.local` and `frontend/.env.local`

1. Sign up at [https://cloud.livekit.io/](https://cloud.livekit.io/)
2. Create a new project
3. Navigate to your project settings
4. Copy the following values:
   - `LIVEKIT_URL` (WebSocket URL, e.g., `wss://your-project.livekit.cloud`)
   - `LIVEKIT_API_KEY` (API Key)
   - `LIVEKIT_API_SECRET` (API Secret)

**Alternative:** Use LiveKit CLI to automatically populate:
```bash
# Install LiveKit CLI first (see below)
lk cloud auth
lk app env -w -d backend/.env.local
```

### 2. Murf Falcon TTS API Key
**Location:** `backend/.env.local`

1. Sign up at [https://murf.ai/api](https://murf.ai/api)
2. Navigate to API settings
3. Generate and copy your API key
4. Add to `backend/.env.local`:
   ```
   MURF_API_KEY=your_murf_api_key_here
   ```

### 3. Google Gemini API Key
**Location:** `backend/.env.local`

1. Go to [https://aistudio.google.com/apikey](https://aistudio.google.com/apikey)
2. Create a new API key
3. Copy the key
4. Add to `backend/.env.local`:
   ```
   GOOGLE_API_KEY=your_google_api_key_here
   ```

### 4. Deepgram API Key (for Speech-to-Text)
**Location:** `backend/.env.local`

1. Sign up at [https://console.deepgram.com/signup](https://console.deepgram.com/signup)
2. Create a new project
3. Generate an API key
4. Add to `backend/.env.local`:
   ```
   DEEPGRAM_API_KEY=your_deepgram_api_key_here
   ```

## 📝 Configuring Environment Files

After obtaining your API keys:

1. **Backend Configuration:**
   - Edit `backend/.env.local`
   - Replace all `your_*_here` placeholders with your actual API keys

2. **Frontend Configuration:**
   - Edit `frontend/.env.local`
   - Replace the LiveKit credentials with your actual values
   - Make sure `NEXT_PUBLIC_LIVEKIT_URL`, `LIVEKIT_API_KEY`, and `LIVEKIT_API_SECRET` match your backend values

## 🖥️ Installing LiveKit Server (Local Development)

Since you're on Windows, you have a few options:

### Option 1: Using Docker (Recommended)
1. Install Docker Desktop from [https://www.docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop)
2. Run LiveKit server in Docker:
   ```bash
   docker run --rm -p 7880:7880 -p 7881:7881 -p 7882:7882/udp -p 50000-50100:50000-50100/udp livekit/livekit-server --dev
   ```

### Option 2: Using LiveKit Cloud (Easiest)
Instead of running a local server, use LiveKit Cloud:
- You already have credentials from step 1 above
- No local server installation needed
- Just use your cloud URL in the environment files

### Option 3: Manual Installation (Advanced)
For Windows, you can download the LiveKit server binary:
1. Visit [https://github.com/livekit/livekit/releases](https://github.com/livekit/livekit/releases)
2. Download the Windows executable
3. Run it with: `livekit-server --dev`

**Note:** For Day 1, using LiveKit Cloud (Option 2) is the easiest and fastest approach!

## 🚀 Running the Application

You have two options to start the application:

### Option A: Using the convenience script (All services)

**Note:** The `start_app.sh` script is for Unix/Linux/Mac. On Windows, you'll need to run services separately.

### Option B: Run services individually (Windows)

Open **3 separate terminal windows**:

**Terminal 1 - LiveKit Server (if using local):**
```bash
# If using Docker:
docker run --rm -p 7880:7880 -p 7881:7881 -p 7882:7882/udp -p 50000-50100:50000-50100/udp livekit/livekit-server --dev

# If using LiveKit Cloud, skip this terminal - your backend will connect to the cloud
```

**Terminal 2 - Backend Agent:**
```bash
cd ten-days-of-voice-agents-2025\backend
uv run python src/agent.py dev
```

**Terminal 3 - Frontend:**
```bash
cd ten-days-of-voice-agents-2025\frontend
pnpm dev
```

### Option C: Using LiveKit Cloud (No local server needed)

If you're using LiveKit Cloud, you only need 2 terminals:

**Terminal 1 - Backend Agent:**
```bash
cd ten-days-of-voice-agents-2025\backend
uv run python src/agent.py dev
```

**Terminal 2 - Frontend:**
```bash
cd ten-days-of-voice-agents-2025\frontend
pnpm dev
```

## 🌐 Accessing the Application

Once all services are running:
1. Open your browser
2. Navigate to: `http://localhost:3000`
3. Click "Start call" to begin talking with your voice agent!

## ✅ Verifying Everything Works

1. **Backend is running:** You should see logs like "Agent ready" or "Connected to LiveKit"
2. **Frontend is running:** Browser should load at `http://localhost:3000`
3. **Connection works:** Click "Start call" and you should be able to talk to the agent

## 📹 Day 1 Challenge Completion

Once your agent is running:
1. ✅ Have a brief conversation with the agent
2. ✅ Record a short video of your session
3. ✅ Post on LinkedIn with:
   - Description of what you did for Day 1
   - Mention you're building with **Murf Falcon** - the fastest TTS API
   - Tag **@Murf AI** (official handle)
   - Use hashtags: **#MurfAIVoiceAgentsChallenge** and **#10DaysofAIVoiceAgents**

## 🆘 Troubleshooting

### Backend won't start
- Check that all API keys are correctly set in `backend/.env.local`
- Ensure you've run `uv sync` to install dependencies
- Make sure you've downloaded models: `uv run python src/agent.py download-files`

### Frontend won't start
- Check that LiveKit credentials are set in `frontend/.env.local`
- Ensure you've run `pnpm install` to install dependencies

### Can't connect to agent
- Verify LiveKit server is running (if using local) or that cloud credentials are correct
- Check that both backend and frontend are using the same LiveKit URL and credentials
- Make sure the backend agent is running and shows "Agent ready" in logs

### Agent not responding
- Check backend logs for errors
- Verify all API keys (MURF_API_KEY, GOOGLE_API_KEY, DEEPGRAM_API_KEY) are valid
- Check browser console for any connection errors

## 🎉 Good Luck!

You're all set to complete Day 1 of the challenge! Once everything is running, have fun talking to your voice agent!


