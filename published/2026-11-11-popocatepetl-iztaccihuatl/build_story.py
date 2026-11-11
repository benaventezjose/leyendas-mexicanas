#!/usr/bin/env python3
"""Builds story.json and script.md for 'Popocatépetl e Iztaccíhuatl'. Edit BEATS here, then run."""
import json, os
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
    if pos: d["pos"] = pos
    return d

def X(name, at=0.0, gain=-6, **args):
    d = {"name": name, "at": at, "gain": gain}
    if args: d["args"] = args
    return d

FOG = {"type": "fog", "strength": 0.35}
FOGL = {"type": "fog", "strength": 0.45, "low": True}
SNOWFOG = {"type": "fog", "strength": 0.4, "color": [210, 222, 235]}
FL = {"type": "flicker", "amp": 0.07}
SNOW = {"type": "rain", "strength": 0.18}
def SH(a, b, amp=7): return {"type": "shake", "amp": amp, "at": [a, b]}
FLOAT = lambda amp=0.006, p=6: [{"type": "float", "amp": amp, "period": p}]
CLOUDS = L("l_clouds", anim=[{"type": "drift", "dx": -0.05}], opacity=[0.85, 0.85])
SMOKE = L("l_smoke", blend="screen", anim=[{"type": "drift", "dx": 0.03, "dy": -0.02}, {"type": "sway", "deg": 1.5, "period": 9, "pivot": [0.5, 1.0]}])
SNOWL = L("l_snowfall", blend="screen", anim=[{"type": "drift", "dx": -0.03, "dy": 0.06, "ease": "linear"}])
TORCH = L("l_torch_glow", blend="screen", anim=[{"type": "flicker", "amp": 0.22, "speed": 2.2}])

N = 0
BEATS = []
def B(text, *scenes, **kw):
    global N; N += 1
    b = {"id": f"b{N:03d}", "text": text}; b.update(kw); b["scenes"] = list(scenes)
    BEATS.append(b)

IZ = dict(voice="ef_dora", speed=0.86)
PO = dict(voice="em_santa", speed=0.86)
FA = dict(voice="em_santa", speed=0.8)

# ======================================================================== COLD OPEN
B("La nieve le llega a las rodillas. El viento le corta la cara como un filo de obsidiana. Y aun así, el guerrero sigue subiendo.",
  S("snow_slope", L("l_popo_carry", depth=1.05, anim=[{"type": "drift", "dx": 0.025, "dy": -0.02}]), SNOWL,
    cam=((0.42, 0.62, 1.35), (0.5, 0.52, 1.15)), fx=[SNOWFOG, SNOW], grade="cold", tr="fade", tl=1.2),
  pre=0.8, music="dread", amb=["wind", {"name": "night", "gain": -12}], sfx=[X("gust", 0.5, -6), X("footsteps", 2.0, -14, dur=6)])
B("En los brazos lleva a una mujer vestida de blanco. No se mueve. No respira.",
  S("carry_close", SNOWL, cam=((0.5, 0.45, 1.1), (0.5, 0.5, 1.4), "in"), fx=[SNOWFOG], grade="cold"),
  sfx=[X("heartbeat", 0.5, -12, dur=5, bpm=58)])
B("Cuando llega a la cima, la recuesta sobre un lecho de flores, enciende una antorcha… y se arrodilla junto a ella.",
  S("summit_kneel", TORCH, SNOWL, cam=((0.5, 0.45, 1.0), (0.52, 0.55, 1.3)), fx=[SNOWFOG, "embers"], w=1.3),
  S("torch_close", cam=((0.5, 0.5, 1.2), (0.5, 0.45, 1.45)), fx=["embers", FL], grade="candle", tr="xfade", tl=0.5),
  sfx=[X("fire", 4.0, -10)])
B("Han pasado más de quinientos años. Y cuentan que él… todavía no se ha levantado.",
  S("popo_face_snow", tr="flash", tl=0.3, cam=((0.5, 0.42, 1.3), (0.5, 0.42, 1.5), "linear"), fx=[SNOWFOG, SH(0, 0.6, 8)], grade="cold"),
  pause=0.8, sfx=[X("sting", 0.0, -3), X("boom", 0.0, -5)])
B("Al oriente de la Ciudad de México hay una montaña que nunca deja de echar humo. Y junto a ella, una mujer de nieve que duerme.",
  S("volcanoes_night", SMOKE, CLOUDS, cam=((0.5, 0.55, 1.2), (0.5, 0.5, 1.0)), fx=[FOGL],
    text=[T("POPOCATÉPETL E IZTACCÍHUATL|la leyenda de los volcanes", "title", 3.0, 8.5)], w=1.4),
  music="mystery")
B("Al final te voy a contar lo que, según los abuelos, pasará el día que ese humo se apague.",
  S("izta_ghost_cloud", cam=((0.5, 0.5, 1.1), (0.5, 0.45, 1.35), "in"), fx=[FOG], grade="cold", out=1.0),
  pause=0.5, sfx=[X("whisper", 0.8, -14, dur=3), X("boom", 4.0, -7)])

# ======================================================================== CAP I
B("",
  S("valley_dawn", CLOUDS, cam=((0.5, 0.55, 1.0), (0.5, 0.5, 1.12)), fx=[FOGL],
    text=[T("CAPÍTULO I|La hija del señor de Tlaxcala", "chapter", 0.6, 5.0)], tr="fade", tl=1.0),
  pause=5.6, music="calm", amb=["wind", {"name": "crickets", "gain": -8}], sfx=[X("bell", 0.4, -12, freq=120)])
B("Hace más de quinientos años, antes de que llegaran los españoles, el valle de México tenía otro dueño.",
  S("tenochtitlan", cam=((0.4, 0.55, 1.2), (0.55, 0.5, 1.05)), fx=[FOGL, "dust"],
    text=[T("Valle de México|antes de mil quinientos diecinueve", "date", 0.5, 5.0)]))
B("En medio de un lago se levantaba Tenochtitlan, la gran ciudad de los mexicas. Sus guerreros eran temidos de un mar al otro, sus templos brillaban sobre el agua, y casi todos los pueblos le pagaban tributo: maíz, cacao, mantas de algodón, plumas preciosas.",
  S("tenochtitlan", cam=((0.6, 0.5, 1.35), (0.45, 0.55, 1.2), "linear"), fx=[FOGL, "dust"]),
  S("tribute_line", cam=((0.3, 0.55, 1.15), (0.6, 0.55, 1.2), "linear"), fx=["dust"], grade="warm", tr="xfade", tl=0.6, w=1.2))
B("Pero al otro lado de los volcanes, en unas tierras de cerros y barrancas, vivía un pueblo que no quería arrodillarse: Tlaxcala. Los mexicas lo tenían rodeado. No le dejaban pasar sal, ni algodón, ni cacao. Y aun así, los tlaxcaltecas preferían comer sin sal… antes que inclinar la cabeza.",
  S("tlaxcala_city", L("l_torches_city", blend="screen", anim=[{"type": "flicker", "amp": 0.12, "speed": 1.2}]),
    cam=((0.5, 0.6, 1.1), (0.5, 0.5, 1.3)), fx=[FOGL, "embers"],
    text=[T("TLAXCALA|el pueblo que no se arrodilló", "big", 4.0, 8.0)], w=1.1),
  S("codex_paper", cam=((0.5, 0.5, 1.05), (0.6, 0.5, 1.3), "linear"), fx=["dust"], grade="sepia", tr="xfade", tl=0.6),
  S("tlaxcala_city", cam=((0.35, 0.65, 1.45), (0.45, 0.6, 1.6)), fx=[FOGL, "embers"], tr="xfade", tl=0.6))
B("Imagina el humo del copal subiendo de los templos, el olor a tortilla en el comal, y en el horizonte, siempre, las dos montañas nevadas vigilando.",
  S("tlaxcala_city", cam=((0.3, 0.6, 1.4), (0.6, 0.45, 1.3)), fx=[FOGL, "embers"], w=1.2),
  S("copal_temple", cam=((0.5, 0.6, 1.1), (0.5, 0.45, 1.3)), fx=["embers", FOG], grade="warm", tr="xfade", tl=0.6))
B("Solo que en esta historia, todavía no eran montañas.",
  S("volcanoes_dawn", cam=((0.5, 0.5, 1.05), (0.5, 0.45, 1.25), "in"), fx=[FOGL]), pause=0.8,
  sfx=[X("riser", -1.0, -10, dur=2)])
B("El señor de Tlaxcala tenía una hija. Se llamaba Iztaccíhuatl.",
  S("izta_portrait", cam=((0.5, 0.45, 1.05), (0.5, 0.4, 1.3)), fx=["embers", FL], tr="xfade", tl=0.6, w=1.3,
    text=[T("IZTACCÍHUATL|mujer blanca", "big", 0.6, 4.6)]))
B("Su nombre, en náhuatl, quiere decir mujer blanca. Cuentan que su piel parecía de luna, que su cabello negro le llegaba a la cintura, y que cuando caminaba por el mercado, hasta los vendedores se callaban.",
  S("izta_portrait", cam=((0.5, 0.4, 1.35), (0.48, 0.45, 1.15)), fx=["embers"], grade="candle"),
  S("market", L("l_izta_walk", depth=1.05, anim=[{"type": "drift", "dx": 0.05}]), cam=((0.4, 0.55, 1.2), (0.55, 0.55, 1.3), "linear"),
    fx=["dust"], grade="warm", tr="xfade", tl=0.6, w=1.2))
B("Muchos príncipes vinieron a pedir su mano. Traían jade, mantas bordadas, plumas de quetzal. A todos los rechazó, uno por uno. Porque su corazón ya tenía dueño.",
  S("palace_hall", L("l_suitors", depth=1.04), cam=((0.5, 0.55, 1.1), (0.5, 0.55, 1.25)), fx=[FL, "embers"], grade="candle"),
  S("izta_moon", cam=((0.5, 0.45, 1.1), (0.5, 0.42, 1.3)), fx=[FOG, "fireflies"], tr="xfade", tl=0.6))
B("Era un guerrero joven, de los más valientes de Tlaxcala. Su nombre era Popocatépetl.",
  S("popo_portrait", cam=((0.5, 0.45, 1.05), (0.5, 0.4, 1.3)), fx=["embers", FL], grade="candle",
    text=[T("POPOCATÉPETL|el cerro que humea", "big", 2.0, 6.0)]))
B("Se veían a escondidas, de noche, junto al agua, bajo un ahuehuete viejo. Él le hablaba de batallas, de los caminos que había recorrido, de los cerros donde la tierra echaba fuego. Ella le hablaba de las estrellas, y le enseñaba a reconocerlas en el reflejo del agua. Nadie más lo sabía. Y nadie más debía saberlo.",
  S("lovers_tree", L("l_lovers", depth=1.05, anim=FLOAT(0.003, 7)), cam=((0.35, 0.55, 1.05), (0.45, 0.6, 1.25)), fx=["fireflies", FOGL]),
  S("lovers_tree", L("l_lovers", depth=1.05, anim=FLOAT(0.003, 7)), cam=((0.47, 0.8, 1.6), (0.47, 0.78, 1.8), "linear"), fx=["fireflies", FOGL], tr="xfade", tl=0.6),
  S("stars_water", cam=((0.5, 0.4, 1.0), (0.5, 0.5, 1.2)), fx=["fireflies"], tr="xfade", tl=0.8),
  amb=["crickets", {"name": "river", "gain": -6}])
B("Y una noche, ella le dijo algo que él nunca iba a olvidar.",
  S("izta_moon", cam=((0.5, 0.42, 1.2), (0.5, 0.42, 1.45), "in"), fx=["fireflies"]), music="sad")
B("Si un día no vuelves… yo tampoco voy a querer seguir aquí.",
  S("izta_moon", cam=((0.5, 0.4, 1.45), (0.5, 0.4, 1.6), "linear"), fx=["fireflies"], text=[T("Si un día no vuelves…|Iztaccíhuatl", "quote", 0.2, 4.2)]),
  pause=0.9, **IZ)

# ======================================================================== CAP II
B("",
  S("war_drums", cam=((0.5, 0.55, 1.0), (0.5, 0.5, 1.12)), fx=["embers", FOGL],
    text=[T("CAPÍTULO II|La promesa", "chapter", 0.6, 5.0)], tr="fade", tl=1.0, grade="blood"),
  pause=5.6, music="tension", amb=["wind"], sfx=[X("boom", 0.6, -6), X("boom", 1.6, -8), X("boom", 2.4, -6)])
B("Un día llegaron los mensajeros. La guerra había empezado. Los enemigos de Tlaxcala avanzaban, y el señor necesitaba a sus mejores guerreros.",
  S("runner_maguey", L("l_runner", depth=1.08, anim=[{"type": "drift", "dx": 0.12, "ease": "linear"}]), cam=((0.35, 0.55, 1.2), (0.6, 0.55, 1.2), "linear"),
    fx=[FOGL, "dust"]),
  S("palace_hall", L("l_brazier", blend="screen", anim=[{"type": "flicker", "amp": 0.18, "speed": 1.6}]), L("l_kneeling_warriors", depth=1.04),
    cam=((0.5, 0.55, 1.15), (0.5, 0.5, 1.3)), fx=["embers", FL], grade="candle", tr="xfade", tl=0.6),
  sfx=[X("footsteps", 0.2, -10, dur=4)])
B("Popocatépetl se presentó ante él, se arrodilló… y le pidió la mano de su hija.",
  S("popo_kneel_hall", L("l_brazier", blend="screen", anim=[{"type": "flicker", "amp": 0.18, "speed": 1.6}]),
    cam=((0.5, 0.55, 1.05), (0.55, 0.5, 1.3)), fx=["embers", FL], grade="candle"))
B("El señor de Tlaxcala lo miró largo rato. Y luego le habló.",
  S("father_portrait", cam=((0.5, 0.45, 1.1), (0.5, 0.42, 1.35), "in"), fx=["embers", FL], grade="candle"))
B("Ve a la guerra. Si regresas vencedor, mi hija será tu esposa. Si no regresas… nadie volverá a pronunciar tu nombre.",
  S("father_portrait", cam=((0.5, 0.42, 1.35), (0.5, 0.42, 1.5), "linear"), fx=["embers", FL], grade="candle",
    text=[T("Si regresas vencedor…|el señor de Tlaxcala", "quote", 0.2, 4.4)], w=1.3),
  S("popo_kneel_hall", L("l_brazier", blend="screen"), cam=((0.5, 0.75, 1.5), (0.5, 0.7, 1.7), "in"), fx=["embers", FL], grade="candle", tr="xfade", tl=0.5),
  pause=0.8, **FA)
B("Esa noche, Iztaccíhuatl le ató al brazo una cinta tejida por ella misma. Y él le hizo una promesa.",
  S("izta_moon", cam=((0.5, 0.45, 1.2), (0.5, 0.5, 1.05)), fx=["fireflies", FOG]),
  S("hands_ribbon", cam=((0.5, 0.5, 1.1), (0.5, 0.5, 1.4)), fx=["fireflies"], tr="xfade", tl=0.6), music="sad")
B("Voy a volver. Te lo juro por el sol.",
  S("popo_portrait", cam=((0.5, 0.42, 1.3), (0.5, 0.42, 1.5), "linear"), fx=["embers"], grade="candle",
    text=[T("Voy a volver|Popocatépetl", "quote", 0.2, 3.6)]), pause=0.8, **PO)
B("Al amanecer, el ejército salió de Tlaxcala. Tambores, caracolas, escudos de plumas brillando bajo el sol, y cientos de guerreros con el cuerpo pintado para la guerra. Ella lo miró desde lo alto del templo hasta que fue un punto en el horizonte. Y se quedó ahí, con el viento en la cara, mucho después de que el polvo del camino se asentara.",
  S("army_depart", cam=((0.3, 0.6, 1.25), (0.6, 0.55, 1.1)), fx=["dust", FOGL], grade="warm"),
  S("army_depart", cam=((0.7, 0.75, 1.7), (0.55, 0.75, 1.7), "linear"), fx=["dust"], grade="warm", tr="xfade", tl=0.5),
  S("izta_temple_top", cam=((0.5, 0.5, 1.05), (0.5, 0.42, 1.3)), fx=[FOGL], grade="warm", tr="xfade", tl=0.8),
  music="hope", sfx=[X("boom", 0.3, -10), X("boom", 1.3, -12)])
B("Lo que ninguno de los dos sabía es que entre los guerreros iba alguien que también quería a Iztaccíhuatl. Y que no pensaba perderla.",
  S("rival_portrait", tr="flash", tl=0.3, cam=((0.5, 0.45, 1.15), (0.5, 0.42, 1.4), "in"), fx=["embers", FL], grade="blood"),
  music="dread", pause=0.8, sfx=[X("sting", 0.0, -3)])
B("Si te gusta este tipo de historias, suscríbete. Aquí cada semana contamos una leyenda de México, como nos la contaron los abuelos.",
  S("valley_dawn", CLOUDS, cam=((0.5, 0.5, 1.0), (0.5, 0.48, 1.15)), fx=[FOGL]), music="mystery")

# ======================================================================== CAP III
B("",
  S("battle_sky", cam=((0.5, 0.55, 1.0), (0.5, 0.5, 1.12)), fx=["ash", "embers"],
    text=[T("CAPÍTULO III|La mentira", "chapter", 0.6, 5.0)], tr="fade", tl=1.0, grade="blood"),
  pause=5.6, music="climax", amb=["wind", {"name": "fire", "gain": -6}], sfx=[X("boom", 0.5, -4)])
B("La guerra duró meses. Lunas enteras de lluvia, de hambre, de flechas que silbaban en la noche. Muchos guerreros no volvieron. Y en Tlaxcala, cada vez que llegaba un mensajero, Iztaccíhuatl corría a la puerta del palacio, con el corazón en la garganta.",
  S("battle_sky", L("l_battle", depth=1.06), cam=((0.35, 0.55, 1.2), (0.6, 0.5, 1.15), "linear"), fx=["ash", "embers", {"type": "lightning", "at": [2.5]}], grade="blood"),
  S("camp_night", cam=((0.3, 0.65, 1.3), (0.4, 0.6, 1.45)), fx=[FOGL, "embers"], tr="xfade", tl=0.6),
  S("palace_hall", cam=((0.5, 0.5, 1.1), (0.5, 0.55, 1.25)), fx=["embers", FL], grade="candle", tr="xfade", tl=0.6),
  sfx=[X("whoosh", 1.0, -8), X("whoosh", 2.8, -9), X("thunder", 2.5, -6)])
B("Y en medio de la batalla, Popocatépetl peleaba como si cada golpe lo acercara a ella.",
  S("popo_battle", cam=((0.5, 0.5, 1.1), (0.5, 0.45, 1.35)), fx=["ash", "embers", SH(1.5, 2.2, 6)], grade="blood"),
  sfx=[X("boom", 1.5, -5)])
B("Pero una noche, el otro guerrero, el que la quería para él, se escapó del campamento.",
  S("camp_night", L("l_rival_sneak", depth=1.06, anim=[{"type": "drift", "dx": -0.06}]), cam=((0.55, 0.55, 1.2), (0.4, 0.55, 1.25), "linear"),
    fx=[FOGL, "embers"]), music="dread")
B("Corrió días enteros, por barrancas y campos de magueyes, hasta llegar a Tlaxcala. Llegó con los pies sangrando y la cara cubierta de polvo.",
  S("runner_maguey", L("l_rival_run", depth=1.08, anim=[{"type": "drift", "dx": 0.14, "ease": "linear"}]), cam=((0.3, 0.55, 1.2), (0.6, 0.55, 1.2), "linear"),
    fx=[FOGL, "dust"], grade="cold"),
  sfx=[X("footsteps", 0.0, -8, dur=6)])
B("Y frente al señor de Tlaxcala, frente a Iztaccíhuatl, dijo las palabras que lo cambiaron todo.",
  S("palace_hall", L("l_brazier", blend="screen", anim=[{"type": "flicker", "amp": 0.18, "speed": 1.6}]), L("l_rival_kneel", depth=1.04),
    cam=((0.5, 0.55, 1.05), (0.5, 0.55, 1.3), "in"), fx=["embers", FL], grade="candle"),
  sfx=[X("heartbeat", 0.0, -9, dur=6, bpm=80)])
B("Popocatépetl ha muerto. Lo vi caer.",
  S("rival_portrait", tr="flash", tl=0.25, cam=((0.5, 0.42, 1.35), (0.5, 0.42, 1.55), "linear"), fx=[FL, SH(0, 0.6, 9)], grade="blood",
    text=[T("Popocatépetl ha muerto|el otro guerrero", "quote", 0.2, 3.4)]),
  pause=1.0, sfx=[X("sting", 0.0, -1), X("boom", 0.0, -4)], **PO)
B("Era mentira. Popocatépetl seguía vivo, y seguía peleando a muchas jornadas de ahí. Pero ella no tenía forma de saberlo. Y el traidor la miraba, esperando que ahora, por fin, ella lo mirara a él.",
  S("izta_shock", cam=((0.5, 0.45, 1.15), (0.5, 0.42, 1.4), "in"), fx=[FL], grade="cold"),
  S("popo_battle", cam=((0.48, 0.45, 1.3), (0.5, 0.5, 1.15)), fx=["ash", "embers"], grade="blood", tr="xfade", tl=0.5, w=0.8),
  S("rival_portrait", cam=((0.5, 0.42, 1.2), (0.52, 0.4, 1.4)), fx=[FL], grade="blood", tr="xfade", tl=0.5), music="sad")
B("Cuentan que no gritó. Que no lloró delante de nadie. Solo se quitó las flores del cabello… y se fue a su habitación.",
  S("izta_grief", L("l_candles", blend="screen", anim=[{"type": "flicker", "amp": 0.2, "speed": 2.0}]), cam=((0.5, 0.55, 1.1), (0.5, 0.5, 1.3)), fx=[FL, "dust"], grade="candle", w=1.2),
  S("flowers_floor", cam=((0.5, 0.5, 1.2), (0.5, 0.55, 1.4)), fx=["dust"], grade="candle", tr="xfade", tl=0.6))
B("Dejó de comer. Dejó de hablar. Pasaba las noches sentada junto a la ventana, mirando el camino por donde él se había ido. Cuentan que la oían murmurar su nombre, despacito, como quien reza. Y que su piel, que siempre había sido clara, se fue poniendo blanca. Blanca como la nieve.",
  S("izta_window", cam=((0.5, 0.5, 1.05), (0.55, 0.45, 1.25)), fx=[FOG, FL], grade="cold"),
  S("izta_pale", cam=((0.45, 0.45, 1.1), (0.45, 0.4, 1.35)), fx=[FOG], grade="cold", tr="xfade", tl=0.8, w=1.2))
B("Los curanderos quemaron copal y hierbas. Los sacerdotes rezaron a los dioses. Nada sirvió.",
  S("copal_temple", cam=((0.5, 0.55, 1.2), (0.5, 0.45, 1.05)), fx=["embers", FOG], grade="candle"),
  amb=["fire", {"name": "wind", "gain": -8}], sfx=[X("whisper", 0.5, -16, dur=5)])
B("Una mañana, la encontraron dormida sobre su petate, con las manos sobre el pecho. Ya no despertó. Cuentan que murió de tristeza.",
  S("izta_bed", cam=((0.5, 0.45, 1.0), (0.5, 0.5, 1.3), "in"), fx=["dust", FOG], grade="cold", w=1.3),
  pause=1.2, sfx=[X("bell", 2.0, -10, freq=90)])

# ======================================================================== CAP IV
B("",
  S("return_gate", cam=((0.5, 0.55, 1.0), (0.5, 0.5, 1.12)), fx=["dust", FOGL],
    text=[T("CAPÍTULO IV|El regreso", "chapter", 0.6, 5.0)], tr="fade", tl=1.0, grade="warm"),
  pause=5.6, music="hope", amb=["wind"], sfx=[X("boom", 0.8, -10), X("boom", 1.8, -10)])
B("Semanas después, los tambores sonaron otra vez en el camino. El ejército de Tlaxcala volvía. Y al frente, vivo, cubierto de cicatrices, venía Popocatépetl.",
  S("army_return", cam=((0.6, 0.55, 1.25), (0.45, 0.55, 1.1)), fx=["dust", FOGL], grade="warm", w=1.3),
  S("popo_portrait", cam=((0.5, 0.45, 1.05), (0.5, 0.42, 1.25)), fx=["dust"], grade="warm", tr="xfade", tl=0.6))
B("Había ganado la guerra. Traía en el brazo la cinta de ella, ya rota y descolorida.",
  S("hands_ribbon", cam=((0.5, 0.5, 1.3), (0.5, 0.5, 1.15)), fx=["dust"], grade="warm"))
B("Pero al entrar a la ciudad, algo estaba mal. Nadie cantaba. Nadie salió a recibirlo.",
  S("return_gate", L("l_crowd_silent", depth=1.04), cam=((0.5, 0.55, 1.1), (0.5, 0.55, 1.35), "in"), fx=["dust", FOGL], grade="cold"),
  music="dread", amb=["wind"], sfx=[X("gust", 0.5, -8)])
B("Y entonces la vio.",
  S("izta_bed", tr="flash", tl=0.3, cam=((0.5, 0.48, 1.3), (0.5, 0.48, 1.45), "linear"), fx=[SH(0, 0.5, 8)], grade="cold"),
  pause=1.0, sfx=[X("sting", 0.0, -2), X("boom", 0.0, -4)])
B("Dicen que su grito se escuchó hasta Tenochtitlan.",
  S("popo_grief", cam=((0.5, 0.45, 1.1), (0.5, 0.42, 1.45), "in"), fx=["embers", SH(0.3, 1.6, 6)], grade="blood",
    text=[T("SU GRITO|se escuchó hasta Tenochtitlan", "big", 0.8, 4.0)]),
  pause=0.8, sfx=[X("boom", 0.3, -3), X("gust", 0.5, -4)])
B("Cuando supo la verdad, buscó al que había mentido. Lo que pasó entre ellos nadie lo cuenta igual. Algunos abuelos ni siquiera quieren decirlo. Unos dicen que lo enfrentó y lo venció. Otros, que el traidor huyó hacia el oriente, lejos, hasta donde nadie volvió a verlo.",
  S("rival_flee", cam=((0.5, 0.5, 1.2), (0.65, 0.5, 1.05)), fx=["ash", FOG], grade="blood", w=1.3),
  S("citlaltepetl", cam=((0.5, 0.5, 1.05), (0.55, 0.45, 1.25)), fx=[FOGL, SNOW], grade="cold", tr="xfade", tl=0.8),
  music="tension", sfx=[X("thunder", 2.0, -8)])
B("Pero a Popocatépetl ya no le importaba la venganza. Solo quería una cosa: que ella descansara en un lugar digno de ella.",
  S("popo_grief", cam=((0.5, 0.42, 1.35), (0.5, 0.45, 1.15)), fx=["embers"], grade="night"), music="sad")
B("La levantó en brazos. Y caminó con ella hacia las montañas.",
  S("procession_valley", L("l_popo_carry_small", depth=1.05, anim=[{"type": "drift", "dx": 0.04, "dy": -0.01}]), CLOUDS,
    cam=((0.4, 0.55, 1.1), (0.55, 0.5, 1.2)), fx=[FOGL], w=1.2))
B("Caminó días y noches, sin comer, sin dormir. No dejó que nadie lo ayudara. Subió entre pinos, entre piedras, hasta donde los árboles ya no crecen y el aire casi no alcanza para respirar. Hasta donde empieza la nieve.",
  S("pines_climb", L("l_popo_carry_small", depth=1.05, anim=[{"type": "drift", "dx": 0.03, "dy": -0.02}]), cam=((0.4, 0.65, 1.2), (0.55, 0.45, 1.25)), fx=[FOGL, "dust"], w=1.2),
  S("snow_slope", L("l_popo_carry", depth=1.05, anim=[{"type": "drift", "dx": 0.02, "dy": -0.015}]), SNOWL,
    cam=((0.45, 0.6, 1.1), (0.5, 0.5, 1.3)), fx=[SNOWFOG, SNOW], grade="cold", tr="xfade", tl=0.8),
  amb=["wind"], sfx=[X("gust", 3.0, -6)])
B("Allá arriba hizo un lecho de flores, la recostó, y encendió una antorcha de ocote para que la luz la acompañara.",
  S("summit_kneel", TORCH, SNOWL, cam=((0.52, 0.55, 1.3), (0.5, 0.48, 1.1)), fx=[SNOWFOG, "embers"], w=1.2),
  S("torch_close", cam=((0.5, 0.45, 1.3), (0.5, 0.5, 1.15)), fx=["embers", FL], grade="candle", tr="xfade", tl=0.5),
  sfx=[X("fire", 2.0, -10)])
B("Y se arrodilló a su lado. Le tomó la mano, que ya estaba fría. Y se quedó ahí, mirándola, mientras la antorcha ardía. Y ya no se movió.",
  S("summit_kneel", TORCH, SNOWL, cam=((0.5, 0.55, 1.1), (0.5, 0.6, 1.4), "in"), fx=[SNOWFOG, "embers"]),
  S("torch_close", cam=((0.5, 0.35, 1.5), (0.5, 0.4, 1.3)), fx=["embers", FL, SNOW], grade="candle", tr="xfade", tl=0.6),
  pause=1.0, music="silence")
B("Dicen que los dioses, conmovidos, mandaron la nieve. Que la nieve los cubrió despacio, noche tras noche. Y que debajo de ese blanco, sus cuerpos fueron creciendo… hasta volverse montañas.",
  S("snow_cover", SNOWL, cam=((0.5, 0.55, 1.2), (0.5, 0.5, 1.0)), fx=[SNOWFOG, SNOW], grade="cold", w=1.2),
  S("transform", CLOUDS, cam=((0.5, 0.6, 1.25), (0.5, 0.5, 1.0)), fx=[FOGL, "fireflies"], tr="xfade", tl=1.2, w=1.4),
  music="hope", sfx=[X("riser", 2.0, -8, dur=6), X("boom", 8.0, -6)])
B("Cuando los tlaxcaltecas subieron a buscarlos, ya no encontraron a nadie. Solo dos montañas nuevas, blancas, donde antes no había nada. Ella quedó acostada, dormida para siempre. Él quedó a su lado, de rodillas, con la antorcha encendida. Y por eso, desde entonces, el Popocatépetl echa humo.",
  S("snow_cover", SNOWL, cam=((0.5, 0.5, 1.0), (0.6, 0.6, 1.15)), fx=[SNOWFOG], grade="cold"),
  S("volcanoes_night", SMOKE, CLOUDS, cam=((0.35, 0.55, 1.3), (0.6, 0.5, 1.2), "linear"), fx=[FOGL], w=1.2),
  S("popo_crater_smoke", SMOKE, cam=((0.5, 0.55, 1.1), (0.5, 0.45, 1.35)), fx=["embers", FOG], tr="xfade", tl=0.8))

# ======================================================================== CAP V
B("",
  S("volcanoes_dawn", CLOUDS, SMOKE, cam=((0.5, 0.55, 1.0), (0.5, 0.5, 1.12)), fx=[FOGL],
    text=[T("CAPÍTULO V|El guardián que humea", "chapter", 0.6, 5.0)], tr="fade", tl=1.0),
  pause=5.6, music="mystery", amb=["wind", {"name": "night", "gain": -10}])
B("Hasta aquí, la leyenda. Ahora, lo que sí podemos comprobar.",
  S("codex_paper", cam=((0.45, 0.5, 1.1), (0.55, 0.5, 1.25), "linear"), fx=["dust"], grade="sepia"))
B("Los dos volcanes existen, y llevan nombres en náhuatl. Popocatépetl significa el cerro que humea. Mide más de cinco mil trescientos metros y es la segunda montaña más alta de México.",
  S("volcanoes_dawn", SMOKE, cam=((0.35, 0.5, 1.3), (0.4, 0.45, 1.15)), fx=[FOGL],
    text=[T("POPOCATÉPETL|el cerro que humea", "caption", 1.0, 6.0, "bottom")]),
  S("popo_crater_smoke", SMOKE, cam=((0.5, 0.6, 1.0), (0.5, 0.5, 1.2)), fx=[FOG], tr="xfade", tl=0.6))
B("La Iztaccíhuatl es la tercera. Y si la miras desde la Ciudad de México o desde Puebla, vas a entender por qué le dicen la Mujer Dormida: se distingue la cabeza, el pecho, las rodillas y los pies. Los alpinistas todavía llaman así a cada parte de la montaña.",
  S("izta_sleeping", L("l_izta_outline", blend="screen", opacity=[0, 0.75], fade_in=2.5, appear_at=2.0), cam=((0.5, 0.5, 1.05), (0.5, 0.5, 1.2)), fx=[FOGL], w=1.4,
    text=[T("LA MUJER DORMIDA|cabeza · pecho · rodillas · pies", "big", 6.0, 10.5)]),
  S("izta_sleeping", L("l_izta_outline", blend="screen", opacity=[0.75, 0.75]), cam=((0.75, 0.45, 1.5), (0.55, 0.42, 1.5), "linear"), fx=[FOGL], tr="xfade", tl=0.6))
B("Tlaxcala también es real. Nunca fue conquistada por los mexicas: vivió rodeada por ellos durante generaciones, peleando las llamadas guerras floridas. Esa rivalidad es el fondo de la historia.",
  S("codex_paper", cam=((0.55, 0.5, 1.25), (0.45, 0.5, 1.1), "linear"), fx=["dust"], grade="sepia"),
  S("tlaxcala_city", cam=((0.5, 0.55, 1.05), (0.5, 0.5, 1.2)), fx=[FOGL, "embers"], tr="xfade", tl=0.6))
B("Y en mil quinientos diecinueve, Hernán Cortés cruzó entre los dos volcanes, por el paso que hoy lleva su nombre. Desde ahí, los españoles vieron por primera vez Tenochtitlan. Ese mismo año, uno de sus capitanes, Diego de Ordaz, subió hasta el cráter del Popocatépetl, que entonces también humeaba. Y los tlaxcaltecas, los del pueblo de la leyenda, se aliaron con Cortés contra sus viejos enemigos, los mexicas.",
  S("cortes_pass", cam=((0.4, 0.55, 1.2), (0.55, 0.5, 1.1)), fx=[FOGL, SNOW], grade="cold",
    text=[T("Paso de Cortés|mil quinientos diecinueve", "date", 0.8, 5.5)], w=1.2),
  S("tenochtitlan", cam=((0.5, 0.6, 1.3), (0.5, 0.55, 1.1)), fx=[FOGL], tr="xfade", tl=0.6),
  S("popo_crater_smoke", SMOKE, cam=((0.5, 0.4, 1.3), (0.5, 0.35, 1.5)), fx=[FOG, SNOW], grade="cold", tr="xfade", tl=0.6),
  S("army_depart", cam=((0.5, 0.6, 1.2), (0.4, 0.6, 1.3), "linear"), fx=["dust"], grade="warm", tr="xfade", tl=0.6), music="tension")
B("La leyenda tiene muchas versiones. En algunas, ella es hija de un señor mexica, y él, un guerrero tlaxcalteca. En otras, el mentiroso se convirtió en el Pico de Orizaba, para mirarlos de lejos, solo, por toda la eternidad.",
  S("codex_paper", cam=((0.4, 0.5, 1.3), (0.5, 0.5, 1.15)), fx=["dust"], grade="sepia"),
  S("citlaltepetl", cam=((0.55, 0.5, 1.2), (0.45, 0.5, 1.05)), fx=[FOGL], grade="cold", tr="xfade", tl=0.6, w=1.2))
B("Y en mil novecientos cuarenta, el pintor Jesús Helguera pintó al guerrero cargando a su princesa para un calendario. Esa imagen colgó durante décadas en miles de casas, fondas y talleres de todo México.",
  S("calendar_wall", cam=((0.45, 0.5, 1.1), (0.5, 0.4, 1.5)), fx=["dust", FL], grade="warm"),
  S("calendar_wall", cam=((0.5, 0.62, 1.7), (0.2, 0.75, 1.5)), fx=["dust", FL], grade="warm", tr="xfade", tl=0.6))
B("Pero aquí viene lo que te prometí al principio.",
  S("izta_night", cam=((0.5, 0.5, 1.05), (0.5, 0.45, 1.25), "in"), fx=[FOGL]), music="dread")
B("En diciembre de mil novecientos noventa y cuatro, después de décadas de calma, el Popocatépetl despertó. Desde entonces no ha dejado de rugir, de lanzar ceniza, de iluminar el cielo por las noches. Hay días en que la ceniza cae sobre los coches de Puebla y de la Ciudad de México, y cierran los aeropuertos. Millones de personas viven a su alrededor, mirándolo de reojo.",
  S("eruption_town", L("l_eruption_glow", blend="screen", anim=[{"type": "pulse", "amp": 0.15, "period": 3}]), cam=((0.5, 0.6, 1.1), (0.5, 0.45, 1.3)),
    fx=["ash", "embers", {"type": "lightning", "at": [3.0]}, SH(3.0, 4.0, 6)], grade="blood", w=1.3),
  S("ash_city", cam=((0.5, 0.55, 1.05), (0.5, 0.6, 1.3)), fx=["ash", FOG], grade="none", tr="xfade", tl=0.6),
  S("eruption_town", L("l_eruption_glow", blend="screen", anim=[{"type": "pulse", "amp": 0.15, "period": 3}]), cam=((0.5, 0.35, 1.5), (0.5, 0.3, 1.7)), fx=["ash", "embers"], grade="blood", tr="xfade", tl=0.6),
  sfx=[X("boom", 3.0, -2), X("thunder", 3.2, -4)])
B("En los pueblos de sus faldas, la gente no le dice volcán. Le dice Don Goyo. Y los tiemperos, los que hablan con el tiempo, le suben ofrendas cada doce de marzo: flores, comida, música. Como se visita a un abuelo. Le piden que sea bueno con las cosechas, que mande lluvia y no granizo, y que no se enoje.",
  S("offering_cave", L("l_candles", blend="screen", anim=[{"type": "flicker", "amp": 0.2, "speed": 2.0}]), cam=((0.5, 0.55, 1.1), (0.5, 0.5, 1.3)), fx=[FOGL, FL], grade="candle", w=1.3,
    text=[T("DON GOYO|el abuelo que humea", "big", 1.5, 5.5)]),
  S("tiemperos_slope", SMOKE, cam=((0.3, 0.75, 1.3), (0.5, 0.55, 1.15)), fx=[FOGL], tr="xfade", tl=0.6, w=1.2),
  S("offering_cave", L("l_candles", blend="screen"), cam=((0.5, 0.72, 1.7), (0.55, 0.7, 1.8), "linear"), fx=[FL], grade="candle", tr="xfade", tl=0.6), music="mystery")
B("Los abuelos dicen que cuando Don Goyo ruge, es porque sigue llorando. Que la ceniza es su tristeza. Y que mientras su antorcha siga encendida, ella puede dormir tranquila.",
  S("popo_crater_smoke", SMOKE, cam=((0.5, 0.5, 1.25), (0.5, 0.45, 1.05)), fx=["embers", FOG], w=1.2),
  S("izta_sleeping", cam=((0.5, 0.5, 1.15), (0.5, 0.52, 1.3)), fx=[FOGL], tr="xfade", tl=0.8))
B("Pero el día que ese humo se apague… el día que él por fin se rinda…",
  S("volcanoes_night", cam=((0.5, 0.5, 1.1), (0.75, 0.5, 1.45), "in"), fx=[FOGL, {"type": "pulse", "bpm": 64, "amp": 0.1}]),
  pause=0.5, sfx=[X("heartbeat", 0.0, -8, dur=5, bpm=64), X("riser", 1.0, -6, dur=3.5)])
B("la Mujer Dormida va a despertar. Y va a bajar a buscarlo.",
  S("izta_awake", tr="flash", tl=0.25, cam=((0.5, 0.42, 1.3), (0.5, 0.42, 1.55)), fx=[SNOWFOG, SH(0, 0.7, 10)], grade="cold",
    text=[T("DESPERTARÁ|y bajará a buscarlo", "big", 0.4, 3.4)]),
  pause=1.2, sfx=[X("sting", 0.0, -1), X("boom", 0.0, -3), X("whisper", 1.0, -14, dur=3)])
B("Así que la próxima vez que veas humo sobre el Popocatépetl, no te asustes. Es él, cuidándola. Lo que debería asustarte… es el día que deje de humear.",
  S("volcanoes_night", SMOKE, CLOUDS, cam=((0.5, 0.5, 1.2), (0.5, 0.5, 1.0)), fx=[FOGL]),
  S("izta_night", cam=((0.6, 0.5, 1.2), (0.5, 0.45, 1.4)), fx=[FOGL], tr="xfade", tl=0.8), music="sad")
B("Y tú, ¿has visto a la Mujer Dormida? ¿Desde dónde la ves tú? Te leo en los comentarios.",
  S("volcanoes_dawn", CLOUDS, cam=((0.5, 0.5, 1.05), (0.5, 0.45, 1.2)), fx=[FOGL], tr="fade", tl=0.8), music="mystery")
B("En el próximo video: un hombre que de noche deja de ser hombre. El Nahual, el brujo que se convierte en animal… y que podría estar viviendo en tu propio pueblo.",
  S("runner_maguey", cam=((0.5, 0.6, 1.2), (0.45, 0.55, 1.35)), fx=[FOGL], grade="night"),
  S("nahual_tease", cam=((0.55, 0.6, 1.4), (0.5, 0.55, 1.05)), fx=[FOGL, "fireflies"], grade="night", tr="xfade", tl=0.6,
    text=[T("PRÓXIMO VIDEO|El Nahual", "big", 1.0, 6.0)], out=2.0),
  pause=1.0, music="dread", sfx=[X("howl", 2.0, -8)])

story = {"title": "Popocatépetl e Iztaccíhuatl: el guerrero que sigue velando a su princesa", "voice": "em_alex", "speed": 0.88,
         "sentence_gap": 0.26, "key": "E", "seed": 11, "grade": "night", "vignette": 0.58, "outro": 5.0,
         "music_gain": -15, "amb_gain": -21, "sfx_gain": -9, "beats": BEATS}
json.dump(story, open(os.path.join(HERE, "story.json"), "w"), ensure_ascii=False, indent=1)

words = 0; out = ["# Popocatépetl e Iztaccíhuatl — guion\n",
                  "Narración en español (narrador: em_alex; Iztaccíhuatl: ef_dora; Popocatépetl, el señor de Tlaxcala y el traidor: em_santa).\n"]
for b in BEATS:
    for sc in b["scenes"]:
        for t in sc.get("text", []):
            if t["style"] in ("chapter", "title"): out.append(f"\n## {t['str'].replace('|', ' — ')}\n")
    if b["text"]:
        who = {"ef_dora": "IZTACCÍHUATL: ", "em_santa": "PERSONAJE: "}.get(b.get("voice"), "")
        out.append(who + b["text"]); words += len(b["text"].split())
open(os.path.join(HERE, "script.md"), "w").write("\n\n".join(out) + "\n")
arts = sorted({l["src"] for b in BEATS for sc in b["scenes"] for l in sc["layers"]})
print(f"beats {len(BEATS)}  scenes {sum(len(b['scenes']) for b in BEATS)}  words {words}  art {len(arts)}")
print(" ".join(a[4:-4] for a in arts))
