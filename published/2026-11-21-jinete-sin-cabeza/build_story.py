#!/usr/bin/env python3
"""Builds story.json and script.md for "El Jinete sin Cabeza" (El Muerto, franja del Nueces). Edit BEATS here, then run.
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
DUST = L("l_dust", blend="screen", opacity=[0, 0.7], anim=[{"type": "drift", "dx": 0.08, "ease": "linear"}])
RIDE = L("l_rider", depth=1.05, anim=[{"type": "drift", "dx": 0.32, "dy": -0.01, "ease": "linear"}])
RIDEIN = L("l_rider", depth=1.05, opacity=[0, 1.0], fade_in=0.8, anim=[{"type": "drift", "dx": 0.18, "ease": "linear"}])
RIDEFAR = L("l_rider_far", depth=1.02, anim=[{"type": "drift", "dx": 0.22, "ease": "linear"}])
GHOST = L("l_rider_ghost", blend="screen", opacity=[0, 0.85], fade_in=1.5, depth=1.05, anim=[{"type": "drift", "dx": 0.2, "ease": "linear"}, {"type": "flicker", "amp": 0.15, "speed": 1.0}])

SANTA = dict(voice="em_santa", speed=0.84)
WALL = dict(voice="em_santa", speed=0.76)
DEAD = dict(voice="em_santa", speed=0.7, fx="eco")
NIGHT = ["wind", {"name": "crickets", "gain": -6}]
BRUSH = ["night", {"name": "wind", "gain": -8}]
CAMP = ["fire", {"name": "crickets", "gain": -6}]
RIVER = ["river", {"name": "crickets", "gain": -8}]
ROOM = ["room", {"name": "clock", "gain": -14}]
FLASH = lambda img="rider_flash", g=None: S(img, tr="flash", tl=0.12, dur=1.4, cam=((0.5, 0.45, 1.15), (0.5, 0.45, 1.4)), fx=[SH(0, 0.6, 9)], grade=g)
SCARE = [X("riser", -3.5, -8, at_scene=1, dur=3.5), X("sting", 0.0, -2, at_scene=1), X("boom", 0.0, -3, at_scene=1)]
GALLOP = lambda at=0.3, d=6, g=-10, dist=0.5: X("hooves", at, g, dur=d, distance=dist, bpm=150)

# ======================================================================== COLD OPEN
B("Sur de Texas. Mil novecientos diecisiete. Un camino de tierra entre mezquites y nopales, a pocas leguas del río Bravo.",
  S("road_night", FOGLAY, cam=((0.5, 0.5, 1.05), (0.5, 0.55, 1.25), "in"), fx=[FOGL], tr="fade", tl=1.2,
    text=[T("Cerca de San Diego, Texas, 1917|tierra que un día fue de México", "date", 0.6, 5.5)]),
  pre=0.6, music="dread", amb=NIGHT)
B("Imagina una carreta que avanza despacio bajo la luna. Un hombre y una mujer vuelven a su rancho… y de pronto, el caballo se detiene. No quiere dar un paso más.",
  S("wagon_1917", cam=((0.45, 0.6, 1.1), (0.52, 0.62, 1.4), "in"), fx=[FOGL]),
  S("wagon_1917", cam=((0.5, 0.65, 1.5), (0.48, 0.66, 1.7), "in"), fx=[FOGL], tr="xfade", tl=0.6),
  sfx=[X("hooves", 0.3, -16, dur=4, bpm=60), X("gust", 6.0, -12)])
B("Entonces lo oyen. Cascos. Un galope que viene del monte, cada vez más fuerte, cada vez más cerca.",
  S("brush_fog", RIDEFAR, cam=((0.5, 0.55, 1.1), (0.55, 0.6, 1.35), "in"), fx=[FOGL]),
  music="tension", sfx=[GALLOP(0.2, 7, -12, 0.9), X("heartbeat", 1.0, -14, dur=6, bpm=84)])
B("Y en la orilla del camino aparece un jinete. Alto. Derecho sobre la silla. Con las manos amarradas a la cabeza de la montura.",
  S("rider_front", cam=((0.5, 0.55, 1.1), (0.5, 0.5, 1.35), "in"), fx=[FOGL]),
  S("hands_tied", cam=((0.5, 0.55, 1.1), (0.5, 0.55, 1.3), "in"), tr="xfade", tl=0.5),
  sfx=[GALLOP(0.0, 4, -9, 0.3)])
B("La mujer levanta la vista para verle la cara… y no hay cara. No hay nada.",
  S("rider_close", cam=((0.45, 0.75, 1.25), (0.42, 0.3, 1.35), "inout"), fx=[FOGL, PU(60, 0.08)]),
  sfx=[X("whisper", 0.5, -18, dur=4)])
B("",
  S("rider_close", cam=((0.42, 0.3, 1.35), (0.42, 0.3, 1.4)), dur=1.2),
  FLASH("rider_flash"), pause=0.6, sfx=SCARE)
B("¡Es mío! ¡Todo es mío!",
  S("rider_close_red", cam=((0.45, 0.4, 1.2), (0.45, 0.38, 1.4), "in"), fx=[SH(0, 1.0, 5)],
    text=[T("¡Es mío! ¡Todo es mío!|", "quote", 0.3, 3.5)]), pause=0.9, **DEAD)
B("",
  S("title_bg", cam=((0.5, 0.5, 1.0), (0.5, 0.48, 1.12)), fx=[FOG], tr="fade", tl=0.8,
    text=[T("EL JINETE SIN CABEZA|la leyenda de El Muerto", "title", 0.6, 6.4)]),
  pause=5.2, sfx=[X("boom", 0.4, -4), X("whoosh", 0.3, -8)])
B("Por esos caminos lo llaman El Muerto. Es el jinete sin cabeza de la frontera. Y hay una pregunta que nadie ha podido responder en casi dos siglos. ¿Qué es lo que reclama? ¿Qué es eso que dice que es suyo? Al final de esta historia te lo voy a contar.",
  S("rider_moon", cam=((0.5, 0.5, 1.05), (0.5, 0.48, 1.25), "in"), fx=[FOGL]),
  S("brush_night", RIDE, cam=((0.5, 0.55, 1.05), (0.55, 0.55, 1.15)), fx=[FOGL], tr="xfade", tl=0.6),
  music="mystery", amb=BRUSH, sfx=[GALLOP(6.0, 6, -14, 0.7)])

# ======================================================================== I
B("Para entender a este jinete hay que regresar mucho antes, a una tierra que hoy pocos recuerdan que fue mexicana.",
  S("map_nueces", cam=((0.5, 0.5, 1.02), (0.55, 0.55, 1.2), "in"), fx=["dust"], tr="fade", tl=1.0, grade="sepia",
    text=[T("CAPÍTULO I|La tierra de nadie", "chapter", 0.6, 5.0)]),
  music="calm", amb=["wind"])
B("Entre el río Nueces y el río Bravo había una franja enorme de monte. Mezquite, nopal, caballos salvajes. Ranchos mexicanos, vaqueros, familias que llevaban generaciones ahí.",
  S("rancho_dusk", cam=((0.4, 0.55, 1.05), (0.6, 0.55, 1.2), "linear"), fx=["dust"]),
  S("mustangs_run", DUST, cam=((0.5, 0.6, 1.1), (0.6, 0.6, 1.25), "linear"), fx=["dust"], tr="xfade", tl=0.6),
  sfx=[X("hooves", 6.0, -16, dur=5, distance=0.8, bpm=140)])
B("En mil ochocientos treinta y seis, Texas se separó de México, y empezó la pelea por esa franja. Texas decía que su frontera era el Bravo. México decía que era el Nueces.",
  S("map_nueces", cam=((0.45, 0.45, 1.3), (0.55, 0.6, 1.5), "inout"), grade="sepia"))
B("En medio quedó una tierra sin ley. La gente le decía la tierra de nadie. Ahí cada quien se cuidaba solo… y de noche, nadie salía al monte sin su rifle.",
  S("brush_night2", FOGLAY, cam=((0.5, 0.55, 1.05), (0.45, 0.55, 1.25), "in"), fx=[FOGL]),
  S("vaqueros_fire", FIREG, cam=((0.45, 0.6, 1.1), (0.5, 0.6, 1.3), "in"), fx=["embers"], tr="xfade", tl=0.6),
  music="mystery", amb=NIGHT, sfx=[X("owl", 3.0, -14), X("howl", 7.0, -16)])
B("Por ese monte cruzaba de todo. Arrieros con mulas cargadas rumbo a Matamoros. Soldados. Contrabandistas. Y bandas de hombres armados que no respetaban ni una bandera ni la otra.",
  S("riders_chase", cam=((0.4, 0.6, 1.05), (0.6, 0.6, 1.2), "linear"), fx=[FOGL]),
  sfx=[X("hooves", 1.0, -14, dur=5, distance=0.6)])
B("Luego vino la guerra entre México y Estados Unidos. Y en mil ochocientos cuarenta y ocho, con el Tratado de Guadalupe Hidalgo, la frontera quedó en el río Bravo.",
  S("treaty", cam=((0.5, 0.45, 1.05), (0.5, 0.4, 1.3), "in"), fx=["dust", FL], grade="candle",
    text=[T("Guadalupe Hidalgo, 1848|fin de la guerra", "date", 3.0, 7.5)]), amb=ROOM)
B("De un día para otro, miles de mexicanos amanecieron del otro lado de la línea. Sus ranchos, sus caballos, sus muertos enterrados… ahora estaban en otro país.",
  S("rio_bravo", FOGLAY, cam=((0.5, 0.55, 1.05), (0.55, 0.6, 1.3), "in"), fx=[FOGL]),
  S("border_fire", cam=((0.6, 0.6, 1.2), (0.68, 0.6, 1.5), "in"), fx=[FOGL], tr="xfade", tl=0.6),
  music="sad", amb=RIVER)
B("Muchos se quedaron a defender lo suyo. Otros cruzaron el río y no volvieron. Y algunos, dicen, se quedaron en el monte, resentidos, sin patria y sin ley.",
  S("brush_dusk", cam=((0.5, 0.5, 1.05), (0.45, 0.55, 1.25), "in"), fx=["dust"]))
B("Y es en esos años, en ese monte, donde aparece el hombre de esta historia. Cuentan que se llamaba Vidal.",
  S("vidal_portrait", cam=((0.5, 0.45, 1.1), (0.5, 0.4, 1.3), "in"), fx=[FL], grade="candle"),
  music="mystery", amb=CAMP)
B("Nadie sabe su apellido. Algunos dicen que fue vaquero, que conocía el monte como la palma de su mano y que podía amansar un mesteño en una sola tarde.",
  S("vidal_smile", cam=((0.5, 0.42, 1.15), (0.48, 0.4, 1.3), "in"), fx=[FL], grade="candle"),
  S("mustangs_run", DUST, cam=((0.45, 0.6, 1.2), (0.55, 0.62, 1.35), "linear"), fx=["dust"], tr="xfade", tl=0.6))
B("Lo que sí cuentan todos es que montaba como pocos, que nunca se quitaba su sombrero de ala ancha… y que se reía de los rinches.",
  S("vidal_portrait", cam=((0.5, 0.35, 1.3), (0.5, 0.32, 1.5), "in"), fx=[FL], grade="candle"))
B("Otros dicen que ya entonces era cuatrero, ladrón de ganado y de caballos… y que por su cabeza se ofrecía una recompensa.",
  S("vidal_night", cam=((0.5, 0.42, 1.15), (0.5, 0.4, 1.35), "in"), fx=[FOG], grade="moon"),
  music="tension", amb=NIGHT)
B("Y quédate con esa frase. Porque en esta historia… la cabeza de Vidal es lo más importante.",
  S("vidal_cold", cam=((0.5, 0.4, 1.25), (0.5, 0.36, 1.5), "in"), fx=[PU(64, 0.12)],
    text=[T("SU CABEZA|tenía precio", "big", 1.5, 5.5)]),
  sfx=[X("sting", 3.5, -10), X("heartbeat", 0.5, -14, dur=6, bpm=64)])

# ======================================================================== II
B("Mil ochocientos cincuenta. Era la temporada que en el monte llamaban la luna comanche.",
  S("comanche_moon", FOGLAY, cam=((0.5, 0.45, 1.05), (0.52, 0.4, 1.25), "in"), fx=[FOGL], tr="fade", tl=1.0,
    text=[T("CAPÍTULO II|Los caballos del rinche", "chapter", 0.6, 5.0)]),
  music="mystery", amb=NIGHT)
B("En las noches de luna llena bajaban partidas a robar caballos, y los rancheros salían a perseguirlas. Las casas se quedaban casi solas.",
  S("comanche_moon", cam=((0.3, 0.6, 1.3), (0.7, 0.6, 1.35), "linear"), fx=[FOGL]),
  S("rancho_night", cam=((0.4, 0.6, 1.1), (0.5, 0.6, 1.3), "in"), fx=[FOGL], tr="xfade", tl=0.6),
  sfx=[X("howl", 2.0, -16), X("hooves", 5.0, -18, dur=4, distance=0.9)])
B("Cuentan que Vidal aprovechó justo eso. Mientras los hombres andaban lejos, él y su gente entraron a los ranchos cerca del río San Antonio y se llevaron una manada entera, rumbo al sur, rumbo a México.",
  S("rancho_night", cam=((0.65, 0.65, 1.3), (0.75, 0.65, 1.5), "in"), fx=[FOGL]),
  S("mustangs_run", DUST, cam=((0.6, 0.6, 1.1), (0.4, 0.6, 1.25), "linear"), fx=["dust"], tr="xfade", tl=0.6, grade="cold"),
  music="tension", sfx=[X("hooves", 6.0, -10, dur=7, distance=0.4, bpm=160)])
B("Pero esa vez se equivocó de corrales. Entre esos animales había mesteños de un hombre que no perdonaba.",
  S("corral_empty", cam=((0.5, 0.6, 1.1), (0.5, 0.7, 1.35), "in"), fx=["dust"]),
  amb=["wind"], sfx=[X("gust", 1.0, -12)])
B("Se llamaba Creed Taylor. Era un rinche, como les decían en la frontera a los guardias montados de Texas. Había peleado en la guerra y conocía el monte tanto como Vidal.",
  S("taylor_portrait", cam=((0.5, 0.45, 1.1), (0.5, 0.4, 1.3), "in"), fx=[FL], grade="candle"),
  music="calm", amb=CAMP)
B("Esos caballos son míos… y los voy a traer de vuelta.",
  S("taylor_night", cam=((0.5, 0.4, 1.25), (0.5, 0.38, 1.45), "in"), fx=[FOG],
    text=[T("Esos caballos son míos.|Creed Taylor", "quote", 0.3, 4.0)]), pause=0.7, **SANTA)
B("Con él iba otro rinche, un hombre enorme al que todos llamaban Pie Grande Wallace. Y un ranchero mexicano de apellido Flores, que también había perdido sus animales.",
  S("wallace_portrait", cam=((0.5, 0.45, 1.1), (0.5, 0.4, 1.3), "in"), fx=[FL], grade="candle"),
  S("riders_chase", cam=((0.45, 0.6, 1.1), (0.55, 0.6, 1.25), "linear"), fx=[FOGL], tr="xfade", tl=0.6),
  music="tension", amb=NIGHT, sfx=[X("hooves", 7.0, -14, dur=5, distance=0.5)])
B("Los tres siguieron el rastro durante días. Huellas de cascos en la tierra seca. Ramas rotas. Cenizas de fogatas apagadas.",
  S("tracks", cam=((0.3, 0.5, 1.1), (0.7, 0.55, 1.25), "linear"), fx=["dust"]),
  S("camp_embers", cam=((0.5, 0.75, 1.3), (0.5, 0.72, 1.5), "in"), fx=[FOGL], tr="xfade", tl=0.6),
  sfx=[X("footsteps", 0.5, -16, dur=4)])
B("De día el sol de la franja quemaba como brasa. De noche el frío se metía en los huesos. Y en cada aguaje, en cada arroyo seco, el rastro de la manada seguía apuntando al sur.",
  S("road_dawn", cam=((0.5, 0.55, 1.05), (0.5, 0.6, 1.3), "in"), fx=["dust"]),
  S("brush_dusk", cam=((0.4, 0.5, 1.1), (0.6, 0.5, 1.2), "linear"), fx=["dust"], tr="xfade", tl=0.6), amb=["wind"])
B("Y una noche, a lo lejos, vieron una lucecita entre los mezquites.",
  S("camp_night", cam=((0.5, 0.65, 1.0), (0.5, 0.68, 1.3), "in"), fx=[FOGL, FL]),
  sfx=[X("owl", 2.0, -14)])
B("Si te gustan las leyendas de México, suscríbete. Porque lo que pasó esa noche es algo que la frontera nunca pudo olvidar.",
  S("rider_moon", cam=((0.5, 0.5, 1.05), (0.5, 0.5, 1.15)), fx=[FOGL]))

# ======================================================================== III
B("El campamento de Vidal estaba en un claro del monte. La fogata casi apagada. Los caballos robados, amarrados a un lado. Y los hombres… dormidos.",
  S("camp_night", FIREG, cam=((0.45, 0.65, 1.15), (0.55, 0.7, 1.4), "in"), fx=["embers", FL], tr="fade", tl=1.0,
    text=[T("CAPÍTULO III|La noche del campamento", "chapter", 0.6, 5.0)]),
  music="dread", amb=CAMP)
B("Imagina el silencio. Solo los grillos y el resoplido de los caballos. Tres sombras que se acercan entre los nopales, agachadas, con los rifles en la mano.",
  S("camp_shadows", cam=((0.3, 0.6, 1.15), (0.4, 0.6, 1.35), "in"), fx=[FOGL]),
  S("camp_shadows", cam=((0.6, 0.65, 1.35), (0.65, 0.65, 1.55), "in"), fx=[FOGL], tr="xfade", tl=0.6),
  sfx=[X("footsteps", 1.0, -18, dur=6), X("heartbeat", 3.0, -12, dur=6, bpm=90)])
B("Uno de los caballos levantó la cabeza. Paró las orejas. Algo había olido en el aire. Pero ninguno de los hombres despertó.",
  S("camp_night", cam=((0.2, 0.62, 1.5), (0.22, 0.62, 1.7), "in"), fx=[FOGL, FL]),
  sfx=[X("heartbeat", 0.5, -12, dur=6, bpm=100)])
B("Los rinches no gritaron. No dieron aviso.",
  S("camp_embers", cam=((0.5, 0.7, 1.3), (0.5, 0.7, 1.45), "in"), fx=[FOGL]), pause=0.3)
B("",
  S("camp_night", cam=((0.5, 0.65, 1.3), (0.5, 0.65, 1.35)), dur=1.0),
  S("muzzle_flash", tr="flash", tl=0.1, dur=2.2, fx=[SH(0, 1.2, 10), {"type": "lightning", "at": [0.0, 0.4, 0.9]}]),
  pause=0.8, music="silence", sfx=[X("boom", 1.0, -3), X("boom", 1.4, -5, pan=-0.5), X("boom", 1.9, -6, pan=0.5)])
B("Cuando volvió el silencio, ninguno de los cuatreros se levantó de su cobija.",
  S("camp_embers", cam=((0.5, 0.7, 1.1), (0.5, 0.75, 1.3), "in"), fx=[FOGL], out=0.8),
  music="sad", amb=["wind"])
B("Pero para Pie Grande Wallace eso no era suficiente. Dicen que se quedó mirando el cuerpo de Vidal a la luz de las brasas… y que se le ocurrió una lección para todos los ladrones de caballos de la frontera.",
  S("wallace_shadow", cam=((0.5, 0.5, 1.05), (0.5, 0.4, 1.3), "in"), fx=["embers", FL], tr="fade", tl=0.8),
  S("wallace_red", cam=((0.5, 0.42, 1.2), (0.5, 0.4, 1.4), "in"), fx=[FL], tr="xfade", tl=0.6),
  music="dread", amb=CAMP)
B("Que todos lo vean. Que nadie vuelva a tocar un caballo de este lado del río.",
  S("wallace_red", cam=((0.5, 0.38, 1.4), (0.5, 0.36, 1.6), "in"), fx=[PU(60, 0.1)],
    text=[T("Que todos lo vean.|Pie Grande Wallace", "quote", 0.3, 4.5)]), pause=0.8, **WALL)
B("Lo que hicieron después, la leyenda lo cuenta en voz baja.",
  S("brush_red", cam=((0.5, 0.5, 1.05), (0.5, 0.5, 1.2), "in"), fx=[FOGL], grade="blood"), pause=0.8,
  sfx=[X("whisper", 0.5, -16, dur=4)])
B("Atraparon un mesteño salvaje, uno que nunca había sentido una silla. Le pusieron la montura. Y sobre ella sentaron a Vidal… muy derecho, con las piernas amarradas a los estribos y las manos atadas a la cabeza de la silla.",
  S("mustang_wild", cam=((0.5, 0.55, 1.05), (0.5, 0.5, 1.3), "in"), fx=[FOGL, SH(0.5, 1.5, 5)]),
  S("hands_tied", cam=((0.5, 0.55, 1.1), (0.5, 0.58, 1.35), "in"), tr="xfade", tl=0.6),
  sfx=[X("whoosh", 0.4, -10), X("hooves", 0.6, -12, dur=2, distance=0.2, bpm=200)])
B("Vidal ya no tenía la cabeza sobre los hombros. Su sombrero, con lo que había quedado debajo, lo colgaron de la montura con una tira de cuero crudo.",
  S("sombrero_horn", cam=((0.45, 0.4, 1.1), (0.5, 0.6, 1.3), "inout"), fx=[PU(56, 0.1)], grade="moon"),
  sfx=[X("heartbeat", 0.5, -12, dur=8, bpm=56)])
B("Luego le dieron un golpe en el anca al caballo. Y el mesteño salió disparado hacia la oscuridad, relinchando, con su jinete muerto encima.",
  S("hooves_dust", cam=((0.5, 0.6, 1.1), (0.6, 0.6, 1.3), "in"), fx=[SH(0, 1.0, 6)]),
  S("release_dark", cam=((0.5, 0.55, 1.05), (0.7, 0.55, 1.25), "linear"), fx=[FOGL], tr="xfade", tl=0.5),
  music="climax", amb=NIGHT, sfx=[X("whoosh", 0.0, -6), GALLOP(0.2, 9, -6, 0.2)])
B("El galope se fue apagando poco a poco en el monte… hasta que no se oyó nada.",
  S("brush_night3", FOGLAY, cam=((0.5, 0.5, 1.05), (0.5, 0.45, 1.2), "in"), fx=[FOGL], out=1.0),
  pause=1.0, music="silence", sfx=[GALLOP(0.0, 5, -20, 1.0)])

# ======================================================================== IV
B("Pasaron semanas. Y en los ranchos del sur de Texas empezaron a contar algo que nadie quería creer.",
  S("vaqueros_fire", FIREG, cam=((0.5, 0.6, 1.05), (0.5, 0.6, 1.25), "in"), fx=["embers"], tr="fade", tl=1.0,
    text=[T("CAPÍTULO IV|El Muerto", "chapter", 0.6, 5.0)]),
  music="mystery", amb=CAMP)
B("Vaqueros que cuidaban ganado de noche veían pasar un caballo salvaje con un hombre encima. Un hombre sin cabeza.",
  S("brush_night", RIDE, cam=((0.5, 0.55, 1.05), (0.55, 0.55, 1.2), "linear"), fx=[FOGL]),
  S("rider_close", cam=((0.45, 0.35, 1.2), (0.45, 0.3, 1.35), "in"), fx=[FOGL], tr="xfade", tl=0.5),
  music="tension", amb=BRUSH, sfx=[GALLOP(0.5, 6, -10, 0.5)])
B("Le gritaban. No contestaba. Le disparaban… y el jinete seguía adelante, como si las balas lo atravesaran.",
  S("vaqueros_shoot", cam=((0.45, 0.55, 1.05), (0.55, 0.55, 1.25), "in"), fx=[FOGL, {"type": "lightning", "at": [3.2, 4.0]}]),
  sfx=[X("boom", 3.2, -8), X("boom", 4.0, -9), GALLOP(0.0, 7, -12, 0.6)])
B("",
  S("brush_night2", cam=((0.5, 0.5, 1.2), (0.5, 0.5, 1.25)), dur=1.0),
  FLASH("red_flash"), pause=0.6, sfx=SCARE)
B("Los soldados del fuerte Inge, donde hoy está la ciudad de Uvalde, juraban haberlo visto cruzar de noche frente a la muralla.",
  S("fort_inge", cam=((0.45, 0.5, 1.05), (0.65, 0.6, 1.3), "inout"), fx=[FOGL],
    text=[T("Fuerte Inge|hoy Uvalde, Texas", "date", 0.8, 5.0)]),
  music="mystery", amb=NIGHT, sfx=[X("hooves", 3.0, -14, dur=5, distance=0.7)])
B("Dicen que el mesteño no paraba nunca. Que cruzaba arroyos, matorrales y nopaleras sin detenerse, como si algo lo persiguiera. Y que sobre su lomo, el jinete se sacudía con cada salto… derecho, amarrado, sin cabeza.",
  S("hooves_dust", cam=((0.45, 0.6, 1.1), (0.55, 0.6, 1.3), "linear"), fx=[SH(0, 4, 3)]),
  S("brush_night2", RIDE, cam=((0.5, 0.55, 1.05), (0.55, 0.55, 1.15), "linear"), fx=[FOGL], tr="xfade", tl=0.5),
  sfx=[GALLOP(0.0, 10, -9, 0.4)])
B("Le pusieron un nombre: El Muerto. Y los vaqueros, mexicanos y texanos por igual, dejaron de salir solos al monte en las noches de luna.",
  S("rider_moon", cam=((0.5, 0.5, 1.1), (0.48, 0.5, 1.3), "in"), fx=[FOGL],
    text=[T("EL MUERTO|", "big", 1.5, 5.0)]),
  S("brush_night3", cam=((0.5, 0.5, 1.05), (0.5, 0.48, 1.2)), fx=[FOGL], tr="xfade", tl=0.6))
B("En los ranchos lo usaban para asustar a los muchachos desobedientes. Pórtate bien, les decían, o va a venir El Muerto. Y los viejos rezaban un Padre Nuestro cada vez que oían cascos en la noche.",
  S("vaqueros_fire", FIREG, cam=((0.4, 0.6, 1.2), (0.45, 0.6, 1.4), "in"), fx=["embers"]), amb=CAMP)
B("Cuentan que al fin, después de mucho tiempo, unos vaqueros atraparon al mesteño en un aguaje cerca de un lugar llamado Ben Bolt, al sur de Alice.",
  S("brush_dawn", cam=((0.5, 0.5, 1.05), (0.55, 0.55, 1.2), "linear"), grade="warm"),
  S("waterhole_dawn", cam=((0.5, 0.6, 1.05), (0.52, 0.62, 1.25), "in"), tr="xfade", tl=0.6),
  music="sad", amb=["wind", {"name": "river", "gain": -14}])
B("El caballo estaba flaco, con el lomo herido por la silla. Y el jinete seguía ahí, amarrado, con la ropa llena de agujeros de bala y de flechas.",
  S("waterhole_dawn", cam=((0.52, 0.55, 1.4), (0.52, 0.5, 1.7), "in")))
B("Dicen que uno de los vaqueros se acercó a revisar el sombrero que colgaba de la montura… y que se alejó sin decir una sola palabra. Nunca quiso contar lo que vio.",
  S("sombrero_horn", cam=((0.33, 0.45, 1.2), (0.34, 0.6, 1.4), "inout"), fx=[PU(56, 0.1)], grade="warm"),
  sfx=[X("heartbeat", 0.5, -12, dur=7, bpm=60)])
B("Lo bajaron y lo enterraron ahí mismo, bajo un mezquite. Sin cruz. Sin nombre.",
  S("grave_mesquite", cam=((0.45, 0.6, 1.05), (0.42, 0.65, 1.3), "in"), fx=["dust"]),
  sfx=[X("bell", 2.5, -18, freq=150)])
B("Pensaron que con eso se acababa todo.",
  S("grave_night", cam=((0.45, 0.62, 1.15), (0.45, 0.65, 1.3), "in"), fx=[FOGL]), pause=1.0,
  music="silence", amb=["wind"])
B("Se equivocaron.",
  S("grave_night", cam=((0.45, 0.65, 1.3), (0.45, 0.65, 1.35)), dur=1.2),
  S("rider_close_red", tr="flash", tl=0.12, cam=((0.45, 0.4, 1.25), (0.45, 0.38, 1.45)), fx=[SH(0, 0.6, 9)],
    text=[T("SE EQUIVOCARON|", "big", 0.2, 2.6)]),
  pause=0.8, sfx=SCARE)
B("Porque el jinete siguió saliendo. Siguió cabalgando por el monte… aunque su cuerpo ya estaba bajo tierra.",
  S("brush_fog", GHOST, cam=((0.45, 0.55, 1.05), (0.55, 0.55, 1.25), "linear"), fx=[FOGL], grade="cold"),
  music="dread", amb=BRUSH, sfx=[GALLOP(0.5, 7, -14, 0.8), X("whisper", 2.0, -18, dur=4)])
B("En mil novecientos diecisiete, una pareja que viajaba en carreta cerca de San Diego, Texas, contó que un jinete sin cabeza les cerró el camino… y que les gritó que todo era suyo.",
  S("wagon_1917", cam=((0.5, 0.6, 1.1), (0.52, 0.62, 1.35), "in"), fx=[FOGL],
    text=[T("1917|San Diego, Texas", "date", 0.8, 4.5)]),
  S("rider_front", cam=((0.5, 0.55, 1.2), (0.5, 0.5, 1.4), "in"), fx=[FOGL], tr="xfade", tl=0.6))
B("Y en mil novecientos sesenta y nueve, cerca de Freer, unos viajeros dijeron haber visto en la carretera, a la luz de los faros, un caballo con un jinete que no tenía cabeza.",
  S("car_1969", cam=((0.5, 0.65, 1.05), (0.5, 0.7, 1.35), "in"), fx=[FOGL],
    text=[T("1969|cerca de Freer, Texas", "date", 0.8, 4.5)]),
  sfx=[X("hooves", 6.0, -12, dur=4, distance=0.4)])
B("Hasta hay una loma en ese monte a la que la gente empezó a llamar la loma del jinete sin cabeza.",
  S("headless_hill", FOGLAY, cam=((0.5, 0.55, 1.05), (0.6, 0.55, 1.4), "in"), fx=[FOGL]),
  sfx=[X("owl", 2.0, -14), X("howl", 5.0, -16)])

# ======================================================================== V
B("Ahora, vamos a separar la historia de la leyenda.",
  S("chronicle", cam=((0.6, 0.45, 1.05), (0.62, 0.4, 1.2), "in"), fx=["dust", FL], tr="fade", tl=1.0, grade="candle",
    text=[T("CAPÍTULO V|Lo que dice la historia", "chapter", 0.6, 5.0)]),
  music="calm", amb=ROOM)
B("La tierra de nadie existió. La disputa entre el Nueces y el Bravo fue real, y el tratado de mil ochocientos cuarenta y ocho cambió la vida de miles de familias mexicanas.",
  S("map_nueces", cam=((0.5, 0.55, 1.1), (0.55, 0.55, 1.3), "in"), grade="sepia"),
  S("treaty", cam=((0.5, 0.45, 1.2), (0.5, 0.42, 1.4), "in"), fx=[FL], grade="candle", tr="xfade", tl=0.6))
B("Creed Taylor y Pie Grande Wallace también existieron. Fueron rinches conocidos en su tiempo, y Wallace terminó convertido en un personaje del folclor texano.",
  S("taylor_portrait", cam=((0.5, 0.42, 1.15), (0.5, 0.4, 1.3), "in"), fx=[FL], grade="candle"),
  S("wallace_portrait", cam=((0.5, 0.42, 1.15), (0.5, 0.4, 1.3), "in"), fx=[FL], grade="candle", tr="xfade", tl=0.6))
B("La historia de Vidal, en cambio, no aparece en documentos oficiales. La conocemos porque se contó de boca en boca… y porque, según se dice, el propio Taylor la relató muchos años después, ya de viejo.",
  S("chronicle", cam=((0.4, 0.6, 1.3), (0.35, 0.6, 1.5), "in"), fx=[FL], grade="candle"),
  S("vidal_night", cam=((0.5, 0.42, 1.15), (0.5, 0.4, 1.3), "in"), fx=[FOG], grade="moon", tr="xfade", tl=0.6))
B("Así que no sabemos si Vidal existió de verdad, ni si aquella noche pasó como la cuentan. Pero en muchos ranchos del norte de México también se habla de jinetes sin cabeza que cruzan los caminos de noche.",
  S("border_fire", cam=((0.6, 0.6, 1.1), (0.68, 0.6, 1.4), "in"), fx=[FOGL]),
  S("road_night", RIDEFAR, cam=((0.5, 0.55, 1.05), (0.5, 0.55, 1.2)), fx=[FOGL], tr="xfade", tl=0.6),
  music="mystery", amb=NIGHT)
B("¿Y qué es lo que reclama El Muerto, cuando grita que todo es suyo?",
  S("rider_close", cam=((0.45, 0.6, 1.2), (0.45, 0.35, 1.35), "inout"), fx=[FOGL, PU(58, 0.08)]),
  music="dread", sfx=[X("heartbeat", 0.5, -14, dur=6, bpm=58)])
B("Algunos dicen que son los caballos. Que Vidal sigue buscando la manada que le quitaron aquella noche.",
  S("mustangs_run", DUST, cam=((0.5, 0.6, 1.1), (0.6, 0.6, 1.25), "linear"), fx=["dust"], grade="cold"))
B("Pero los viejos de la frontera cuentan otra cosa. Dicen que Vidal no habla de caballos. Que habla de la tierra. De esa franja de monte entre dos ríos que un día fue de México… y que de la noche a la mañana dejó de serlo.",
  S("rio_bravo", FOGLAY, cam=((0.5, 0.55, 1.05), (0.55, 0.6, 1.3), "in"), fx=[FOGL]),
  S("map_nueces", cam=((0.5, 0.6, 1.4), (0.5, 0.6, 1.6), "in"), grade="sepia", tr="xfade", tl=0.8),
  music="sad", amb=RIVER)
B("Y que por eso cabalga siempre hacia el sur. Hacia el río. Buscando su cabeza… y buscando su tierra.",
  S("road_night", RIDEIN, cam=((0.5, 0.55, 1.05), (0.55, 0.55, 1.2), "linear"), fx=[FOGL],
    text=[T("SU TIERRA|", "big", 4.0, 7.5)]),
  music="dread", amb=BRUSH, sfx=[GALLOP(0.5, 7, -10, 0.5)])
B("Así que si alguna noche, en un camino del norte, tu caballo se detiene y oyes un galope entre los mezquites… no levantes la vista para buscarle la cara.",
  S("brush_fog", FOGLAY, cam=((0.5, 0.55, 1.05), (0.5, 0.6, 1.3), "in"), fx=[FOGL]),
  S("rider_front", cam=((0.5, 0.5, 1.2), (0.5, 0.42, 1.45), "in"), fx=[FOGL], tr="xfade", tl=0.6),
  sfx=[GALLOP(1.0, 9, -10, 0.6), X("heartbeat", 4.0, -12, dur=6, bpm=96)])
B("Porque no la vas a encontrar.",
  S("rider_close", cam=((0.42, 0.32, 1.3), (0.42, 0.3, 1.4)), dur=2.2),
  FLASH("rider_flash"), pause=0.8, sfx=SCARE)
B("¿Tú crees que El Muerto reclama sus caballos… o su tierra? Te leo en los comentarios.",
  S("rider_moon", cam=((0.5, 0.5, 1.1), (0.5, 0.48, 1.25), "in"), fx=[FOGL],
    text=[T("¿Sus caballos… o su tierra?|", "quote", 1.0, 6.0, pos="center")]), music="mystery", pause=0.8)
B("En el próximo video viajamos a los canales de Xochimilco, a una isla donde cientos de muñecas cuelgan de los árboles… y dicen que te siguen con la mirada. La Isla de las Muñecas.",
  S("dolls_tease", FOGLAY, cam=((0.5, 0.55, 1.05), (0.5, 0.5, 1.3), "in"), fx=[FOGL],
    text=[T("PRÓXIMO VIDEO|La Isla de las Muñecas", "big", 2.0, 7.5)]), amb=RIVER, sfx=[X("whisper", 3.0, -18, dur=4)])
B("Hasta la próxima leyenda. Y recuerda… en la frontera, alguien todavía cabalga sin cabeza.",
  S("brush_night", RIDEFAR, cam=((0.5, 0.5, 1.1), (0.5, 0.45, 1.35), "in"), fx=[FOGL], out=2.0),
  pause=1.0, music="dread", amb=BRUSH, sfx=[GALLOP(1.0, 6, -16, 0.9)])

VARIANTS = {}
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

story = {"title": "El Jinete sin Cabeza", "voice": "em_alex", "speed": 0.88,
         "sentence_gap": 0.28, "key": "D", "seed": 151, "grade": "night", "vignette": 0.58, "outro": 5.0,
         "music_gain": -15, "amb_gain": -21, "sfx_gain": -9, "beats": BEATS}
json.dump(story, open(os.path.join(HERE, "story.json"), "w"), ensure_ascii=False, indent=1)

words = 0; out = ["# El Jinete sin Cabeza — guion\n",
                  "Narración en español (narrador: em_alex; voces de personajes: em_santa; Vidal muerto: em_santa con eco).\n"]
WHO = {"em_santa": "VOZ: "}
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
