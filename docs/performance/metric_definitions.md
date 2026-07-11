# Performance Metric Definitions

InferDoctor performance commands run lightweight smoke tests. They are designed to find obvious responsiveness and endpoint problems, not to produce benchmark claims.

## Request Start

Request timing starts immediately before InferDoctor sends the HTTP request to the configured OpenAI-compatible endpoint.

## TTFT

Time to first token (TTFT) is measured from request start to the first non-empty user-visible generated content in a streaming response.

InferDoctor does not count these as first token:

- HTTP headers
- blank SSE lines
- SSE comments or keepalive lines
- role-only deltas
- empty content deltas
- metadata-only events
- malformed JSON events

If no non-empty generated content is observed, TTFT is reported as unknown.

## Total Latency

Total latency is measured from request start until a full non-streaming response is received or a streaming response completes.

## Generation Duration

For streaming responses, generation duration is measured from the first non-empty generated content until stream completion. For non-streaming responses, InferDoctor does not claim to know generation duration because the server only returns the completed response.

## Output Tokens And TPS

InferDoctor prefers API usage fields such as `completion_tokens` when they are present. If usage is unavailable, InferDoctor may use a rough word-based estimate and labels the result as estimated.

Generation TPS is calculated only when a generation duration is available. InferDoctor does not silently divide output tokens by total request latency and call it generation TPS.

## Streaming Observed

Streaming state is reported as one of:

- `confirmed`: stream=true produced non-empty generated content chunks.
- `accepted_full_response`: stream=true was accepted, but the server returned a full JSON response instead of SSE chunks.
- `no_content`: the server returned SSE events but no user-visible generated content.
- `inconclusive`: the response shape was not enough to decide.
- `failed`: the streaming request failed.
- `not_requested`: streaming was not part of the test.

## Smoke Test, Not Benchmark

These measurements use a tiny built-in prompt, strict timeouts, and at most a few bounded requests. They are useful for early diagnosis and demo readiness, but not for publishing throughput or quality claims.


## Experience Readiness

InferDoctor maps smoke-test metrics to a small set of user-experience categories:

- Responsive for interactive use
- Usable with streaming
- Acceptable for an internal prototype
- Likely frustrating without progress feedback
- Too slow for an interactive demo
- Inconclusive
- Endpoint/configuration failure

The thresholds are heuristics. A low TTFT can make a slower total response feel acceptable when streaming is smooth. A high TPS does not compensate for a long blank wait before the first token. A single measured run is useful for smoke testing but not enough for stability claims.
