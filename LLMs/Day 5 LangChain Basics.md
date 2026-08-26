# Day 5 — LangChain Basics: Chains, Agents, aur LCEL
### (deep-dive version, updated for where things stand in 2026)

> Prerequisite: Day 1-4 (LLM mechanics, hardware, local models, prompting). Ab tak
> humne LLM ko *directly* use kiya (Ollama chat, ya ek prompt bhej ke jawab liya). Aaj
> se hum LLM ko ek **bade application** ke andar ek component ki tarah use karna
> seekhenge.

---

## 0. Goal

**Hinglish:** Ek LLM se seedha chat karna ek cheez hai. Lekin agar tumhe ek **poora
system** banana ho — jisme prompt template ho, output structured JSON mein aana ho,
purani conversation yaad rahe, aur zaroorat pade to LLM khud calculator/web-search
jaisa tool use kar le — to tumhe ek framework chahiye jo ye sab pieces ko jodta hai.
**LangChain** yehi karta hai.

**English:** Talking to an LLM directly is one thing. But once you need an actual
system — reusable prompt templates, structured output parsing, memory across turns,
and the ability for the model to call external tools when needed — you need a
framework that wires these pieces together. That's what **LangChain** provides.

---

## 1. LangChain kya hai

**Hinglish:** LangChain ek framework hai (React jaisa, lekin frontend ke liye nahi, LLM
apps ke liye) jo tumhe chhote building blocks deta hai:
- LLMs (GPT, Claude, Gemini, ya Ollama pe chal raha koi local model)
- Prompts (templates)
- Memory (chat history)
- Tools/APIs
- Chains & Agents (inko jodne ka tareeka)

**English:** LangChain is a framework (think React, but for LLM-powered apps instead of
frontends) that gives you small, composable building blocks — LLMs, prompt templates,
memory, tools/APIs, and a way to wire them together as chains or agents.

```
LangChain =  LLM wrapper  +  Prompt templates  +  Memory
           +  Tools/APIs  +  Chains (fixed flow)  +  Agents (dynamic flow)
```

**IRL analogy:** Socho LangChain ek electrician ka tool-kit hai. Bulb (LLM), switch
(prompt), wiring (chains), aur ek smart automation panel (agent) — sab alag-alag
cheezein hain, lekin LangChain unko ek dusre se jodne ka standard tareeka deta hai,
taaki tumhe har baar naye sire se wiring na sochni pade.

---

## 2. Chain vs Agent — sabse zaroori distinction

**Hinglish:** Ye difference poore din ka core hai.

- **Chain** = ek **fixed recipe**. Har baar wahi steps, wahi order mein.
  `Prompt → LLM → Parse → Output`. Koi decision-making nahi.
- **Agent** = ek **smart decision-maker**. Model khud decide karta hai kaunsa tool use
  karna hai, kab karna hai, aur kab final answer dena hai.

**English:**
- A **Chain** is a fixed recipe — the same steps, same order, every time
  (`Prompt → LLM → Parse → Output`). No decision-making involved.
- An **Agent** is a dynamic decision-maker — the LLM itself decides which tool to call,
  when to call it, and when it has enough information to produce a final answer.

```
CHAIN (jaise chai banana):
  Boil water → Add tea leaves → Pour into cup → Serve
  (fixed order, har baar same)

AGENT (jaise ek personal assistant):
  "Book me a flight to Goa under ₹5000"
  → assistant khud decide karta hai: flight API search karo → cheapest chuno → confirm bhejo
  (dynamic — kya karna hai ye khud decide hota hai)
```

| | Chain | Agent |
|---|---|---|
| Sochta hai? | ❌ Nahi | ✅ Haan |
| Dynamic? | ❌ Nahi | ✅ Haan |
| Example | Chatbot jo hamesha "input → GPT → show response" karta hai | AI assistant jo khud decide karta hai search karna hai ya calculator |

**IRL example — bank ka udaharan:** Ek chain wala bot hamesha bolega "aapka balance
X hai" — kyunki uska flow fix hai (balance API call → format → show). Ek agent wala
bot pehle decide karega "ye sawaal balance ke baare mein hai ya loan ke baare mein"
aur uske hisaab se **alag-alag tool** choose karega — ye flexibility hi agent ko
"smart" banati hai.

**Yaad rakhne wali baat:** LangChain sirf "Chains" aur "Agents" tak simit nahi hai —
ye ek poora toolbox hai (prompts, memory, output parsers, document loaders, vector
stores) jisse tum in dono ko bana sakte ho.

---

## 3. Setup — 2026 mein package structure thoda badal gaya hai

**⚠️ Important update:** Original bootcamp material `LLMChain` aur
`initializeAgentExecutorWithOptions` jaisi cheezein use karta tha. **Ye ab
`langchain_classic` / legacy package mein move ho chuki hain** — abhi bhi kaam karti
hain (backward compatibility ke liye), lekin naye projects ke liye LangChain team
**`create_agent`** (jo andar se **LangGraph** use karta hai) recommend karta hai. Hum
neeche **dono** dikhayenge — classic pattern (kyunki zyaadatar tutorials/existing code
abhi bhi ye use karte hain) aur naya recommended pattern.

```bash
npm install langchain @langchain/core @langchain/google-genai dotenv
```

**Key concepts:**
- `@langchain/core` — foundation: prompts kaise format hote hain, chains kaise connect
  hote hain, LCEL (LangChain Expression Language) ka core.
- `@langchain/community` — third-party integrations (SerpAPI, Pinecone, HuggingFace...)
- Provider packages — `@langchain/google-genai` (Gemini), `@langchain/openai`,
  `@langchain/anthropic` — sirf jis provider ki zaroorat hai wahi install karo.
- `langchain` — prebuilt agents/chains/retrievers jo upar wale sab blocks ko smartly
  jodte hain.

**IRL analogy:** `@langchain/core` engine hai, provider packages (Gemini/OpenAI/
Anthropic) alag-alag fuel-types hain jo usi engine mein daal sakte ho, aur `langchain`
package driver hai jo jaanta hai kab clutch dabana hai.

---

## 4. Basic Chain banana (LCEL ke saath — current recommended style)

**Hinglish:** LCEL (LangChain Expression Language) ka matlab hai `.pipe()` use karke
components ko jodna — jaise ek pipeline. Ye purane `LLMChain` class se zyada modern,
readable, aur composable hai.

**English:** LCEL means chaining components together with `.pipe()`, like a data
pipeline. It's the modern, composable replacement for the older `LLMChain` class.

```javascript
import { config } from "dotenv";
config();

import { ChatGoogleGenerativeAI } from "@langchain/google-genai";
import { PromptTemplate } from "@langchain/core/prompts";
import { StringOutputParser } from "@langchain/core/output_parsers";

// 1. Model
const model = new ChatGoogleGenerativeAI({
  model: "gemini-2.5-flash",
  temperature: 0.7,
  apiKey: process.env.GOOGLE_API_KEY,
});

// 2. Prompt
const prompt = PromptTemplate.fromTemplate(
  "You are a helpful assistant. Answer the question: {question}"
);

// 3. Chain via LCEL — prompt → model → parser
const chain = prompt.pipe(model).pipe(new StringOutputParser());

// 4. Run
const response = await chain.invoke({ question: "What is the future of AI in healthcare?" });
console.log(response);
```

**`.pipe()` samjho — water-filter analogy:**
```
PromptTemplate  →  (pipe)  →  Model  →  (pipe)  →  Output Parser
   [pehla filter:      [doosra filter:      [teesra filter:
    input format karta   actual response      raw output ko
    hai]                 generate karta hai]  clean string mein
                                               badalta hai]
```

**IRL example:** `.pipe()` bilkul factory assembly line jaisa hai — raw material
(question) ek station (prompt formatting) se guzarta hai, phir agle station (model)
pe processing hoti hai, phir final packaging station (output parser) se ek clean
product (final answer) nikalta hai. Har station apna specific kaam karta hai, aur pipe
unhe order mein jodta hai.

---

## 5. Agent banana — do tareeke (classic vs current)

### 5a. Classic pattern (`createToolCallingAgent` + `AgentExecutor`) — abhi bhi kaam karta hai

**Hinglish:** Ye wahi pattern hai jo zyaadatar existing tutorials/bootcamps sikhate
hain. Prompt banao, agent banao, executor banao.

```javascript
import { ChatPromptTemplate } from "@langchain/core/prompts";
import { AgentExecutor, createToolCallingAgent } from "langchain/agents";

const prompt = ChatPromptTemplate.fromMessages([
  ["system", "You are a helpful assistant that uses tools when needed."],
  ["placeholder", "{chat_history}"],
  ["human", "{input}"],
  ["placeholder", "{agent_scratchpad}"],
]);

const agent = await createToolCallingAgent({ llm: model, tools: [myTool], prompt });
const executor = new AgentExecutor({ agent, tools: [myTool], maxIterations: 10 });

const result = await executor.invoke({ input: "What's for lunch?" });
console.log(result.output);
```

**Note:** `{agent_scratchpad}` wahi jagah hai jahan agent apna internal
reasoning/tool-calls "sochta" hai before final answer — Day 1 ke reasoning-model
concept se related hai, bas yahan ye explicitly agent-loop ke through control hota
hai, model ke internal built-in thinking se nahi.

### 5b. 2026 recommended pattern (`create_agent`, LangGraph-backed)

**Hinglish:** LangChain team ka current guidance hai naye projects `create_agent` se
shuru karein — ye seedha, kam boilerplate hai, aur andar se **LangGraph** (low-level
orchestration engine) use karta hai jo better streaming, memory, aur reliability deta
hai.

**English:** LangChain's current guidance for new projects is `create_agent` — less
boilerplate, and internally powered by **LangGraph** for better streaming, memory
handling, and reliability under the hood.

```javascript
import { createAgent } from "langchain/agents";

const agent = createAgent({
  model: "gemini-2.5-flash",   // provider automatically inferred
  tools: [myTool],
});

const result = await agent.invoke({
  messages: [{ role: "user", content: "What's for lunch?" }],
});
```

**IRL example jo dono pattern ko jodta hai:** Classic pattern = manual gearbox car —
zyada control, zyada steps, lekin poori tarah samajh aata hai kya ho raha hai. Naya
`create_agent` = automatic gearbox — kam code, LangGraph "andar" gear khud badalta hai,
lekin result same jagah pahunchta hai. Seekhne ke liye dono jaanna faaydemand hai,
kyunki bahut sa existing code (aur tutorials) abhi bhi classic pattern mein hai.

---

## 6. LangChain package family — poora map

| Package | Kaam | Analogy |
|---|---|---|
| `@langchain/core` | Foundation — prompts, LCEL, base abstractions | Engine + steering |
| `@langchain/community` | Third-party integrations (SerpAPI, Pinecone, HF) | Toolbox of adapters |
| `@langchain/<provider>` | Ek specific LLM provider se connect karna | Ek specific fuel-type |
| `langchain` | Prebuilt agents, chains, retrievers | Driver jo sab jodta hai |
| `langgraph` *(2026 ka important addition)* | Low-level, graph-based agent orchestration | Poori engineering blueprint — jab tumhe fine control chahiye |
| `LangSmith` | Observability, evals, debugging | Dashboard/black-box recorder |

**IRL example — kab kaunsa use karo:** Agar tum ek simple chatbot bana rahe ho, `langchain`
(high-level, `create_agent`) kaafi hai. Agar tumhe complex, multi-agent, branching
workflow chahiye (jaise "agar X ho to agent A, warna agent B, phir dono ka result
merge karo"), tab `langgraph` directly use karna better hai — jaise simple car chalane
ke liye automatic gearbox kaafi hai, lekin agar tumhe engine tune karna hai to manual
control chahiye.

---

## 7. Poora Day-5 flow

```
                     "Main ek AI app banana chahta hoon"
                                    │
                                    ▼
                ┌──────────────────────────────────────┐
                │  Kya flow FIXED hai (input→process→out)?  │
                └───────────┬──────────────┬─────────────┘
                          HAAN              NAHI
                            ▼                ▼
                ┌───────────────────┐  ┌─────────────────────┐
                │   CHAIN banao        │  │   AGENT banao          │
                │   (LCEL: .pipe())    │  │   (tools + reasoning)  │
                └───────────────────┘  └──────────┬──────────┘
                                                    ▼
                                    ┌─────────────────────────────┐
                                    │  Classic: createToolCallingAgent │
                                    │  + AgentExecutor                │
                                    │       — OR —                    │
                                    │  2026: create_agent (LangGraph)  │
                                    └─────────────────────────────┘
```

---

## 8. Revision — apne alfaaz mein bolke dekho

1. Chain = fixed recipe, koi decision-making nahi. Agent = dynamic, model khud decide
   karta hai kya karna hai.
2. LCEL (`.pipe()`) ek modern tareeka hai components (prompt/model/parser) ko jodne ka
   — purane `LLMChain` class se zyada composable.
3. 2026 mein `createToolCallingAgent`/`AgentExecutor` (classic, `langchain_classic`
   mein move ho chuki) abhi bhi kaam karti hai, lekin naye projects ke liye
   `create_agent` (LangGraph-backed) recommended hai.
4. `@langchain/core` = foundation, `@langchain/community` = integrations,
   `@langchain/<provider>` = ek specific LLM se connect, `langchain` = high-level
   prebuilt agents/chains, `langgraph` = low-level fine-control orchestration.
5. LangChain sirf Chains/Agents nahi — memory, prompts, output parsers, document
   loaders, aur vector stores bhi isi toolbox ka hissa hain.

---
*Part of the 7-day LLM bootcamp notes — Day 5 of 6 in this set (deep-dive edition).
See `day1.md`-`day4.md` for LLM mechanics, hardware, local models, and prompting. See
`day6.md` for tools, memory, and building a working agent end-to-end.*
