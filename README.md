# cchat

Claude Code를 브라우저(PC·폰)에서 쓰는 웹 터미널. 맥 한 대에서 [ttyd](https://github.com/tsl0922/ttyd) + tmux로 claude 대화 여러 개를 띄워 두고, 아래 탭으로 오간다.

*Browser front-end for Claude Code on a Mac: ttyd + tmux, several claude sessions as tabs, with done / needs-approval / working indicators.*

## 무엇이 되나

- **대화 탭**: 맨 아래 두 줄이 대화 탭. 위 줄은 번호, 아래 줄은 대화 이름표(길면 `…`로 줄임).
  - 검정 = 지금 보는 대화
  - 녹색 = 답이 끝났는데 아직 안 본 대화
  - 주황 = 허락·질문을 기다리는 대화
  - 회색 깜빡임(2초) = 작업 중(여러 탭이 같은 박자로)
- **PC 단축키**: Alt(Option)+숫자 = 그 번호 대화, Alt+←/→ = 이전/다음. Ctrl+V는 PC 클립보드를 붙인다.
- **폰**: 손가락 드래그 스크롤, 키 바(Esc·Tab·화살표 등), 다크 테마.
- 대화는 tmux 안에 있어 브라우저를 닫아도 계속 돈다. URL `?arg=이름`으로 그 이름의 대화에 붙는다(없으면 만든다).

## 필요한 것

macOS, Homebrew `ttyd` `tmux`, python3, [Claude Code](https://docs.anthropic.com/claude-code) CLI(`~/.local/bin/claude`).

## 설치

```sh
cp cchat.conf.example my.conf     # 값 고치기 (작업 폴더, 포트, 권한 모드 등)
./install.sh -c my.conf
open http://127.0.0.1:7681/cchat/
```

`install.sh`는 `bin/ config/ launchd/`의 `@@이름@@` 자리에 설정 값을 넣어 `~/.local/bin`, `~/.config/cchat`, `~/Library/LaunchAgents`에 깔고 launchd 서비스를 (다시) 올린다.
설치 없이 결과만 보려면 `./install.sh -c my.conf --render-only /tmp/out`.

## 밖에서 접속할 때 (주의)

ttyd는 127.0.0.1에만 열리고 **자체 인증이 없다**. 밖에서 쓰려면 `TUNNEL_HOST`(SSH 역방향 통로)로 서버에 열고, 그 앞에 반드시 인증(Cloudflare Access, OAuth 프록시 등)을 둔다.
`PERMISSION_MODE=bypassPermissions`는 claude가 확인 없이 명령을 실행하므로, 접속 인증이 확실할 때만 쓴다.

## 구성

| 파일 | 역할 |
|---|---|
| `bin/cchat-session` | ttyd가 접속마다 실행. tmux 대화에 붙고, 안에서 claude를 반복 실행 |
| `bin/cchat-tabs` | 상태줄 대화 탭 그리기, 클릭·단축키 전환 |
| `bin/cchat-unread` | claude 훅(완료·허락·작업 시작)에서 탭 색 표시 |
| `bin/cchat-build-index` | ttyd 기본 화면에 cchat 부분(테마, 폰 키 바·스크롤, 단축키, 깜빡임)을 넣어 `index.html` 생성 |
| `bin/cchat-label` | 대화 이름표 직접 달기 |
| `bin/cchat-tunnel` | (선택) SSH 역방향 통로 |
| `bin/cchat-update` | (선택) 매일 claude CLI 업데이트 |
| `config/` | tmux 설정, claude 설정(테마·훅) |
| `launchd/` | 서비스 정의 |

탭 이름표는 `~/.cache/cchat-tablabel/<대화>` 파일이 있으면 그것(상태줄 스크립트 등에서 써 넣을 수 있음), 없으면 claude가 붙인 대화 제목을 쓴다.

## License

MIT
