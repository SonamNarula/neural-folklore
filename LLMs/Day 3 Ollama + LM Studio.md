# Day 3 — Ollama + LM Studio: LLMs ko apne laptop pe chalana
### (deep-dive version, updated for where things stand in 2026)

> Prerequisite: Day 1 (tokenization/attention/MoE/reasoning models) aur Day 2
> (HuggingFace, CPU/GPU/NPU, quantization — especially "MoE mein RAM total parameters
> se decide hoti hai" wala point). Aaj hum wahi theory **actually run** karenge.

---

## 0. Aaj ka goal

**Hinglish:** Day 2 mein humne seekha ki model "chhota" (quantized) banaya ja sakta hai
taaki weak laptop pe fit ho jaaye. Aaj hum dekhenge ki wo chhote/quantized models
**actually kaise chalate hain** — bina Python code likhe, bina cloud API bill pay kiye.

**English:** Day 2 established that a model can be shrunk (quantized) to fit modest
hardware. Today we cover *how* to actually run those quantized models — without writing
Python and without paying a cloud API bill.

---

## 1. Ollama kya hai — "Docker for LLMs"

**Hinglish:** Ollama ek command-line tool hai jo open-source LLMs (Llama, Qwen, Gemma,
DeepSeek, gpt-oss...) ko tumhare apne laptop/desktop pe download karke chalana bahut
aasaan bana deta hai.

**English:** Ollama is a CLI (and, since 2025, a GUI) tool that makes it easy to
download and run open-source LLMs directly on your own machine.

**IRL analogy — Docker se compare:** Docker mein tum ek `docker pull` karke ek poora
app-with-its-environment download kar lete ho aur `docker run` se chala dete ho, bina
manually dependencies install kiye. Ollama exactly yehi karta hai LLMs ke liye — `ollama
pull qwen3` aur `ollama run qwen3`, bas. Andar se GGUF-format quantized model already
packaged hota hai, tumhe kuch configure nahi karna.

```
Docker:  docker pull nginx   → docker run nginx     (poora web-server environment)
Ollama:  ollama pull qwen3   → ollama run qwen3      (poora quantized LLM + runtime)
```

**Key properties:**
- Local hi chalta hai (offline bhi kaam karta hai internet download ke baad)
- Privacy — data kahin bahar nahi jaata
- Latency kam — koi network round-trip nahi
- Cost zero — no per-token API bill

---

## 2. Install karna — 2026 mein aasaan ho chuka hai

**Hinglish — bada update:** Original bootcamp material Windows pe WSL (Windows
Subsystem for Linux) install karne ko bolta tha. **Ye ab zaroori nahi hai.** Late-2024
se Ollama ka **native Windows installer** hai — ek single `.exe`, no WSL, no Docker,
GPU (NVIDIA CUDA / AMD ROCm) auto-detect ho jaata hai. Since 2025, ek **native GUI app**
bhi hai (system tray mein icon, chat window) — agar terminal se dar lagta hai to bina
CLI touch kiye bhi chala sakte ho.

**English — key update:** The original material's Windows instructions (install WSL
first) are outdated. Ollama has had a **native Windows installer** since late 2024 — a
single `.exe`, no WSL, no Docker, with automatic GPU detection (NVIDIA CUDA / AMD
ROCm). Since 2025 it also ships a **native GUI app** (system tray icon + chat window),
so command-line use is now optional, not required.

### Windows
```
1. ollama.com se OllamaSetup.exe download karo
2. Run karo (admin rights ki zaroorat nahi)
3. Ho gaya — tray icon dikhega, aur "ollama" command turant terminal mein kaam karega
```

### Mac
```bash
curl -fsSL https://ollama.com/install.sh | sh
```
(ya seedha ollama.com se `.dmg` app download karo — Apple Silicon pe Metal ke through
GPU automatically use hota hai, aur unified memory ki wajah se Mac apni RAM jitni bhi
hai, GPU usko access kar leta hai — separate VRAM ki zaroorat nahi.)

### Linux
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

**IRL example:** Ye bilkul aisa hai jaise pehle kisi naye printer ko install karne ke
liye driver CD dhundhni padti thi, aur ab plug-and-play ho gaya hai — same shift Ollama
ke Windows support mein hua hai.

---

## 3. Ollama andar se kaam kaise karta hai

**Hinglish:**
1. **Model kahan store hote hain?** — `~/.ollama/models` mein (default), quantized
   GGUF format mein.
2. **Models kahan se aate hain?** — `ollama.com/library` se, jahan sab pre-quantized
   models curated hain.
3. **API kaisi hai?** — Har ek Ollama install ek local REST API bhi chalata hai
   `http://localhost:11434` pe, aur ye **OpenAI-compatible** hai — matlab koi bhi tool
   jo OpenAI API ke liye bana hai (Cursor, VS Code extensions, LangChain), wo Ollama ke
   saath bhi chal jaata hai, bas base URL badal do.

**English:**
1. Models are stored locally at `~/.ollama/models`, in quantized GGUF format.
2. Models are pulled from the curated `ollama.com/library` registry.
3. Ollama also runs a local REST API at `http://localhost:11434`, which is
   **OpenAI-compatible** — any tool built for OpenAI's API (Cursor, VS Code extensions,
   LangChain) works with Ollama by just changing the base URL.

```
                     ┌──────────────────────────┐
   ollama.com/library │  curated GGUF model repo  │
                     └────────────┬─────────────┘
                          ollama pull <model>
                                  ▼
                     ┌──────────────────────────┐
                     │   ~/.ollama/models          │  (local disk)
                     └────────────┬─────────────┘
                          ollama run <model>
                                  ▼
                     ┌──────────────────────────┐
                     │  local REST API :11434       │ ← OpenAI-compatible
                     │  (CLI chat / VS Code / apps) │
                     └──────────────────────────┘
```

---

## 4. Step-by-step commands (cheatsheet)

```bash
ollama pull qwen3          # model download karo, bina chalaye
ollama run qwen3           # interactive chat shuru karo (auto-pull if not present)
ollama list                # kaunse models locally installed hain
ollama show qwen3.6:27b    # model ki capabilities dekho (vision? tools? thinking?)
ollama rm llama3.2:3b      # disk space free karne ke liye model remove karo
```

**API se use karna (Node.js example):**
```javascript
const axios = require('axios');
const response = await axios.post('http://localhost:11434/api/generate', {
  model: 'qwen3',
  prompt: 'Explain Blockchain in simple terms',
});
console.log(response.data.response);
```

**IRL example:** `ollama show` bilkul aisa hai jaise kisi naye employee ka resume padhna
before usko kaam sonpna — pata chal jaata hai "ye tool-calling handle kar sakta hai ya
nahi", "vision support hai ya nahi", "thinking/reasoning mode hai ya nahi" — bina usse
directly test kiye.

---

## 5. Sabse important practical sawaal — **"MERE laptop pe KAUNSA model chalega?"**

Ye Day 2 ka MoE-memory lesson yahan directly kaam aata hai. Neeche August 2026 ke
current landscape ke hisaab se ek practical decision guide hai (exact model names time
ke saath badalte rahenge, lekin **tareeka** samajhna important hai):

**Hinglish:** Pehle apna VRAM/RAM check karo, phir uss tier ke liye best model choose
karo — sirf "parameter count" mat dekho, Day 2 wala total-vs-active wala point yaad
rakho.

| Tumhare paas | General chat/writing | Coding | Reasoning/math |
|---|---|---|---|
| ~8 GB RAM, no dedicated GPU | chhota dense model (jaise 1B-3B class) | chhota coding-tuned model (~7-8B class) | chhota distilled reasoning model |
| 8–16 GB VRAM | mid dense model (~9B class) ya chhota MoE | mid coding model | mid distilled reasoning model |
| 16–24 GB VRAM | bada dense (~27B) ya MoE jiska total size fit ho jaaye at 4-bit | coding-specialised ~27-30B class | mid-large distilled reasoning model |
| 24 GB+ VRAM | bade MoE models (jinka total parameter count, quantized, fit ho jaaye) | agentic/multi-file coding models | bade reasoning models |

**English:** First check your VRAM/RAM, then pick within that tier — don't just look at
"parameter count" in isolation; remember the Day 2 total-vs-active distinction for MoE
models.

```
Decision flow:

  "Kitna VRAM/RAM hai?"
        │
        ├── ~8GB, no GPU     → chhota dense model (1B-3B), CPU pe theek-thaak chalega
        ├── 8-16GB VRAM      → mid dense ya chhota MoE, GPU pe fast
        ├── 16-24GB VRAM     → bade dense (~27B) ya MoE jinka TOTAL size 4-bit pe fit ho
        └── 24GB+ VRAM       → bade MoE (total parameters ka 4-bit size dekh ke)

  Use-case ke hisaab se further filter:
        │
        ├── General chat/writing → dense general-purpose model
        ├── Coding                → coding-tuned/coding-specialised model
        ├── Reasoning/math        → distilled reasoning model (chain-of-thought trained)
        └── Vision/multimodal     → vision-capable variant
```

**IRL example — 2026 ka ek concrete scenario:** Socho tumhare paas 8 GB RAM ka college
laptop hai, koi dedicated GPU nahi. Tum coding help chahte ho. Tum ek "small,
coding-focused, quantized model" dhundhoge (na ki koi bada 70B general model, jo load
hi nahi hoga). Yehi wo decision hai jo Day 2 mein humne "total parameters = RAM ki
requirement" bola tha — usका direct application yahan ho raha hai.

**Common quantization tag jo tumhe milega:** Ollama default `Q4_K_M` (~4-bit) quantize
karke deta hai. Agar quality thoda better chahiye aur RAM allow karta hai, `q8_0`
(8-bit) try kar sakte ho — bigger download, better output, dono trade-off mein.

---

## 6. LM Studio — GUI wala alternative

**Hinglish:** LM Studio ek free desktop app hai jo bilkul Ollama jaisa kaam karta hai —
same GGUF format, same idea (local, offline LLMs) — lekin poora GUI-based hai, koi
terminal command nahi chahiye.

**English:** LM Studio is a free desktop app that does the same job as Ollama — same
GGUF format, same local/offline philosophy — but through a full GUI, no terminal
required.

```
Step 1: lmstudio.ai se install karo (Windows/macOS/Linux)
Step 2: "Models" tab → search karo (jaise "Qwen" ya "Gemma")
Step 3: Download click karo
Step 4: "Chat" tab → model select karo → type karke chat karo
```

**IRL example:** Ollama = ek terminal-savvy dost jo command likh ke kaam karwa deta
hai. LM Studio = wahi kaam, lekin ek app ke through jahan sab kuch click-and-select
hai — dono same jagah pahunchte hain, bas interface style alag hai.

---

## 7. HuggingFace vs Ollama vs LM Studio — final comparison

| Feature | HuggingFace | Ollama | LM Studio |
|---|---|---|---|
| Interface | Python/API, Spaces (web) | CLI + native GUI (2025+) | Full GUI |
| Format | Transformers/Safetensors | GGUF | GGUF |
| Best for | Research, training, hosted inference | Developers who want local + scriptable | Non-coders who want a chat UI |
| Setup difficulty | Medium (Python env) | Low (single installer) | Lowest (click-and-download) |

---

## 8. Poora Day-3 flow

```
[Day 2 output: "ye quantized model mere hardware pe fit hoga"]
                          │
                          ▼
        ┌───────────────────────────────────┐
        │  ollama pull <model>                │  → GGUF download from ollama.com/library
        └───────────────────┬─────────────────┘
                          ▼
        ┌───────────────────────────────────┐
        │  ollama run <model>                 │  → local chat, ya
        │  http://localhost:11434/api/generate│  → OpenAI-compatible API se apps se use
        └───────────────────┬─────────────────┘
                          ▼
        ┌───────────────────────────────────┐
        │  Poora offline, private, zero-cost   │
        │  LLM setup, tumhare apne laptop pe    │
        └───────────────────────────────────┘
```

---

## 9. Revision — apne alfaaz mein bolke dekho

1. Ollama = "Docker for LLMs" — `pull` karke download, `run` karke chalao.
2. 2026 mein Windows pe **WSL zaroori nahi hai** — native installer + GUI app already
   available hai.
3. Models GGUF format mein `~/.ollama/models` mein store hote hain, aur ek
   OpenAI-compatible local API `localhost:11434` pe chalti hai.
4. Model choose karte waqt sabse pehle apna VRAM/RAM dekho, phir use-case
   (chat/coding/reasoning) ke hisaab se filter karo — MoE models ke case mein **total**
   parameter size hi decide karta hai fit hoga ya nahi.
5. LM Studio wahi cheez hai jo Ollama karta hai, bas full GUI ke saath, no terminal
   needed.

---
*Part of the 7-day LLM bootcamp notes — Day 3 of 4 in this set (deep-dive edition).
See `day1.md` (core LLM mechanics + MoE + reasoning), `day2.md` (HuggingFace, hardware,
quantization), and `day4.md` (prompt engineering, updated for the context-engineering
era).*
