# Model selection (measured 2026-11-05)

## Bake-off: 4 models x 2 modes x 6 probes x 5 runs

| model | mode | usable | clean | p50 | p95 | verdict |
| --- | --- | --- | --- | --- | --- | --- |
| glm-5.3 | native | 100% | 100% | 2.26s | 9.74s | PASS |
| glm-5.3 | json | 87% | 83% | 1.9s | 8.16s | MARGINAL |
| deepseek-v4.1-flash-1017 | native | 90% | 90% | 0.6s | 1.35s | MARGINAL |
| deepseek-v4.1-flash-1017 | json | 93% | 87% | 0.74s | 2.51s | MARGINAL |
| mimo-v2.6-pro | native | 100% | 100% | 0.89s | 1.44s | PASS |
| mimo-v2.6-pro | json | 97% | 93% | 1.08s | 1.92s | PASS |
| qwen3.8-27b | native | 100% | 100% | 0.68s | 2.01s | PASS |
| qwen3.8-27b | json | 97% | 87% | 0.69s | 3.09s | PASS |

deepseek-v4.1-flash-1017 failed `answer_after_result` in 3/5 native runs: it re-ran a shell command instead of answering from the result it already had.

## Whole-task tiebreak: fix_repo_v2, strict profile, 3 runs each

| model (native) | passed | finished cleanly | median steps | median tokens | median time |
| --- | --- | --- | --- | --- | --- |
| mimo-v2.6-pro | 3/3 | 3/3 | 8 | 41,309 | 104.8s |
| qwen3.8-27b | 3/3 | 1/3 | 12 | 80,749 | 84.5s |

qwen3.8-27b fixed the repo every time but hit the token budget in 2 of 3 runs instead of finishing.

## Decision

`LLM_MODEL=mimo-v2.6-pro`, `LLM_TOOL_MODE=native`. Fallback: `qwen3.8-27b`, native.
Three runs cannot separate pass rates (95% interval 44-100% for both); the 10-run measurement is the number to quote.
