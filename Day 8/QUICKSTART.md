# Quick Start Guide - Stranger Things Game Master

## 🚀 Get Started in 3 Steps

### Step 1: Start the Backend

Open a terminal and run:

```bash
cd "ten-days-of-voice-agents-2025/Day 8/backend"
python src/game_master.py dev
```

**Expected output:**
```
INFO   livekit.agents   process initialized
```

Keep this terminal running!

### Step 2: Start the Frontend

Open a **new terminal** and run:

```bash
cd "ten-days-of-voice-agents-2025/Day 7/frontend"
pnpm dev
```

**Expected output:**
```
ready - started server on 0.0.0.0:3000
```

Keep this terminal running too!

### Step 3: Play the Game

1. Open your browser to: **http://localhost:3000**
2. Click **"Connect"**
3. Say: **"Start adventure, my name is [Your Name]"**
4. Listen to the Game Master and respond with your actions!

## 🎮 Example Gameplay

```
You: "Start adventure, my name is Mike"

GM: "Welcome, Mike. It's the summer of 1985 in Hawkins, Indiana. 
     The sun is setting as you ride your bike past the new Starcourt Mall. 
     Suddenly, the streetlights flicker and die. In the distance, you hear 
     a strange, low humming sound coming from the direction of the old 
     Hawkins Lab. What do you do?"

You: "I ride my bike toward the sound"

GM: "You pedal faster, your heart racing. As you approach the abandoned lab, 
     the humming grows louder. The chain-link fence has a hole torn in it. 
     Through the fence, you see a faint blue glow coming from one of the 
     basement windows. What do you do?"

You: "I look through the window"

GM: "Peering into the basement window, you see strange vines covering the 
     walls, pulsing with that eerie blue light. You notice a walkie-talkie 
     on the ground near the window, still working. What do you do?"
```

## 💾 Saving Your Game

When you're done playing, say:

```
"Save session"
```

Your adventure will be saved to:
```
Day 8/backend/sessions/session_[YourName]_[Timestamp].json
```

## 🔧 Troubleshooting

### Backend won't start

**Check:**
- Is `.env.local` file present in `Day 8/backend/`?
- Are all API keys configured?
- Is Python 3.9+ installed?

**Fix:**
```bash
# Copy from Day 7 if needed
cp "Day 7/backend/.env.local" "Day 8/backend/.env.local"
```

### Frontend won't start

**Check:**
- Is pnpm installed? (`pnpm --version`)
- Are dependencies installed?

**Fix:**
```bash
cd "Day 7/frontend"
pnpm install
pnpm dev
```

### Can't connect in browser

**Check:**
- Are both backend AND frontend running?
- Is the URL http://localhost:3000?
- Check browser console for errors (F12)

### GM doesn't respond

**Try:**
- Refresh the browser page
- Disconnect and reconnect
- Check that both terminals are still running
- Say "Start adventure" to begin

## 🎯 Tips for Playing

1. **Be specific** - "I search the desk" vs "I look around"
2. **Be creative** - Try unusual solutions!
3. **Ask questions** - "What do I see?" "Is anyone nearby?"
4. **Make choices** - The story adapts to you
5. **Have fun** - Embrace the Stranger Things vibe!

## 📝 What to Say

### Starting
- "Start adventure"
- "My name is [Name]"
- "Begin the game"

### Actions
- "I investigate the [thing]"
- "I go to [place]"
- "I talk to [person]"
- "I pick up the [item]"
- "I run away"
- "I hide"

### Questions
- "What do I see?"
- "Is there anyone nearby?"
- "What's that sound?"
- "Can I use my [item]?"

### Ending
- "Save session"
- "End the game"

## 🌟 Enjoy Your Adventure!

You're now ready to explore the mysteries of Hawkins, Indiana!

Remember: The Game Master adapts to your choices, so there's no "wrong" way to play. Be creative, be brave, and watch out for the Upside Down! 🎲👾

