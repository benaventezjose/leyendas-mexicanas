#!/usr/bin/env python3
"""Builds story.json and script.md for 'El Hombre Caimán' (San Pedro Huamelula, Oaxaca). Edit BEATS here, then run.
After tts.py has run, re-run this: shots longer than ~9.5 s are split automatically with a second camera move."""
import json, os, math
HERE = os.path.dirname(os.path.abspath(__file__))


def L(src, **kw):
    d = {"src": f"art/{src}.png"}; d.update(kw); return d


def S(bg, *layers, cam=None, fx=None, text=None, tr=None, tl=None, w=None, grade=None, out=None, dur=None, vig=None):
    sc = {"layers": [L(bg)] + list(layers)}
    if cam: sc["cam"] = {"from": list(cam[0]), "to": list(cam[1]), "ease": cam[2] if len(cam) > 2 else "inout"}
    if fx: sc["fx"] = fx
    if text: sc["text"] = text
    if tr: sc["transition"] = tr
    if tl: sc["transition_len"] = tl
    if w: sc["weight"] = w
    if dur: sc["dur"] = dur
    if grade: sc["grade"] = grade
    if out: sc["out"] = "fade"; sc["out_len"] = out
    if vig: sc["vignette"] = vig
    return sc


def T(s, style, a=0.3, b=None, pos=None):
    d = {"str": s, "style": style, "at": [a, b if b else a + 4.0]}
    if not pos and style in ("quote", "big") and not s.startswith("PRÓXIMO"): pos = "bottom"
    if pos: d["pos"] = pos
    return d


def X(name, at=0.0, gain=-6, at_scene=None, pan=None, **args):
    d = {"name": name, "at": at, "gain": gain}
    if at_scene is not None: d["scene"] = at_scene
    if pan is not None: d["pan"] = pan
    if args: d["args"] = args
    return d


FOG = {"type": "fog", "strength": 0.35}
FOGL = {"type": "fog", "strength": 0.45, "low": True}
FL = {"type": "flicker", "amp": 0.08}
def SH(a, b, amp=7): return {"type": "shake", "amp": amp, "at": [a, b]}
def PU(bpm=70, amp=0.1): return {"type": "pulse", "bpm": bpm, "amp": amp}

N = 0
BEATS = []
def B(text, *scenes, **kw):
    global N; N += 1
    b = {"id": f"b{N:03d}", "text": text}; b.update(kw); b["scenes"] = list(scenes)
    BEATS.append(b)

FOGLAY = L("l_fog", blend="screen", opacity=[0, 0.8], anim=[{"type": "drift", "dx": -0.06, "ease": "linear"}])
FIREG = L("l_fire_glow", blend="screen", anim=[{"type": "flicker", "amp": 0.2, "speed": 1.2}])
CAND = L("l_candle_glow", blend="screen", anim=[{"type": "flicker", "amp": 0.15, "speed": 1.8}])
SWIM = L("l_caiman_swim", depth=1.05, anim=[{"type": "drift", "dx": -0.12, "dy": 0.01, "ease": "inout"}])
SWIMR = L("l_caiman_swim", depth=1.05, anim=[{"type": "drift", "dx": 0.10, "ease": "inout"}])
EYES = L("l_eyes", blend="screen", opacity=[0, 1.0], appear_at=1.2, fade_in=1.2, anim=[{"type": "float", "amp": 0.003, "period": 4}])
EYESQ = L("l_eyes", blend="screen", opacity=[0, 1.0], appear_at=0.2, fade_in=0.3)
PRIN = L("l_princess", depth=1.08, opacity=[0, 1.0], fade_in=1.5, anim=[{"type": "sway", "deg": 0.6, "period": 6, "pivot": [0.5, 0.95]}])
KWALK = L("l_king_walk", depth=1.1, anim=[{"type": "drift", "dx": 0.08, "ease": "linear"}])
TORCH = L("l_torch_glow", blend="screen", anim=[{"type": "flicker", "amp": 0.2, "speed": 1.5}])
COPAL = L("l_copal", blend="screen", opacity=[0, 0.85], anim=[{"type": "drift", "dy": -0.08, "ease": "linear"}])

KING = dict(voice="em_santa", speed=0.84)
HUAVE = dict(voice="em_santa", speed=0.74)
PRINV = dict(voice="ef_dora", speed=0.8, fx="eco")
NIGHT = ["night", {"name": "crickets", "gain": -8}]
LAGOON = ["river", {"name": "crickets", "gain": -6}, {"name": "night", "gain": -10}]
SEA = ["sea", {"name": "wind", "gain": -10}]
DRY = ["wind", {"name": "fire", "gain": -20}]
TOWN = ["city", {"name": "crickets", "gain": -12}]
FLASH = lambda img="caiman_close": S(img, tr="flash", tl=0.12, dur=1.4, cam=((0.5, 0.45, 1.25), (0.5, 0.45, 1.5)), fx=[SH(0, 0.6, 9)])
SCARE = [X("riser", -3.5, -8, at_scene=1, dur=3.5), X("sting", 0.0, -2, at_scene=1), X("boom", 0.0, -3, at_scene=1)]
SPLASH = lambda at=0.5, g=-8: X("splash", at, g)

# ======================================================================== COLD OPEN
B("Costa de Oaxaca. Una noche sin viento. La laguna está tan quieta que parece un espejo negro.",
  S("lagoon_night", FOGLAY, cam=((0.5, 0.5, 1.05), (0.5, 0.52, 1.25), "in"), fx=[FOGL], tr="fade", tl=1.2,
    text=[T("Costa de Oaxaca|hace muchos siglos", "date", 0.6, 5.0)]),
  pre=0.6, music="dread", amb=LAGOON)
B("Imagina a un hombre que camina hacia el agua con collar de conchas y flores en las manos. Va vestido de novio. Y nadie del pueblo se atreve a seguirlo.",
  S("king_shore", TORCH, cam=((0.45, 0.55, 1.1), (0.5, 0.5, 1.35), "in"), fx=[FOGL]),
  S("king_portrait", cam=((0.5, 0.42, 1.2), (0.5, 0.42, 1.4), "in"), fx=[{"type": "flicker", "amp": 0.05}], tr="xfade", tl=0.6),
  sfx=[STEPS(0.4, 5, -14)] if False else [X("footsteps", 0.4, -14, dur=5)])
B("Se detiene en la orilla. Espera. Y entonces, en medio de la laguna, se abren dos ojos dorados.",
  S("lagoon_eyes", EYES, cam=((0.5, 0.5, 1.1), (0.5, 0.52, 1.45), "in"), fx=[FOGL]),
  music="tension", sfx=[X("heartbeat", 1.0, -12, dur=7, bpm=76)])
B("Algo enorme empieza a nadar hacia él. Despacio. Sin hacer ruido.",
  S("lagoon_night", SWIM, cam=((0.55, 0.6, 1.2), (0.45, 0.6, 1.45), "in"), fx=[FOGL]),
  sfx=[X("whisper", 0.5, -18, dur=4)])
B("",
  S("lagoon_eyes", cam=((0.5, 0.5, 1.4), (0.5, 0.5, 1.5), "in"), fx=[FOGL], dur=1.4),
  FLASH("caiman_close"), pause=0.8, sfx=SCARE + [SPLASH(1.4, -4)])
B("Esa noche, un rey se casó con una lagarta. Y lo más extraño de esta historia… es que esa boda se sigue celebrando. Todos los años. Hasta hoy.",
  S("caiman_bride", cam=((0.5, 0.5, 1.1), (0.5, 0.45, 1.35), "in"), fx=["dust"], grade="warm"),
  S("church_huamelula", cam=((0.5, 0.5, 1.05), (0.5, 0.48, 1.2), "in"), fx=["dust"], grade="warm", tr="xfade", tl=0.8),
  music="mystery", amb=TOWN, sfx=[X("bell", 5.0, -14, freq=180)])
B("",
  S("title_bg", cam=((0.5, 0.5, 1.0), (0.5, 0.48, 1.12)), fx=[FOG], tr="fade", tl=0.8,
    text=[T("EL HOMBRE CAIMÁN|la boda con la lagarta", "title", 0.6, 6.4)]),
  pause=5.2, music="mystery", sfx=[X("boom", 0.4, -4), X("whoosh", 0.3, -8)])
B("Pero hay una pregunta que en ese pueblo nadie quiere hacer en voz alta. ¿Qué pasaría si un año… no hubiera boda? Esa respuesta te la cuento al final.",
  S("lagoon_night", FOGLAY, cam=((0.5, 0.5, 1.1), (0.5, 0.48, 1.3), "in"), fx=[FOGL]),
  amb=LAGOON)

# ======================================================================== I
B("Cuentan que hace muchos siglos, en la costa del Istmo de Tehuantepec, vivían dos pueblos que no se podían ver.",
  S("map_isthmus", cam=((0.5, 0.5, 1.05), (0.55, 0.55, 1.3), "in"), fx=["dust"], tr="fade", tl=1.0, grade="sepia",
    text=[T("CAPÍTULO I|La sequía", "chapter", 0.6, 5.0)]),
  music="calm", amb=SEA)
B("En los cerros, mirando al mar, estaban los chontales. Abajo, en las barras de arena entre las lagunas, vivían los huaves, que se llaman a sí mismos ikoots.",
  S("village_chontal", FIREG, cam=((0.4, 0.5, 1.05), (0.6, 0.5, 1.2), "linear"), fx=["embers"]),
  S("huave_village", cam=((0.6, 0.55, 1.05), (0.4, 0.55, 1.2), "linear"), fx=[FOGL], tr="xfade", tl=0.6))
B("Unos sembraban maíz en las laderas. Los otros eran dueños del agua. De las lagunas llenas de camarón, de pescado, de vida.",
  S("milpa_coast", cam=((0.45, 0.55, 1.05), (0.55, 0.5, 1.2), "linear"), fx=["dust"], grade="warm"),
  S("canoe_night", cam=((0.5, 0.55, 1.1), (0.55, 0.55, 1.3), "in"), fx=[FOGL], tr="xfade", tl=0.6))
B("Y por esa agua peleaban. Canoas que se encontraban de noche en la laguna. Antorchas. Gritos. Redes cortadas al amanecer.",
  S("war_canoes", TORCH, cam=((0.45, 0.55, 1.1), (0.55, 0.5, 1.35), "in"), fx=["embers", FOGL], grade="night"),
  music="tension", sfx=[X("whoosh", 1.0, -10), X("splash", 2.5, -10), X("splash", 4.0, -12)])
B("Cada pueblo tenía sus muertos y sus rencores. Y cada uno le enseñaba a sus hijos que del otro lado de la laguna vivía el enemigo.",
  S("war_canoes", TORCH, cam=((0.55, 0.5, 1.3), (0.45, 0.5, 1.45), "inout"), fx=["embers", FOGL], grade="night"),
  sfx=[X("whoosh", 2.0, -12)])
B("Hasta que un año, el cielo dejó de llover.",
  S("drought", cam=((0.5, 0.5, 1.05), (0.5, 0.45, 1.3), "in"), fx=["dust"], grade="warm"),
  music="sad", amb=DRY, pre=0.4)
B("Imagina el sol de la costa, blanco, encima de tu cabeza, un día tras otro. La milpa se dobla y se seca. La tierra se abre en grietas tan anchas que cabe tu mano.",
  S("drought", cam=((0.4, 0.6, 1.2), (0.6, 0.62, 1.4), "linear"), fx=["dust", {"type": "pulse", "bpm": 50, "amp": 0.05}], grade="warm"),
  S("cracked_earth", cam=((0.5, 0.5, 1.15), (0.5, 0.55, 1.45), "in"), fx=["dust"], grade="warm", tr="xfade", tl=0.6))
B("Las lagunas empezaron a encogerse. Primero un palmo. Luego una brazada. Al final, los pescadores caminaban sobre lodo donde antes había agua hasta el pecho.",
  S("dry_lagoon", cam=((0.5, 0.55, 1.05), (0.5, 0.55, 1.3), "in"), fx=["dust"], grade="warm"),
  S("nets_empty", cam=((0.45, 0.55, 1.1), (0.55, 0.5, 1.3), "inout"), fx=["dust"], grade="warm", tr="xfade", tl=0.6))
B("Las redes salían vacías. Los niños lloraban de hambre. Y los viejos, sentados junto al fuego, decían algo que daba miedo escuchar.",
  S("nets_close", cam=((0.5, 0.5, 1.15), (0.5, 0.5, 1.4), "in"), fx=["dust"], grade="warm"),
  S("council", FIREG, cam=((0.5, 0.55, 1.1), (0.5, 0.5, 1.3), "in"), fx=["embers"], grade="candle", tr="xfade", tl=0.6),
  amb=["fire", {"name": "wind", "gain": -10}])
B("Decían que el agua no se había ido. Que alguien se la había llevado. Que el agua estaba enojada.",
  S("elder_portrait", FIREG, cam=((0.5, 0.42, 1.2), (0.5, 0.42, 1.4), "in"), fx=[{"type": "flicker", "amp": 0.08}], grade="candle"),
  music="dread", sfx=[X("whisper", 0.5, -16, dur=5)])

# ======================================================================== II
B("Y había un nombre que los viejos repetían una y otra vez, junto al fuego, como si fuera una oración. El nombre de la laguna de los huaves.",
  S("council", FIREG, cam=((0.5, 0.5, 1.3), (0.5, 0.48, 1.45), "in"), fx=["embers"], grade="candle"),
  sfx=[X("whisper", 1.0, -18, dur=5)])
B("El rey de los chontales era joven. Dicen que tenía el pelo largo, una manta de algodón blanco y un collar de conchas que sonaba cuando caminaba.",
  S("king_portrait", cam=((0.5, 0.45, 1.05), (0.5, 0.42, 1.3), "in"), fx=["dust"], tr="fade", tl=1.0,
    text=[T("CAPÍTULO II|La hija de la laguna", "chapter", 0.6, 5.0)]),
  music="mystery", amb=NIGHT)
B("Y una noche hizo lo que ningún chontal se había atrevido a hacer. Bajó solo a la laguna de los huaves. Sin armas. Con una antorcha.",
  S("king_walk_bg", KWALK, TORCH, cam=((0.4, 0.55, 1.1), (0.6, 0.55, 1.3), "linear"), fx=[FOGL]),
  amb=LAGOON, sfx=[X("footsteps", 0.3, -12, dur=7)])
B("Cruzó los manglares con el lodo hasta las rodillas. Las raíces parecían manos saliendo del agua. Y sintió, todo el camino, que algo lo estaba mirando desde la oscuridad.",
  S("mangrove_path", TORCH, cam=((0.45, 0.55, 1.1), (0.55, 0.52, 1.35), "in"), fx=[FOGL]),
  S("lagoon_eyes", EYES, cam=((0.6, 0.5, 1.3), (0.6, 0.5, 1.45), "in"), fx=[FOGL], tr="xfade", tl=0.5, w=0.6),
  music="tension", sfx=[X("splash", 3.0, -14), X("owl", 6.0, -14)])
B("Lo recibió el viejo rey de los huaves, sentado frente a su casa de palma, con el agua de la laguna a sus pies.",
  S("huave_king", FIREG, cam=((0.5, 0.45, 1.1), (0.5, 0.42, 1.3), "in"), fx=[{"type": "flicker", "amp": 0.06}], grade="candle"))
B("Alrededor, en la oscuridad, los pescadores huaves lo miraban con los arpones en la mano. Bastaba una palabra del viejo para que el rey chontal no volviera a ver el amanecer.",
  S("crowd_shore", TORCH, cam=((0.55, 0.55, 1.2), (0.45, 0.55, 1.35), "linear"), fx=[FOGL]),
  sfx=[X("heartbeat", 1.0, -14, dur=6, bpm=84)])
B("Mi pueblo se muere. Te ofrezco la paz. Pide lo que quieras.",
  S("king_resolve", FIREG, cam=((0.5, 0.42, 1.2), (0.5, 0.42, 1.35), "in"), fx=[{"type": "flicker", "amp": 0.06}], grade="candle",
    text=[T("Te ofrezco la paz.|el rey chontal", "quote", 0.5, 4.5)]), **KING)
B("El viejo se quedó callado mucho rato. Luego sonrió, despacio, como quien ya sabía que esa visita iba a llegar.",
  S("huave_king_smile", FIREG, cam=((0.5, 0.42, 1.25), (0.5, 0.4, 1.45), "in"), fx=[{"type": "flicker", "amp": 0.06}], grade="candle"),
  music="tension")
B("Habrá paz. Habrá agua. Pero tendrás que casarte con mi hija.",
  S("huave_king_smile", FIREG, cam=((0.5, 0.4, 1.45), (0.5, 0.38, 1.6), "in"), fx=[{"type": "flicker", "amp": 0.06}], grade="candle",
    text=[T("Tendrás que casarte con mi hija.|el rey huave", "quote", 0.5, 5.0)]), **HUAVE)
B("El rey chontal aceptó sin pensarlo. Había oído hablar de la princesa huave. Decían que era la mujer más hermosa de toda la costa.",
  S("princess_portrait", cam=((0.5, 0.45, 1.1), (0.5, 0.42, 1.3), "in"), fx=["fireflies"], grade="moon"),
  music="calm")
B("Pero había algo que nadie le había contado. Algo que los huaves solo decían en voz baja.",
  S("princess_portrait", cam=((0.5, 0.42, 1.3), (0.5, 0.38, 1.55), "in"), fx=[FOGL], grade="night"),
  music="dread", sfx=[X("whisper", 0.3, -16, dur=4)])
B("Que la princesa había nacido de la laguna. Que de día caminaba entre ellos como cualquier muchacha. Y que de noche… volvía al agua.",
  S("princess_shore", PRIN, cam=((0.5, 0.55, 1.1), (0.5, 0.5, 1.35), "in"), fx=[FOGL]),
  S("lagoon_night", SWIMR, cam=((0.4, 0.6, 1.2), (0.6, 0.6, 1.4), "inout"), fx=[FOGL], tr="xfade", tl=0.8),
  sfx=[X("splash", 7.0, -10)])
B("Si te está gustando esta leyenda, suscríbete y activa la campanita. Aquí, cada semana, una nueva historia de México.",
  S("canoe_night", cam=((0.5, 0.55, 1.1), (0.5, 0.52, 1.25), "in"), fx=[FOGL],
    text=[T("SUSCRÍBETE|una leyenda nueva cada semana", "big", 0.8, 6.0)]), music="mystery")

# ======================================================================== III
B("La boda sería en la orilla, la noche de luna llena. Los huaves llenaron la arena de flores y quemaron copal.",
  S("wedding_ancient", COPAL, TORCH, cam=((0.5, 0.55, 1.05), (0.5, 0.5, 1.25), "in"), fx=[FOGL, "fireflies"], tr="fade", tl=1.0,
    text=[T("CAPÍTULO III|La boda", "chapter", 0.6, 5.0)]),
  music="mystery", amb=LAGOON, sfx=[X("bell", 2.0, -18, freq=220)])
B("Las mujeres huaves tejieron un vestido de algodón blanco, bordado con flores y peces. Los hombres llevaron tambores y caracoles de mar. Pero nadie, en todo el día, vio a la novia.",
  S("weaving", CAND, cam=((0.5, 0.55, 1.1), (0.5, 0.5, 1.3), "in"), fx=["dust"], grade="candle"),
  amb=["fire", {"name": "crickets", "gain": -8}])
B("El rey chontal esperó en la orilla, con su collar de conchas, mirando hacia el agua negra. Detrás de él, los dos pueblos guardaban silencio.",
  S("king_shore", TORCH, cam=((0.5, 0.5, 1.15), (0.5, 0.5, 1.4), "in"), fx=[FOGL]),
  S("crowd_shore", TORCH, cam=((0.45, 0.55, 1.1), (0.55, 0.55, 1.25), "linear"), fx=[FOGL], tr="xfade", tl=0.6),
  music="tension", sfx=[X("heartbeat", 2.0, -14, dur=8, bpm=70)])
B("Entonces el viejo rey huave levantó los brazos y llamó a su hija por su nombre.",
  S("huave_king_call", TORCH, cam=((0.5, 0.5, 1.1), (0.5, 0.45, 1.3), "in"), fx=[FOGL]),
  sfx=[X("gust", 1.0, -10)])
B("La laguna se movió. Las olas pequeñas llegaron hasta los pies del rey. Y del agua salió una cabeza larga, cubierta de escamas, con dos ojos dorados que lo miraban fijo.",
  S("lagoon_eyes", EYES, cam=((0.5, 0.5, 1.2), (0.5, 0.52, 1.5), "in"), fx=[FOGL]),
  S("caiman_full", cam=((0.5, 0.55, 1.1), (0.5, 0.55, 1.35), "in"), fx=[FOGL], tr="xfade", tl=0.5),
  music="dread", sfx=[X("splash", 0.8, -8), X("riser", 6.0, -10, dur=4)])
B("",
  S("caiman_full", cam=((0.5, 0.55, 1.35), (0.5, 0.55, 1.45), "in"), fx=[FOGL], dur=1.2),
  FLASH("caiman_close"), pause=0.8, sfx=SCARE)
B("Ella es mi hija. Ella es tu esposa.",
  S("huave_king_call", TORCH, cam=((0.5, 0.45, 1.3), (0.5, 0.42, 1.5), "in"), fx=[FOGL],
    text=[T("Ella es tu esposa.|el rey huave", "quote", 0.5, 4.5)]), **HUAVE)
B("Imagina estar ahí. Frente a ti, una lagarta del largo de tu brazo extendido, con la boca llena de dientes. Detrás de ti, tu pueblo muriéndose de hambre.",
  S("king_fear", TORCH, cam=((0.5, 0.42, 1.2), (0.5, 0.42, 1.4), "in"), fx=[{"type": "flicker", "amp": 0.06}]),
  S("caiman_close", cam=((0.5, 0.5, 1.15), (0.5, 0.5, 1.35), "in"), fx=[FOGL], tr="xfade", tl=0.5))
B("El rey se arrodilló en la arena. Extendió las manos. Y la lagarta, muy despacio, se dejó cargar.",
  S("king_kneel", TORCH, cam=((0.5, 0.55, 1.1), (0.5, 0.5, 1.35), "in"), fx=[FOGL]),
  music="sad")
B("Nadie respiraba. Las antorchas temblaban con el viento del mar. La lagarta abrió la boca… y la volvió a cerrar, despacio, como si sonriera.",
  S("caiman_close", TORCH, cam=((0.5, 0.5, 1.3), (0.5, 0.5, 1.5), "in"), fx=[FOGL, {"type": "flicker", "amp": 0.06}]),
  sfx=[X("gust", 0.5, -12)])
B("Dicen que en ese momento, por un instante, el rey vio en el reflejo del agua a una muchacha de pelo largo que le sonreía.",
  S("reflection", cam=((0.5, 0.6, 1.1), (0.5, 0.62, 1.35), "in"), fx=[FOGL], grade="moon"),
  S("princess_soft", cam=((0.5, 0.42, 1.2), (0.5, 0.42, 1.35), "in"), fx=["fireflies"], grade="moon", tr="xfade", tl=0.8),
  music="hope")
B("Te estaba esperando.",
  S("princess_soft", cam=((0.5, 0.42, 1.35), (0.5, 0.4, 1.5), "in"), fx=["fireflies"], grade="moon",
    text=[T("Te estaba esperando.|", "whisper", 0.4, 3.4)]), **PRINV)
B("Y el rey besó a su esposa.",
  S("kiss_ancient", TORCH, cam=((0.5, 0.5, 1.15), (0.5, 0.48, 1.4), "in"), fx=[FOGL]), pause=0.4)
B("En ese mismo instante, un trueno partió el cielo en dos.",
  S("storm_village", cam=((0.5, 0.45, 1.05), (0.5, 0.45, 1.2), "in"), fx=[{"type": "lightning", "at": [0.4, 2.6]}, SH(0.4, 1.2, 6)], grade="cold"),
  music="climax", amb=["rain", {"name": "wind", "gain": -6}], sfx=[X("thunder", 0.3, -2), X("thunder", 2.6, -5)])
B("Y empezó a llover. Después de tantos meses, empezó a llover. La gente salió de sus casas con los brazos abiertos. Los niños bailaban en el lodo.",
  S("rain_joy", cam=((0.45, 0.5, 1.05), (0.55, 0.5, 1.25), "linear"), fx=[{"type": "rain", "strength": 0.45}, {"type": "lightning", "at": [3.0]}], grade="cold"),
  S("cracked_rain", cam=((0.5, 0.5, 1.2), (0.5, 0.55, 1.4), "in"), fx=[{"type": "rain", "strength": 0.5}], grade="cold", tr="xfade", tl=0.6),
  sfx=[X("thunder", 3.0, -8)])
B("Las lagunas se llenaron otra vez. Y a la mañana siguiente, las redes salieron tan pesadas de pescado que hacían falta cuatro hombres para sacarlas.",
  S("lagoon_dawn", cam=((0.5, 0.5, 1.05), (0.5, 0.48, 1.25), "in"), fx=[FOGL], grade="none"),
  S("fish_abundance", cam=((0.5, 0.55, 1.1), (0.5, 0.5, 1.3), "in"), fx=["dust"], grade="warm", tr="xfade", tl=0.6),
  music="hope", amb=SEA, sfx=[X("splash", 4.0, -12)])
B("Desde esa noche, chontales y huaves dejaron de pelear. El hombre del cerro y la hija de la laguna habían quedado unidos para siempre.",
  S("two_peoples", FIREG, cam=((0.5, 0.55, 1.05), (0.5, 0.5, 1.2), "in"), fx=["embers"], grade="candle"))

# ======================================================================== IV
B("Pero un pacto con el agua no se firma una sola vez.",
  S("lagoon_night", cam=((0.5, 0.5, 1.05), (0.5, 0.5, 1.25), "in"), fx=[FOGL], tr="fade", tl=1.0,
    text=[T("CAPÍTULO IV|La promesa", "chapter", 0.6, 5.0)]),
  music="dread", amb=LAGOON, pre=0.4)
B("Cuentan que la princesa le hizo prometer al rey una sola cosa.",
  S("princess_soft", cam=((0.5, 0.42, 1.15), (0.5, 0.42, 1.3), "in"), fx=[FOGL], grade="moon"))
B("Cada año, cuando vuelvan las lluvias, cásate conmigo otra vez. Y que nadie en tu pueblo me falte al respeto.",
  S("princess_eyes", cam=((0.5, 0.42, 1.25), (0.5, 0.4, 1.45), "in"), fx=[FOGL], grade="moon",
    text=[T("Cásate conmigo otra vez.|la princesa", "quote", 0.5, 5.0)]), **PRINV)
B("Y así fue durante generaciones. Cada año, una lagarta era vestida de novia, llevada de casa en casa y casada con el señor del pueblo. Y cada año, llovía.",
  S("caiman_bride", cam=((0.5, 0.5, 1.1), (0.5, 0.45, 1.3), "in"), fx=["dust"], grade="warm"),
  S("rain_joy", cam=((0.5, 0.5, 1.1), (0.5, 0.5, 1.25), "linear"), fx=[{"type": "rain", "strength": 0.3}], grade="cold", tr="xfade", tl=0.6),
  music="mystery")
B("Pero dicen que hubo un pescador que no creía en esas cosas.",
  S("fisher_portrait", cam=((0.5, 0.45, 1.1), (0.5, 0.42, 1.3), "in"), fx=[FOGL]),
  music="tension")
B("Un muchacho que se reía de la boda. Que decía que una lagarta era solo un animal, y que él no le tenía miedo a nada que viviera en el agua.",
  S("fisher_laugh", FIREG, cam=((0.5, 0.42, 1.15), (0.5, 0.42, 1.35), "in"), fx=["embers"], grade="candle"),
  amb=["fire", {"name": "crickets", "gain": -8}])
B("Gritaba en la playa, delante de todos, que él iba a traer a la novia arrastrando de la cola. Los viejos bajaban la mirada. Nadie le contestaba.",
  S("council", FIREG, cam=((0.4, 0.55, 1.2), (0.55, 0.55, 1.35), "linear"), fx=["embers"], grade="candle"))
B("Una noche, borracho, salió solo en su canoa. Llevaba un arpón. Iba a buscar a la novia de la laguna.",
  S("canoe_night", TORCH, cam=((0.5, 0.55, 1.1), (0.55, 0.55, 1.35), "in"), fx=[FOGL]),
  amb=LAGOON, sfx=[X("splash", 1.0, -14), X("splash", 4.0, -14)])
B("La laguna estaba en silencio. Ni un grillo. Ni una rana. Solo el ruido del remo entrando en el agua… y saliendo… y entrando.",
  S("canoe_far", cam=((0.5, 0.55, 1.15), (0.5, 0.55, 1.45), "in"), fx=[FOGL]),
  amb=[], music="silence", sfx=[X("splash", 1.5, -16), X("splash", 4.0, -16), X("splash", 6.5, -16)])
B("Entonces sintió que algo golpeaba la canoa por debajo. Una vez. Dos veces.",
  S("canoe_close", cam=((0.5, 0.55, 1.2), (0.5, 0.55, 1.4), "in"), fx=[FOGL, SH(1.5, 2.0, 8), SH(3.4, 3.9, 10)]),
  music="dread", sfx=[X("knock", 1.5, -4, times=1), X("knock", 3.4, -2, times=1)])
B("Se asomó por la orilla de la canoa. Y en el agua negra no vio su propia cara. Vio la cara de una mujer… con los ojos dorados de una lagarta.",
  S("water_face", cam=((0.5, 0.5, 1.15), (0.5, 0.5, 1.45), "in"), fx=[FOGL], grade="moon"),
  sfx=[X("riser", 3.0, -9, dur=4)])
B("",
  S("water_face", cam=((0.5, 0.5, 1.45), (0.5, 0.5, 1.55), "in"), fx=[FOGL], dur=1.2),
  FLASH("princess_eyes"), pause=0.8, sfx=SCARE + [SPLASH(1.4, -3)])
B("A la mañana siguiente encontraron la canoa vacía, flotando en medio de la laguna. El arpón estaba partido en dos.",
  S("canoe_dawn", cam=((0.5, 0.55, 1.05), (0.5, 0.55, 1.3), "in"), fx=[FOGL], grade="cold"),
  music="sad", amb=["river", {"name": "wind", "gain": -10}])
B("En el lodo de la orilla había unas huellas largas, de patas con garras. Y junto a ellas, las huellas de unos pies descalzos, pequeños, de mujer. Las dos se metían juntas al agua.",
  S("prints_mud", cam=((0.4, 0.55, 1.1), (0.6, 0.55, 1.35), "linear"), fx=[FOGL], grade="cold"),
  sfx=[X("whisper", 3.0, -18, dur=4)])
B("Al muchacho lo hallaron horas después, en la orilla, temblando, con los ojos abiertos. Vivo. Pero nunca más volvió a hablar. Solo señalaba el agua.",
  S("fisher_mute", cam=((0.5, 0.42, 1.15), (0.5, 0.42, 1.35), "in"), fx=[FOGL], grade="cold"),
  sfx=[X("whisper", 2.0, -18, dur=4)])
B("Y dicen que ese año, en la costa de los chontales, no cayó ni una gota de lluvia.",
  S("drought", cam=((0.5, 0.5, 1.1), (0.5, 0.45, 1.3), "in"), fx=["dust"], grade="warm"),
  amb=DRY, pause=0.9)

# ======================================================================== V
B("Hasta aquí, la leyenda. Ahora, lo que sí es historia.",
  S("church_huamelula", cam=((0.5, 0.5, 1.05), (0.5, 0.48, 1.2), "in"), fx=["dust"], tr="fade", tl=1.0, grade="warm",
    text=[T("CAPÍTULO V|Lo que dice la historia", "chapter", 0.6, 5.0)]),
  music="calm", amb=TOWN)
B("Ese pueblo existe. Se llama San Pedro Huamelula. Es un pueblo chontal de la costa de Oaxaca, en el Istmo de Tehuantepec, no muy lejos del mar.",
  S("map_isthmus", cam=((0.5, 0.5, 1.1), (0.62, 0.6, 1.5), "in"), fx=["dust"], grade="sepia",
    text=[T("San Pedro Huamelula|Oaxaca, Istmo de Tehuantepec", "date", 1.0, 6.0)]))
B("Sus vecinos huaves, los ikoots, viven todavía junto a las grandes lagunas del Istmo, como pescadores, igual que en la leyenda.",
  S("huave_village", cam=((0.5, 0.55, 1.1), (0.5, 0.55, 1.3), "in"), fx=[FOGL], grade="moon"))
B("Y cada año, al terminar las fiestas de San Pedro Apóstol, el presidente municipal se casa con una lagarta de verdad. Un caimán hembra pequeño, al que llaman la princesa.",
  S("church_fiesta", cam=((0.45, 0.5, 1.05), (0.55, 0.5, 1.2), "linear"), fx=["dust"], grade="warm"),
  S("caiman_bride", cam=((0.5, 0.45, 1.15), (0.5, 0.42, 1.35), "in"), fx=["dust"], grade="warm", tr="xfade", tl=0.6),
  amb=["city"], sfx=[X("bell", 1.0, -14, freq=180)])
B("Una madrina la viste con trajes tradicionales y, al final, con vestido blanco de novia. Le amarran el hocico con cuidado, para que nadie salga herido, y la llevan en procesión de casa en casa.",
  S("procession", cam=((0.4, 0.5, 1.05), (0.6, 0.5, 1.2), "linear"), fx=["dust"], grade="warm"),
  S("bride_close", cam=((0.5, 0.5, 1.15), (0.5, 0.48, 1.35), "in"), fx=["dust"], grade="warm", tr="xfade", tl=0.6),
  music="hope")
B("Hay música, flores y baile. El presidente municipal baila con la novia en brazos. Y al final, delante de todo el pueblo… le da un beso.",
  S("dance_mayor", cam=((0.5, 0.5, 1.05), (0.5, 0.48, 1.25), "in"), fx=["dust"], grade="warm"),
  S("kiss_today", cam=((0.5, 0.5, 1.15), (0.5, 0.5, 1.35), "in"), fx=["dust"], grade="warm", tr="xfade", tl=0.6))
B("Es una fiesta alegre, de tres días, llena de color. Y aun así, si te fijas, hay un momento en que la música baja y todo el pueblo guarda silencio, mirando a la novia.",
  S("procession", cam=((0.6, 0.5, 1.2), (0.45, 0.5, 1.35), "linear"), fx=["dust"], grade="warm"))
B("En el pueblo dicen que la tradición tiene más de doscientos treinta años, aunque sus raíces seguramente son mucho más antiguas que eso. Hoy se mezcla con la fiesta católica del santo patrono.",
  S("church_night", cam=((0.5, 0.5, 1.05), (0.5, 0.45, 1.25), "in"), fx=["fireflies"]),
  music="calm")
B("Y su sentido es el mismo que en la leyenda. Es una ofrenda. Se le pide a la Madre Tierra y al Creador que haya lluvia, buena cosecha y buena pesca. Y se celebra la unión de dos pueblos, chontales y huaves.",
  S("copal_altar", COPAL, CAND, cam=((0.5, 0.55, 1.1), (0.5, 0.5, 1.3), "in"), fx=["dust"], grade="candle"),
  S("two_peoples", FIREG, cam=((0.5, 0.55, 1.1), (0.5, 0.5, 1.25), "in"), fx=["embers"], grade="candle", tr="xfade", tl=0.6))

# ======================================================================== ENDING
B("Para mucha gente de fuera parece una curiosidad, algo raro para salir en las noticias. Para Huamelula es otra cosa. Es su manera de cumplir, cada año, la promesa que hizo un rey en la orilla de una laguna.",
  S("church_fiesta", cam=((0.55, 0.5, 1.15), (0.45, 0.5, 1.3), "linear"), fx=["dust"], grade="warm"))
B("Y ahora sí, la respuesta a la pregunta del principio. ¿Qué pasaría si un año no hubiera boda?",
  S("lagoon_night", FOGLAY, cam=((0.5, 0.5, 1.05), (0.5, 0.5, 1.25), "in"), fx=[FOGL], tr="fade", tl=1.0),
  music="dread", amb=LAGOON)
B("La verdad es que nadie lo sabe. Porque en San Pedro Huamelula nadie ha querido averiguarlo. Ni los abuelos, ni los pescadores, ni el presidente municipal en turno.",
  S("elder_portrait", FIREG, cam=((0.5, 0.42, 1.15), (0.5, 0.42, 1.35), "in"), fx=[{"type": "flicker", "amp": 0.08}], grade="candle"),
  S("fisher_mute", cam=((0.5, 0.42, 1.2), (0.5, 0.42, 1.35), "in"), fx=[FOGL], grade="cold", tr="xfade", tl=0.6))
B("Porque los viejos todavía recuerdan lo que les contaron sus abuelos. El año del pescador. El año en que no llovió.",
  S("cracked_earth", cam=((0.5, 0.5, 1.15), (0.5, 0.55, 1.35), "in"), fx=["dust"], grade="warm"))
B("Y si alguna noche, en una laguna de Oaxaca, ves dos ojos dorados que te miran desde el agua… no te rías. No le faltes al respeto. Puede que sea una novia… esperando a que cumplas tu promesa.",
  S("lagoon_eyes", EYES, cam=((0.5, 0.5, 1.15), (0.5, 0.5, 1.45), "in"), fx=[FOGL]),
  S("princess_eyes", cam=((0.5, 0.42, 1.25), (0.5, 0.4, 1.45), "in"), fx=[FOGL], grade="moon", tr="xfade", tl=0.8),
  sfx=[X("heartbeat", 1.0, -14, dur=8, bpm=66)])
B("¿Tú te casarías con la lagarta para salvar a tu pueblo? Te leo en los comentarios.",
  S("caiman_bride", cam=((0.5, 0.5, 1.1), (0.5, 0.45, 1.25), "in"), fx=["dust"], grade="warm",
    text=[T("¿Te casarías con la lagarta?|", "quote", 1.0, 6.0, pos="center")]), music="mystery", pause=0.8)
B("En el próximo video viajamos por los caminos de México para conocer a un jinete que cabalga de noche… sin cabeza. La leyenda del Jinete sin Cabeza.",
  S("rider_road", cam=((0.5, 0.5, 1.05), (0.5, 0.45, 1.3), "in"), fx=[FOGL], grade="night",
    text=[T("PRÓXIMO VIDEO|El Jinete sin Cabeza", "big", 2.0, 7.0)]), amb=["wind", "crickets"], sfx=[X("hooves", 1.0, -12, dur=5, distance=0.6)])
B("Hasta la próxima leyenda. Y recuerda… en la laguna, alguien todavía espera a su novio.",
  S("lagoon_night", SWIM, cam=((0.5, 0.5, 1.15), (0.5, 0.45, 1.4), "in"), fx=[FOGL], out=2.0),
  pause=1.0, music="dread", amb=LAGOON)
VARIANTS = {"lagoon_night": ["lagoon_night", "lagoon_night2", "lagoon_night3"], "caiman_close": ["caiman_close", "caiman_close2"]}
_cnt = {}
for b in BEATS:
    for sc in b["scenes"]:
        n = sc["layers"][0]["src"][4:-4]
        if n in VARIANTS:
            k = _cnt.get(n, 0); _cnt[n] = k + 1
            sc["layers"][0]["src"] = f"art/{VARIANTS[n][k % len(VARIANTS[n])]}.png"

# timeline-aware pass: split long shots, resolve sfx relative to a scene
TL = os.path.join(HERE, "audio", "timeline.json")
MAXSHOT = 9.9
if os.path.exists(TL):
    tl = json.load(open(TL)); tb = tl["beats"]
    for i, b in enumerate(BEATS):
        if i >= len(tb): break
        end = tb[i + 1]["start"] if i + 1 < len(tb) else tl["duration"] + 5.0
        d = end - tb[i]["start"]; sc = b["scenes"]
        fixed = sum(s.get("dur", 0) for s in sc); wsum = sum(s.get("weight", 1) for s in sc if "dur" not in s) or 1
        # split
        new = []; idxmap = []
        for j, s in enumerate(sc):
            sd = s["dur"] if "dur" in s else max(0, d - fixed) * s.get("weight", 1) / wsum
            k = max(1, math.ceil(sd / MAXSHOT)) if "dur" not in s else 1
            idxmap.append(len(new))
            if k == 1: new.append(s); continue
            cam = s.get("cam", {"from": [0.5, 0.5, 1.05], "to": [0.5, 0.5, 1.25], "ease": "inout"})
            f, t = cam["from"], cam["to"]
            for m in range(k):
                c = json.loads(json.dumps(s))
                c["weight"] = s.get("weight", 1) / k
                if m > 0:
                    c.pop("text", None); c["transition"] = "xfade"; c["transition_len"] = 0.7
                    c.pop("fx", None) if False else None
                    z = max(f[2], t[2]) + 0.12 * m
                    dx = 0.08 if m % 2 else -0.08
                    c["cam"] = {"from": [min(0.75, max(0.25, t[0] + dx)), t[1], min(1.8, z)],
                                "to": [min(0.75, max(0.25, t[0] - dx)), t[1] - 0.02, min(1.85, z + 0.12)], "ease": "inout"}
                if m < k - 1: c.pop("out", None); c.pop("out_len", None)
                new.append(c)
        b["scenes"] = new
        sc = new
        fixed = sum(s.get("dur", 0) for s in sc); wsum = sum(s.get("weight", 1) for s in sc if "dur" not in s) or 1
        offs = []; t = 0.0
        for s in sc:
            offs.append(t); t += s["dur"] if "dur" in s else max(0, d - fixed) * s.get("weight", 1) / wsum
        for c in b.get("sfx", []):
            if "scene" in c:
                c["at"] = round(offs[idxmap[c["scene"]]] + c["at"], 3); del c["scene"]

story = {"title": "El Hombre Caimán", "voice": "em_alex", "speed": 0.88,
         "sentence_gap": 0.28, "key": "E", "seed": 147, "grade": "night", "vignette": 0.58, "outro": 5.0,
         "music_gain": -15, "amb_gain": -21, "sfx_gain": -9, "beats": BEATS}
json.dump(story, open(os.path.join(HERE, "story.json"), "w"), ensure_ascii=False, indent=1)

words = 0; out = ["# El Hombre Caimán — guion\n",
                  "Narración en español (narrador: em_alex; voces de personajes: em_santa; la princesa: ef_dora).\n"]
WHO = {"ef_dora": "PRINCESA: ", "em_santa": "VOZ: "}
for b in BEATS:
    for sc in b["scenes"]:
        for t in sc.get("text", []):
            if t["style"] in ("chapter", "title"): out.append(f"\n## {t['str'].replace('|', ' — ').rstrip(' —')}\n")
    if b["text"]:
        out.append(WHO.get(b.get("voice"), "") + b["text"]); words += len(b["text"].split())
open(os.path.join(HERE, "script.md"), "w").write("\n\n".join(out) + "\n")
arts = sorted({l["src"] for b in BEATS for sc in b["scenes"] for l in sc["layers"]})
print(f"beats {len(BEATS)}  scenes {sum(len(b['scenes']) for b in BEATS)}  words {words}  art {len(arts)}")
print(" ".join(a[4:-4] for a in arts))
