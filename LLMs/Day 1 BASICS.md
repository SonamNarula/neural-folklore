# Day 1 — LLM kya hoti hai, aur andar chal kya raha hota hai
### (deep-dive version, updated for where things stand in 2026)

> Padhne wala assume kiya gaya hai: zero background. Agar "tokenization" sunke dar
> lagta hai, ye file usi ke liye hai. Ye Day 1 ka **extended** version hai — original
> bootcamp jo cover karta hai wo sab hai, plus wo cheezein jo 2025–26 mein industry-standard
> ban chuki hain (MoE architecture, reasoning/thinking models, huge context windows)
> kyunki agar tum aaj LLM seekh rahe ho to "GPT-2 ka zamana" wali baat se kaam nahi
> chalega — tumhe pata hona chahiye ki August 2026 mein cheezein kahan khadi hain.

---

## 0. Sabse pehle — ek line mein LLM

**Hinglish:** LLM matlab **Large Language Model**. Ye ek aisa program hai jisne itni
saari kitaabein, websites, code, articles padh liye hain ki ab wo tumhare sentence ko
dekh ke agla sabse "sahi lagne wala" token guess kar sakta hai. Bas itna hi. Baaki sab jo
magic lagta hai — chat karna, code likhna, poem banana, ek agent ki tarah tools call
karna — sab isi "agla token guess karo, baar-baar" ke upar khada hai.

**English:** An LLM is a program trained on massive amounts of text (books, websites,
code, articles) so that, given some text, it can predict what token is most likely to
come next. Every capability you see today — conversation, code generation,
summarization, tool-calling agents — is built on repeatedly applying this one
operation: predict the next token, one at a time.

**IRL analogy:** Tumhara phone ka keyboard jab type karte waqt next word suggest karta
hai ("I am going to the ___" → "market", "gym", "office") — LLM wahi cheez hai, bas
lakhon guna zyada powerful version, jisne pura internet padha hai instead of sirf
tumhare purane messages.

```
Tumhara keyboard:  "I am going to the" → [market, gym, office]   (chhota model, chhota data)
LLM (2026):        "I am going to the" → [market, gym, office, moon, doctor's, ...]
                   (bahut bada model, trillions tokens ka training data, deep context samajhta hai)
```

---

## 1. LLM 2026 mein kahan khade hain — landscape samjho pehle

Original bootcamp "2025" ke context mein likha gaya tha aur usme sirf GPT, Claude,
LLaMA, Mistral, Gemini list the — wo abhi bhi sahi naam hain, lekin har family ke andar
kai naye generations aa chuke hain. **Ye jaan na isliye zaroori hai kyunki naam wahi
hain, lekin andar ka architecture aur "kya kar sakte hain" bahut aage nikal chuka hai.**

**Hinglish — August 2026 tak ka snapshot:**
- **Anthropic (Claude):** Sonnet 5, Opus, aur ek naya top-tier "Mythos-class" (Fable 5 /
  Mythos 5) launch ho chuka hai jo Opus se bhi upar rank karta hai reasoning/coding
  benchmarks pe.
- **OpenAI (GPT):** GPT-5 family aage badh ke GPT-5.4/5.5/5.6 tak pahunch chuki hai,
  saath hi ek "o-series"-style reasoning behaviour built-in hai.
- **Google (Gemini):** Gemini 3 family (3.1 Pro, 3.5/3.7 Flash) — Flash variants
  cheap+fast ke liye, Pro deep reasoning ke liye.
- **xAI (Grok):** Grok 4.x series, real-time X/web search ke saath tight integration.
- **Open-weight (khud download karke chala sakte ho):** DeepSeek V4, Qwen 3.5/3.6,
  Llama 4 (Scout/Maverick/Behemoth), GLM-5, Kimi K2/K3, Mistral Large 3, Gemma 4,
  aur khud OpenAI ka open-weight release `gpt-oss`.

**English — where things stand as of August 2026:** The same lab names from the
original bootcamp material still lead the field, but each has shipped multiple new
generations since. Anthropic's lineup now runs Sonnet, Opus, and a new top tier above
Opus called "Mythos-class" (Fable 5 for general availability, Mythos 5 restricted).
OpenAI's GPT-5 family has iterated through several point releases with built-in
reasoning behaviour. Google's Gemini 3 family splits into Pro (deep reasoning) and
Flash (fast/cheap) variants. Open-weight models you can self-host have become genuinely
competitive with closed frontier models on coding and reasoning — DeepSeek V4, Qwen
3.5/3.6, Llama 4, GLM-5, Kimi K2/K3, and even a Meta-style open release from OpenAI
itself (`gpt-oss`).

**IRL example — kyun ye matter karta hai tumhare liye:** Agar tum job interview mein bol
do "LLMs jaise GPT-3.5" — 2026 mein ye waise hi lagega jaise koi abhi bhi "latest
iPhone" bolke iPhone 6 point kare. Naam same reh sakta hai, generation nahi.

### 1.1 Sabse bada shift: architecture ab MoE hai, dense nahi

Ye sabse important 2025→2026 ka technical shift hai jo original bootcamp material mein
nahi tha, aur agar tumhe koi bhi modern open-weight model naam sunayi de (Llama 4,
DeepSeek V4, Qwen3, GLM-5, Mistral Large 3) to unme ek common cheez hai:

**Hinglish:** Purane models (GPT-2, original GPT-3) **dense** the — matlab har single
token predict karne ke liye model ke **saare** parameters use hote the. Naye models
**Mixture-of-Experts (MoE)** hain — model ke andar bahut saare chhote "expert"
sub-networks hote hain, aur har token ke liye ek chhota router decide karta hai ki
kaunse **kuch** experts is baar use honge — baaki sab skip ho jaate hain.

**English:** Older models were **dense** — every parameter was used for every token.
Modern frontier and open-weight models are **Mixture-of-Experts (MoE)** — the model
contains many smaller "expert" sub-networks, and a small router network picks a handful
of experts to actually run for each token, leaving the rest inactive for that step.

**IRL analogy — hospital ka example:** Socho ek bade hospital mein 100 specialist
doctors hain (dermatologist, cardiologist, neurologist...). Jab tum ek problem leke
aate ho, reception (router) decide karta hai kaunse 2-3 specialists actually zaroori
hain — poore 100 doctors ko bulaya nahi jaata. Isse hospital (model) ke paas capacity
100 doctors jitni hai, lekin ek patient ke liye kaam sirf 2-3 doctors jitna hota hai.

```
DENSE model (purana style):
   Input → [ALL 70B parameters activate] → Output
           (bahut accurate ho sakta hai, lekin bahut slow/expensive)

MoE model (2025-26 ka standard):
   Input → Router → chooses 2-8 experts out of e.g. 128/256
         → [sirf chuने hue experts activate, ~5-20% of total parameters]
         → Output
           (total "knowledge capacity" trillion-scale ho sakti hai,
            lekin per-token compute chhote model jaisa hi lagta hai)
```

**Real numbers (2026 ke examples):**

| Model | Total parameters | Active per token | Matlab |
|---|---|---|---|
| DeepSeek V4 Pro | ~1.6 trillion | ~49 billion | Sirf ~3% "jaaga" hota hai har token pe |
| Llama 4 Maverick | 400 billion | 17 billion | 128 experts mein se chunindaa activate hote hain |
| Qwen 3.5 | 397 billion | 17 billion | Vision+language dono, 201 languages |

**Yaad rakhne wali baat (agla topic Day 2 mein important hoga):** MoE se **compute**
(speed) bachta hai, lekin **memory** nahi — poore model ke saare experts RAM/VRAM mein
load hone hi hote hain kyunki router kisi bhi token ke liye kisi bhi expert ko choose
kar sakta hai. Ye galatfehmi bahut logon ko hoti hai — "MoE model chhota lagega RAM
mein" — **nahi**, ye sirf compute chhota karta hai, RAM requirement total-parameter size
pe hi based hai.

---

## 2. Real use-cases — 2026 mein kya naya hai

Original list (chatbots, summarizers, translation, auto-coding, tutoring) abhi bhi
valid hai, lekin ab do naye categories mainstream ho chuke hain:

| Use case | Kaise kaam karta hai (Hinglish) | 2026 example |
|---|---|---|
| Chatbot | Context yaad rakhta hai, jawab generate karta hai | ChatGPT, bank helpdesk bot |
| Summarizer | Lamba text padh ke chhota, apne-alfaaz mein likhta hai | News app "3-line summary" |
| Translation | Ek language ke tokens ko doosri language mein map karta hai | Google Translate |
| Auto-coding | Code patterns seekhe hain, agli line predict karta hai | GitHub Copilot |
| Tutoring | Step-by-step explanation, level-adjust karta hai | Khanmigo |
| **Agentic workflows** *(2026 mainstream)* | Model khud decide karta hai kaunsa tool/API call karna hai, multi-step task complete karta hai bina insaan ke har step pe poochhe | Claude Code / Cowork jaise coding & knowledge-work agents jo terminal/files/APIs use kar sakte hain |
| **Computer use / browsing agents** *(2026 mainstream)* | Model screen dekhta hai, click/type karta hai jaise insaan browser use karta hai | "Claude in Chrome"-type browsing agents |

**IRL example jo dono naye categories jode:** Pehle tum LLM se bolte the "is code mein
bug dhundo" aur wo sirf **bata** deta tha. Ab (2026 mein) tum bol sakte ho "is bug ko
fix karo aur PR bhi bana do" — aur agent khud file edit karega, terminal mein test
chalayega, aur result confirm karega — bina tumhe har chhota step manually karna pade.

---

## 3. LLM ke andar hota kya hai — 4 steps (core pipeline, still the foundation)

Ye is poore din ka sabse important part hai — architecture chahe dense ho ya MoE, ye
4-step pipeline foundation hamesha same rehta hai:

```
[Input Text] → [1. Tokenization] → [2. Embedding] → [3. Transformer/Attention] → [4. Prediction] → [Output Text]
```

**Hinglish overview:** Text seedha model ko samajh nahi aata — model sirf numbers ke
saath kaam karta hai. Isliye text ko pehle chhote tokens mein todte hain, phir un
tokens ko numbers (vectors) mein badalte hain, phir model un numbers ko dekh ke
samajhta hai kaunsa word kis se related hai, aur last mein agla token predict karta
hai.

**English overview:** Text can't be fed directly into a neural network — networks only
understand numbers. So text is broken into small pieces (tokens), those pieces are
converted into number-lists (embeddings), a component called the Transformer figures
out which words relate to which, and finally the model predicts the next most likely
token.

### Step 1 — Tokenization (thoda gehraai mein)

**Hinglish:** Sentence ko chhote-chhote tukdon (tokens) mein todna. Zyaadatar modern
tokenizers **Byte-Pair Encoding (BPE)** ya usके variants use karte hain — jo statistically
sabse common word-pieces ko ek token bana deta hai, aur rare words ko chhote pieces
mein todta hai.

**English:** Breaking input text into smaller units called tokens. Most modern
tokenizers use **Byte-Pair Encoding (BPE)** or a close variant — common word-fragments
get merged into single tokens, while rare/unusual words get split into smaller pieces.

**Example (real tokenizer behaviour):**
```
Input:  "Most famous cheese in France?"
Tokens: ["Most", " famous", " cheese", " in", " France", "?"]
```
Notice: space bhi token ka part hota hai (" famous" not "famous") — isse model ko pata
chalta hai ki ye word kisi doosre word ke baad aaya hai.

**Mini worked BPE intuition (jo tumhe koi bhi cheatsheet nahi batata):**
```
Training corpus mein "lower", "lowest", "newer" bahut baar aate hain.
BPE dekhta hai "e"+"r" saath mein bahut baar aata hai → inhe merge kar deta hai: "er"
Phir "low"+"er" bhi bahut baar → merge: "lower" ek hi token ban jaata hai
Lekin ek naya/rare word jaise "lowerification" → "lower" + "ific" + "ation" mein toot jaata hai
```
Isi wajah se rare Hindi/regional words, brand names, ya code variable names kabhi-kabhi
model ke liye "mehnga" (zyada tokens le lete) ho jaate hain.

**IRL example:** Jaise tum Hindi mein "khaanapeena" bolke ek hi shabd mein 2 concepts
daal dete ho, waise hi tokenizer kabhi ek word ko 2+ tokens mein tod sakta hai agar wo
rare/unusual ho — e.g. "unbelievable" → "un" + "believable". Isse model naye/unseen
words bhi handle kar leta hai.

You can literally see this happen at **platform.openai.com/tokenizer** — koi bhi
sentence daalo aur dekho wo kitne tokens mein toot raha hai.

### Step 2 — Embedding

**Hinglish:** Ab har token ko ek list of numbers (vector) mein convert karte hain. Ye
numbers word ka "meaning" mathematically represent karte hain — "king" aur "queen" ke
vectors ek dusre ke paas honge (meaning-wise related), lekin "king" aur "banana" ke
vectors door honge.

**English:** Each token is converted into a vector (list of numbers, typically 768 to
several thousand dimensions in modern models) that represents its meaning in a
mathematical space.

```
"cheese" → [0.12, -0.55, 1.03, ...]     (illustrative example only)

["I", "love", "AI"]  →  [
  [0.01, -0.92, 0.11, ...],   // vector for "I"
  [0.45,  0.82, 0.66, ...],   // vector for "love"
  [0.12,  0.34, -0.75, ...],  // vector for "AI"
]
```

**IRL example:** Socho ek movie recommendation system — har movie ko genre, mood,
actor-similarity ke basis pe ek "point" diya jaata hai multi-dimensional space mein.
Similar movies ek dusre ke paas honge, unrelated movies door honge. Embeddings bhi
yही karte hain, bas words ke liye.

**Gotcha:** Har model ka "apple" ke liye same vector nahi hota — depend karta hai model,
training data, aur tokenizer pe. Ek model ka embedding doosre model mein directly reuse
nahi ho sakta.

**Bonus — positional info:** Attention khud order nahi samajhta (ye ek "set" processing
karta hai), isliye har token ke embedding mein uski **position** (1st word, 2nd word,
...) ki jaankari bhi add ki jaati hai — isko *positional encoding* kehte hain. Isके
bina model "cat chased dog" aur "dog chased cat" mein farak nahi kar payega.

### Step 3 — Transformer (Attention) — multi-head tak

**Hinglish:** Ye "smart" part hai. Transformer poore sentence ko ek saath dekhta hai aur
decide karta hai ki kaunsa word kis doosre word se **related** hai, aur kis pe zyada
"attention" (dhyaan) dena hai.

**English:** The transformer looks at the whole sentence at once and uses an
*attention mechanism* to figure out relationships between words.

**Example:** "Most famous cheese in France?" → model seekhta hai ki "cheese" aur
"France" ek dusre se strongly related hain, aur "famous" extra weight deta hai.

```
Input:  "Most  famous  cheese  in  France  ?"
                  ↑________________↑
           attention "cheese" aur "France" ko strongly link karta hai
```

**Multi-head attention — depth wala part:** Ek hi attention "head" sirf ek type ka
relationship pakad sakta hai. Isliye real models mein **kai heads parallel** mein chalte
hain — ek head grammar relationship pakad sakta hai (subject-verb), doosra head
factual relationship (cheese-France), teesra kuch aur. In sabko combine karke final,
zyada rich understanding banta hai.

**IRL example — ek class discussion mein alag-alag log alag cheez pe dhyaan de rahe
hain:** Ek teacher "cheese in France" bolta hai. Ek student (head 1) grammar pe focus
karta hai (subject kaun hai). Doosra student (head 2) fact pe focus karta hai (France
famous for cheese). Teesra (head 3) tone/context pe. Sab apna apna analysis class
discussion (final layer) mein la ke milaate hain — final samajh sabse rich hota hai
kisi ek akele insaan se.

**Context window — 2026 mein bahut bada topic:** Attention jitne tokens ek saath "dekh"
sakta hai, wahi uski *context window* hai. 2023 mein ye 4K-32K tokens tak simit thi.
2026 mein flagship open models 1M–10M tokens tak context handle kar sakte hain (Llama
4 Scout: 10M, DeepSeek V4/Qwen3.5: 1M).

```
Chhota context window (jaise 8K tokens) → sirf ek chhota chapter yaad rakh sakta hai
Bada context window (jaise 1M+ tokens)  → poori kitaab (ya bade codebase) ek saath "dekh" sakta hai
```

**Lekin sach ye hai:** Sirf window bada hone se practically use karna free nahi hai —
lamba context zyada memory (KV cache) leta hai aur inference dheera/mehenga ho jaata
hai. Isliye zyaadatar production apps chhote se medium context (128K–256K) mein hi kaam
karte hain, poora 1M-10M sirf special cases ke liye.

### Step 4 — Prediction

**Hinglish:** Ab model ready hai agla token predict karne ke liye. Wo har possible agle
token ko ek probability deta hai, aur usmein se koi ek choose karta hai.

**English:** The model generates a probability distribution over all possible next
tokens, then a token gets selected based on that distribution.

```
Prompt: "Deep Learning is very"
Model output probabilities:
  powerful     → 43%
  innovative   → 37%
  complex      → 15%
  weak         →  3%
  limited      →  1%
→ Decoding algorithm picks one → "powerful"
```

**IRL example:** Jaise exam mein MCQ dete waqt tumhare paas 4 options hote hain aur
tumhe sabse "confident" wale option pe tick karna hota hai — model bhi aisa hi karta
hai, bas usके paas poore vocabulary (~50,000–200,000+ tokens) ke options hote hain har
baar.

**Important truth to remember:** LLM internet **search** nahi karta jab wo bina-tool
answer deta hai — wo sirf apne training data se seekhe hue **patterns** ke basis pe
predict karta hai. Isi wajah se hallucination hoti hai (confident lekin galat answer).
(Agents apne aap search/tools use kar sakte hain — wo alag cheez hai, Day 5-6 ka topic.)

---

## 4. 2026 ka naya normal — "Reasoning" ya "Thinking" models

Ye original 7-day bootcamp mein cover nahi hua tha kyunki ye trend 2025 ke aakhir aur
2026 mein mainstream bana — lekin agar tum aaj koi bhi flagship model (Claude, GPT-5,
Gemini, DeepSeek R1, Qwen3) use karoge to "thinking"/"extended reasoning" mode zaroor
dekhoge, isliye ye samajhna zaroori hai.

**Hinglish:** Normal prediction mein model turant agla token bol deta hai. **Reasoning
models** ek extra step karte hain — final answer dene se pehle, model apne aap ek
internal "scratchpad" mein step-by-step soch (chain-of-thought) generate karta hai, phir
usi soch ko dekh ke final answer deta hai. Isse harder math/logic/coding problems mein
accuracy bahut badh jaati hai.

**English:** Regular models predict the next token immediately. **Reasoning
("thinking") models** insert an extra phase — before producing a final answer, the
model generates an internal, extended chain-of-thought as scratch work, then uses that
scratch work to produce a more reliable final answer. This is often called *test-time
compute* — spending more compute at answer-time (not just training-time) to get a
better answer.

```
Normal model:    Question → [predict next token repeatedly] → Answer

Reasoning model: Question → [extended internal "thinking" tokens — not shown, or shown
                              collapsed] → then → Answer
                 (jaise ek student rough-sheet pe kaam kare, phir final answer likhe)
```

**IRL example:** Ye bilkul aisa hai jaise ek tez student exam mein seedha final answer
na likhe, balki pehle rough page pe steps kare (jaise integration steps, ya code test
cases dimaag mein chalaana), aur phir final clean answer likhe. Fast student bhi kabhi
rough kaam karta hai jab sawaal tricky ho — reasoning models yehi karte hain, automated.

**Note — Day 4 se farak:** Bootcamp ka Day 4 "chain-of-thought **prompting**" sikhaata
hai — jahan **tum** khud prompt mein bolte ho "step by step socho". Ye reasoning models
mein **built-in/automatic** hai — model khud decide karta hai kitna "sochna" hai, bina
tumhare bole.

---

## 5. Sampling — model "kaunsa" token choose karta hai

Highest-probability token हमेशा nahi choose hota — kyunki hamesha top-1 choose karne
se output boring/repetitive ho jaata hai.

### Temperature
**Hinglish:** Randomness control karta hai. Low (~0.2) = safe/deterministic. High
(~1.0+) = creative/diverse.

**English:** Temperature controls randomness in sampling. Lower values sharpen the
distribution (near-deterministic). Higher values flatten it (more diverse, more
creative).

```
Low temperature  (peaked):      Cake=0.40 ██████████        Apple=0.001 ▏
High temperature (flatter):     Cake=0.15 ████    Apple=0.04 ██   Banana=0.08 ███
```

### Top-k Sampling
**Hinglish:** Sirf top-k (jaise top 40) sabse likely tokens mein se randomly choose
karta hai, baaki discard.

**English:** Restrict sampling to the k most probable tokens.

### Top-p (Nucleus) Sampling
**Hinglish:** Fixed count ki jagah, jab tak cumulative probability ek threshold
(jaise 0.9) tak nahi pahunchti tab tak tokens include karo.

**English:** Pick the smallest set of tokens whose cumulative probability exceeds p,
then sample within that set — adapts based on model's confidence.

### Min-p
**Hinglish:** Jo token ki probability minimum threshold (jaise 0.1) se kam hai usse
hata do — garbage output se bachne ke liye.

**English:** Discard any token whose probability falls below a minimum cutoff.

### Repetition / frequency / presence penalty (extra depth)
**Hinglish:** Model kabhi-kabhi ek hi phrase baar-baar repeat karne lagta hai (loop mein
phaas jaata hai). Ye penalties usko rokte hain — jo token pehle use ho chuka hai, uski
probability thodi kam kar dete hain.

**English:** Models can sometimes get stuck repeating phrases. Frequency/presence
penalties slightly reduce the probability of tokens that have already appeared,
discouraging loops.

**Sab ek jagah — cheat table:**

| Parameter | Kya karta hai | Range |
|---|---|---|
| `max_tokens` | Model kitne tokens generate karega, upper limit | 1 to ∞ |
| `temperature` | Randomness/creativity control | 0 to 2 (common) |
| `top_p` | Probability-mass based cutoff | 0 to 1 |
| `top_k` | Fixed count based cutoff | 1 to ∞ |
| `frequency_penalty` | Repeat hone wale tokens ko penalize karta hai | -2 to 2 |
| `presence_penalty` | Naye/unused tokens use karne ko encourage karta hai | -2 to 2 |
| `stop` | Yahan pohochte hi generation ruk jaayegi | custom list |

**IRL example jo sab jodta hai:** Socho tum ek AI se "ek chhoti kahani likho" bolte ho.
- High temperature + top_p high → creative, unpredictable story
- Low temperature + top_k low → safe, generic, thoda boring story
- `max_tokens` decide karega kahani kitni lambi hogi
- `stop` = ["THE END"] set kar do to jaise hi model ye likhega, generation ruk jaayegi

---

## 6. Poora Day-1 flow — ek hi diagram mein (updated)

```
                         ┌───────────────────────────────────────────┐
                         │              USER PROMPT                    │
                         │   "Most famous cheese in France?"           │
                         └───────────────────┬───────────────────────┘
                                             ▼
                         ┌───────────────────────────────────────────┐
                         │  1. TOKENIZATION (BPE)                      │
                         │  "Most" " famous" " cheese" " in" " France" │
                         └───────────────────┬───────────────────────┘
                                             ▼
                         ┌───────────────────────────────────────────┐
                         │  2. EMBEDDING + positional info              │
                         │  har token → vector [0.1, -0.5, 1.0, ...]   │
                         └───────────────────┬───────────────────────┘
                                             ▼
                         ┌───────────────────────────────────────────┐
                         │  3. TRANSFORMER / MULTI-HEAD ATTENTION       │
                         │  "cheese" ↔ "France" strongly linked         │
                         │  (agar MoE hai: router chunta hai kaunse    │
                         │   few experts is token ke liye chalenge)    │
                         └───────────────────┬───────────────────────┘
                                             ▼
                         ┌───────────────────────────────────────────┐
                         │  [Optional, 2026-era] EXTENDED THINKING       │
                         │  reasoning models yahan internal            │
                         │  step-by-step scratch-work karte hain        │
                         └───────────────────┬───────────────────────┘
                                             ▼
                         ┌───────────────────────────────────────────┐
                         │  4. PREDICTION + SAMPLING                    │
                         │  Brie=43% Camembert=30% ... → pick one       │
                         │  (temperature/top-k/top-p decide "kaise")   │
                         └───────────────────┬───────────────────────┘
                                             ▼
                         ┌───────────────────────────────────────────┐
                         │              OUTPUT: "Brie"                  │
                         └───────────────────────────────────────────┘
```

---

## 7. Revision — apne alfaaz mein bolke dekho

Agar ye 8 sentences kisi ko explain kar sako bina notes dekhe, Day 1 clear hai:

1. LLM next-token predictor hai, internet search nahi karta (jab tak tools na diye ho).
2. Text → tokens (BPE) → embeddings (+positional info) → multi-head attention →
   prediction, yahi core pipeline hai.
3. Attention wahi mechanism hai jo batata hai kaunsa word kis se related hai; multiple
   heads parallel mein alag-alag relationships pakadte hain.
4. 2026 ke flagship models zyaadatar **Mixture-of-Experts** hain — total parameters
   bade hain but har token pe sirf chhote se fraction (few experts) activate hote hain.
   Isse compute bachta hai, **memory nahi**.
5. Context window batata hai model ek saath kitna text "dekh" sakta hai — 2026 mein ye
   1M-10M tokens tak pahunch chuki hai, lekin practically zyada context = zyada
   memory/cost.
6. **Reasoning/thinking models** answer dene se pehle internally step-by-step sochte
   hain (test-time compute) — ye automatic hai, Day-4 wali manual CoT prompting se alag.
7. Temperature/top-k/top-p/min-p sab "kaunsa next token choose karein" ko control karte
   hain; repetition penalties loops rokte hain.
8. Same model ka embedding kisi doosre model mein reuse nahi ho sakta.

---
*Part of the 7-day LLM bootcamp notes — Day 1 of 2 in this set (deep-dive edition).
See `day2.md` for HuggingFace, GPUs/NPUs vs CPUs, and quantization — updated for the
MoE-heavy 2026 model landscape.*
