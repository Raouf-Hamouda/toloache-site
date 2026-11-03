"""Generate img/doodles.svg: hand-drawn Mexican doodles as dense sketch strokes.
Each doodle = many polylines, jittered (hand wobble) and drawn twice (ink pass + light ghost pass)."""
import math, random, pathlib
random.seed(7)
OUT = pathlib.Path(__file__).resolve().parent.parent / "img" / "doodles.svg"
SW = 3.1
DETAIL = .4   # share of fine texture strokes kept; 1 = everything

def wob(pts, amp=0.9, freq=0.35, close=False):
    """resample a polyline finely and add low-frequency hand wobble"""
    if close: pts = pts + [pts[0]]
    res = []
    ph = random.random() * 10
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        d = math.hypot(x1 - x0, y1 - y0); n = max(2, int(d / 2.2))
        for i in range(n):
            t = i / n; x = x0 + (x1 - x0) * t; y = y0 + (y1 - y0) * t
            s = (x + y) * freq + ph
            res.append((x + amp * math.sin(s) * 0.6 + random.uniform(-.25, .25), y + amp * math.cos(s * 1.3) * 0.6 + random.uniform(-.25, .25)))
    res.append(pts[-1]); return res

def path(pts, amp=0.9, close=False):
    p = wob(pts, amp, close=close)
    d = "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in p)
    return d

def circle(cx, cy, r, n=48, a0=0, a1=2 * math.pi):
    return [(cx + r * math.cos(a0 + (a1 - a0) * i / n), cy + r * math.sin(a0 + (a1 - a0) * i / n)) for i in range(n + 1)]

def arc(cx, cy, rx, ry, a0, a1, n=32):
    return [(cx + rx * math.cos(a0 + (a1 - a0) * i / n), cy + ry * math.sin(a0 + (a1 - a0) * i / n)) for i in range(n + 1)]

def bez(p0, p1, p2, p3, n=24):
    out = []
    for i in range(n + 1):
        t = i / n; u = 1 - t
        out.append((u**3*p0[0]+3*u*u*t*p1[0]+3*u*t*t*p2[0]+t**3*p3[0], u**3*p0[1]+3*u*u*t*p1[1]+3*u*t*t*p2[1]+t**3*p3[1]))
    return out

def hatch(x0, y0, x1, y1, step=3.5, ang=-35, jitter=1.2):
    """diagonal hatch lines clipped to a rectangle"""
    a = math.radians(ang); dx, dy = math.cos(a), math.sin(a); lines = []
    L = math.hypot(x1 - x0, y1 - y0) * 2
    for k in range(-40, 40):
        cx = (x0 + x1) / 2 + k * step * (-dy); cy = (y0 + y1) / 2 + k * step * dx
        pts = [(cx - dx * L, cy - dy * L), (cx + dx * L, cy + dy * L)]
        seg = [(x, y) for x, y in [(pts[0][0] + (pts[1][0]-pts[0][0]) * i / 60, pts[0][1] + (pts[1][1]-pts[0][1]) * i / 60) for i in range(61)] if x0 <= x <= x1 and y0 <= y <= y1]
        if len(seg) > 3 and k % 2 == 0 and random.random() < .7:
            a_, b_ = seg[0], seg[-1]; t0, t1 = random.uniform(0, .25), random.uniform(.75, 1)
            lines.append([(a_[0] + (b_[0]-a_[0]) * t0, a_[1] + (b_[1]-a_[1]) * t0), (a_[0] + (b_[0]-a_[0]) * t1, a_[1] + (b_[1]-a_[1]) * t1)])
    return lines

def ribbon(pts, base, taper=True):
    """turn a polyline into a filled ribbon whose width breathes like pen pressure"""
    n = len(pts)
    if n < 2: return ""
    ph = random.random() * 6; L, R = [], []
    for i, (x, y) in enumerate(pts):
        x0, y0 = pts[max(i - 1, 0)]; x1, y1 = pts[min(i + 1, n - 1)]
        dx, dy = x1 - x0, y1 - y0; d = math.hypot(dx, dy) or 1; nx, ny = -dy / d, dx / d
        t = i / (n - 1)
        w = base * (0.6 + 0.4 * math.sin(t * math.pi) if taper else 1) * (0.8 + 0.3 * math.sin(i * 0.11 + ph) + 0.1 * math.sin(i * 0.37 + ph * 2))
        w = max(w, base * 0.3) / 2
        L.append((x + nx * w, y + ny * w)); R.append((x - nx * w, y - ny * w))
    poly = L + R[::-1]
    return "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in poly) + "Z"

def overshoot(pts, amt):
    (x0, y0), (x1, y1) = pts[0], pts[1]; d = math.hypot(x1 - x0, y1 - y0) or 1
    a = (x0 - (x1 - x0) / d * amt, y0 - (y1 - y0) / d * amt)
    (x2, y2), (x3, y3) = pts[-2], pts[-1]; d = math.hypot(x3 - x2, y3 - y2) or 1
    b = (x3 + (x3 - x2) / d * amt, y3 + (y3 - y2) / d * amt)
    return [a] + pts + [b]

class D:
    def __init__(s, id, vb="0 0 100 100"):
        s.id = id; s.vb = vb; s.strokes = []; s.fills = []
        s.wa, s.wb, s.wc = random.uniform(.6, 1.4), random.uniform(0, 6), random.uniform(.02, .05)   # per-drawing warp
    def line(s, pts, amp=0.9, close=False, w=None):
        if w is not None and w < 1.15 and random.random() > DETAIL: return   # fewer, bolder lines
        if w is not None: w = max(w, 1.4)
        s.strokes.append((pts, amp, close, w))
    def dot(s, x, y, r=1.4): s.fills.append((x, y, r))
    def warp(s, p):
        return [(x + s.wa * math.sin(y * s.wc + s.wb), y + s.wa * math.cos(x * s.wc * 1.3 + s.wb)) for x, y in p]
    def svg(s):
        parts = []
        for p, a, c, w in s.strokes:
            pts = wob(p, a * 1.15, close=c)
            if not c and len(p) > 1 and random.random() < .45: pts = overshoot(pts, random.uniform(.6, 2.2))
            pts = s.warp(pts)
            base = (w or SW) * random.uniform(.85, 1.15)
            op = random.choice([1, 1, 1, .92, .85])
            parts.append(f'<path d="{ribbon(pts, base)}"{f" opacity=\"{op}\"" if op < 1 else ""}/>')
        dots = "".join(f'<path d="{ribbon(s.warp(circle(x, y, r * .55, 10)), r * 1.1, False)}"/>' for x, y, r in s.fills)
        return f'<g id="{s.id}" data-vb="{s.vb}" fill="currentColor" stroke="none">{"".join(parts)}{dots}</g>'

doodles = []

# ---------- papel picado bunting (300x60) ----------
d = D("d-bunting", "0 0 300 60")
string = bez((4, 16), (90, 44), (170, 4), (296, 18), 80)
d.line(string, .5, w=1.6)
d.line([(x, y + 1.6) for x, y in string[::2]], .4, w=1.0)
def on_string(x):
    best = min(string, key=lambda p: abs(p[0] - x)); return best[1]
xs = [20, 50, 80, 110, 140, 170, 200, 230, 260, 288]
for i, x in enumerate(xs):
    y = on_string(x); w = 13 + (i % 3); h = 22 + (i % 2) * 3
    # rectangular papel picado flag with scalloped bottom
    top = [(x - w, y + 1), (x + w, y + 1)]
    right = [(x + w, y + 1), (x + w, y + h)]
    left = [(x - w, y + h), (x - w, y + 1)]
    scal = []
    for k in range(5):
        a = x - w + 2 * w * k / 5; b = x - w + 2 * w * (k + 1) / 5
        scal += arc((a + b) / 2, y + h, (b - a) / 2, 3.2, math.pi, 2 * math.pi, 8)[::-1] if k % 2 == 0 else arc((a + b) / 2, y + h, (b - a) / 2, 3.2, 0, math.pi, 8)
    d.line(top + right[1:] + scal[::-1] + left[1:], .7, close=False)
    # cut-out motif inside: alternating patterns
    m = i % 4
    cx, cy = x, y + h * 0.5
    if m == 0:   # flower: ring of petals + centre
        for k in range(6):
            a = k * math.pi / 3; px, py = cx + 5.5 * math.cos(a), cy + 5.5 * math.sin(a)
            d.line(arc(px, py, 2.6, 1.6, a + .3, a + 2 * math.pi - .3, 14), .4)
        d.line(circle(cx, cy, 2.2, 16), .3)
    elif m == 1: # diamond lattice
        for k in range(-2, 3):
            d.line([(cx + k * 4 - 6, cy - 6), (cx + k * 4 + 6, cy + 6)], .3, w=1.1)
            d.line([(cx + k * 4 + 6, cy - 6), (cx + k * 4 - 6, cy + 6)], .3, w=1.1)
    elif m == 2: # bird silhouette
        d.line([(cx - 7, cy + 2), (cx - 3, cy - 2), (cx + 1, cy - 1), (cx + 5, cy - 4), (cx + 7, cy - 2), (cx + 4, cy + 1), (cx + 1, cy + 4), (cx - 4, cy + 5), (cx - 7, cy + 2)], .5)
        d.dot(cx + 4.5, cy - 2.3, .9)
        d.line([(cx - 2, cy + 1), (cx - 5, cy + 3)], .3, w=1.1)
    else:        # heart + small dots
        d.line(bez((cx, cy + 6), (cx - 9, cy - 2), (cx - 4, cy - 8), (cx, cy - 3), 12) + bez((cx, cy - 3), (cx + 4, cy - 8), (cx + 9, cy - 2), (cx, cy + 6), 12), .4)
        for k in range(4): d.dot(cx - 7 + k * 4.6, cy + 9, .7)
    # tiny holes row near top
    for k in range(4): d.dot(x - w + 3 + k * (2 * w - 6) / 3, y + 4.2, .8)
    # knot on the string
    d.line(circle(x, y, 1.6, 10), .2, w=1.2)
doodles.append(d)

# ---------- guitar ----------
d = D("d-guitar")
body = (bez((50, 92), (30, 92), (25, 78), (26, 72), 14) + bez((26, 72), (27, 64), (35, 60), (33, 52), 14) +
        bez((33, 52), (31, 46), (27, 44), (28, 36), 14) + bez((28, 36), (29, 26), (40, 24), (50, 24), 14))
mirror = [(100 - x, y) for x, y in body[::-1]]
d.line(body + mirror, .8)
inner = [(50 + (x - 50) * .9, 58 + (y - 58) * .9) for x, y in body + mirror]
d.line(inner, .5, w=1.0)
d.line(circle(50, 64, 8, 40), .5); d.line(circle(50, 64, 9.8, 40), .4, w=1.0)
for k in range(16):  # rosette ticks
    a = k * math.pi / 8; d.line([(50 + 8.4 * math.cos(a), 64 + 8.4 * math.sin(a)), (50 + 9.6 * math.cos(a), 64 + 9.6 * math.sin(a))], .2, w=1.2)
d.line([(44, 24), (44, 6)], .5); d.line([(56, 24), (56, 6)], .5)
d.line([(42, 2), (58, 2), (59, 9), (41, 9), (42, 2)], .6)
for k, y in enumerate((4, 6.5)):
    d.line([(41, y), (36, y - 1)], .3, w=1.2); d.line([(59, y), (64, y - 1)], .3, w=1.2); d.dot(35, y - 1, 1.1); d.dot(65, y - 1, 1.1)
for k in range(5): d.line([(44.3, 11 + k * 2.6), (55.7, 11 + k * 2.6)], .2, w=1.0)  # frets
for k in range(4): d.line([(45.6 + k * 2.9, 9), (45.6 + k * 2.9, 80)], .25, w=1.3)  # strings
d.line([(42, 78), (58, 78), (58, 83), (42, 83), (42, 78)], .5)  # bridge
for k in range(4): d.dot(45.6 + k * 2.9, 80.5, .8)
d.line([(34, 44), (31, 52)], .4, w=1.2); d.line([(66, 44), (69, 52)], .4, w=1.2)
for seg in hatch(26, 70, 40, 90, 4, -40): d.line(seg, .3, w=0.8)
doodles.append(d)

# ---------- sombrero ----------
d = D("d-sombrero")
d.line(arc(50, 42, 17, 21, math.pi, 2 * math.pi, 40), .8)              # crown dome
d.line(arc(50, 44, 16, 4, 0, 2 * math.pi, 40), .5, w=1.2)              # crown base ring
d.line(arc(50, 36, 15, 3.5, 0, 2 * math.pi, 40), .4, w=1.0)             # band
for k in range(9):  # band embroidery zigzag
    x = 36 + k * 3.5; d.line([(x, 38), (x + 1.75, 34.5), (x + 3.5, 38)], .3, w=1.3)
d.line(arc(50, 60, 44, 11, 0, 2 * math.pi, 80), .8)                    # brim outer
d.line(arc(50, 60, 40, 9, 0, 2 * math.pi, 80), .5, w=1.1)              # brim inner
d.line(arc(50, 60, 36, 7, 0, 2 * math.pi, 80), .4, w=0.9)
d.line(arc(50, 62, 46, 10, 0, math.pi, 50), .6)                        # brim curl front
d.line(arc(6, 58, 5, 8, math.pi * 0.5, math.pi * 1.6, 20), .5)         # lifted edges
d.line(arc(94, 58, 5, 8, math.pi * 1.4, math.pi * 2.5, 20), .5)
for k in range(24):  # pom-pom balls under the brim
    a = k * math.pi / 12 + .13; px, py = 50 + 44 * math.cos(a), 62 + 11 * math.sin(a)
    if py > 60: d.line(circle(px, py + 3.5, 1.8, 10), .2, w=1.0); d.line([(px, py), (px, py + 1.7)], .2, w=0.9)
for k in range(10):  # brim stitching
    a = k * math.pi / 5 + .3; d.line([(50 + 37 * math.cos(a), 60 + 7.5 * math.sin(a)), (50 + 39 * math.cos(a), 60 + 8.5 * math.sin(a))], .2, w=1)
for k in range(5): d.line([(44 + k * 3, 24 + (k % 2) * 2), (45.5 + k * 3, 22 + (k % 2) * 2)], .2, w=1.0)   # crown stitches
for seg in hatch(34, 42, 66, 47, 3.5, -30): d.line(seg, .2, w=.7)
doodles.append(d)

# ---------- cactus in pot ----------
d = D("d-cactus")
trunk = [(42, 70), (42, 26)] + arc(50, 26, 8, 8, math.pi, 2 * math.pi, 16) + [(58, 26), (58, 70)]
d.line(trunk, .8)
armL = [(42, 48), (36, 48)] + arc(30, 42, 6, 6, math.pi / 2, math.pi, 10) + [(24, 42), (24, 30)] + arc(28, 30, 4, 4, math.pi, 2 * math.pi, 10) + [(32, 30), (32, 40), (36, 42), (42, 42)]
d.line(armL, .7)
armR = [(58, 40), (64, 40)] + arc(70, 34, 6, 6, math.pi / 2, 0, 10) + [(76, 34), (76, 22)] + arc(72, 22, 4, 4, 0, -math.pi, 10) + [(68, 22), (68, 32), (64, 34), (58, 34)]
d.line(armR, .7)
for x in (46, 50, 54): d.line([(x, 30 + abs(x - 50)), (x, 70)], .35, w=1.3)   # ribs
for x in (26.5, 29.5): d.line([(x, 31), (x, 41)], .3, w=.9)
for x in (70.5, 73.5): d.line([(x, 23), (x, 33)], .3, w=.9)
for k in range(10):  # spines
    y = 32 + k * 4
    for x in (44, 48, 52, 56): d.line([(x - 1.2, y + (x % 3)), (x + 1.2, y - 1 + (x % 3))], .15, w=1.0)
for k in range(3): d.line([(25 + k * 2.5, 33 + k * 3), (26.5 + k * 2.5, 32 + k * 3)], .1, w=1)
for k in range(3): d.line([(69 + k * 2.5, 25 + k * 3), (70.5 + k * 2.5, 24 + k * 3)], .1, w=1)
d.line(arc(50, 17, 3, 4, 0, 2 * math.pi, 16), .4)   # flower on top
for k in range(5):
    a = k * 2 * math.pi / 5 - math.pi / 2; d.line(arc(50 + 4.5 * math.cos(a), 17 + 4.5 * math.sin(a), 2.4, 1.8, a - 1.6, a + 1.6, 8), .3, w=1)
d.line([(32, 70), (68, 70), (68, 76), (32, 76), (32, 70)], .7)               # pot rim
d.line([(34, 76), (66, 76), (63, 94), (37, 94), (34, 76)], .7)              # pot body
for k in range(5): d.line([(38 + k * 6, 80), (38 + k * 6, 90)], .3, w=1.0)   # pot stripes
for k in range(6): d.line([(34 + k * 6, 72), (37 + k * 6, 74), (40 + k * 6, 72)], .2, w=.9)  # rim zigzag
for seg in hatch(37, 86, 63, 94, 3.5, -40): d.line(seg, .2, w=.7)
d.line([(32, 70), (68, 70)], .3, w=1.0)
doodles.append(d)

# ---------- chili ----------
d = D("d-chili")
top = bez((66, 24), (72, 30), (70, 44), (62, 56), 20) + bez((62, 56), (54, 70), (40, 82), (22, 84), 20)
bot = bez((22, 84), (16, 84), (14, 80), (18, 78), 10) + bez((18, 78), (34, 76), (48, 66), (54, 50), 20) + bez((54, 50), (58, 40), (60, 30), (66, 24), 16)
d.line(top + bot, .8)
d.line(bez((60, 34), (62, 44), (56, 58), (44, 70), 20), .5, w=1.1)   # highlight ridge
d.line(bez((64, 22), (68, 14), (76, 12), (84, 14), 14), .6)          # stem
d.line(bez((84, 14), (80, 16), (74, 18), (70, 22), 10), .5)
d.line([(62, 25), (66, 20), (72, 22), (70, 27)], .5)                 # calyx
d.line([(60, 27), (64, 30)], .3, w=1.1); d.line([(68, 27), (72, 29)], .3, w=1.1)
for seg in hatch(20, 70, 50, 86, 3.2, -35): d.line(seg, .2, w=.7)  # shade bottom
for k in range(6): d.dot(24 + k * 5, 62 - k * 2.2, .6)              # specks
doodles.append(d)

# ---------- maracas ----------
d = D("d-maracas")
def maraca(cx, cy, r, ang, L):
    a = math.radians(ang)
    d.line(circle(cx, cy, r, 40), .8)
    d.line(arc(cx, cy, r * .7, r * .7, a + .5, a + 2.6, 20), .4, w=1.0)
    for k in range(5): d.line(arc(cx, cy, r * (.3 + k * .15), r * (.3 + k * .15), a - 1, a + 1.2, 14), .3, w=.9)   # bands
    for k in range(7):  # dots pattern
        b = a + 2.2 + k * .35; d.dot(cx + r * .62 * math.cos(b), cy + r * .62 * math.sin(b), 1.0)
    hx, hy = cx + r * math.cos(a + math.pi), cy + r * math.sin(a + math.pi)
    nx, ny = -math.sin(a), math.cos(a)
    ex, ey = hx + L * math.cos(a + math.pi), hy + L * math.sin(a + math.pi)
    d.line([(hx + nx * 3.5, hy + ny * 3.5), (ex + nx * 3, ey + ny * 3), (ex - nx * 3, ey - ny * 3), (hx - nx * 3.5, hy - ny * 3.5)], .6)
    d.line(arc(ex, ey, 3, 3, a + math.pi / 2, a + 3 * math.pi / 2, 10), .4)  # handle end
    for k in range(4):  # handle rings
        t = .25 + k * .18; px, py = hx + (ex - hx) * t, hy + (ey - hy) * t
        d.line([(px + nx * 3.4, py + ny * 3.4), (px - nx * 3.4, py - ny * 3.4)], .2, w=1.0)
    d.line([(hx, hy), (hx + 6 * math.cos(a), hy + 6 * math.sin(a))], .2, w=.8)
maraca(36, 36, 17, -60, 34)
maraca(70, 32, 14, -110, 30)
for k in range(3): d.line([(14 + k * 3, 14 - k * 4), (16 + k * 3, 11 - k * 4)], .2, w=1)   # motion marks
for k in range(3): d.line([(90 + k * 2, 20 + k * 5), (93 + k * 2, 21 + k * 5)], .2, w=1)
doodles.append(d)

# ---------- piñata ----------
d = D("d-pinata")
body = arc(55, 52, 30, 15, 0, 2 * math.pi, 60); d.line(body, .8)
for row in range(4):   # fringe rows
    y = 44 + row * 6
    pts = []; x = 27
    while x < 83:
        pts += [(x, y), (x + 2, y + 3.2), (x + 4, y)]; x += 4
    d.line(pts, .35, w=1.3)
d.line(bez((30, 46), (24, 38), (24, 28), (30, 22), 16), .7)      # neck
d.line(bez((42, 40), (40, 34), (38, 30), (36, 24), 12), .6)
head = arc(26, 22, 10, 8, 0, 2 * math.pi, 36); d.line(head, .8)
d.line([(19, 16), (16, 6), (23, 13)], .6); d.line([(31, 15), (34, 5), (26, 13)], .6)   # ears
d.dot(21, 20, 1.5); d.line(arc(21, 20, 2.6, 2.6, 0, 2 * math.pi, 12), .2, w=.9)   # eye
d.line([(16, 25), (18, 27), (21, 27)], .3, w=1.0)                 # mouth
d.line(bez((17, 23), (12, 24), (10, 27), (13, 29), 8), .4)        # muzzle
for k in range(4): d.line([(23 + k * 2.5, 14 - k * 1.2), (24.5 + k * 2.5, 11 - k * 1.2)], .2, w=1)   # mane
for lx in (36, 48, 64, 76):   # legs with fringe
    d.line([(lx - 3, 66), (lx - 3, 88), (lx + 3, 88), (lx + 3, 66)], .6)
    for k in range(3): d.line([(lx - 3, 72 + k * 5), (lx, 74 + k * 5), (lx + 3, 72 + k * 5)], .25, w=1.3)
    d.line([(lx - 5, 88), (lx + 5, 88)], .3)
d.line(bez((85, 50), (92, 44), (96, 50), (92, 58), 12), .6)       # tail
for k in range(4): d.line([(92 + k, 52 + k * 2), (96 + k, 50 + k * 2)], .2, w=.9)
for k in range(6): d.line([(40 + k * 7, 38 + (k % 2)), (43 + k * 7, 36)], .2, w=.9)   # top fringe tufts
d.line([(55, 37), (55, 30)], .3, w=1.0); d.line([(53, 30), (57, 30)], .2, w=1.0)       # hanging string
doodles.append(d)

# ---------- lime ----------
d = D("d-lime")
d.line(circle(50, 50, 36, 80), .8); d.line(circle(50, 50, 33, 80), .4, w=1.0); d.line(circle(50, 50, 29, 80), .5, w=1.2)
for k in range(8):
    a = k * math.pi / 4
    d.line([(50 + 3 * math.cos(a), 50 + 3 * math.sin(a)), (50 + 28 * math.cos(a), 50 + 28 * math.sin(a))], .3, w=1.0)
    seg = arc(50, 50, 24, 24, a + .18, a + math.pi / 4 - .18, 12)
    d.line([(50 + 5 * math.cos(a + .2), 50 + 5 * math.sin(a + .2))] + seg + [(50 + 5 * math.cos(a + math.pi / 4 - .2), 50 + 5 * math.sin(a + math.pi / 4 - .2))], .4, w=1.0)
    for j in range(4):  # pulp texture
        r = 9 + j * 4; b = a + .1 + random.uniform(.05, .5)
        d.line([(50 + r * math.cos(b), 50 + r * math.sin(b)), (50 + (r + 2.5) * math.cos(b + .05), 50 + (r + 2.5) * math.sin(b + .05))], .1, w=.8)
for k in range(28):  # rind dimples
    a = k * 2 * math.pi / 28; d.dot(50 + 34.6 * math.cos(a), 50 + 34.6 * math.sin(a), .55)
d.line(circle(50, 50, 2.5, 12), .2)
doodles.append(d)

# ---------- taco ----------
d = D("d-taco")
shell = bez((10, 64), (10, 36), (28, 22), (50, 22), 24) + bez((50, 22), (72, 22), (90, 36), (90, 64), 24)
d.line(shell + [(90, 64), (10, 64)], .8)
d.line(bez((16, 60), (18, 44), (32, 32), (50, 32), 20) + bez((50, 32), (68, 32), (82, 44), (84, 60), 20), .4, w=1.0)   # shell inner edge
fill = bez((12, 60), (22, 52), (30, 58), (40, 52), 16) + bez((40, 52), (50, 46), (58, 56), (68, 50), 16) + bez((68, 50), (78, 46), (84, 54), (88, 58), 12)
d.line(fill, .6)
for k in range(7):  # lettuce frills
    x = 16 + k * 11; d.line(bez((x, 56), (x + 2, 50), (x + 5, 52), (x + 7, 47), 8) + bez((x + 7, 47), (x + 9, 50), (x + 11, 50), (x + 12, 56), 8), .4, w=1.0)
for k in range(5):  # meat chunks
    x = 24 + k * 12; d.line([(x, 58), (x + 4, 55), (x + 8, 58), (x + 5, 61), (x, 58)], .4, w=1.0)
    for seg in hatch(x, 55, x + 8, 61, 2.2, -40): d.line(seg, .1, w=.6)
for k in range(4): d.line(circle(30 + k * 14, 50, 2.2, 10), .3, w=.9)   # onion rings
for k in range(6): d.dot(22 + k * 11, 54 - (k % 2) * 3, .7)             # cilantro specks
for k in range(14): d.line([(14 + k * 5.5, 66), (14 + k * 5.5, 70)], .2, w=.9)   # shell texture bottom
for seg in hatch(10, 46, 30, 64, 3.6, -35): d.line(seg, .2, w=.7)
for seg in hatch(70, 46, 90, 64, 3.6, 35): d.line(seg, .2, w=.7)
d.line([(50, 22), (52, 16), (50, 12)], .3, w=1); d.line([(44, 24), (42, 18)], .3, w=1); d.line([(56, 24), (58, 18)], .3, w=1)   # steam
doodles.append(d)

# ---------- music note ----------
d = D("d-note")
d.line([(38, 72), (38, 24), (72, 14), (72, 60)], .7)
d.line([(38, 32), (72, 22)], .4, w=1.0); d.line([(38, 36), (72, 26)], .3, w=.9)
d.line(arc(31, 74, 9, 6.5, 0, 2 * math.pi, 30), .6); d.line(arc(65, 62, 9, 6.5, 0, 2 * math.pi, 30), .6)
for seg in hatch(22, 68, 40, 80, 2.6, -40): d.line(seg, .2, w=.8)
for seg in hatch(56, 56, 74, 68, 2.6, -40): d.line(seg, .2, w=.8)
doodles.append(d)

# ---------- star ----------
d = D("d-star")
pts = [(50 + (34 if k % 2 == 0 else 15) * math.cos(-math.pi / 2 + k * math.pi / 5), 52 + (34 if k % 2 == 0 else 15) * math.sin(-math.pi / 2 + k * math.pi / 5)) for k in range(10)]
d.line(pts, .8, close=True)
inner = [(50 + (x - 50) * .62, 52 + (y - 52) * .62) for x, y in pts]; d.line(inner, .4, close=True, w=1.0)
for k in range(5):
    a = -math.pi / 2 + k * 2 * math.pi / 5; d.line([(50, 52), (50 + 15 * math.cos(a + math.pi / 5), 52 + 15 * math.sin(a + math.pi / 5))], .2, w=.9)
d.dot(50, 52, 1.6)
for k in range(5):
    a = -math.pi / 2 + k * 2 * math.pi / 5; d.dot(50 + 40 * math.cos(a), 52 + 40 * math.sin(a), 1.0)
doodles.append(d)

# ---------- sparkle ----------
d = D("d-sparkle")
d.line(bez((50, 8), (52, 40), (60, 48), (92, 50), 16) + bez((92, 50), (60, 52), (52, 60), (50, 92), 16) + bez((50, 92), (48, 60), (40, 52), (8, 50), 16) + bez((8, 50), (40, 48), (48, 40), (50, 8), 16), .6)
d.line([(50, 36), (50, 64)], .2, w=1.0); d.line([(36, 50), (64, 50)], .2, w=1.0)
for k in range(4):
    a = math.pi / 4 + k * math.pi / 2; d.dot(50 + 24 * math.cos(a), 50 + 24 * math.sin(a), 1.2)
doodles.append(d)

# ---------- heart ----------
d = D("d-heart")
h = bez((50, 84), (20, 62), (10, 46), (14, 32), 20) + bez((14, 32), (18, 16), (40, 14), (50, 30), 20) + bez((50, 30), (60, 14), (82, 16), (86, 32), 20) + bez((86, 32), (90, 46), (80, 62), (50, 84), 20)
d.line(h, .8)
d.line([(50 + (x - 50) * .82, 48 + (y - 48) * .82) for x, y in h], .4, w=1.0)
d.line(bez((22, 34), (24, 26), (30, 22), (36, 22), 10), .3, w=1.2)   # highlight
for seg in hatch(44, 60, 76, 84, 3.4, -40): d.line(seg, .2, w=.7)
for k in range(5): d.dot(30 + k * 10, 92, .7)
doodles.append(d)

# ---------- agave ----------
d = D("d-agave")
for k in range(7):
    a = -math.pi / 2 + (k - 3) * .36; L = 46 - abs(k - 3) * 6; wdt = 5 - abs(k - 3) * .6
    tip = (50 + L * math.cos(a), 88 + L * math.sin(a))
    nx, ny = -math.sin(a), math.cos(a)
    left = bez((50 + nx * 2, 88 + ny * 2), (50 + nx * wdt + L * .4 * math.cos(a), 88 + ny * wdt + L * .4 * math.sin(a)), (tip[0] + nx * 1.5, tip[1] + ny * 1.5), tip, 14)
    right = bez(tip, (tip[0] - nx * 1.5, tip[1] - ny * 1.5), (50 - nx * wdt + L * .4 * math.cos(a), 88 - ny * wdt + L * .4 * math.sin(a)), (50 - nx * 2, 88 - ny * 2), 14)
    d.line(left + right[1:], .5)
    d.line(bez((50, 86), (50 + L * .3 * math.cos(a), 88 + L * .3 * math.sin(a)), (50 + L * .7 * math.cos(a), 88 + L * .7 * math.sin(a)), tip, 10), .25, w=.8)
    for j in range(4):
        t = .35 + j * .16; p = left[int(t * 14)]; d.line([(p[0], p[1]), (p[0] + nx * 1.6, p[1] + ny * 1.6)], .1, w=.8)
d.line(arc(50, 90, 24, 4, math.pi, 2 * math.pi, 24), .5)
for k in range(7): d.dot(28 + k * 7.5, 94 + (k % 2) * .8, .6)
doodles.append(d)

# ---------- sun ----------
d = D("d-sun")
d.line(circle(50, 50, 20, 60), .8); d.line(circle(50, 50, 16, 50), .4, w=1.0)
for k in range(16):
    a = k * math.pi / 8; r0, r1 = 24, (36 if k % 2 == 0 else 30)
    d.line([(50 + r0 * math.cos(a), 50 + r0 * math.sin(a)), (50 + r1 * math.cos(a), 50 + r1 * math.sin(a))], .4, w=1.3 if k % 2 == 0 else 1.0)
# face
d.line(arc(42, 46, 3, 2, 0, math.pi, 10), .3, w=1.2); d.line(arc(58, 46, 3, 2, 0, math.pi, 10), .3, w=1.2)
d.line(arc(50, 54, 7, 4, .2, math.pi - .2, 14), .3, w=1.2)
d.line([(50, 47), (49, 52), (51, 52)], .2, w=1.0)
for k in range(6): d.dot(44 + k * 2.4, 40, .5)
for seg in hatch(36, 56, 64, 70, 3, -35): d.line([p for p in seg if math.hypot(p[0]-50, p[1]-50) < 19.5] or seg[:1] * 2, .2, w=.7)
doodles.append(d)

# ---------- skull (calavera) ----------
d = D("d-skull")
d.line(arc(50, 42, 30, 32, math.pi, 2 * math.pi, 50) + [(80, 42), (80, 56), (72, 66), (70, 80), (30, 80), (28, 66), (20, 56), (20, 42)], .8)
for cx in (38, 62):
    d.line(circle(cx, 44, 9, 30), .6)
    for k in range(8):  # petal eyes
        a = k * math.pi / 4; d.line(arc(cx + 11.5 * math.cos(a), 44 + 11.5 * math.sin(a), 3, 2, a - 1.5, a + 1.5, 8), .3, w=1.3)
    d.line(circle(cx, 44, 4, 16), .3, w=1.0)
d.line([(50, 54), (46, 61), (54, 61), (50, 54)], .5)
d.line([(32, 70), (68, 70)], .4, w=1.0)
for x in range(35, 68, 5): d.line([(x, 70), (x, 80)], .3, w=1.0)
for k in range(5): d.line(arc(30 + k * 10, 28, 3, 3, math.pi, 2 * math.pi, 10), .3, w=1)   # forehead scallops
for k in range(3): d.line(circle(50, 20 - k * 0, 2 + k * 2.5, 16), .2, w=.9)              # forehead flower
for k in range(6): d.dot(26 + k * 9.6, 62, .9)
doodles.append(d)

# ---------- flag / banner tile ----------
d = D("d-flag")
d.line([(14, 12), (86, 12), (86, 62), (50, 88), (14, 62), (14, 12)], .8)
d.line([(18, 16), (82, 16), (82, 60), (50, 83), (18, 60), (18, 16)], .4, w=1.0)
d.line(circle(50, 46, 12, 36), .6)
for k in range(8):
    a = k * math.pi / 4; d.line(arc(50 + 15 * math.cos(a), 46 + 15 * math.sin(a), 4, 2.6, a - 1.5, a + 1.5, 8), .3, w=.9)
for k in range(10): d.line([(20 + k * 6.5, 20), (23 + k * 6.5, 24), (26 + k * 6.5, 20)], .2, w=.9)
for k in range(6): d.dot(24 + k * 10.5, 70 - abs(k - 2.5) * 2, .8)
doodles.append(d)

# ---------- squiggle + dots (dividers) ----------
d = D("d-squiggle")
w = []
for i in range(81):
    x = 8 + i * 1.05; w.append((x, 50 + 10 * math.sin(i / 5.0)))
d.line(w, .6)
doodles.append(d)
d = D("d-dots")
for k in range(3): d.dot(20 + k * 30, 50, 3.2); d.line(circle(20 + k * 30, 50, 5.5, 16), .3, w=1.0)
doodles.append(d)

# ---------- hat (small) alias to sombrero look ----------
d = D("d-hat")
d.line(arc(50, 40, 16, 18, math.pi, 2 * math.pi, 30), .8); d.line(arc(50, 42, 15, 4, 0, 2 * math.pi, 30), .4, w=1)
d.line(arc(50, 58, 42, 9, 0, 2 * math.pi, 60), .8); d.line(arc(50, 58, 38, 7, 0, 2 * math.pi, 60), .4, w=1)
for k in range(7): d.line([(38 + k * 4, 36), (40 + k * 4, 33), (42 + k * 4, 36)], .3, w=1)
doodles.append(d)

svg = '<svg xmlns="http://www.w3.org/2000/svg" style="display:none"><defs>' + "".join(x.svg() for x in doodles) + "</defs></svg>"
OUT.write_text(svg, encoding="utf-8")
print(OUT, len(svg), "bytes,", len(doodles), "doodles,", sum(len(x.strokes) for x in doodles), "strokes")
