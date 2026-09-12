# Python for LLM Applications and Function Calling

> LLM orchestration combines prompt engineering, token budget management, streaming execution, and dynamic function/tool calling architectures.

---

## 1. Why This Matters

### Why This Concept Exists
Raw LLMs are stateless text generators. Building useful AI agents and assistants requires orchestration: managing conversational memory, counting tokens, injecting contextual tools, and executing API actions.

### Why Python Developers Need It
Python is the undisputed primary language for building Generative AI systems, powering official SDKs for OpenAI, Anthropic, Google, and open-source frameworks.

### Why It Matters Specifically in AI/ML/GenAI
- **Token Counting & Context Management**: Calculating prompt tokens using `tiktoken` to prevent exceeding model context windows.
- **Function / Tool Calling Architecture**: Exposing Python functions as executable tools to LLMs via JSON Schema contracts.
- **Dynamic Prompt Templating**: Safely formatting instructions, system guardrails, and user context.

### Where It Appears in Real Projects
- Agentic workflows in LangGraph, CrewAI, AutoGen.
- Customer support chatbots with database lookup tools.
- Production LLM middleware and gateways.

---

## 2. Core Concept

### 2.1 Token Counting with `tiktoken`
Language models do not process characters or words; they process **tokens** (subword integer IDs).

```python
# Conceptual tiktoken usage:
"""
import tiktoken

encoder = tiktoken.encoding_for_model("gpt-4o")
tokens = encoder.encode("Hello world! Transformers are amazing.")
print(f"Token IDs: {tokens} | Count: {len(tokens)}")
"""
```

### 2.2 Function / Tool Calling Lifecycle
1. **Tool Definition**: Provide the LLM with a JSON Schema describing a Python function's name, description, and parameters.
2. **Model Decision**: The LLM determines if a tool is needed and emits a structured tool call: `{"name": "get_weather", "arguments": "{"location": "Tokyo"}"}`.
3. **Local Execution**: The Python backend parses the JSON arguments and executes the local Python function.
4. **Context Return**: The function's result is appended to the message history and sent back to the LLM for a final synthesis.

---

## 3. Mental Model

```text
The Tool Calling Loop:
User Query: "What is the stock price of AAPL?"
        │
        ▼
[ LLM Provider ] ──► Decides to call tool:
                      {"name": "fetch_stock", "args": {"symbol": "AAPL"}}
        │
        ▼
[ Python Application Router ]
  Executes: fetch_stock(symbol="AAPL") ──► Returns "$220.50"
        │
        ▼
[ LLM Provider ] (Receives tool output in context)
  Synthesizes final answer: "The current stock price of Apple (AAPL) is $220.50."
```

---

## 4. Practical Implementation & AI/ML/GenAI Patterns

### Pattern: Complete Tool Calling Execution Router
A production dispatcher that registers Python functions, auto-generates schemas, and executes tool calls:

```python
import json
import inspect
from typing import Callable, Dict, Any

class ToolRegistry:
    def __init__(self) -> None:
        self.tools: Dict[str, Callable[..., Any]] = {}

    def register(self, fn: Callable[..., Any]) -> Callable[..., Any]:
        self.tools[fn.__name__] = fn
        return fn

    def execute_tool_call(self, tool_name: str, args_json: str) -> str:
        """Parses tool arguments and executes local function safely."""
        if tool_name not in self.tools:
            return f"Error: Tool '{tool_name}' not found."

        try:
            kwargs = json.loads(args_json)
        except json.JSONDecodeError as e:
            return f"Error: Invalid JSON arguments: {e}"

        target_fn = self.tools[tool_name]
        try:
            result = target_fn(**kwargs)
            return json.dumps(result)
        except Exception as e:
            return f"Error executing tool {tool_name}: {e}"

# Tool Definitions:
registry = ToolRegistry()

@registry.register
def calculate_mortgage(principal: float, rate: float, years: int) -> dict:
    """Calculates monthly mortgage payment."""
    monthly_rate = rate / 12 / 100
    n_payments = years * 12
    monthly_payment = (principal * monthly_rate) / (1 - (1 + monthly_rate) ** -n_payments)
    return {"monthly_payment": round(monthly_payment, 2)}

# Simulating an LLM tool call response:
llm_emitted_call = {
    "name": "calculate_mortgage",
    "arguments": '{"principal": 500000, "rate": 6.5, "years": 30}'
}

tool_output = registry.execute_tool_call(
    llm_emitted_call["name"],
    llm_emitted_call["arguments"]
)
print("Tool Execution Output:", tool_output)
```

---

## 5. Edge Cases, Pitfalls & Common Bugs

### 1. Hallucinated Tool Arguments
LLMs occasionally hallucinate parameters not present in your function signature. Use Pydantic or `inspect.signature` to validate arguments before calling `fn(**kwargs)`.

### 2. Unsanitized Code Execution
Never execute arbitrary Python code emitted by an LLM via `eval()` or `exec()` without sandboxing (e.g., Docker containers or gVisor).

---

## 6. Interview Questions & Coding Traps

### Q1: How do you handle multi-turn conversation memory within context window limits?
1. **Sliding Window**: Retain only the most recent $K$ message turns.
2. **Token-Budgeted Truncation**: Use `tiktoken` to calculate total tokens, evicting oldest user/assistant turns while preserving the system prompt.
3. **Hierarchical Summarization**: Summarize earlier conversation history into a condensed memory block.

### Complexity Reference
| Step | Latency Cost |
| :--- | :--- |
| Schema Formatting | $O(1)$ one-time configuration |
| Tool Dispatching | $O(1)$ dictionary lookup |
| Tool Execution | Dependent on external tool (e.g. database query 10ms-100ms) |
