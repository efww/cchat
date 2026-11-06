# cchat

**English** | [한국어](README.ko.md)

A browser front-end (desktop and phone) for [Claude Code](https://docs.anthropic.com/claude-code) running on a Mac. It uses [ttyd](https://github.com/tsl0922/ttyd) + tmux to keep several claude sessions alive and lets you switch between them with tabs at the bottom of the screen.

## Features

- **Session tabs**: the bottom two rows are session tabs. The top row shows the number; the bottom row shows the session label (cut off with `…` when too long).
  - Black = the session you are viewing
  - Green = finished replying, not seen yet
  - Orange = waiting for your permission or answer
  - Blinking gray (2 s) = working (all working tabs blink in sync)
- **Desktop shortcuts**: Alt(Option)+number = go to that session, Alt+←/→ = previous/next. Ctrl+V pastes your local (browser) clipboard.
- **Phone**: finger-drag scrolling, a key bar (Esc, Tab, arrows, …), dark theme.
- Sessions live inside tmux, so they keep running after you close the browser. Open the URL with `?arg=name` to attach to that session (created if missing).

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
