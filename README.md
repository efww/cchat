# cchat

**English** | [한국어](README.ko.md)

A browser front-end (desktop and phone) for [Claude Code](https://docs.anthropic.com/claude-code) running on a Mac. It uses [ttyd](https://github.com/tsl0922/ttyd) + tmux to keep several claude sessions alive and lets you switch between them with tabs at the bottom of the screen.

**For** people who run several Claude Code jobs at once and switch between phone and PC.

**Why**
- **Same screen on phone and PC.** Both open the very same tmux sessions — start on the PC, continue on the phone mid-task.
- **One tap between jobs.** Sessions are tabs; switching is a single tap or Alt+number.
- **Status at a glance.** Blinking = working, orange = needs you, green = done. No need to open each session.
- **Your real Claude Code.** Runs on your own Mac with your files, tools and settings. Nothing to install on the phone — just a browser.

**Limits**
- No push notifications: colors show only while the page is open.
- macOS only, and the Mac must stay on.
- Remote access needs your own tunnel + authentication.

![cchat demo](docs/demo.gif)

*One-minute walkthrough ([mp4](docs/demo.mp4)).*

## Features

- **Session tabs**: the bottom two rows are session tabs. The top row shows the number; the bottom row shows the session label (cut off with `…` when too long).
  - Black = the session you are viewing
  - Green = finished replying, not seen yet
  - Orange = waiting for your permission or answer
  - Blinking gray (2 s) = working (all working tabs blink in sync)
- **Desktop shortcuts**: Alt(Option)+number = go to that session, Alt+←/→ = previous/next. Ctrl+V pastes your local (browser) clipboard.
- **Phone**: finger-drag scrolling, a key bar (Esc, Tab, arrows, …), dark theme.
- Sessions live inside tmux, so they keep running after you close the browser. Open the URL with `?arg=name` to attach to that session (created if missing).

## How to use

1. **Open a session**: go to `http://127.0.0.1:7681/cchat/?arg=1`. Each `?arg=name` is its own claude session; a new name creates a new tab.
2. **Start a task and move on**: type your prompt, press Enter, then switch to another tab with **Alt+number** (or click it). The tab you left blinks gray while claude works.
3. **Watch the colors**: when that tab turns **green**, the answer is ready; **orange** means claude is waiting for your approval or an answer.
4. **Go back**: click the tab, or use **Alt+←/→**. Opening a tab clears its color. Approve in the orange tab and claude continues.
5. **Close the browser any time**: sessions keep running in tmux. Open the page again and everything is where you left it. Type `/exit` in a session to close its tab.

On a phone, tap a tab to switch; drag with your finger to scroll, and use the key bar for Esc, Tab and arrows.

## Requirements

macOS, Homebrew `ttyd` and `tmux`, python3, and the Claude Code CLI (`~/.local/bin/claude`).

## Install

```sh
cp cchat.conf.example my.conf     # edit values (work folder, port, permission mode, …)
./install.sh -c my.conf
open http://127.0.0.1:7681/cchat/
```

`install.sh` fills the `@@NAME@@` placeholders in `bin/ config/ launchd/` with your config values, installs them into `~/.local/bin`, `~/.config/cchat` and `~/Library/LaunchAgents`, and (re)starts the launchd services.
To render without installing: `./install.sh -c my.conf --render-only /tmp/out`.

## Remote access (read this)

ttyd listens on 127.0.0.1 only and has **no authentication of its own**. To use it from outside, expose it through `TUNNEL_HOST` (a reverse SSH tunnel to your server) and always put authentication in front of it (Cloudflare Access, an OAuth proxy, etc.).
`PERMISSION_MODE=bypassPermissions` lets claude run commands without asking — use it only when access is properly authenticated.

## Layout

| File | Role |
|---|---|
| `bin/cchat-session` | Run by ttyd for each connection. Attaches to a tmux session and runs claude in a loop inside it |
| `bin/cchat-tabs` | Draws the session tabs in the status line; handles clicks and shortcuts |
| `bin/cchat-unread` | Called by claude hooks (done, permission, started work) to color the tabs |
| `bin/cchat-build-index` | Builds `index.html` from ttyd's default page plus the cchat parts (themes, phone key bar and scrolling, shortcuts, blinking) |
| `bin/cchat-label` | Set a session label by hand |
| `bin/cchat-tunnel` | (optional) reverse SSH tunnel |
| `bin/cchat-update` | (optional) daily claude CLI update |
| `config/` | tmux config, claude settings (theme, hooks) |
| `launchd/` | Service definitions |

Tab labels come from `~/.cache/cchat-tablabel/<session>` if that file exists (e.g. written by your status line script); otherwise the title claude gave the conversation is used.

Code comments are in Korean.

## License

MIT
