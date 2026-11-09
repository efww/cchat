#!/bin/zsh
# cchat 설치/갱신: 설정 파일 값을 bin/ config/ launchd/ 의 @@이름@@ 자리에 넣어 제자리에 깔고,
# index.html을 다시 만들고, launchd 서비스를 다시 올린다.
#   ./install.sh -c <설정파일>                    설치(설정 예시: cchat.conf.example)
#   ./install.sh -c <설정파일> --render-only <폴더>  설치하지 않고 <폴더>/{bin,config,launchd}에 결과만 만든다(비교·검증용)
set -euo pipefail
cd "${0:A:h}"

conf="" out=""
while (( $# )); do
  case "$1" in
    -c) conf="$2"; shift 2 ;;
    --render-only) out="$2"; shift 2 ;;
    *) print -u2 "알 수 없는 인자: $1"; exit 2 ;;
  esac
done
[[ -n "$conf" && -f "$conf" ]] || { print -u2 "설정 파일을 -c로 주세요 (예: cp cchat.conf.example my.conf)"; exit 2; }
source "$conf"
# 선택 항목(없으면 기본값): TMUX_SOCKET = tmux 서버 이름(시험용 샌드박스를 따로 띄울 때 바꾼다),
# CLAUDE_BIN = claude 실행 파일(없으면 지금 PATH에서 찾는다. nvm·npm으로 깐 경우도 그대로 잡힌다).
: ${TMUX_SOCKET:=cchat}
: ${INBOX_REMOTE:=}     # 폰 📎 업로드를 받아 둘 원격 "호스트:폴더"(원격 중계가 있을 때만, 비우면 끔)
: ${KEEP_AWAKE:=0}     # 1이면 ttyd가 떠 있는 동안 맥이 잠들지 않게(caffeinate -is)
: ${BASE_PATH:=/cchat}   # ttyd 주소 경로(시험용 샌드박스는 /cchat/t 처럼 따로)
[[ -n "${CLAUDE_BIN:-}" ]] || CLAUDE_BIN=$(command -v claude 2>/dev/null || true)
[[ -n "$CLAUDE_BIN" ]] || { [[ -x $HOME_DIR/.local/bin/claude ]] && CLAUDE_BIN=$HOME_DIR/.local/bin/claude; }
KEYS=(HOME_DIR BREW WORKDIR PERMISSION_MODE PORT FONT_SIZE LAUNCHD_PREFIX PUBLIC_URL TUNNEL_HOST TUNNEL_REMOTE_PORT TMUX_SOCKET CLAUDE_BIN BASE_PATH KEEP_AWAKE INBOX_REMOTE)
for k in $KEYS AUTO_UPDATE; do [[ -v $k ]] || { print -u2 "설정에 $k 가 없습니다"; exit 2; }; done

# 설치 전 점검: 하나라도 틀리면 아무것도 바꾸지 않고 멈춘다(예전엔 서비스가 조용히 죽거나 claude가 끝없이 재시작됐다).
problems=()
for b in ttyd tmux; do [[ -x $BREW/$b ]] || problems+=("$BREW/$b 가 없습니다 — brew install ttyd tmux, BREW=\"\$(brew --prefix)/bin\" 확인"); done
[[ -n "$CLAUDE_BIN" && -x "$CLAUDE_BIN" ]] || problems+=("claude 실행 파일을 찾지 못했습니다 — Claude Code를 설치하거나 설정에 CLAUDE_BIN=<경로>")
[[ "$PERMISSION_MODE" == (default|acceptEdits|plan|bypassPermissions) ]] || problems+=("PERMISSION_MODE=$PERMISSION_MODE 는 쓸 수 없습니다(default|acceptEdits|plan|bypassPermissions)")
[[ "$PORT" == <1024-65535> ]] || problems+=("PORT=$PORT 가 올바르지 않습니다")
[[ -d "$WORKDIR" ]] || problems+=("WORKDIR=$WORKDIR 폴더가 없습니다")
[[ "$BASE_PATH" =~ '^(/[A-Za-z0-9_-]+)+$' ]] || problems+=("BASE_PATH=$BASE_PATH 형식은 /cchat 처럼")
[[ "$KEEP_AWAKE" == (0|1) ]] || problems+=("KEEP_AWAKE 는 0 또는 1")
[[ "$TMUX_SOCKET" =~ '^[A-Za-z0-9_-]+$' ]] || problems+=("TMUX_SOCKET=$TMUX_SOCKET 은 영문·숫자·-·_ 만")
if [[ -z "${out:-}" ]]; then
  # 포트를 다른 프로그램이 쓰고 있으면 멈춘다(우리 ttyd면 괜찮음 — 재설치).
  holder=$(lsof -nP -iTCP:$PORT -sTCP:LISTEN -Fc 2>/dev/null | sed -n 's/^c//p' | head -1)
  [[ -z "$holder" || "$holder" == ttyd ]] || problems+=("포트 $PORT 를 $holder 가 쓰고 있습니다 — 설정의 PORT를 바꾸세요")
fi
(( $#problems )) && { print -u2 "설치 전 점검 실패:"; for p in $problems; do print -u2 "  - $p"; done; exit 2; }

# 파일 하나를 렌더링: @@HOME@@ 은 HOME_DIR 값, 나머지는 같은 이름. 남은 @@...@@가 있으면 실패.
render() {  # <원본> <결과>
  CCHAT_VALUES="$(for k in $KEYS; do print -r -- "$k=${(P)k}"; done)" python3 -I - "$1" "$2" <<'PY'
import os, re, sys
vals = dict(l.split("=", 1) for l in os.environ["CCHAT_VALUES"].splitlines())
vals["HOME"] = vals.pop("HOME_DIR")
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf-8").read()
s = re.sub(r"@@([A-Z_]+)@@", lambda m: vals[m.group(1)] if m.group(1) in vals else m.group(0), s)
left = re.findall(r"@@[A-Z_]+@@", s)
if left:
    sys.exit(f"{src}: 값이 없는 자리 {sorted(set(left))}")
open(dst, "w", encoding="utf-8").write(s)
PY
}

SERVICES=(ttyd)
[[ -n "$TUNNEL_HOST" ]] && SERVICES+=(tunnel)
[[ "$AUTO_UPDATE" == 1 ]] && SERVICES+=(update)
BINS=(bin/*)

if [[ -n "$out" ]]; then
  mkdir -p "$out"/{bin,config,launchd}
  for f in $BINS; do render $f "$out/bin/${f:t}"; done
  for f in config/*; do render $f "$out/config/${f:t}"; done
  for n in $SERVICES; do render launchd/$n.plist "$out/launchd/$LAUNCHD_PREFIX.$n.plist"; done
  print "rendered -> $out"
  exit 0
fi

H=$HOME_DIR
mkdir -p $H/.local/bin $H/.config/cchat $H/Library/LaunchAgents $H/Library/Logs
tmp=$(mktemp -d); trap 'rm -rf $tmp' EXIT
for f in $BINS; do render $f $tmp/${f:t}; install -m 755 $tmp/${f:t} $H/.local/bin/; done
for f in config/*; do render $f $tmp/${f:t}; install -m 644 $tmp/${f:t} $H/.config/cchat/; done
$H/.local/bin/cchat-build-index

U="gui/$(id -u)"
for n in $SERVICES; do
  label="$LAUNCHD_PREFIX.$n"
  render launchd/$n.plist $tmp/$label.plist
  install -m 644 $tmp/$label.plist $H/Library/LaunchAgents/
  launchctl bootout "$U/$label" 2>/dev/null || true
  # bootout은 비동기라 바로 bootstrap하면 "5: Input/output error"로 실패할 때가 있다(2026-11-06 통로가 끊김) → 내려갈 때까지 기다리고 몇 번 다시 시도.
  for i in {1..50}; do launchctl print "$U/$label" >/dev/null 2>&1 || break; sleep 0.1; done
  ok=0
  for i in {1..5}; do launchctl bootstrap "$U" $H/Library/LaunchAgents/$label.plist 2>/dev/null && { ok=1; break; }; sleep 1; done
  (( ok )) || { print -u2 "실패: $label 서비스를 올리지 못했습니다"; exit 1; }
  print "loaded $label"
done
# 이미 떠 있는 tmux 서버에 새 설정을 읽힌다(없으면 무시).
$BREW/tmux -L $TMUX_SOCKET source-file $H/.config/cchat/tmux.conf 2>/dev/null || true

print "done. 폰/PC 브라우저는 새로고침해야 새 화면이 적용된다."
