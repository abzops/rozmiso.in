# Antigravity CLI findings

Checked 6 October 2026. Research complete; executable discovery and authenticated execution remain unverified.

## Local evidence

- `Get-Command antigravity, agy, ag -ErrorAction SilentlyContinue` returned no command in the current PowerShell session.
- Found `C:/Users/Abhinand/AppData/Local/Programs/Antigravity/Antigravity.exe`. Windows product metadata reports `2.19.1.0`. This is the installed GUI application, not evidence of a headless agent CLI.
- No executable found at the documented user installation path `C:/Users/Abhinand/AppData/Local/agy/bin/agy.exe`, the troubleshooting path `C:/Program Files/Google/antigravity-cli/agy.exe`, or `C:/Users/Abhinand/.local/bin/agy.exe`.
- The GUI installation has no top-level `bin` directory. Its `resources/bin` contains `language_server.exe` and `webm_encoder.exe`; neither was treated as a supported public CLI.
- No supported CLI was located, so no `--version`, `--help`, sign-in, model request, installation or GUI launch was executed. This checks known paths, not every possible portable installation on the computer.
- No credential stores, browser authentication data, account settings or environment-secret values were inspected.

## Supported authentication options

The official Windows agent CLI command is `agy`. The documented installer places it under the user's `AppData/Local/agy/bin`. Local interactive startup uses the operating-system keyring if authenticated; otherwise it opens Google sign-in in the default browser. The owner enters credentials directly there, never into a team prompt or chat. Remote SSH authentication instead uses a browser authorization URL and a code pasted into that terminal; it does not meet a strict no-code-copy preference. API-key mode requires `modelProvider: "gemini"` in `~/.gemini/antigravity-cli/settings.json` plus `GEMINI_API_KEY` in the environment, and uses the Gemini API rather than an account session. It is not selected for this subscription-based setup. `/logout` removes cached account authentication and must not be run merely to inspect access. [Official installation and authentication](https://www.antigravity.google/docs/cli/install/).

Enterprise ADC is another documented option: Google Cloud project onboarding and `AGY_ADC_AUTH=true`. It is not evidence that the owner's Pro subscriptions include enterprise/API access, and it is not configured here. [Official enterprise authentication](https://www.antigravity.google/docs/enterprise/).

## Supported automation and limitations

After interactive authentication, `agy -p` runs a prompt non-interactively using cached credentials. A non-interactive unauthenticated run exits with an authentication-required error. `--output-format json` or `stream-json` supplies machine-readable results, `--agent` selects an agent, and `--print-timeout` bounds a run. `agy agents` lists profiles. Headless workspace reads/writes are normally allowed, while unapproved shell actions can be soft-denied even with exit code zero. A controller must inspect result status, notices and required artifacts, not only exit code. Prompt-only task boundaries are not technical isolation. Do not use `--dangerously-skip-permissions` as a setup shortcut. [Official headless mode](https://www.antigravity.google/docs/cli/headless/).

The reference documents `/agents`, `/usage` and `/permissions`; `useG1Credits` defaults to false in documented settings. No settings were read or changed here, so the actual account's credit fallback and permissions remain unknown. [Official CLI reference](https://www.antigravity.google/docs/cli/reference/).

The reviewed authentication/flag documentation does not establish a per-task Google-account selector or two simultaneously isolated consumer-account profiles in one Windows login. Do not infer account separation from two terminals, two app windows or two subscriptions. Independent supported authenticated environments, or sequential owner-controlled account selection, need verification before assigning concurrent A/B requests.

## Practical next steps

1. The orchestrator can prepare bounded CLI briefs and an isolated smoke-test workspace now. Locate a supported executable if the owner installed it elsewhere; otherwise installing the official CLI is a distinct system change not performed in this audit.
2. Once available, inspect its actual help/version before relying on flags. Authenticate interactively with the owner selecting the intended Google account and completing any verification directly in Google's browser flow. No password/token/code needs to enter this chat for local sign-in.
3. Confirm the runtime's displayed account, plan/usage and profile discovery using supported interfaces. Do not claim successful model execution from an authenticated-looking header alone. Use a tiny authorized read-only agent task afterwards to prove functioning access, with no live Shopify changes or spending and no credit-overage fallback.
4. Start one authenticated lane first. Only enable the second lane after supported account isolation is demonstrated. Codex remains the board writer and acceptance authority.

An authenticated runtime cannot be verified within this audit's read-only discovery scope: no supported executable was found, and launching/sign-in/model requests were expressly excluded. Current status is prepared instructions, not a connected operational team.
