# LMU Campus LLM - Personality Enhancements 🤖

## Overview

Your LMU Campus LLM chatbot now has **authentic Gen-Z personality** that matches the examples you provided! The chatbot speaks like a real LMU student who's been on The Bluff for years and knows all the campus tea.

## ✨ What's New

### 🎯 Enhanced Personality Features

1. **Authentic Gen-Z Voice**
   - Natural slang: `fr`, `ngl`, `lowkey`, `no cap`, `say less`, `bet`, `periodt`
   - Real student energy, not corporate speak
   - Matches user's vibe and energy level

2. **LMU-Specific Knowledge**
   - 35+ campus locations with personality descriptions
   - LMU slang: `Bluff life`, `C-Store run`, `PROWL moment`, `Gersten vibes`
   - Inside jokes and campus culture references

3. **Conversation Examples Training**
   - 5 specific conversation examples from your reference
   - Teaches the model authentic response patterns
   - Consistent personality across different question types

4. **Optimized Model Parameters**
   - Temperature: `0.8` (higher creativity)
   - Top-p: `0.95` (more diverse responses)
   - Top-k: `50` (creative word choices)
   - Repeat penalty: `1.1` (avoid repetition)

## 🗣️ Personality Examples

### Before vs After

**Before (Generic AI):**
```
User: what should i eat rn?
Bot: I recommend checking out the dining options available on campus. You might want to visit the food court or look into meal plans that suit your dietary preferences.
```

**After (Gen-Z LMU Student):**
```
User: what should i eat rn?
Bot: u hungry-hungry or just bored?
– real hunger = hit up iggy's, get that grilled chicken bowl no cap
– broke & bored = snag snacks from the C-store & manifest a meal
– tryna flirt = get lunch at la monica & hope a cutie sits nearby 💅
```

## 🏫 Campus Knowledge

The chatbot now knows specific LMU spots with personality:

- **The Rock** = main character energy, best outdoor study vibes
- **Burns Backcourt** = the grind location, 2nd floor hits different
- **C-Store** = overpriced but convenient for 2am snack runs
- **Gersten Pavilion** = basketball games get WILD
- **PROWL** = everyone's worst enemy but we need it

## 🔧 Technical Implementation

### Files Modified/Created:

1. **`src/personality_config.py`** (NEW)
   - Modular personality configuration
   - Easy to update conversation examples
   - Centralized campus knowledge base

2. **`src/llm_handler.py`** (ENHANCED)
   - Uses personality configuration
   - Optimized model parameters
   - Enhanced prompt formatting

3. **`config.json`** (UPDATED)
   - Increased max tokens (750)
   - Higher temperature (0.8)
   - Extended timeout (45s)

### System Prompt Structure:

```
1. Personality Core (who you are)
2. Speaking Style (how you talk)
3. Conversation Examples (learning patterns)
4. Campus Knowledge (what you know)
5. Response Guidelines (how to help)
```

## 🚀 Testing the New Personality

Run the demo to see all enhancements:
```bash
python3 personality_demo.py
```

### Suggested Test Questions:

1. `"what even is campus llm?"`
2. `"what should i eat rn?"`
3. `"how do i email my prof when i fumbled an assignment?"`
4. `"where should i study on campus?"`
5. `"i feel like i'm failing everything"`

## 📊 Enhancement Stats

- **System Prompt**: 5,148 characters (comprehensive personality)
- **Conversation Examples**: 5 authentic patterns
- **Campus Knowledge**: 35+ locations/items
- **Gen-Z Expressions**: 22 natural terms
- **LMU-Specific Terms**: 13 campus slang terms

## 🎯 Expected Personality Features

When you use the chatbot, you should see:

✅ **Natural Gen-Z slang** (not forced or overdone)
✅ **LMU-specific references** that make sense
✅ **Authentic student voice** (not corporate)
✅ **Helpful but real** - admits when unsure
✅ **Matches your energy** and tone
✅ **Concise responses** (1-3 sentences usually)
✅ **Formatting used wisely** (bullets, code blocks)
✅ **Emojis sparingly** (0-2 max, where appropriate)

## 🔄 Easy Updates

The modular design makes it easy to:

1. **Add new conversation examples** in `personality_config.py`
2. **Update campus knowledge** as things change
3. **Adjust personality parameters** for fine-tuning
4. **Modify speaking style** rules

## 🛠️ Fine-Tuning Options

If you want to adjust the personality further:

### Make it More Creative:
```python
# In personality_config.py
MODEL_PERSONALITY_PARAMS = {
    "temperature": 0.9,  # Higher = more creative
    "top_p": 0.98,       # Higher = more diverse
}
```

### Make it More Focused:
```python
MODEL_PERSONALITY_PARAMS = {
    "temperature": 0.7,  # Lower = more focused
    "top_k": 30,         # Lower = more predictable
}
```

### Add New Conversation Examples:
```python
# In personality_config.py
CONVERSATION_EXAMPLES.append({
    "user": "your new question",
    "response": "desired chatbot response"
})
```

## 🎉 Ready to Use!

Your chatbot now has the authentic Gen-Z LMU student personality you wanted! It should respond just like the examples you provided - helpful, real, and full of campus knowledge.

The personality will work with both:
- **Direct LLaMA integration** (via Ollama)
- **Fine-tuning workflows** (using the enhanced prompts as training data)

Start chatting and watch your LMU Campus LLM come to life with authentic student personality! 🦁