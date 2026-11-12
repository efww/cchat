# cchat

[English](README.md) | **한국어**

Claude Code를 브라우저(PC·폰)에서 쓰는 웹 터미널. 맥 한 대에서 [ttyd](https://github.com/tsl0922/ttyd) + tmux로 claude 대화 여러 개를 띄워 두고, 아래 탭으로 오간다.

**누구를 위한 것:** Claude Code 작업 여러 개를 동시에 돌리면서 폰과 PC를 오가는 사람.

**장점**
- **폰과 PC가 같은 화면.** 둘 다 같은 tmux 대화를 연다. PC에서 하던 걸 폰에서 그대로 이어서 한다.
- **작업 이동이 탭 한 번.** 대화가 탭이라 폰은 한 번 누르면, PC는 Alt+숫자로 넘어간다.
- **진행 상황이 한눈에.** 번호 옆 ⠹ 스피너 = 작업 중, 주황 = 내 차례, 녹색 = 끝남. 하나씩 열어 볼 필요가 없다.
- **내 맥의 진짜 Claude Code.** 내 파일·도구·설정 그대로. 폰엔 설치할 것 없이 브라우저만.

**한계**
- 알림은 직접 고른 작은 훅이 보낸다([ntfy](examples/notify-ntfy)·[macOS](examples/notify-macos) 예시 포함). 푸시 서버는 들어 있지 않다.
- macOS 전용이고, 맥이 켜져 있어야 한다.
- 밖에서 접속하려면 통로와 인증을 직접 갖춰야 한다.

![cchat 시연](docs/demo.gif)

*1분 사용 시연 ([mp4](docs/demo.mp4)). 화면 안내 문구는 영어입니다.*

## 설치

맥에서 Claude Code(또는 다른 코딩 에이전트)에 이 문장을 붙여 넣으면 됩니다:

```
https://github.com/efww/cchat 을 ~/cchat 에 clone하고, ~/cchat/INSTALL.md 를 읽고 그대로 따라서 이 맥에 cchat을 설치해줘.
```

필요한 것(macOS, Homebrew, Claude Code)을 확인하고 `ttyd`·`tmux`를 깐 뒤, 세 가지(작업 폴더, 권한 모드, 포트)를 물어보고 설치해서 페이지까지 열어 줍니다.

<details><summary>직접 설치</summary>

```sh
brew install ttyd tmux
git clone https://github.com/efww/cchat.git ~/cchat && cd ~/cchat
cp cchat.conf.example my.conf     # WORKDIR, PERMISSION_MODE, PORT 고치기
./install.sh -c my.conf
open "http://127.0.0.1:7681/cchat/?arg=1"
```

업데이트: `git pull && ./install.sh -c my.conf`. 지우는 법과 자세한 내용: [INSTALL.md](INSTALL.md)(영어).
</details>

## 무엇이 되나

- **대화 탭**: 맨 아래 두 줄이 대화 탭. 위 줄은 번호, 아래 줄은 대화 이름표(길면 `…`로 줄임).
  - 검정 = 지금 보는 대화
  - 녹색 = 답이 끝났는데 아직 안 본 대화
  - 주황 = 허락·질문을 기다리는 대화
  - 흐린 탭 = 1시간 넘게 일 안 한 대화(바탕이 상태줄 색으로 물러나고 글자가 흐림)
  - 번호 옆 도는 기호(⠋⠙⠹…) = 작업 중(모든 탭이 같은 박자로). 답이 끝나도 백그라운드 셸·에이전트가 돌면 계속 돌고, 다 끝나면 녹색
  - 이름표 줄 끝 숫자: 작업 중이면 걸린 시간(`3m`), 끝나면 대화 크기(`42k` 토큰)
  - 끝의 **+** 는 새 대화. 탭이 넘치면 ◀ ▶에 숨은 확인할 탭 수(`▶2`)
- **PC 단축키**: Alt(Option)+숫자 = 그 번호 대화, Alt+←/→ = 이전/다음, Alt+↑/↓ = 위/아래 칸(탭 2줄 이상일 때), Alt+A = 확인할 다음 탭, Alt+L = Claude 세션 목록(탭마다 마지막 작업 뒤 지난 시간·큰 흐름·지금 하는 일·끄기, cchat 밖 claude 포함. 요약은 답이 끝날 때·지시를 받을 때 claude haiku로 미리 만들어 둠), Alt+O = 전체 모아보기(화면 미리보기). Shift+Enter = 줄바꿈(보내지 않음). Ctrl+V는 PC 클립보드를 붙인다.
- **브라우저 대신 터미널 앱**(예: 안드 Termux에서 ssh): `tmux -u -L cchat attach`로 같은 탭·대화를 본다. 색을 맞추려면 `cchat-build-index --termux dark`(또는 `light`) 출력을 `~/.termux/colors.properties`로 저장. 색 설정이 16색까지뿐인 터미널(윈도우 터미널 등)은 attach 직전에 `cchat-build-index --osc dark` 실행(`--osc reset`으로 되돌림). Termux는 화면을 탭해도 키보드가 다시 안 올라온다(cchat이 tmux 마우스 모드를 켜 두면 Termux가 탭을 프로그램에 넘김) → `~/.termux/termux.properties`의 `extra-keys`에 `KEYBOARD` 키를 넣는다.
- **폰**: 손가락 드래그 스크롤, 좌우로 밀어 탭 바꾸기, 주소(URL)를 톡 치면 열기(줄바꿈된 주소 포함), 다크 테마. 키 바: ★ = 확인할 다음 탭, Esc·Tab·화살표, ⋯ = 세션 목록(☰)·음성 입력·저장한 지시문(✎)·사진/파일 올리기(📎, 원격 중계가 있을 때).
- **한 번에 승인**: claude가 번호 선택지(허락·질문)를 띄우면 번호가 버튼으로 뜬다.
- **claude에게 시킬 수 있는 도구**: `cchat-send 1 2`(1번 마지막 답을 2번 입력칸에), `cchat-history`(닫은 대화 찾아 다시 열기), `cchat-snip`(지시문 저장), `cchat-label`(탭 이름), `cchat-set`(설정).
- 대화는 tmux 안에 있어 브라우저를 닫아도 계속 돈다. URL `?arg=이름`으로 그 이름의 대화에 붙는다(없으면 만든다).

## 사용법

1. **대화 열기**: `http://127.0.0.1:7681/cchat/?arg=1`로 접속한다. `?arg=이름`마다 따로인 claude 대화이고, 새 이름이면 탭이 새로 생긴다.
2. **일 시키고 다른 탭으로**: 할 일을 입력하고 Enter, 그다음 **Alt+숫자**(또는 클릭)로 다른 탭으로 간다. 떠난 탭은 claude가 일하는 동안 번호 옆에 스피너가 돈다.
3. **색 보기**: 그 탭이 **녹색**이 되면 답이 나온 것, **주황**이면 허락이나 대답을 기다리는 것.
4. **돌아가기**: 탭을 클릭하거나 **Alt+←/→**. 탭을 열면 색이 지워진다. 주황 탭에서 허락하면 claude가 이어서 한다.
5. **브라우저는 아무 때나 닫아도 된다**: 대화는 tmux에서 계속 돈다. 다시 열면 그대로 있다. 대화에서 `/exit`를 치면 그 탭이 닫힌다.

폰에서는 탭을 눌러 옮기고, 손가락으로 끌어 스크롤하고, 키 바로 Esc·Tab·화살표를 쓴다.

## 설정: 말로 시키면 됨

cchat 탭 아무 데서나 claude에게 "PC는 다크 테마로", "폰 글자 크게"라고 하면 됩니다. claude가 `cchat-set`을 씁니다(직접 쳐도 됨):

| 명령 | 하는 일 |
|---|---|
| `cchat-set` | 지금 설정 보기 |
| `cchat-set tab ctx off` | 탭의 대화 크기(42k) 표시 끄기 |
| `cchat-set tab rows 2` | 탭 줄 수 1~5. 1(기본)은 탭이 2줄 높이(번호/이름), 2는 두 줄 탭(번호/이름)을 2줄, 3~5는 한 줄짜리 탭을 그 줄 수에 배치(탭이 많을 때). 줄 수를 바꾸면 높이도 그 기본값으로 |
| `cchat-set tab height 1.5` | 여러 줄 모드(tab rows 2~5)의 탭 높이. 1(기본)은 글자 한 줄, 1.5는 한 줄 반(블록 문자로 칠함), 2는 기본 모드처럼 윗줄 번호·아랫줄 이름표. 상태줄은 최대 5줄이라 줄 수×높이가 넘치면 낮춘다 |
| `cchat-set font phone 16` / `font pc off` | 기기별 글자 크기(`off` = `FONT_SIZE`) |
| `cchat-set theme pc dark` | 기기별 라이트/다크(기본 PC 라이트, 폰 다크) |
| `cchat-set notify on\|off`, `notify pc\|phone\|telegram\|done\|ask on\|off`, `quiet 01-08` | 알림(알림 훅 필요, 아래) |

글자 크기·테마는 브라우저 새로고침 뒤 적용됩니다. 알림: `~/.config/cchat/notify`가 실행 파일로 있으면, 보고 있지 않은 탭이 녹색·주황이 될 때 `notify <세션> <done|ask|test>`로 부릅니다(`CCHAT_NOTIFY_DEVICES` 함께). 푸시 서버는 들어 있지 않고, 훅에서 웹 푸시·ntfy·텔레그램 등 원하는 곳으로 보내면 됩니다. 바로 쓰기: `cp examples/notify-ntfy ~/.config/cchat/notify`(안의 `TOPIC` 수정) 후 `cchat-set notify test`.

## 밖에서 접속할 때 (주의)

ttyd는 127.0.0.1에만 열리고 **자체 인증이 없다**. 밖에서 쓰려면 `TUNNEL_HOST`(SSH 역방향 통로)로 서버에 열고, 그 앞에 반드시 인증(Cloudflare Access, OAuth 프록시 등)을 둔다.
`PERMISSION_MODE=bypassPermissions`는 claude가 확인 없이 명령을 실행하므로, 접속 인증이 확실할 때만 쓴다.

## 구성

| 파일 | 역할 |
|---|---|
| `bin/cchat-session` | ttyd가 접속마다 실행. tmux 대화에 붙고, 안에서 claude를 반복 실행 |
| `bin/cchat-tabs` | 상태줄 대화 탭 그리기, 클릭·단축키 전환 |
| `bin/cchat-unread` | claude 훅(완료·허락·작업 시작)에서 탭 색 표시 |
| `bin/cchat-build-index` | ttyd 기본 화면에 cchat 부분(테마, 폰 키 바·스크롤, 단축키, 작업 중 스피너)을 넣어 `index.html` 생성 |
| `bin/cchat-set` | 설정 보기·바꾸기(`~/.config/cchat/settings`) |
| `bin/cchat-send` · `bin/cchat-history` · `bin/cchat-snip` | 탭 사이 답 넘기기 · 닫은 대화 다시 열기 · 지시문 저장 |
| `bin/cchat-ttyd` | ttyd 시작(ttyd 업그레이드 뒤 페이지 다시 만들기, `KEEP_AWAKE=1`이면 맥 잠자기 막기) |
| `bin/cchat-inbox` | (선택, `INBOX_REMOTE`) 폰에서 올린 파일 가져오기 |
| `examples/` | 알림 훅 예시(ntfy, macOS) |
| `bin/cchat-label` | 대화 이름표 직접 달기 |
| `bin/cchat-restart` | claude 다시 시작(업데이트 반영), 대화는 이어서. 작업 중인 탭은 건너뜀(`--all`이면 포함) |
| `bin/cchat-tunnel` | (선택) SSH 역방향 통로 |
| `bin/cchat-update` | (선택) 매일 claude CLI 업데이트 |
| `config/` | tmux 설정, claude 설정(테마·훅) |
| `launchd/` | 서비스 정의 |

탭 이름표는 `~/.cache/cchat-tablabel/<대화>` 파일이 있으면 그것(상태줄 스크립트 등에서 써 넣을 수 있음), 없으면 claude가 붙인 대화 제목을 쓴다.

## License

MIT
