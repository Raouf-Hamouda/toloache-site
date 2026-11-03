#!/usr/bin/env python3
"""gen.py -> index.html carte.html actualites.html avis.html commander.html. Source: this file + data/menu.json."""
import json, html, pathlib, time
H = pathlib.Path(__file__).parent
menu = json.loads((H/"data/menu.json").read_text())
STAMP = time.strftime("%Y%m%d%H%M"); esc = html.escape
TEL = "+33 7 84 60 09 11"; TEL_HREF = "tel:+33784600911"; ADDR = "49 rue de Clignancourt, 75018 Paris"
MAP = "https://maps.google.com/maps?q=Restaurant%20Toloache%2049%20rue%20de%20Clignancourt&t=&z=16&ie=UTF8&iwloc=&output=embed"
HOURS = [("Lundi","Fermé"),("Mardi","12h-15h et 19h-23h"),("Mercredi","12h-15h et 19h-23h"),("Jeudi","12h-15h et 19h-23h"),("Vendredi","12h-15h et 19h-2h"),("Samedi","12h-15h et 19h-2h"),("Dimanche","Fermé")]
ORDER = [("Deliveroo","https://deliveroo.fr/fr/menu/paris/18eme-montmartre/toloache-75018","deliveroo"),("Uber Eats","https://www.ubereats.com/fr/paris/food-delivery/toloache/StUMa6sYQpORNPihbeYHlQ","ubereats"),("Just Eat","https://www.just-eat.fr/","justeat")]
SUPPLIERS = [("La Esquinita","logo_esquinita"),("Mezcal Toloache","logo_mezcal"),("Bleu Agave","logo_bleuagave"),("Pepe Comala","logo_pepecomala")]
PAGES = [("index.html","Accueil","accueil"),("carte.html","La carte","carte"),("actualites.html","Actualités","actualites"),("avis.html","Avis","reviews")]
MAIL = "contact@toloache.fr"  # à confirmer, pas trouvé sur le site d'origine
FB = "https://facebook.com/toloacheparis/"; IG = "https://www.instagram.com/toloacheparis/"

INTRO = '<div class="intro" id="intro" aria-hidden="true"><img src="img/logo.svg" alt="" width="586" height="628"></div>'
def shell(file, title, desc, body, cls=""):
    links = "".join(f'<a href="{f}"{" aria-current=page" if f==file else ""}><img src="img/nav_{i}.png" alt="{n}"></a>' for f,n,i in PAGES)
    return f'''<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(desc)}"><meta property="og:image" content="https://toloacheparis.com/img/plat5.webp">
<link rel="icon" href="img/favicon.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Arvo:ital,wght@0,400;0,700;1,400&family=Roboto+Slab:wght@300;400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="style.css?v={STAMP}">
</head>
<body class="{cls}">
{DOODLES}
{INTRO if cls=="home" else ""}<header class="nav" id="top">
  <a class="brand" href="index.html" aria-label="Toloache, accueil"><img src="img/logo_cream.png" alt="" width="40" height="47"><span>Toloache</span></a>
  <nav class="links" aria-label="Pages">{links}</nav>
  <div class="cta"><a class="btn ghost" href="{TEL_HREF}"><img src="img/nav_telephone.png" alt="Réserver par téléphone"></a><a class="btn" href="commander.html"><img src="img/nav_commander.png" alt="Commander"></a></div>
</header>
{body}
<footer class="foot">
  {dd("bunting","flow fb")}
  <div class="wrap">
    <div class="footgrid">
      <div class="fcol brandcol">
        <img src="img/logo_cream.png" alt="Toloache" width="84" height="90">
        <p class="ftag">Fusion franco-mexicaine,<br>sur les flancs de la butte Montmartre.</p>
      </div>
      <div class="fcol">
        <p class="eyebrow">Horaires</p>
        <dl class="fhours">
          <dt>Mar à jeu</dt><dd>12h-15h et 19h-23h</dd>
          <dt>Ven et sam</dt><dd>12h-15h et 19h-2h</dd>
          <dt>Dim et lun</dt><dd class="muted">fermé</dd>
        </dl>
      </div>
      <div class="fcol">
        <p class="eyebrow">Contact</p>
        <p class="faddr">49 rue de Clignancourt<br>75018 Paris</p>
        <p><a href="{TEL_HREF}">{TEL}</a></p>
        <p><a href="mailto:{MAIL}">{MAIL}</a></p>
        <div class="ficons">
          <a href="{IG}" target="_blank" rel="noopener" aria-label="Instagram" title="Instagram"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.3" cy="6.7" r="1" fill="currentColor" stroke="none"/></svg></a>
          <a href="{FB}" target="_blank" rel="noopener" aria-label="Facebook" title="Facebook"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M13.5 21v-7h2.4l.4-3h-2.8V9.2c0-.9.3-1.5 1.5-1.5h1.4V5.1c-.3 0-1.1-.1-2.1-.1-2.1 0-3.6 1.3-3.6 3.7V11H8v3h2.7v7z"/></svg></a>
          <a href="mailto:{MAIL}" aria-label="Email" title="Email"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/></svg></a>
          <a href="https://maps.google.com/?q={ADDR}" target="_blank" rel="noopener" aria-label="Itinéraire" title="Itinéraire"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M12 21s-7-6.2-7-11a7 7 0 0 1 14 0c0 4.8-7 11-7 11z"/><circle cx="12" cy="10" r="2.5"/></svg></a>
        </div>
      </div>
    </div>
    <div class="fbottom"><span>© 2020-{time.strftime("%Y")} Toloache Paris. <a href="#">Mentions légales</a></span><span>Site : Raouf Hamouda</span></div>
  </div>
</footer>
<nav class="phonebar" aria-label="Actions rapides"><a href="{TEL_HREF}">Appeler</a><a href="carte.html">La carte</a><a class="hi" href="commander.html">Commander</a></nav>
<script src="app.js?v={STAMP}" defer></script>
</body>
</html>'''

def pagehead(eyebrow, title, extra="", dl="sombrero", dr="chili"):
    return f'<section class="pagehead">{dd(dl,"abs ph phl")}{dd(dr,"abs ph phr")}{dd("sparkle","abs ph phs")}<div class="wrap"><p class="eyebrow center">{eyebrow}</p><h1 class="center">{title}</h1>{extra}</div></section>'

# ---------- index ----------

SIGN_ITEMS = [("specialites","Mole Poblano","plat6"),("specialites","300 g d'Arrachera","plat3"),("tacos","Arrachera","plat1"),("tortas","Mexicaine","plat8"),("desserts","Gâteau au cacao mexicain et mezcal","plat4"),("cocktails","Mezcalita","plat7")]
def _find(sec,name):
    for s in menu["sections"]:
        if s["id"]==sec:
            for it in s["items"]:
                if (it.get("n") or it.get("name"))==name: return s,it
    return None,None
def _sign():
    out=[]
    for sec,name,img in SIGN_ITEMS:
        s,it=_find(sec,name)
        if not it: continue
        price=(it.get("p") or it.get("price") or "").split("/")[0].strip()
        desc=esc(it.get("d") or it.get("desc") or "")
        label=name if sec in ("specialites","desserts","cocktails") else f'{s["title"][:-1] if s["title"].endswith("s") else s["title"]} {name}'
        out.append(f'<article class="dish"><img src="img/{img}.webp" alt="{esc(name)}" loading="lazy"><div class="row"><b>{esc(label)}</b><span class="p">{esc(price)}</span></div>{"<p>"+desc+"</p>" if desc else ""}</article>')
    return "".join(out)

DOODLES=open("img/doodles.svg",encoding="utf-8").read()
def dd(i,cls="",w=None):
    vb="0 0 300 60" if i=="bunting" else "0 0 100 100"
    st=f' style="--w:{w}"' if w else ""
    return f'<svg class="dd dd-{i} {cls}" viewBox="{vb}" aria-hidden="true"{st}><use href="#d-{i}"/></svg>'
SIGN=_sign()
home = f'''
<section class="hero">
  <picture><source media="(max-width:700px)" srcset="img/hero_m.webp"><img src="img/hero.webp" alt="La salle du Toloache, rue de Clignancourt" fetchpriority="high"></picture>
  <div class="hero-text">
    <img class="wordmark" src="img/wordmark.png" alt="Toloache. Tacos, chelas, música, mezcal y arte. 49 rue de Clignancourt 75018 Paris">
    <p class="lede">La cuisine de Mexico, à la plancha, sur les flancs de la butte. Ouvert tard, jusqu'à 1h30.</p>
    <div class="hero-cta"><a class="btn" href="carte.html">Voir la carte</a><a class="btn ghost" href="{TEL_HREF}">Réserver</a></div>
  </div>
</section>

<section class="concept reveal" id="concept">
  {dd("sombrero","abs c1")}{dd("sparkle","abs c2")}{dd("chili","abs c3")}{dd("star","abs c4")}
  <div class="wrap cgrid">
    <div class="ctext">
      <h2>Une union culinaire jamais vue : <span class="hl">Mexico et Paris</span> à la même table.</h2>
      <p class="clede">Niché sur les flancs de la butte Montmartre, Toloache marie les parfums mexicains et français.</p>
      <p>Une carte faite de produits frais, un taquero qui manie la plancha comme un maître, et un service à l'écoute. Tacos, tortas, enchiladas, mole poblano, mezcal : tout est fait maison et sur place.</p>
      <p>Cuisine ouverte jusqu'à 1h30, options végétariennes et vegan, sur place, à emporter ou en livraison.</p>
      <a class="btn" href="carte.html">Voir la carte</a>
    </div>
    <figure class="cphoto"><img src="img/plat5.webp" alt="Plat de la maison" loading="lazy"></figure>
  </div>
</section>

<section class="gallery reveal" aria-label="Photos des plats">
  <figure class="g1"><img src="img/plat5.webp" alt="" loading="lazy"></figure><figure class="g2"><img src="img/plat1.webp" alt="" loading="lazy"></figure>
  <figure class="g3"><img src="img/plat7.webp" alt="" loading="lazy"></figure><figure class="g4"><img src="img/plat3.webp" alt="" loading="lazy"></figure>
  <figure class="g5"><img src="img/plat6.webp" alt="" loading="lazy"></figure><figure class="g6"><img src="img/plat8.webp" alt="" loading="lazy"></figure>
  <figure class="g7"><img src="img/plat2.webp" alt="" loading="lazy"></figure><figure class="g8"><img src="img/plat4.webp" alt="" loading="lazy"></figure>
</section>

<section class="signatures reveal">
  <div class="wrap">
    {dd("bunting","flow")}
    <div class="sighead"><h2>Les plats qu'on vient chercher.</h2><a class="btn ghost" href="carte.html">Toute la carte</a></div>
    <div class="strip">{SIGN}</div>
  </div>
</section>

<section class="playita reveal" id="playita">
  {dd("guitar","abs p1")}{dd("note","abs p2")}{dd("note","abs p3")}{dd("maracas","abs p4")}{dd("sparkle","abs p5")}
  <div class="wrap pgrid">
    <div>
      <p class="eyebrow">En sous-sol</p>
      <h2>La Playita <span class="hl">de Montmartre</span></h2>
      <p>Quelques marches à descendre et vous voilà dans l'espace pop-up, multiculturel et artistique de Montmartre. Projections, expositions, théâtre, musique live, dj sets et soirées privées s'y succèdent.</p>
      <p>La Playita se veut la fenêtre d'expression des artistes du XVIIIe et d'au-delà. Vous avez un projet ? Manifestez-vous.</p>
      <div class="hero-cta"><a class="btn" href="{TEL_HREF}">Proposer un projet</a><a class="btn ghost" href="actualites.html">Le programme</a></div>
    </div>
    <div class="days"><b>JEU<br>VEN<br>SAM<br>DIM</b><span>du jeudi au dimanche, dès 19h</span></div>
  </div>
</section>

<section class="suppliers reveal">
  <div class="wrap"><div class="ddrow">{dd("sun")}{dd("lime")}{dd("taco")}{dd("agave")}{dd("heart")}</div><h2>Nos fournisseurs</h2>
    <ul class="logos">{"".join(f'<li><img src="img/{f}.webp" alt="{esc(n)}" loading="lazy"></li>' for n,f in SUPPLIERS)}</ul></div>
</section>

<section class="infos" id="infos">
  <div class="wrap">
    <div class="h2row"><h2>Montmartre,<br><span class="hl">côté Clignancourt</span>.</h2>{dd("cactus","i1")}{dd("pinata","i2")}</div>
    <div class="infogrid reveal">
      <div>
        <h3>Horaires</h3>
        <dl class="hours2">
          <div><dt>Mardi à jeudi</dt><dd>12h-15h<br>19h-23h</dd></div>
          <div><dt>Vendredi et samedi</dt><dd>12h-15h<br>19h-2h</dd></div>
          <div class="off"><dt>Dimanche et lundi</dt><dd>Fermé</dd></div>
        </dl>
        <p class="muted small">Cuisine ouverte jusqu'à 1h30 le week-end.</p>
      </div>
      <div>
        <h3>Venir</h3>
        <p class="addr"><a href="https://maps.google.com/?q=Restaurant+Toloache+49+rue+de+Clignancourt+75018+Paris" target="_blank" rel="noopener">49 rue de Clignancourt<br>75018 Paris</a></p>
        <p class="muted">Métro Château Rouge (4) ou Anvers (2). Au pied de la butte.</p>
        <a class="btn" href="{TEL_HREF}">{TEL}</a>
        <p class="muted small">Groupes et soirées privées à La Playita : appelez-nous.</p>
      </div>
      <div class="map"><iframe title="Plan d'accès" src="{MAP}" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe></div>
    </div>
  </div>
</section>'''


# ---------- carte ----------
def section_html(s):
    icon = f'<img class="sec-icon" src="img/{s["icon"]}.png" alt="">' if s.get("icon") else ""
    gf = '<img class="gf" src="img/gluten_free.png" alt="Sans gluten" title="Sans gluten">' if s.get("gf") else ""
    intro = f'<p class="menu-intro">{esc(s["intro"])}</p>' if s.get("intro") else ""
    items = "".join(f'<li><div class="it"><span class="n">{esc(it["n"])}{" <i class=v title=végétarien>v</i>" if it.get("v") else ""}</span><span class="dots"></span><span class="p">{esc(it["p"])}</span></div>'
                    + (f'<p class="d">{esc(it["d"])}</p>' if it.get("d") else "") + "</li>" for it in s["items"])
    return f'<section class="msec" id="{s["id"]}"><h2 class="mtitle"><img class="fleuron" src="img/fleuron.svg" alt=""> {esc(s["title"])} {icon}{gf}</h2>{intro}<ul class="menu-list">{items}</ul></section>'
chips = "".join(f'<a class="chip" href="#{s["id"]}">{esc(s["title"])}</a>' for s in menu["sections"])
carte = pagehead("La carte", "Tout est fait maison, <span class=hl>sur place</span>", dl="taco", dr="chili", extra= f'<p class="menu-note center">{esc(menu["note"])} <i class="v">v</i> végétarien ou vegan possible.</p>') + f'''
<nav class="chips" aria-label="Sections de la carte">{chips}</nav>
<div class="wrap menu-wrap">{"".join(section_html(s) for s in menu["sections"])}</div>'''

actus = pagehead("Actualités", "Ce qui se passe <span class=hl>à Toloache</span>", dl="guitar", dr="note", extra='<p class="menu-note center">Du jeudi au dimanche, La Playita ouvre en sous-sol. Le programme vit sur Facebook et Instagram.</p>') + f'''
<section class="program">
  <div class="wrap">
    <ul class="cards">
      <li><img src="img/plat7.webp" alt="" loading="lazy"><h3>Projections</h3><p>Films et courts-métrages, en salle, un verre à la main.</p></li>
      <li><img src="img/plat3.webp" alt="" loading="lazy"><h3>Expositions</h3><p>Les artistes du XVIIIe et d'au-delà accrochent à La Playita.</p></li>
      <li><img src="img/plat6.webp" alt="" loading="lazy"><h3>Musique live &amp; DJ sets</h3><p>Du jeudi au samedi, jusqu'à 2h.</p></li>
      <li><img src="img/plat8.webp" alt="" loading="lazy"><h3>Soirées privées</h3><p>Anniversaires, vernissages, privatisation. <a href="{TEL_HREF}">Appelez-nous.</a></p></li>
    </ul>
  </div>
</section>
<section class="social">
  <div class="wrap">
    <div class="socialgrid">
      <a class="socard" href="{FB}" target="_blank" rel="noopener"><span class="eyebrow">Facebook</span><strong>Événements et programme</strong><span class="muted">facebook.com/toloacheparis</span></a>
      <a class="socard" href="{IG}" target="_blank" rel="noopener"><span class="eyebrow">Instagram</span><strong>Les photos du moment</strong><span class="muted">@toloacheparis</span></a>
      <a class="socard" href="{TEL_HREF}"><span class="eyebrow">Un projet ?</span><strong>Proposer une soirée à La Playita</strong><span class="muted">{TEL}</span></a>
    </div>
    <div id="fb-root"></div><script async defer crossorigin="anonymous" src="https://connect.facebook.net/fr_FR/sdk.js#xfbml=1&version=v8.0"></script>
    <div class="fbwrap"><div class="fb-page" data-href="{FB}" data-tabs="events,timeline" data-width="500" data-height="900" data-small-header="true" data-adapt-container-width="true" data-hide-cover="true" data-show-facepile="false"></div></div>
  </div>
</section>'''

QUOTES = [("Les cocktails au mezcal sont très bons, et l'arrachera à la plancha vaut le détour.","Avis Google"),
          ("Le meilleur mexicain de Paris. Le chef vient de Mexico et ça se sent dans l'assiette.","Avis Google"),
          ("Ceviche et tacos de poisson impeccables, ambiance de quartier, on y retourne.","Avis Google")]
avis = pagehead("Les avis", "Ce que vous <span class=hl>en dites</span>", dl="heart", dr="star", extra='<p class="menu-note center">Des centaines d\'avis sur Google. Voici ce qui revient le plus souvent.</p>') + f'''
<section class="reviews">
  <div class="wrap">
    <div class="ratingrow">
      <div class="rating"><span class="big">4,7</span><span class="stars" aria-label="4,7 sur 5">★★★★★</span><span class="muted">sur Google · plus de 300 avis</span></div>
      <ul class="quotes">{"".join(f'<li><img class="fleuron" src="img/fleuron.svg" alt=""><blockquote>{esc(q)}</blockquote><cite>{src}</cite></li>' for q,src in QUOTES)}</ul>
    </div>
    <div class="widget"><script src="https://apps.elfsight.com/p/platform.js" defer></script><div class="elfsight-app-1c99a5b8-7455-4f89-90ed-3f691dbfe586"></div></div>
    <p class="center"><a class="btn" href="https://www.google.com/maps/search/?api=1&query=Restaurant+Toloache+49+rue+de+Clignancourt+75018+Paris" target="_blank" rel="noopener">Laisser un avis sur Google</a></p>
  </div>
</section>'''

commander = pagehead("Commander", "Toloache <span class=hl>chez vous</span>", dl="pinata", dr="maracas", extra='<p class="menu-note center">À emporter : appelez-nous. En livraison : choisissez votre partenaire.</p>') + f'''
<section class="order"><div class="wrap">
  <ul class="partners">{"".join(f'<li><a href="{u}" target="_blank" rel="noopener"><img src="img/{f}.webp" alt="" loading="lazy"><span>{n}</span></a></li>' for n,u,f in ORDER)}</ul>
  <p class="center"><a class="btn" href="{TEL_HREF}">À emporter · {TEL}</a></p>
</div></section>'''

out = {
 "index.html": ("Toloache · Restaurant mexicain à Montmartre, Paris 18","Toloache, restaurant mexicain sur la butte Montmartre : tacos, tortas, mole, mezcal. Cuisine de Mexico à la plancha, ouverte tard. 49 rue de Clignancourt, Paris 18.",home,"home"),
 "carte.html": ("La carte · Toloache","Tacos, tortas, burritos, spécialités, cocktails au mezcal. Tout est fait maison et sur place.",carte,"inner"),
 "actualites.html": ("Actualités · Toloache","Concerts, projections, expos et soirées à La Playita de Montmartre.",actus,"inner"),
 "avis.html": ("Avis · Toloache","Les avis de nos clients.",avis,"inner"),
 "commander.html": ("Commander · Toloache","Toloache en livraison sur Deliveroo, Uber Eats et Just Eat, ou à emporter.",commander,"inner"),
}
for f,(t,d,b,c) in out.items(): (H/f).write_text(shell(f,t,d,b,c))
print("built", ", ".join(out), "stamp", STAMP)
