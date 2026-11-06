# Installing cchat (instructions for an AI coding agent)

You are installing cchat for the user on **this Mac**. Follow the steps in order, run the checks, and stop to ask the user only where it says **Ask**. Report what you did at the end.

## 0. Check the machine

```sh
sw_vers -productName                 # must be macOS
command -v brew                      # Homebrew is required
xcode-select -p                      # Command Line Tools (provides /usr/bin/python3, git)
command -v claude || ls ~/.local/bin/claude   # Claude Code CLI must be installed and logged in
```

- If Homebrew or the Command Line Tools are missing, tell the user and stop (both need the user's password).
- If `claude` is missing, tell the user to install Claude Code first (https://docs.anthropic.com/claude-code) and stop.

Install the two dependencies:

```sh
brew install ttyd tmux
```

## 1. Get the code

```sh
git clone https://github.com/efww/cchat.git ~/cchat   # or `git -C ~/cchat pull` if it exists
cd ~/cchat
cp cchat.conf.example my.conf
```

## 2. Fill in `my.conf`

Set `BREW` to the output of `echo "$(brew --prefix)/bin"` (Apple Silicon: `/opt/homebrew/bin`, Intel: `/usr/local/bin`).

**Ask** the user these, one message, with the defaults shown:

1. **Work folder** for the claude sessions (`WORKDIR`, default: home folder).
2. **Permission mode** (`PERMISSION_MODE`): `default` (claude asks before running commands — recommended) or `bypassPermissions` (never asks; only if the page will be reachable by nobody but them).
3. **Port** (`PORT`, default 7681). Check it is free: `lsof -nP -iTCP:7681 -sTCP:LISTEN` prints nothing.

Leave the rest as is. `TUNNEL_HOST` stays empty: cchat is then reachable only from this Mac (`127.0.0.1`). Remote access is a separate step (section 5) and only if the user asks.

## 3. Install

```sh
./install.sh -c my.conf
```

It installs scripts into `~/.local/bin`, config into `~/.config/cchat`, and a launchd service `<LAUNCHD_PREFIX>.ttyd` (default `local.cchat.ttyd`) that starts at login.

## 4. Verify

```sh
curl -s -o /dev/null -w '%{http_code}\n' http://127.0.0.1:7681/cchat/     # 200 (use the chosen port)
launchctl print gui/$(id -u)/local.cchat.ttyd | grep -m1 state            # state = running
```

Then open it for the user: `open "http://127.0.0.1:7681/cchat/?arg=1"`. A claude session should start in the work folder, with the session tabs in the bottom two rows.

Tell the user:
- `?arg=name` opens (or creates) the session `name`; each one becomes a tab.
- Alt+number / Alt+←→ switch tabs on desktop; tap a tab on a phone.
- Green = done, orange = waiting for them, blinking gray = working.
- Logs: `~/Library/Logs/cchat-ttyd.log`.

## 5. Remote access (only if the user asks)

ttyd has **no authentication**. Never expose the port directly. The supported way:

1. The user needs a server they reach with `ssh <host>` (key login, no password prompt) and an authenticating reverse proxy on it (e.g. Cloudflare Access, oauth2-proxy) that forwards to `127.0.0.1:<TUNNEL_REMOTE_PORT>` on that server.
2. Set `TUNNEL_HOST=<host>` and `TUNNEL_REMOTE_PORT` in `my.conf`, run `./install.sh -c my.conf` again. This adds the `…tunnel` launchd service (a reverse SSH tunnel).
3. Set `PUBLIC_URL` to the proxied URL.

Explain this to the user and let them set up the server side; do not configure their server without being asked.

## Update

```sh
cd ~/cchat && git pull && ./install.sh -c my.conf
```

Also run `./install.sh -c my.conf` after `brew upgrade ttyd`. Open browser pages need a reload to pick up changes.

## Uninstall

```sh
for s in ttyd tunnel update; do launchctl bootout gui/$(id -u)/local.cchat.$s 2>/dev/null; rm -f ~/Library/LaunchAgents/local.cchat.$s.plist; done
tmux -L cchat kill-server 2>/dev/null
rm -f ~/.local/bin/cchat-*
rm -rf ~/.config/cchat ~/.cache/cchat-*
```

(Replace `local.cchat` if `LAUNCHD_PREFIX` was changed.)
