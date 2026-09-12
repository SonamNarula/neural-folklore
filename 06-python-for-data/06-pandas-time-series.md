# Pandas Time Series Analysis

> Pandas provides native datetime indexing, frequency resampling, rolling window aggregations, and lagging operations engineered for sequential and temporal data.

---

## 1. Why This Matters

### Why This Concept Exists
Temporal data has inherent directionality and variable frequency (daily, hourly, milliseconds). Standard tabular indexing cannot handle time-zone conversions, calendar holidays, or windowed statistical calculations.

### Why Python Developers Need It
Time-series data is ubiquitous across finance, IoT, telemetry, and demand forecasting.

### Why It Matters Specifically in AI/ML/GenAI
- **LLM Token Velocity & Rate Limit Telemetry**: Tracking token consumption over rolling 1-minute and 1-hour windows to manage API rate limits.
- **Sequential Feature Engineering**: Creating lag features (`t-1`, `t-7`) and rolling statistics (moving averages, exponential moving averages) for forecasting models.
- **Preventing Temporal Data Leakage**: Enforcing strict forward-only temporal splits in cross-validation.

### Where It Appears in Real Projects
- Real-time token usage telemetry monitors.
- Algorithmic trading and financial time series models.
- Server load and GPU cluster capacity forecasting.

---

## 2. Core Concept

### 2.1 DatetimeIndex and Parsing
```python
import pandas as pd
import numpy as np

# Convert strings to native DatetimeIndex
dates = pd.date_range(start="2026-01-01", periods=10, freq="D")
ts = pd.Series(np.random.randn(10), index=dates)
print("DatetimeIndex Head:
", ts.head(2))

# Partial string slicing (Native date filtering)
print("Slice specific range:
", ts["2026-01-03":"2026-01-05"])
```

### 2.2 Resampling & Frequency Conversion
- **Downsampling** (e.g., Hourly -> Daily): Requires an aggregation function (e.g., `.sum()`, `.mean()`).
- **Upsampling** (e.g., Daily -> Hourly): Requires interpolation (e.g., `.ffill()`, `.interpolate()`).

```python
# Downsample from daily to 3-day frequency:
resampled = ts.resample("3D").mean()
```

### 2.3 Rolling Windows and Shift (Lagging)
```python
# Rolling 3-day moving average:
ts_rolling = ts.rolling(window=3).mean()

# Shift by 1 period (Create lag-1 feature):
ts_lag1 = ts.shift(1)  # ts[t] becomes ts[t-1]
```

---

## 3. Mental Model

```text
Lag & Rolling Windows:
Timestamp:       t-2    t-1     t
Value:           10     20     30
Shift(1):        --     10     20    <-- Previous value (feature for prediction!)
Rolling(2).mean: --     15     25    <-- Moving average (trend feature!)
```

---

## 4. Practical Implementation & AI/ML/GenAI Patterns

### Pattern: Rolling Token-Rate Limiter and Usage Monitor
Tracking API token consumption across sliding 60-second windows:

```python
import pandas as pd
import numpy as np

# Simulate API invocation timestamps:
time_index = pd.date_range(start="2026-09-12 12:00:00", periods=60, freq="2s")
token_usage = pd.DataFrame({
    "tokens": np.random.randint(50, 300, size=len(time_index))
}, index=time_index)

# 1. Compute rolling 10-second token consumption
token_usage["rolling_10s_tokens"] = token_usage["tokens"].rolling("10s").sum()

# 2. Flag when rolling rate exceeds safety threshold (e.g. 1000 tokens / 10s)
token_usage["rate_limit_warning"] = token_usage["rolling_10s_tokens"] > 1000

print("Token Telemetry Summary:")
print(token_usage[["tokens", "rolling_10s_tokens", "rate_limit_warning"]].head(8))
```

---

## 5. Edge Cases, Pitfalls & Common Bugs

### 1. Temporal Data Leakage in Shifting
When calculating rolling features, using `rolling(3, center=True)` incorporates **future** data points into the current row's calculation, causing catastrophic look-ahead bias in predictive models!

### 2. Timezone Naive vs Aware
Comparing a timezone-naive timestamp to a timezone-aware timestamp raises `TypeError: Cannot compare tz-naive and tz-aware timestamps`. Always standardize on UTC: `df.index = df.index.tz_localize('UTC')`.

---

## 6. Interview Questions & Coding Traps

### Q1: What is the difference between `df.resample()` and `df.rolling()`?
- `resample()` is a **frequency-based groupby** that groups records into non-overlapping temporal buckets (e.g., hourly), reducing the row count of the DataFrame.
- `rolling()` maintains the **exact same row count**, sliding a window of fixed time or row width across consecutive entries.

### Q2: How do you forward-fill missing values in a time series and why is it preferred over backward-filling?
Use `df.ffill()`. Forward-filling propagates the last known valid observation forward in time. Backward-filling (`bfill`) uses future information to fill past missing values, which introduces forward-looking data leakage into predictive models!

### Complexity Reference
| Operation | Time Complexity | Space Complexity |
| :--- | :--- | :--- |
| `df.shift(1)` | $O(N)$ pointer shift | $O(N)$ new Series |
| `df.rolling(k).mean()` | $O(N)$ sliding window accumulator | $O(N)$ |
| `df.resample('D').sum()` | $O(N)$ bucket sort | $O(U)$ unique periods |
