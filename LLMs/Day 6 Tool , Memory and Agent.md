# Day 6 — Tools, Memory, aur ek poora Agent banana
### (deep-dive version, updated for where things stand in 2026)

> Prerequisite: Day 5 (Chain vs Agent, LCEL, `create_agent`/LangGraph). Aaj hum agent
> ke do sabse zaroori building blocks — **Tools** aur **Memory** — gehraai mein
> samjhenge, aur ek poora chhota project bana ke khatam karenge.

---

## 0. Goal

**Hinglish:** Ek agent tab tak "smart" nahi lagta jab tak wo (a) apne knowledge se
bahar ka kaam kar na sake (jaise calculator, database query, ya kisi bhi custom
function ko call karna) — ye **Tools** hain — aur (b) purani baatein yaad na rakh sake
— ye **Memory** hai. Aaj dono seekhenge, aur ek working "Q&A bot" bana ke khatam
karenge.

**English:** An agent isn't really "smart" until it can (a) reach beyond its own
training data by calling external functions — these are **Tools** — and (b) remember
prior turns of a conversation — this is **Memory**. Today covers both, ending in a
working Q&A bot.

---

## 1. Tools — agent ko "haath-pair" dena

**Hinglish:** LangChain khud web-search, calculator, database jaise cheezein provide
nahi karta — wo sirf ek **standard wrapper/adapter** deta hai jisse tum apna koi bhi
function agent ko "available" bana sako. Tool = ek function + ek description jo LLM ko
batata hai "ye kab use karna hai" + ek schema jo batata hai "isko kaunsa input chahiye".

**English:** LangChain doesn't itself provide services like web search or databases —
it provides a standard adapter so you can expose any function to an agent. A tool is a
function + a description (tells the LLM *when* to use it) + a schema (tells the LLM
*what input* it needs).

### Tool banane ke do tareeke

**⚠️ Update:** Original bootcamp material sirf `DynamicStructuredTool` class dikhata
tha. Wo **abhi bhi kaam karti hai**, lekin ab ek halka, functional alternative bhi hai
— `tool()` helper function — jo current docs mein zyada suggest hota hai naye code ke
liye.

**Purana/classic style (`DynamicStructuredTool`):**
```javascript
import { DynamicStructuredTool } from "@langchain/core/tools";
import { z } from "zod";

const getMenuTool = new DynamicStructuredTool({
  name: "getMenu",
  description: "Returns today's menu for a given category (breakfast, lunch, dinner).",
  schema: z.object({
    category: z.string().describe("Type of food. Example: breakfast, lunch, dinner"),
  }),
  func: async ({ category }) => {
    const menus = {
      breakfast: "Aloo Paratha, Poha, Masala Chai",
      lunch: "Paneer Butter Masala, Dal Fry, Jeera Rice, Roti",
      dinner: "Veg Biryani, Raita, Salad, Gulab Jamun",
    };
    return menus[category.toLowerCase()] || "No menu found for that category.";
  },
});
```

**Naya/current style (`tool()` helper):**
```javascript
import { tool } from "@langchain/core/tools";
import { z } from "zod";

const getMenuTool = tool(
  async ({ category }) => {
    const menus = {
      breakfast: "Aloo Paratha, Poha, Masala Chai",
      lunch: "Paneer Butter Masala, Dal Fry, Jeera Rice, Roti",
      dinner: "Veg Biryani, Raita, Salad, Gulab Jamun",
    };
    return menus[category.toLowerCase()] || "No menu found for that category.";
  },
  {
    name: "getMenu",
    description: "Returns today's menu for a given category (breakfast, lunch, dinner).",
    schema: z.object({
      category: z.string().describe("Type of food. Example: breakfast, lunch, dinner"),
    }),
  }
);
```

**IRL analogy — dono style ka farak:** Ye bilkul aisa hai jaise ek form fill karne ke
do tareeke — ek lamba class-based form (`DynamicStructuredTool`, sab kuch explicit
object mein), aur ek chhota function-call style form (`tool()`, jyada concise). Result
same hota hai — LLM ko ek naya "capability" mil jaata hai — bas likhne ka tareeka
halka hai.

### Har part ka matlab (recap, dono style pe applicable)

- **`name`** → internal label jo LLM ke liye hai ("agar menu poochha jaaye, `getMenu`
  use karo")
- **`description`** → **sabse important part** — LLM isi ke basis pe decide karta hai
  *kab* is tool ko call karna hai. Jitni specific description, utna better decision.
- **`schema`** (zod se) → batata hai tool ko kaunsa input chahiye, aur kis type ka
- **`func`** → actual code jo chalta hai jab tool call hota hai

**IRL example:** Description likhna bilkul job-posting likhne jaisa hai — agar tum
vague likhoge ("food se related kuch bhi"), agent confuse ho jaayega kab use kare.
Agar specific likhoge ("returns today's menu for breakfast/lunch/dinner"), agent
sahi waqt pe hi call karega.

---

## 2. Memory — agent ko "yaad" dena

Ye Day 6 ka sabse bada 2026 update hai — original bootcamp `BufferMemory`
(`langchain/memory`) dikhata tha. **Ye ab deprecated hai (v0.3+ se)**. Naya, current
tareeka **LangGraph checkpointer** hai.

### Purana tareeka (ab deprecated, samajhne ke liye zaroori hai kyunki bahut purana code isi mein hai)
```javascript
import { BufferMemory } from "langchain/memory";  // ⚠️ deprecated since v0.3
```

### Naya tareeka — Checkpointer + thread_id

**Hinglish:** LangGraph-backed agents mein memory **checkpointer** ke through kaam
karti hai — ek object jo poore conversation ki "state" (messages) ko save karta hai,
jise ek `thread_id` se identify kiya jaata hai (jaise WhatsApp mein har chat ka apna
alag thread hota hai).

**English:** In LangGraph-backed agents, memory works through a **checkpointer** — an
object that persists the conversation's state (messages), identified by a `thread_id`
(similar to how each WhatsApp chat is its own separate thread).

```javascript
import { MemorySaver } from "@langchain/langgraph";
import { createAgent } from "langchain/agents";

const checkpointer = new MemorySaver();   // dev/testing ke liye — RAM mein rehta hai

const agent = createAgent({
  model: "gemini-2.5-flash",
  tools: [getMenuTool],
  checkpointSaver: checkpointer,
});

const config = { configurable: { thread_id: "sonam-chat-1" } };

// Turn 1
await agent.invoke({ messages: [{ role: "user", content: "Hi, I'm Sonam!" }] }, config);

// Turn 2 — same thread_id, isliye agent ko "Sonam" yaad rahega
await agent.invoke({ messages: [{ role: "user", content: "What's my name?" }] }, config);
```

**IRL analogy:** `thread_id` bilkul ek WhatsApp chat ka naam hai. Agar tum apne dost ke
saath "Family Group" mein baat karo aur "Office Group" mein — dono alag "threads" hain,
alag context/history ke saath. `MemorySaver` in-memory hai (dev/testing ke liye —
server restart hote hi gayab ho jaata hai); production ke liye `PostgresSaver` ya
`MongoDBSaver` use karte hain jo actual database mein persist karte hain.

### ⚠️ Ek zaroori, honest caveat (2026 mein industry isko discuss kar rahi hai)

**Hinglish:** Checkpointer sirf **ek thread ke andar ki** memory handle karta hai
(short-term). Agar tumhe **cross-session** memory chahiye (jaise "user ne pichhle
hafte bola tha wo vegetarian hai, aaj bhi yaad rahe" — alag conversation mein bhi),
uske liye ek **alag `Store` interface** chahiye hoti hai — checkpointer akela ye nahi
karta.

**English:** A checkpointer only handles memory *within* a single thread (short-term).
Cross-session memory (recalling facts from an entirely different past conversation)
requires a separate **Store** interface — a checkpointer alone doesn't provide that.

**Ek known, real limitation (research se, sirf isliye bata raha hoon taaki galat
expectation na bane):** Long-running memory systems mein ek common problem dekha gaya
hai — agent ke paas do conflicting facts store ho jaate hain (jaise Turn 3 mein "user
Python prefer karta hai" aur Turn 47 mein "user ab TypeScript use karta hai") — aur
similarity-search-based retrieval kabhi purana fact wapas la sakta hai. Isliye memory
systems abhi bhi **perfect nahi hain** — ye ek active research area hai, "solved
problem" nahi.

```
CHECKPOINTER (thread-level, short-term):
   thread_id "chat-1" → [msg1, msg2, msg3, ...]   (isi conversation ke andar yaad rahega)

STORE (cross-session, long-term):
   user_id "sonam" → {preferences, facts, past summaries}  (alag conversations ke beech bhi yaad rahega)
```

---

## 3. Poora example — Restaurant Q&A Bot (tool + memory dono ke saath)

```javascript
import { config as loadEnv } from "dotenv";
loadEnv();

import { ChatGoogleGenerativeAI } from "@langchain/google-genai";
import { tool } from "@langchain/core/tools";
import { z } from "zod";
import { createAgent } from "langchain/agents";
import { MemorySaver } from "@langchain/langgraph";

// 1. Model
const model = new ChatGoogleGenerativeAI({
  model: "gemini-2.5-flash",
  temperature: 0.7,
  apiKey: process.env.GOOGLE_API_KEY,
});

// 2. Tool
const getMenuTool = tool(
  async ({ category }) => {
    const menus = {
      breakfast: "Aloo Paratha, Poha, Masala Chai",
      lunch: "Paneer Butter Masala, Dal Fry, Jeera Rice, Roti",
      dinner: "Veg Biryani, Raita, Salad, Gulab Jamun",
    };
    return menus[category.toLowerCase()] || "No menu found for that category.";
  },
  {
    name: "getMenu",
    description: "Returns today's menu for breakfast, lunch, or dinner.",
    schema: z.object({ category: z.string() }),
  }
);

// 3. Memory
const checkpointer = new MemorySaver();

// 4. Agent
const agent = createAgent({
  model,
  tools: [getMenuTool],
  checkpointSaver: checkpointer,
});

// 5. Use it
const config = { configurable: { thread_id: "table-12" } };

const r1 = await agent.invoke(
  { messages: [{ role: "user", content: "What's for dinner today?" }] },
  config
);
console.log(r1.messages.at(-1).content);

const r2 = await agent.invoke(
  { messages: [{ role: "user", content: "Does it have dessert?" }] },
  config   // same thread_id → pichla context (dinner menu) yaad rahega
);
console.log(r2.messages.at(-1).content);
```

**IRL example jo poora flow samjhaata hai:** Ye bilkul ek restaurant waiter jaisa hai
jo (a) menu book (tool) dekh sakta hai jab customer poochhe, aur (b) usi table ke
saath poori conversation yaad rakhta hai (memory) — agar customer bole "usme dessert
hai?", waiter samajh jaata hai "usme" ka matlab "jo dinner menu abhi bataya tha".

---

## 4. Poora Day-6 flow

```
   User: "What's for dinner? Does it have dessert?"
                          │
                          ▼
        ┌─────────────────────────────────────────┐
        │  Agent (LangGraph-backed, createAgent)      │
        └───────────────────┬─────────────────────┘
                          ▼
        ┌─────────────────────────────────────────┐
        │  Turn 1: "dinner?" → router decides:          │
        │  TOOL zaroori hai → getMenuTool("dinner")      │
        │  → "Veg Biryani, Raita, Salad, Gulab Jamun"    │
        └───────────────────┬─────────────────────┘
                          ▼
        ┌─────────────────────────────────────────┐
        │  CHECKPOINTER (thread_id: "table-12")         │
        │  is poore exchange ko save kar leta hai         │
        └───────────────────┬─────────────────────┘
                          ▼
        ┌─────────────────────────────────────────┐
        │  Turn 2: "dessert hai?" → memory se pata chalta │
        │  hai "usme" = dinner menu → answer: "Haan,      │
        │  Gulab Jamun hai"                              │
        └─────────────────────────────────────────┘
```

---

## 5. Revision — apne alfaaz mein bolke dekho

1. Tool = function + description (LLM ke liye "kab use karo") + schema (input format).
   `DynamicStructuredTool` class abhi bhi kaam karti hai, lekin `tool()` helper
   function ab zyada current/recommended tareeka hai.
2. Memory ab `BufferMemory` (deprecated) se **checkpointer + thread_id** pattern mein
   shift ho chuki hai — `MemorySaver` dev ke liye, `PostgresSaver`/`MongoDBSaver`
   production ke liye.
3. Checkpointer sirf **ek thread ke andar** (short-term) memory deta hai; cross-session
   (long-term) memory ke liye alag **Store** interface chahiye hoti hai.
4. Memory systems abhi bhi imperfect hain — conflicting facts store ho sakte hain aur
   retrieval kabhi galat/purana fact utha sakta hai. Ye "solved" problem nahi hai.
5. Ek poora working agent = Model + Tool(s) + Checkpointer (memory), sab
   `createAgent()` mein ek saath diye jaate hain.

---
*Part of the 7-day LLM bootcamp notes — Day 6 of 6 in this set (deep-dive edition).
See `day1.md`-`day4.md` for LLM mechanics, hardware, local models, and prompting, and
`day5.md` for chains, agents, and LCEL basics.*
