# Day 8 - Stranger Things Game Master Testing Guide

## Quick Start Testing

### 1. Start the Backend

```bash
cd "Day 8/backend"
python src/game_master.py dev
```

Expected output:
```
INFO   livekit.agents   process initialized
```

### 2. Start the Frontend

```bash
cd "Day 7/frontend"  # Using shared frontend
pnpm dev
```

Expected output:
```
ready - started server on 0.0.0.0:3000
```

### 3. Open Browser

Navigate to: http://localhost:3000

## Testing Checklist

### ✅ Game Master Persona

**Test:** Does the GM establish the Stranger Things universe?

**Expected:**
- References to Hawkins, Indiana, 1985
- Mentions of Starcourt Mall, Hawkins Lab, or other locations
- 80s atmosphere and Stranger Things tone
- Mysterious, suspenseful storytelling

**Try saying:**
- "Start adventure"
- "My name is Mike"

### ✅ Interactive Story

**Test:** Does the GM describe scenes and ask for player input?

**Expected:**
- Vivid scene descriptions with sensory details
- Each GM response ends with "What do you do?" or similar
- GM responds to player actions
- Story progresses based on choices

**Try saying:**
- "I investigate the sound"
- "I look around"
- "I run away"
- "I call my friends on the walkie-talkie"

### ✅ Continuity & Memory

**Test:** Does the GM remember past decisions?

**Expected:**
- References to previous locations visited
- Mentions items you've found
- Recalls NPCs you've met
- Story builds on past events

**Try:**
1. Visit a location (e.g., "I go to the arcade")
2. Later say: "I go back to the arcade"
3. GM should remember you were there before

### ✅ Story Arc

**Test:** Does the session have a complete mini-arc?

**Expected:**
- Opening: Discovery of something strange
- Middle: Investigation and tension building
- Climax: Encounter or revelation
- Resolution: Finding a clue, escaping, or making a discovery
- 8-15 exchanges total

**Try:**
- Play through a complete session
- Count the number of exchanges
- Check if there's a satisfying conclusion

### ✅ Session Persistence

**Test:** Are sessions saved to JSON files?

**Expected:**
- File created in `backend/sessions/`
- Filename: `session_[PlayerName]_[Timestamp].json`
- Contains story log, locations, items, NPCs
- Turn count and timestamps

**Try saying:**
- "Save session"

**Then check:**
```bash
ls "Day 8/backend/sessions/"
```

## Example Test Session

### Full Playthrough Example

```
Turn 1:
You: "Start adventure, my name is Dustin"
GM: "Welcome, Dustin. It's the summer of 1985 in Hawkins, Indiana..."

Turn 2:
You: "I ride toward the humming sound"
GM: "You pedal faster, approaching the old Hawkins Lab..."

Turn 3:
You: "I look through the fence"
GM: "Peering through the chain-link, you see strange vines..."

Turn 4:
You: "I squeeze through the hole in the fence"
GM: "You carefully slip through. The humming is louder now..."

Turn 5:
You: "I pick up the walkie-talkie"
GM: "You grab the device. It crackles to life..."

Turn 6:
You: "I try to call for help on the walkie-talkie"
GM: "You press the button. Static, then a voice..."

Turn 7:
You: "I ask who's there"
GM: "The voice responds, it's your friend Lucas..."

Turn 8:
You: "I tell Lucas where I am"
GM: "Lucas says he's on his way with the others..."

Turn 9:
You: "I wait for my friends while watching the lab"
GM: "Minutes pass. You see headlights approaching..."

Turn 10:
You: "I wave to my friends"
GM: "Lucas, Mike, and Will arrive on their bikes..."

Turn 11:
You: "I show them the glowing vines"
GM: "They peer through the window, eyes wide..."

Turn 12:
You: "We decide to investigate together"
GM: "You've discovered something strange in Hawkins. The adventure continues... Save session?"

Turn 13:
You: "Save session"
GM: "Session saved! You completed 13 turns. Thanks for playing!"
```

## Common Issues & Solutions

### Issue: GM doesn't start the adventure

**Solution:**
- Make sure to say "Start adventure" or provide your name
- Try: "My name is [Name], start the game"

### Issue: GM responses are too long

**Solution:**
- This is expected - the GM is instructed to keep responses to 2-4 sentences
- If responses are longer, the LLM may need adjustment

### Issue: GM doesn't remember past events

**Solution:**
- The GM uses chat history for memory
- Make sure the session hasn't been restarted
- Check that the conversation is continuous

### Issue: Session not saving

**Solution:**
- Say "Save session" explicitly
- Check that `backend/sessions/` directory exists
- Verify file permissions

## Advanced Testing

### Test Creative Solutions

**Try unusual actions:**
- "I use my bike as a weapon"
- "I try to communicate with the vines"
- "I draw a map of what I've seen"

**Expected:** GM should respond creatively and adapt the story

### Test Dice Rolls

**Try risky actions:**
- "I try to climb the fence"
- "I sneak past the guard"
- "I throw a rock at the window"

**Expected:** GM may introduce dice rolls for uncertain outcomes

### Test NPCs

**Try social interactions:**
- "I talk to the person"
- "I ask them questions"
- "I try to convince them to help"

**Expected:** GM creates believable NPCs and tracks them

## Success Criteria

✅ **Primary Goal Complete** if:
1. GM establishes Stranger Things universe clearly
2. Story is interactive with player choices mattering
3. GM remembers past decisions and references them
4. Session completes a mini-arc in 8-15 turns
5. Sessions are saved to JSON files

## Performance Metrics

- **Response Time:** < 2 seconds per GM response
- **Session Length:** 8-15 exchanges
- **Memory Accuracy:** 100% recall of major events
- **Story Coherence:** Logical progression from start to finish
- **Player Engagement:** Multiple valid choices at each turn

