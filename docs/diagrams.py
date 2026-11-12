#!/usr/bin/env python3
"""README 구조 그림(docs/arch-*.svg)을 만든다. 고치면: python3 docs/diagrams.py
한 벌의 모양(노드·선·색)으로 기기별 세 장(PC 브라우저, 폰 브라우저, 폰 Termux) × 언어 둘(en, ko).
SVG 안에 라이트/다크 색을 함께 넣고(prefers-color-scheme), 흐름 선에는 점이 따라 흐른다(animateMotion)."""
from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path(__file__).resolve().parent
W = 960

STYLE = """
.bg{fill:#ffffff;stroke:#d0d7de}
.mac{fill:#f6f8fa;stroke:#d0d7de;stroke-dasharray:5 5}
.macl{fill:#59636e;font-size:12px;font-weight:600;letter-spacing:.08em}
.n{fill:#ffffff;stroke:#d0d7de}
.nd{fill:#ffffff;stroke:#0969da;stroke-width:1.5}
.t{fill:#1f2328;font-size:15px;font-weight:650}
.s{fill:#59636e;font-size:12px}
.e{fill:none;stroke:#8c959f;stroke-width:1.5}
.ea{fill:none;stroke:#0969da;stroke-width:1.75}
.eg{fill:none;stroke:#1a7f37;stroke-width:1.5;stroke-dasharray:4 4}
.eo{fill:none;stroke:#bc4c00;stroke-width:1.5;stroke-dasharray:4 4}
.el{fill:#59636e;font-size:11.5px}
.ah{fill:#8c959f}.aha{fill:#0969da}.ahg{fill:#1a7f37}.aho{fill:#bc4c00}
.dot{fill:#0969da}.dotg{fill:#1a7f37}.doto{fill:#bc4c00}
.k{fill:#f6f8fa;stroke:#d0d7de}.kt{fill:#1f2328;font-size:11px;font-weight:600}
.tb0{fill:#24292f}.tb1{fill:#d3f0dc}.tb2{fill:#fde4c4}.tb3{fill:#eceef1}
.title{fill:#1f2328;font-size:17px;font-weight:700}.sub{fill:#59636e;font-size:12.5px}
@media (prefers-color-scheme: dark){
.bg{fill:#0d1117;stroke:#30363d}
.mac{fill:#151b23;stroke:#3d444d}.macl{fill:#9198a1}
.n{fill:#161b22;stroke:#3d444d}.nd{fill:#161b22;stroke:#4493f8}
.t{fill:#e6edf3}.s,.el,.sub{fill:#9198a1}.title{fill:#e6edf3}
.e{stroke:#656c76}.ea{stroke:#4493f8}.eg{stroke:#3fb950}.eo{stroke:#db6d28}
.ah{fill:#656c76}.aha{fill:#4493f8}.ahg{fill:#3fb950}.aho{fill:#db6d28}
.dot{fill:#4493f8}.dotg{fill:#3fb950}.doto{fill:#db6d28}
.k{fill:#21262d;stroke:#3d444d}.kt{fill:#e6edf3}
.tb0{fill:#e6edf3}.tb1{fill:#173b26}.tb2{fill:#45300f}.tb3{fill:#272e37}
}
text{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","Apple SD Gothic Neo","Noto Sans KR",Helvetica,Arial,sans-serif}
"""


class D:
    def __init__(self, h, title, sub):
        self.h, self.parts, self.n = h, [], 0
        self.parts.append(f'<rect class="bg" x=".5" y=".5" width="{W-1}" height="{h-1}" rx="16"/>')
        self.parts.append(f'<text class="title" x="28" y="38">{escape(title)}</text>')
        self.parts.append(f'<text class="sub" x="28" y="58">{escape(sub)}</text>')

    def mac(self, x, y, w, h, label, right=False):
        self.parts.append(f'<rect class="mac" x="{x}" y="{y}" width="{w}" height="{h}" rx="18"/>')
        if right:
            self.parts.append(f'<text class="macl" x="{x+w-18}" y="{y+22}" text-anchor="end">{escape(label)}</text>')
        else:
            self.parts.append(f'<text class="macl" x="{x+18}" y="{y+22}">{escape(label)}</text>')

    def node(self, x, y, w, h, title, sub="", device=False, extra=""):
        self.parts.append(f'<rect class="{"nd" if device else "n"}" x="{x}" y="{y}" width="{w}" height="{h}" rx="12"/>')
        self.parts.append(f'<text class="t" x="{x+16}" y="{y+28}">{escape(title)}</text>')
        for i, line in enumerate(sub.split("\n") if sub else []):
            self.parts.append(f'<text class="s" x="{x+16}" y="{y+48+i*17}">{escape(line)}</text>')
        if extra:
            self.parts.append(extra)

    def tabs(self, x, y):
        """cchat 탭 바 축소판: 지금(진함)·끝남(녹색)·내 차례(주황)·보통."""
        out = []
        for i, c in enumerate(("tb0", "tb1", "tb2", "tb3", "tb3")):
            out.append(f'<rect class="{c}" x="{x+i*22}" y="{y}" width="19" height="10" rx="3"/>')
        return "".join(out)

    def keys(self, x, y, labels, kw=30):
        out = []
        for i, l in enumerate(labels):
            out.append(f'<rect class="k" x="{x+i*(kw+4)}" y="{y}" width="{kw}" height="22" rx="5"/>'
                       f'<text class="kt" x="{x+i*(kw+4)+kw/2}" y="{y+15}" text-anchor="middle">{escape(l)}</text>')
        return "".join(out)

    def edge(self, pts, label="", kind="", lx=None, ly=None, dur=2.6, anchor="middle", flow=True):
        cls = {"": "e", "a": "ea", "g": "eg", "o": "eo"}[kind]
        d = "M" + " L".join(f"{x},{y}" for x, y in pts)
        self.n += 1
        pid = f"p{self.n}"
        self.parts.append(f'<path id="{pid}" class="{cls}" d="{d}"/>')
        (x1, y1), (x2, y2) = pts[-2], pts[-1]
        ah = {"": "ah", "a": "aha", "g": "ahg", "o": "aho"}[kind]
        if x2 != x1:
            s = 1 if x2 > x1 else -1
            tri = f"{x2},{y2} {x2-8*s},{y2-4.5} {x2-8*s},{y2+4.5}"
        else:
            s = 1 if y2 > y1 else -1
            tri = f"{x2},{y2} {x2-4.5},{y2-8*s} {x2+4.5},{y2-8*s}"
        self.parts.append(f'<polygon class="{ah}" points="{tri}"/>')
        if flow:
            dot = {"": "dot", "a": "dot", "g": "dotg", "o": "doto"}[kind]
            self.parts.append(f'<circle class="{dot}" r="3.2"><animateMotion dur="{dur}s" repeatCount="indefinite">'
                              f'<mpath href="#{pid}"/></animateMotion></circle>')
        if label:
            if lx is None:
                lx, ly = (pts[0][0] + pts[-1][0]) / 2, min(p[1] for p in pts) - 8
            self.parts.append(f'<text class="el" x="{lx}" y="{ly}" text-anchor="{anchor}">{escape(label)}</text>')

    def svg(self, desc):
        return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {self.h}" width="{W}" height="{self.h}" role="img">'
                f'<title>{escape(desc)}</title><style>{STYLE}</style>' + "".join(self.parts) + "</svg>\n")


T = {
    "en": dict(
        mac="YOUR MAC", kb="KB",
        pc=("Desktop browser", "Tabs at the bottom, Alt shortcuts. Close the browser any time: sessions keep running in tmux."),
        pcdev=("PC browser", "click a tab · Alt+number\nAlt+L session list"),
        ttyd=("ttyd", "web terminal\n127.0.0.1 only"),
        tmux=("tmux", "one session per tab"),
        claude=("claude × N", "your files, tools,\nsettings"),
        unread=("cchat-unread", "claude hooks → tab color"),
        notify=("Notify hook", "ntfy · web push · …\n(you choose)"),
        local="same Mac: localhost",
        away="away: auth + tunnel",
        hook="hooks", color="color", push="not watching → notify",
        ph=("Phone browser", "Same sessions as the PC, with a key bar, swipe between tabs and tap-to-open links."),
        phdev=("Phone browser", "swipe tabs · tap links\nchoices → buttons"),
        auth=("Auth + server", "e.g. Cloudflare\nAccess"),
        tunnel="SSH reverse tunnel", https="https",
        tx=("Phone terminal (Termux)", "No web in between: ssh straight into tmux. 🎤 records on the phone, the Mac turns it into text."),
        txdev=("Termux", "ssh · same tabs"),
        wrap=("cchat-termux", "catches 🎤 and ⏎"),
        rec=("Record", "Termux:API, no window"),
        stt=("cchat-stt", "whisper.cpp · ~1.5 s\nmemory only while used"),
        ssh="ssh (private network)", attach="tmux attach", audio="audio", text="text → input box",
        enter="🎤 again = text only · ⏎ = send",
    ),
    "ko": dict(
        mac="내 맥", kb="키보드",
        pc=("PC 브라우저", "아래 탭과 Alt 단축키. 브라우저를 닫아도 대화는 tmux에서 계속 돈다."),
        pcdev=("PC 브라우저", "탭 클릭 · Alt+숫자\nAlt+L 세션 목록"),
        ttyd=("ttyd", "웹 터미널\n127.0.0.1에만"),
        tmux=("tmux", "대화 하나 = 탭 하나"),
        claude=("claude × N", "내 파일·도구·설정\n그대로"),
        unread=("cchat-unread", "claude 훅 → 탭 색"),
        notify=("알림 훅", "ntfy · 웹 푸시 · …\n(직접 고름)"),
        local="같은 맥: localhost",
        away="밖에서: 인증 + 통로",
        hook="훅", color="색", push="안 보고 있으면 알림",
        ph=("폰 브라우저", "PC와 같은 대화. 키 바, 좌우로 밀어 탭 이동, 링크 톡 열기."),
        phdev=("폰 브라우저", "밀어서 탭 이동 · 링크 톡\n번호 선택지 → 버튼"),
        auth=("인증 + 서버", "예: Cloudflare\nAccess"),
        tunnel="SSH 역방향 통로", https="https",
        tx=("폰 터미널 (Termux)", "웹을 거치지 않고 ssh로 tmux에 바로. 🎤는 폰이 녹음하고 맥이 글로 바꾼다."),
        txdev=("Termux", "ssh · 같은 탭"),
        wrap=("cchat-termux", "🎤와 ⏎를 가로챔"),
        rec=("녹음", "Termux:API, 창 없음"),
        stt=("cchat-stt", "whisper.cpp · 약 1.5초\n쓸 때만 메모리"),
        ssh="ssh (사설망)", attach="tmux attach", audio="녹음 파일", text="글 → 입력칸",
        enter="🎤 다시 = 글만 · ⏎ = 바로 보냄",
    ),
}


def mac_core(d, t, x0, y, w=(150, 196, 168), gap=36):
    """맥 안: ttyd → tmux → claude, 아래 cchat-unread. 돌려줌: (unread 가운데 x, unread 아래 y)."""
    a, b, c = w
    xt, xc = x0 + a + gap, x0 + a + gap + b + gap
    d.node(x0, y, a, 92, *t["ttyd"])
    d.node(xt, y, b, 92, *t["tmux"], extra=d.tabs(xt + 16, y + 62))
    d.node(xc, y, c, 92, *t["claude"])
    d.edge([(x0 + a, y + 46), (xt, y + 46)], flow=False)
    d.edge([(xt + b, y + 46), (xc, y + 46)], flow=False)
    d.node(xt, y + 126, b, 64, *t["unread"])
    d.edge([(xc + c / 2, y + 92), (xc + c / 2, y + 158), (xt + b, y + 158)], t["hook"], "g", xc + c / 2 + 8, y + 122, anchor="start")
    d.edge([(xt + b / 2, y + 126), (xt + b / 2, y + 92)], t["color"], "g", xt + b / 2 + 8, y + 113, dur=1.6, anchor="start")
    return xt + b / 2, y + 190


def pc(t):
    d = D(372, *t["pc"])
    d.mac(312, 76, 624, 272, t["mac"])
    y = 116
    d.node(24, y, 186, 92, *t["pcdev"], device=True)
    ux, uy = mac_core(d, t, 336, y)
    d.edge([(210, y + 34), (336, y + 34)], t["local"], "a", 273, y + 26)
    d.edge([(336, y + 62), (210, y + 62)], flow=False)
    d.parts.append(f'<text class="el" x="273" y="{y + 80}" text-anchor="middle">{escape(t["away"])}</text>')
    d.node(24, 246, 186, 74, *t["notify"])
    d.edge([(ux, uy), (ux, 336), (117, 336), (117, 320)], t["push"], "o", 330, 330, dur=3.2)
    return d.svg(t["pc"][0])


def phone(t):
    d = D(392, *t["ph"])
    d.mac(392, 76, 544, 292, t["mac"])
    y = 116
    keys = d.keys(40, y + 86, ["★", "Esc", "⇥", "↑", "⋯"], 28)
    d.node(24, y, 184, 124, *t["phdev"], device=True, extra=keys)
    d.node(236, y + 8, 132, 76, *t["auth"])
    d.edge([(208, y + 46), (236, y + 46)], flow=False)
    ux, uy = mac_core(d, t, 412, y, (128, 176, 148), 28)
    d.edge([(368, y + 46), (412, y + 46)], "", "a")
    d.parts.append(f'<text class="el" x="302" y="{y + 104}" text-anchor="middle">{escape(t["tunnel"])}</text>')
    d.node(24, 270, 184, 74, *t["notify"])
    d.edge([(ux, uy), (ux, 358), (116, 358), (116, 344)], t["push"], "o", 330, 352, dur=3.2)
    return d.svg(t["ph"][0])


def termux(t):
    d = D(404, *t["tx"])
    d.mac(452, 76, 484, 300, t["mac"], right=True)
    y = 116
    keys = d.keys(38, y + 64, ["🎤", t["kb"], "ALT", "↑", "⇧⏎"], 26) + d.keys(38, y + 90, ["⏎", "TAB", "←", "↓", "→"], 26)
    d.node(24, y, 186, 124, *t["txdev"], device=True, extra=keys)
    d.node(240, y, 180, 64, *t["wrap"])
    d.edge([(210, y + 32), (240, y + 32)], flow=False)
    d.node(476, y, 196, 92, *t["tmux"], extra=d.tabs(492, y + 62))
    d.node(712, y, 200, 92, *t["claude"])
    d.edge([(672, y + 46), (712, y + 46)], flow=False)
    d.edge([(420, y + 24), (476, y + 24)], "", "a")
    d.parts.append(f'<text class="el" x="470" y="{y - 12}" text-anchor="start">{escape(t["ssh"])}</text>')
    d.node(240, 264, 180, 64, *t["rec"])
    d.edge([(300, y + 64), (300, 264)], "🎤", "o", 308, 226, anchor="start", dur=1.8)
    d.node(476, 264, 196, 92, *t["stt"])
    d.edge([(420, 296), (476, 296)], t["audio"], "o", 448, 288, dur=1.8)
    d.edge([(574, 264), (574, 236), (380, 236), (380, y + 64)], t["text"], "a", 480, 230, dur=2.2)
    d.parts.append(f'<text class="el" x="24" y="388">{escape(t["enter"])}</text>')
    return d.svg(t["tx"][0])


if __name__ == "__main__":
    for lang, t in T.items():
        for name, fn in (("pc", pc), ("phone", phone), ("termux", termux)):
            p = OUT / f"arch-{name}{'' if lang == 'en' else '.' + lang}.svg"
            p.write_text(fn(t), encoding="utf-8")
            print("wrote", p.name)
