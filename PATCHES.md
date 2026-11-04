# MiniLocker patch series — context, method, and commit messages

This document explains how the project `Unavailable4u/draft` was split into 10 ordered `.patch` files, how that
was verified, what can go wrong, and how to fix it. It is written so another person or model with **no access to
the original session** can pick it up and continue.

## 1. TL;DR

- **Source:** `https://github.com/Unavailable4u/draft.git`, commit `0120ff4b4ca86349c662183ad84dca606ca50df6`
  ("best design till now"), git tree hash `a3d2ab3d550f281cd9403d0b9e0d786e99799a7f`, **167 tracked files**.
- **Goal:** rebuild that exact tree from an empty folder by applying 10 patches in numeric order.
- **Result:** applying `01`…`10` with `git apply` into an empty root reproduces the source tree. The git tree hash
  matches the original commit, and all 167 files match byte for byte (sha256) with the same file modes.
- **Project code was not modified.** The patches are a re-slicing of the existing commit, not a rewrite.
- **Verified with:** Python 3.13, Node 22, git 2.43 (Linux sandbox, no Docker daemon).

## 2. What the project is (from the README layout, not re-audited)

A FastAPI backend (`backend/minilocker/`) plus a React/Vite/Tailwind frontend (`frontend/`), with Docker deploy
files. Backend packages: `agent` (agent loop and tools), `scenarios`, `llm` (OpenAI-compatible client, tolerant
tool-call parsing, bake-off), `policy` (risk rules, approvals, injection scanner), `sandbox` (hardened code
sandbox, browser sandbox and in-container worker), `egress` (allowlisting proxy), `ledger` (hash chain, Blast
Radius report, session summaries), `trust` (decoy credentials), `infra`, `artifacts` (S3 artifact store),
`attacks` (Attack Lab), `api` (control plane). Also `images/browser/`, `deploy/`, `docs/`.

## 3. The patch series

Every patch **only adds new files** and no file appears in more than one patch (0 overlapping diffs, 167 file
diffs in total). Order follows the import dependency graph, so each patch only depends on earlier ones.

| # | File | Files | Contents | Tests added here |
|---|------|------:|----------|------------------|
| 01 | `01-foundation.patch` | 9 | `.gitignore`, `.gitattributes`, `.dockerignore`, `LICENSE`, `backend/requirements.txt`, `backend/pytest.ini`, `minilocker/__init__.py`, `config.py` | `test_config` |
| 02 | `02-policy-trust-ledger.patch` | 15 | `policy/` (approvals, engine, injection), `trust/` (canary, secrets), `ledger/` (chain, report, summary) | `test_injection`, `test_ledger`, `test_policy`, `test_report_measured` |
| 03 | `03-sandbox-egress.patch` | 20 | `sandbox/` (browser, browser_worker, docker_provider, measure, smoke, snapshot), `egress/` (manager, proxy_server), `images/browser/` (Dockerfile + 5 HTML fixtures) | `test_broker`, `test_browser_worker`, `test_exec_capped`, `test_sandbox_basic` |
| 04 | `04-artifacts-llm.patch` | 10 | `artifacts/` (export, index, serve, store), `llm/` (`__init__`, client, toolcalls) | `test_artifacts`, `test_browser_integration` |
| 05 | `05-agent-runtime.patch` | 20 | `agent/` (browse_tool, control, hooks, loop, watch), `llm/bakeoff.py`, `cli.py`, `backend/smoke_llm.py` | `test_agent_loop`, `test_bakeoff`, `test_browse_loop`, `test_egress`, `test_empty_reply`, `test_live_egress`, `test_llm_client`, `test_policy_loop`, `test_salvage_loop`, `test_toolcalls`, `test_watch_loop` |
| 06 | `06-scenarios-attacks.patch` | 23 | `scenarios/` (base, repo_fix, repo_fix_v2, research, runner), `attacks/` (browser_attacks, catalog, model, runner, scripted) | `test_attack_checks`, `test_bad_arguments`, `test_browser_attacks`, `test_browser_fixtures`, `test_browser_preflight`, `test_check_leaves_workspace`, `test_scenarios_repo`, `test_scenarios_repo_v2`, `test_scenarios_research`, `test_scenarios_runner` |
| 07 | `07-api-infra.patch` | 14 | `api/` (app, tasks, `__main__`), `infra/status.py` | `test_api`, `test_api_artifacts`, `test_api_control`, `test_api_docker`, `test_attacks`, `test_attacks_unit`, `test_deploy_wiring`, `test_sessions` |
| 08 | `08-frontend-base.patch` | 25 | frontend config (`package.json`, lockfile, `tsconfig*`, `vite.config.ts`, `index.html`), `src/` base layer (`api`, `derive`, `theme`, `index.css`, `useTask`, `useAttacks`, `ui`, `Md`, `components`), `src/fonts/*` | — |
| 09 | `09-frontend-views.patch` | 10 | `App`, `AttackLab`, `Browser`, `Files`, `Infra`, `Report`, `Sessions`, `Terminal`, `Timeline`, `main.tsx` | — |
| 10 | `10-deploy-ci-docs.patch` | 21 | `deploy/` (compose, Caddyfile, Dockerfiles, bootstrap/dry_run/dev-storage scripts, env examples, smoke_check), `.github/workflows/ci.yml`, `README.md`, `SECURITY.md`, `docs/` (+ `assets/cover.png`) | `test_bootstrap`, `test_ci_hygiene`, `test_docs`, `test_smoke_check` |

Why 08 is split from 09: the frontend base files (`api`, `derive`, `ui`, `Md`, `components`, hooks) never import a
view, while `App.tsx` imports every view and `main.tsx` imports `App`. So 08 type-checks on its own, and 09 adds
the views on top.

Why 10 is last: `test_docs`, `test_ci_hygiene`, `test_bootstrap` and `test_smoke_check` read `README.md`,
`SECURITY.md`, `.gitattributes`, `deploy/*` and the git index from disk, so they only make sense once those exist.

### Integrity checksums (SHA-256)

```
998371193c701264658ba5f3b797f208a1876e9e746e21781531bd229ed08bb0  01-foundation.patch
5efe587d88a1d023f66237c6415654e3bb0cc9a9520d9bc94c2ee9912b1b785a  02-policy-trust-ledger.patch
fee32a57c2842375650a3b3e322c52fea6d2199547a1824b5df3ac424f20652d  03-sandbox-egress.patch
0df327d8fb7c92bc658761f0340f217683b103cdbb357fc815c5b0e3241951db  04-artifacts-llm.patch
77335f7b586448065cd9b9ded967691e13994551e8a0b1210b0454a1837e67a9  05-agent-runtime.patch
fb6182a4ee7d07484e85426b63e57c7ad8d926da7f591c1141382863d98ae8d9  06-scenarios-attacks.patch
8882434a15c5207b85a2928e85930c7c530bd3b3ad203b882fb55434a132fff7  07-api-infra.patch
7d0b4367fb12399e3919959f188f1dcd4a468bd3152ed5a014ef2de990cb88ce  08-frontend-base.patch
6ed505ba4e62d83f2eeea8c393c43fc7b9d363bad7080a69432f51e21d03bb02  09-frontend-views.patch
21eeaf1e7c2d77a6c0433e42935565afb7e89269961c5dbc3aec867c7250ac9f  10-deploy-ci-docs.patch
```

Check with `sha256sum -c` (Git Bash) or `Get-FileHash -Algorithm SHA256 *.patch` (PowerShell). If a hash differs,
the patch file was altered after download. Re-download it. Do not try to hand-fix it.

## 4. How to apply

Use an **empty** folder. `git apply` refuses to overwrite existing files, so a second run fails with
`already exists in working directory` instead of clobbering anything.

Git Bash (this is the form that was tested):

```bash
git init
git config core.autocrlf false        # optional: keep LF files, same bytes as the source repo
for p in /path/to/patches/*.patch; do git apply --binary --whitespace=nowarn "$p" || break; done
```

PowerShell (equivalent, not tested):

```powershell
foreach ($p in (Get-ChildItem C:\path\to\patches\*.patch | Sort-Object Name)) {
  git apply --binary --whitespace=nowarn $p.FullName
  if ($LASTEXITCODE) { break }
}
```

To also get **one git commit per patch** with the embedded messages, use `git am --keep-cr patches/*.patch`.
`--keep-cr` is required: without it `git am` strips the single CRLF line in `.gitignore`, which changes the tree
hash. The patch files carry short built-in commit messages and author `Shaikh Md Abu Ahad` (taken from the original
commit). Their dates (2026-11-05 01:31–01:40 +0600) are synthetic and do not reflect real history. The fuller
messages in section 8 are meant to replace those if you commit by hand.

`--binary` matters: `08` contains seven `.woff2` fonts and `10` contains `docs/assets/cover.png`, stored as git
binary patches.

### VS Code notes

- Use the integrated terminal with the **Git Bash** profile for the loop above.
- After applying, the Source Control panel shows every file as new. Stage all, paste a message from section 8
  into the message box (first line is the subject), and commit. Do this after each patch if you want 10 commits.
- **Do not open and save the `.patch` files in the editor.** Format-on-save, `files.trimTrailingWhitespace` and
  automatic EOL conversion can silently corrupt a patch (it contains CRLF, trailing whitespace and base85 data
  that must stay byte-exact). Reading is fine; just don't save.

## 5. How the patches were made

Two scripts (shipped alongside this file) drive everything. Both take paths as arguments.

1. **`build_patches.py SRC_CLONE STAGING_DIR OUT_DIR`**
   - Lists every tracked file (`git ls-files`) and records the file modes (`100644` / `100755`).
   - Assigns each non-test file to a patch by directory (the table above).
   - Places each test in the **earliest patch where everything it needs already exists**. It finds what a test
     needs by (a) parsing its imports with `ast`, (b) regex-scanning the text for any `minilocker.x.y` string,
     and (c) following imports of *other test files* (`from test_api import make`) to a fixpoint. Tests that read
     non-Python files (`test_docs`, `test_ci_hygiene`, `test_bootstrap`, `test_smoke_check`) are pinned to patch 10.
   - Asserts every file is assigned exactly once, copies files into a throwaway git repo (preserving the exec
     bit), makes one commit per patch, then runs
     `git format-patch --root --numbered --binary --full-index --no-signature --zero-commit`.
   - Renames the output to `NN-slug.patch`.
2. **`staged_tests.py PATCH_DIR WORK_DIR VENV_PYTHON`**
   - Applies the patches one at a time into a fresh directory. After each, it byte-compiles the backend and runs
     **only the test files that patch introduced**. Finally it runs the whole suite on the finished tree and
     compares per-test outcomes. Any difference means a test landed too early.
   - Needs a venv with `backend/requirements.txt` installed.

A real bug was caught this way: `test_sessions.py` does `from test_api import make, run, stream_all`, and the first
version of the planner only followed `minilocker` imports, so it put `test_sessions` in patch 02 where it failed
to collect. Following test-to-test imports moved it to patch 07.

## 6. Verification results

| Check | Result |
|-------|--------|
| `git apply --check` then apply, 01→10, empty root | all 10 apply cleanly |
| File set / sha256 / file mode vs original (167 files) | identical |
| Git tree hash (`git add -f -A && git write-tree`) | `a3d2ab3d550f281cd9403d0b9e0d786e99799a7f`, equal to original |
| `git am --keep-cr` in a fresh repo | 10 commits, same tree hash |
| `git am` without `--keep-cr` | differs, only the CR in `.gitignore` |
| Repo with `core.autocrlf=true` (Windows default) | 141 files differ from source **only** in CRLF (0 real diffs); `*.sh`, `Dockerfile*`, `Caddyfile` stay LF because `.gitattributes` pins them |
| Executable bit | kept on `deploy/bootstrap.sh`, `deploy/dev-storage.sh`, `deploy/dry_run.sh` |
| Backend tests, each at its own stage vs full tree | 872 tests, **0 outcome mismatches** |
| Frontend | `npm ci` (131 packages) then `tsc --noEmit` clean at patch 08 and 09; `vite build` succeeds (one chunk-size warning, ~787 kB JS) |

### Expected test failures without Docker

Full suite on the finished tree: 804 passed, 24 skipped, 44 failed or errored. The original repo gives the same
44. **43 are "Docker daemon not reachable"** (`test_sandbox_basic`, `test_attacks`, `test_api_docker`,
`test_egress`, `test_agent_loop`, `test_policy_loop`). The 44th, `test_api_docker::test_strict_task_through_api`,
runs a real container task and stays `running` with no daemon. With Docker running these should pass; they were
not run against Docker here.

Two `test_ci_hygiene` tests skip with "not a git checkout" unless the tree is a git repo. In a repo all three pass,
which also confirms the exec bits and LF pinning survived.

## 7. Troubleshooting for the next person or model

| Symptom | Likely cause and fix |
|---------|----------------------|
| `already exists in working directory` | Target folder isn't empty, or the patch was already applied. Use a clean folder. |
| `corrupt patch at line N` / `patch does not apply` | Patch file was changed after download (editor saved it, EOL conversion, truncated download). Compare SHA-256 against section 3 and re-download. |
| Hash of rebuilt tree ≠ `a3d2ab3d…` | Check `core.autocrlf` (should be `false` to compare), and whether `git am` was used without `--keep-cr`. Then diff against a fresh clone of the source commit: `git diff --no-index <clone> <applied>`. |
| `Permission denied` running `deploy/*.sh` after applying on Linux/WSL | Exec bit lost (e.g. applied via a Windows filesystem). Run `git update-index --chmod=+x deploy/*.sh` and `chmod +x deploy/*.sh`. |
| Tests that need Docker fail | Start Docker; see section 6. |
| `test_ci_hygiene` skips | Run inside a git repo (`git init && git add -A`). |
| Want to regenerate | `python3 -I build_patches.py <clone-at-0120ff4> <staging> <out>`; it prints which tests were moved and the per-patch file counts. |
| `git apply` warns "trailing whitespace" | Harmless. `frontend/src/fonts/OFL.txt` has trailing spaces in the original; `--whitespace=nowarn` silences it. |

### Observations about the source repo (not changed)

- `frontend/tsconfig.tsbuildinfo` is a build artifact tracked in git.
- `frontend/src/fonts/*.woff2` (about 1.4 MB) is not referenced by any code; `main.tsx` imports the
  `computer-modern` npm package instead.
- `.gitignore` is the only file with CRLF line endings. Git strips the CR when reading ignore files, so it works.

## 8. Commit messages (one per patch)

Each block is ready to paste into the VS Code Source Control message box or use with `git commit -F`. The two
trailer lines at the bottom of each can be deleted if you don't want them in your history.

### 01

```
Add repo foundation: meta files, env loader, backend skeleton

Part 1 of 10. Adds the files everything else builds on: .gitignore,
.gitattributes (LF pinned for *.sh, Dockerfile*, Caddyfile),
.dockerignore and LICENSE; backend requirements and pytest config; the
minilocker package root and the .env loader (config.py).

Tests: test_config.

Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01GwkPXgi2RD84RLYTh11Wws
```

### 02

```
Add security core: policy engine, canaries and hash-chained ledger

Part 2 of 10. Adds policy/ (risk rules, approvals, prompt-injection
scanner), trust/ (decoy credentials and the list of real secrets the
audit looks for) and ledger/ (hash chain, Blast Radius report, session
summaries).

Depends on: 01.
Tests: test_policy, test_injection, test_ledger, test_report_measured.

Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01GwkPXgi2RD84RLYTh11Wws
```

### 03

```
Add isolation layer: sandboxes, egress proxy and browser image

Part 3 of 10. Adds sandbox/ (hardened Docker sandbox, resource
measurement, snapshots, browser sandbox and its in-container worker),
egress/ (allowlisting proxy and network manager) and images/browser/
(Dockerfile plus HTML test fixtures).

Depends on: 01.
Tests: test_sandbox_basic, test_exec_capped, test_broker,
test_browser_worker. Docker-backed tests need a running daemon.

Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01GwkPXgi2RD84RLYTh11Wws
```

### 04

```
Add artifact store and OpenAI-compatible LLM client

Part 4 of 10. Adds artifacts/ (S3 artifact store, workspace export,
serving and index) and llm/ (OpenAI-compatible client with retry
nudges, tolerant tool-call parsing).

Depends on: 03.
Tests: test_artifacts, test_browser_integration (needs Docker and the
minilocker-browser image, skipped otherwise).

Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01GwkPXgi2RD84RLYTh11Wws
```

### 05

```
Add agent runtime: loop, watch, hooks, browse tool, CLI, bake-off

Part 5 of 10. Adds agent/ (the agent loop and its tools, watch,
hooks, task control, browse tool), the model bake-off (llm/bakeoff.py),
the CLI entry point and backend/smoke_llm.py.

Depends on: 02, 03, 04.
Tests: test_agent_loop, test_browse_loop, test_watch_loop,
test_policy_loop, test_salvage_loop, test_empty_reply, test_llm_client,
test_toolcalls, test_bakeoff, test_egress, test_live_egress.

Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01GwkPXgi2RD84RLYTh11Wws
```

### 06

```
Add hero scenarios and the Attack Lab catalog

Part 6 of 10. Adds scenarios/ (repo-fix v1 and v2, research, shared
base and the repeating runner) and attacks/ (scripted and browser
attacks, the catalog, the runner and result model).

Depends on: 05.
Tests: the scenario, attack-check, browser-attack and bad-argument
suites (10 files).

Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01GwkPXgi2RD84RLYTh11Wws
```

### 07

```
Add FastAPI control plane and infra status

Part 7 of 10. Adds api/ (REST and SSE endpoints, task manager) and
infra/ (host, Docker and endpoint status read by the Infra screen).

Depends on: 06.
Tests: API, artifacts API, control, Docker API, attacks, deploy wiring
and sessions (8 files).

Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01GwkPXgi2RD84RLYTh11Wws
```

### 08

```
Add frontend base: build config, fonts, API client, shared UI

Part 8 of 10. Adds the Vite, TypeScript and Tailwind setup with the
lockfile, the theme and CSS, the typed API client, derived-state
helpers, the task and attack hooks, shared UI and Markdown components,
and the bundled font files. Type-checks on its own.

Depends on: none (frontend only; talks to the API from 07 at runtime).

Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01GwkPXgi2RD84RLYTh11Wws
```

### 09

```
Add frontend views: App shell and all screens

Part 9 of 10. Adds App, the Attack Lab, Browser, Files, Infra, Report,
Sessions, Terminal and Timeline screens, and main.tsx.

Depends on: 08.

Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01GwkPXgi2RD84RLYTh11Wws
```

### 10

```
Add deploy stack, CI, docs and deploy/docs tests

Part 10 of 10. Adds deploy/ (compose stack, Caddy config, Dockerfiles,
bootstrap, dry-run and smoke-check scripts, env examples),
.github/workflows/ci.yml, README, SECURITY, docs/ and the cover image.

Depends on: all earlier patches.
Tests: test_docs, test_ci_hygiene, test_bootstrap, test_smoke_check.

Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01GwkPXgi2RD84RLYTh11Wws
```

## 9. Handoff prompt for another model

> I'm rebuilding the repo `Unavailable4u/draft` (commit `0120ff4`) from 10 ordered patches in an empty folder.
> Read `PATCHES.md` first. Apply with
> `git apply --binary --whitespace=nowarn` in numeric order. Do not edit the `.patch` files. Here is my error:
> `<paste output>`. Check section 7 before suggesting a fix, and tell me which patch and file it concerns.
