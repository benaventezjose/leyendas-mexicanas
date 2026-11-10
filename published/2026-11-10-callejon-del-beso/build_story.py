#!/usr/bin/env python3
"""Builds story.json and script.md for 'El Callejón del Beso'. Edit BEATS here, then run."""
import json, os, re
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
FL = {"type": "flicker", "amp": 0.07}
def SH(a, b, amp=7): return {"type": "shake", "amp": amp, "at": [a, b]}
FLOAT = lambda amp=0.006, p=6: [{"type": "float", "amp": amp, "period": p}]
CLOUDS = L("l_clouds", anim=[{"type": "drift", "dx": -0.05}], opacity=[0.8, 0.8])
FLAME = lambda x, y: L("l_flame", anim=[{"type": "flicker", "amp": 0.25, "speed": 2.0}], blend="screen")

N = 0
BEATS = []
def B(text, *scenes, **kw):
    global N; N += 1
    b = {"id": f"b{N:03d}", "text": text}; b.update(kw); b["scenes"] = list(scenes)
    BEATS.append(b)

# ======================================================================== COLD OPEN
B("Imagina un callejón tan angosto que, si abres los brazos, tocas las dos paredes al mismo tiempo.",
  S("alley_low", L("l_lamp_glow", blend="screen", anim=[{"type": "flicker", "amp": 0.12, "speed": 1.4}]),
    cam=((0.5, 0.85, 1.35), (0.5, 0.55, 1.15)), fx=[FOGL, "dust"], tr="fade", tl=1.2),
  pre=0.8, music="dread", amb=["night", {"name": "wind", "gain": -6}], sfx=[X("footsteps", 0.4, -12, dur=5)])
B("Arriba, muy arriba, dos balcones casi se besan. Entre uno y otro no cabe ni un metro de aire.",
  S("balcony_close", CLOUDS, cam=((0.5, 0.5, 1.05), (0.5, 0.45, 1.3)), fx=[FOG]))
B("Esa noche, una mano de mujer se estira desde el balcón de la izquierda… y del otro lado, un muchacho la sostiene, como si con eso pudiera detener el tiempo.",
  S("hands_reach", cam=((0.5, 0.5, 1.1), (0.5, 0.48, 1.4)), fx=["dust", FL], w=1.2),
  S("balcony_close", L("l_kiss_far", opacity=[0.95, 0.95]), cam=((0.5, 0.42, 1.25), (0.5, 0.45, 1.1)), fx=[FOG]),
  sfx=[X("heartbeat", 1.0, -14, dur=8, bpm=62)])
B("Él no ve la sombra que sube por la escalera, detrás de ella.",
  S("stairs_interior", L("l_father_climb", depth=1.05, anim=[{"type": "drift", "dx": 0.03, "dy": -0.04}]),
    cam=((0.4, 0.65, 1.15), (0.45, 0.5, 1.35)), fx=[FL, "dust"], grade="candle"),
  S("father_portrait_red", dur=0.8, tr="flash", cam=((0.5, 0.42, 1.3), (0.5, 0.42, 1.45), "linear"), fx=[SH(0, 0.8, 9)]),
  sfx=[X("footsteps", 0.0, -9, dur=3), X("sting", 2.6, -3)], music_at=0.0)
B("No ve el brillo de la daga.",
  S("dagger_bg", cam=((0.45, 0.5, 1.2), (0.55, 0.5, 1.5)), fx=[FL], grade="candle"), pause=0.7,
  sfx=[X("whoosh", 0.4, -8)])
B("Cuentan que esa mano nunca se soltó. Y que lo que pasó aquí es la razón por la que, todavía hoy, en Guanajuato, nadie sube el tercer escalón de este callejón sin hacer una cosa.",
  S("alley_steps", L("l_step_glow", blend="screen", anim=[{"type": "pulse", "amp": 0.08, "period": 3}]),
    cam=((0.5, 0.5, 1.05), (0.5, 0.7, 1.45)), fx=[FOGL, "dust"],
    text=[T("EL CALLEJÓN DEL BESO|Guanajuato · una leyenda de amor y sangre", "title", 0.3, 5.5)]))
B("Lo que te pasa si no la haces… te lo cuento al final.",
  S("alley_low_red", cam=((0.5, 0.5, 1.2), (0.5, 0.45, 1.5), "in"), fx=[FOG, {"type": "pulse", "bpm": 60, "amp": 0.1}], out=1.0),
  pause=0.4, sfx=[X("boom", 2.0, -6)])
B("",
  S("moon_sky", CLOUDS, cam=((0.5, 0.55, 1.0), (0.5, 0.5, 1.12)), fx=[FOG],
    text=[T("Guanajuato, Nueva España|siglo XVIII", "date", 0.8, 5.4)], tr="fade", tl=1.0, out=0.8),
  pause=6.4, music="mystery", sfx=[X("bell", 0.4, -10, freq=140)])

# ======================================================================== CAP I
B("Guanajuato no se construyó en un valle. Se construyó dentro de una herida de la sierra: una cañada estrecha, donde las casas se trepan unas sobre otras por los cerros, como si quisieran escapar hacia arriba.",
  S("gto_panorama", CLOUDS, cam=((0.35, 0.55, 1.25), (0.6, 0.5, 1.05)), fx=[FOGL],
    text=[T("CAPÍTULO I|La ciudad de plata", "chapter", 0.5, 4.8)], tr="fade", tl=0.8, w=1.5),
  amb=["night", {"name": "wind", "gain": -8}])
B("En el siglo dieciocho, de esas montañas salía tanta plata, que Guanajuato llegó a ser una de las ciudades más ricas de todo el mundo.",
  S("mine", L("l_fog", depth=1.2, anim=[{"type": "drift", "dx": 0.04}]), cam=((0.5, 0.5, 1.05), (0.45, 0.55, 1.3)), fx=["embers", FL],
    text=[T("Guanajuato, siglo XVIII|Nueva España", "date", 0.4, 4.6)]),
  sfx=[X("bell", 0.5, -16, freq=220)])
B("Arriba, en los socavones, miles de mineros bajaban cada día a la oscuridad. Abajo, en las casonas de cantera, los dueños de esa plata contaban monedas a la luz de las velas.",
  S("mine", cam=((0.62, 0.62, 1.5), (0.55, 0.6, 1.3)), fx=["dust", FL], w=1),
  S("coins", cam=((0.5, 0.5, 1.15), (0.52, 0.55, 1.4)), fx=[FL, "dust"], grade="candle"),
  sfx=[X("coins", 4.5, -8)])
B("Y como no había espacio, las calles se volvieron callejones: pasadizos de piedra, con escalones, tan angostos y torcidos que la luz de la luna apenas alcanza a tocar el suelo.",
  S("alley_steps", cam=((0.5, 0.3, 1.3), (0.5, 0.65, 1.1)), fx=[FOGL, "dust"]),
  S("rooftops", CLOUDS, cam=((0.4, 0.5, 1.1), (0.55, 0.45, 1.25)), fx=[FOG], tr="xfade", tl=0.8))
B("En uno de esos callejones vivía una muchacha llamada Carmen.",
  S("carmen_room", L("l_carmen_window", depth=1.05, anim=FLOAT(0.003, 7)), cam=((0.5, 0.5, 1.05), (0.55, 0.45, 1.3)), fx=[FL, "dust"]))
B("Cuentan que era hermosa, sí. Pero lo que todos recordaban eran sus ojos: oscuros, tristes, como los de alguien que mira la calle desde una jaula.",
  S("carmen_portrait", cam=((0.5, 0.5, 1.05), (0.5, 0.42, 1.5)), fx=["dust", FL], w=1.4))
B("Porque Carmen casi nunca salía de su casa. Su padre no la dejaba.",
  S("house_facade", CLOUDS, cam=((0.5, 0.5, 1.1), (0.5, 0.42, 1.35)), fx=[FOGL]), sfx=[X("door", 2.4, -6)])
B("Era un hombre rico, de los que se habían hecho poderosos con la plata. Severo. Celoso. Y con un carácter que hacía temblar a toda la casa.",
  S("father_study", L("l_father_back", depth=1.08), cam=((0.45, 0.5, 1.1), (0.5, 0.45, 1.3)), fx=[FL, "dust"], grade="candle", w=1.3),
  S("father_portrait", tr="flash", tl=0.3, cam=((0.5, 0.45, 1.2), (0.5, 0.4, 1.45)), fx=[SH(0, 0.6, 6), FL], w=1),
  music="tension", music_at=3.0, sfx=[X("boom", 4.8, -4), X("sting", 4.85, -6)])
B("Para él, su hija no era una hija. Era un tesoro. Y los tesoros… se guardan bajo llave.",
  S("coins", cam=((0.55, 0.55, 1.35), (0.5, 0.5, 1.1)), fx=[FL], grade="candle"),
  S("house_facade", cam=((0.5, 0.75, 1.6), (0.5, 0.78, 1.75)), fx=[FOGL, FL],
    text=[T("BAJO LLAVE", "big", 0.3, 2.8)]),
  sfx=[X("knock", 4.2, -6, times=1), X("chains", 4.4, -10)])
B("Ya le tenía marido escogido: un noble español, viejo y muy rico, que haría a la familia todavía más poderosa.",
  S("suitor_portrait", cam=((0.5, 0.5, 1.1), (0.47, 0.45, 1.35)), fx=[FL, "dust"], grade="candle"))
B("Carmen no lo quería. Pero en esa casa, lo que ella quisiera no le importaba a nadie.",
  S("carmen_room", cam=((0.6, 0.55, 1.4), (0.5, 0.5, 1.15)), fx=[FL, "dust"]),
  pause=0.8, music="sad", music_at=0.0)

# ======================================================================== CAP II
B("Imagina saber que tu vida entera ya está decidida. Que alguien firmó tu futuro sin preguntarte nada. Así vivía Carmen: entre bordados, rezos, y una ventana que daba a un callejón oscuro.",
  S("balcony_pov", L("l_carmen_window_far", depth=1.03), cam=((0.55, 0.5, 1.15), (0.5, 0.5, 1.35)), fx=[FOG, "dust"], grade="cold"))
B("La única vez que Carmen podía salir era para ir a misa, y siempre vigilada por su dama de compañía: una mujer mayor, de rebozo oscuro, llamada Brígida.",
  S("temple_facade", L("l_brigida_carmen", depth=1.06, anim=[{"type": "drift", "dx": 0.02}]), CLOUDS,
    cam=((0.5, 0.45, 1.05), (0.52, 0.55, 1.25)), fx=[FOGL],
    text=[T("CAPÍTULO II|Una mirada en el templo", "chapter", 0.5, 4.8)], tr="fade", tl=0.8, w=1.4),
  music="mystery", sfx=[X("bell", 0.6, -8, freq=180), X("bell", 2.2, -10, freq=180)])
B("Y fue ahí, entre el humo de las velas y el murmullo de los rezos, donde lo vio por primera vez.",
  S("temple_interior", cam=((0.5, 0.6, 1.05), (0.5, 0.5, 1.3)), fx=[FL, "dust", FOG], grade="candle"),
  amb=["room"], sfx=[X("whisper", 0.2, -14, dur=5)])
B("Un muchacho de pie junto a una columna. Sin sombrero de pluma, sin capa fina. Se llamaba Luis. No tenía nada más que su nombre, y unas manos curtidas de minero.",
  S("temple_interior", L("l_luis_column", depth=1.06), cam=((0.72, 0.55, 1.5), (0.7, 0.5, 1.7)), fx=[FL, "dust"], grade="candle"),
  S("luis_portrait", cam=((0.5, 0.5, 1.1), (0.5, 0.43, 1.4)), fx=["dust", FL], tr="xfade", tl=0.6, w=1.3))
B("Imagina esa mirada. Dura apenas un segundo. Ella baja los ojos… pero ya es tarde.",
  S("carmen_portrait", cam=((0.5, 0.4, 1.5), (0.5, 0.38, 1.7)), fx=["dust"]),
  sfx=[X("heartbeat", 0.5, -12, dur=4, bpm=74)])
B("Domingo tras domingo, Luis volvió al templo. Y domingo tras domingo, Carmen lo buscó con los ojos, entre la gente.",
  S("temple_interior", cam=((0.3, 0.55, 1.4), (0.6, 0.55, 1.4), "linear"), fx=[FL, "dust", FOG], grade="candle"),
  sfx=[X("bell", 0.3, -14, freq=180)])
B("Brígida lo notó. Y en lugar de acusarla con su padre… se volvió su cómplice.",
  S("brigida_portrait", cam=((0.5, 0.5, 1.1), (0.5, 0.45, 1.4)), fx=[FL, "dust"], grade="candle"))
B("Escondidas en el rebozo empezaron a viajar cartas: papeles doblados, escritos de noche, que olían a cera y a miedo.",
  S("letters_table", FLAME(0, 0), cam=((0.45, 0.55, 1.1), (0.5, 0.5, 1.4)), fx=["dust", FL], grade="candle"))
B("Luis le escribía que la esperaría toda la vida. Ella le contestaba que su padre jamás lo aceptaría, que era peligroso, que se olvidara de ella. Y en la carta siguiente… le pedía que no la olvidara nunca.",
  S("letters_table", FLAME(0, 0), cam=((0.6, 0.45, 1.5), (0.55, 0.5, 1.25)), fx=["dust", FL], grade="candle"),
  S("carmen_room", L("l_carmen_window", depth=1.05), cam=((0.45, 0.45, 1.5), (0.45, 0.42, 1.7)), fx=[FL], w=0.8))
B("Hasta que una tarde… el padre encontró una.",
  S("letters_table", cam=((0.4, 0.55, 1.5), (0.42, 0.55, 1.7)), fx=[FL], grade="candle"),
  S("father_portrait_red", dur=1.2, tr="flash", cam=((0.5, 0.42, 1.25), (0.5, 0.4, 1.5), "linear"), fx=[SH(0, 1.0, 8)]),
  music="tension", sfx=[X("door", 0.0, -8), X("sting", 1.9, -2), X("boom", 1.9, -5)])
B("Si vuelves a ver a ese muerto de hambre, te encierro en un convento. O te casas con quien yo diga.",
  S("father_study", L("l_father_back", depth=1.08), cam=((0.5, 0.5, 1.3), (0.5, 0.45, 1.5)), fx=[FL, SH(0.2, 0.9, 4)], grade="candle",
    text=[T("«Te encierro en un convento.»|su padre", "quote", 0.3, 5.5)]),
  voice="em_santa", speed=0.84, pause=0.8)
B("Esa noche, todo el barrio escuchó los gritos.",
  S("house_facade", L("l_window_red", blend="screen", anim=[{"type": "flicker", "amp": 0.2, "speed": 1.5}]), cam=((0.5, 0.45, 1.25), (0.5, 0.42, 1.45)), fx=[FOGL]),
  amb=["night", {"name": "wind", "gain": -6}], sfx=[X("door", 1.2, -6)])
B("Cuentan que el padre arrastró a Carmen hasta su cuarto, y que esa misma semana mandó decir al noble español que la boda se haría pronto. Muy pronto.",
  S("suitor_portrait", cam=((0.45, 0.4, 1.4), (0.5, 0.42, 1.2)), fx=[FL], grade="candle"),
  sfx=[X("bell", 6.0, -12, freq=200)])
B("Y desde entonces, Carmen ya no salió ni a misa. Las ventanas se cerraron. La puerta también. Y la jaula se hizo más pequeña.",
  S("carmen_room", L("l_carmen_window", depth=1.05), cam=((0.5, 0.5, 1.3), (0.5, 0.5, 1.05)), fx=[FL, "dust"], grade="cold"),
  pause=0.9, music="sad", sfx=[X("door", 4.0, -6), X("knock", 4.6, -10, times=1)])

# ======================================================================== CAP III
B("Cualquier otro se habría rendido. Luis no.",
  S("alley_low", cam=((0.5, 0.7, 1.1), (0.5, 0.62, 1.25)), fx=[FOGL, "dust"],
    text=[T("CAPÍTULO III|Sesenta y ocho centímetros", "chapter", 0.4, 4.8)], tr="fade", tl=0.8, w=1.5),
  music="mystery")
B("Recorrió el barrio de Carmen piedra por piedra, mirando siempre hacia arriba… hasta que vio algo que nadie más había notado.",
  S("alley_steps", L("l_luis_walk", depth=1.12, anim=[{"type": "drift", "dx": 0.05, "dy": -0.02}]),
    cam=((0.45, 0.6, 1.15), (0.5, 0.45, 1.3)), fx=[FOGL, "dust"]),
  sfx=[X("footsteps", 0.3, -10, dur=6)])
B("La casa de enfrente. Su balcón quedaba tan cerca del balcón de ella, que desde abajo parecían uno solo.",
  S("balcony_close", cam=((0.5, 0.55, 1.4), (0.5, 0.5, 1.1), "out"), fx=[FOG, "dust"]))
B("Dicen que entre uno y otro había apenas sesenta y ocho centímetros.",
  S("balcony_close", cam=((0.5, 0.45, 1.5), (0.5, 0.45, 1.7)), fx=[FOG],
    text=[T("68 cm|entre un balcón y otro", "big", 0.4, 4.2)]), pause=0.8, sfx=[X("boom", 0.4, -8)])
B("Luis juntó todo lo que tenía. Todo lo que había sacado de la mina en años de trabajo. Y pagó lo que le pidieron por esa casa: un precio de locos.",
  S("mine", cam=((0.5, 0.55, 1.2), (0.55, 0.6, 1.4)), fx=["embers", "dust"]),
  S("coins", cam=((0.45, 0.5, 1.4), (0.5, 0.5, 1.15)), fx=[FL], grade="candle"),
  sfx=[X("coins", 5.5, -8)])
B("Y una noche, cuando Carmen abrió su ventana para respirar un poco de aire… él estaba ahí. Del otro lado. Tan cerca, que podía oír su respiración.",
  S("alley_low", L("l_carmen_balc"), cam=((0.42, 0.42, 1.5), (0.42, 0.42, 1.65)), fx=[FOG], w=1.2),
  S("alley_low", L("l_carmen_balc"), L("l_luis_balc"), cam=((0.6, 0.45, 1.6), (0.5, 0.45, 1.3)), fx=[FOG], tr="xfade", tl=0.6, w=1.2),
  sfx=[X("door", 0.6, -12)])
B("¿Luis?",
  S("carmen_portrait_fear", cam=((0.5, 0.45, 1.3), (0.5, 0.43, 1.42)), fx=["dust"]),
  voice="ef_dora", speed=0.8, pause=0.9)
B("Si estas historias te ponen la piel chinita, suscríbete al canal. Aquí contamos las leyendas que México se cuenta en voz baja.",
  S("rooftops", CLOUDS, cam=((0.6, 0.45, 1.25), (0.45, 0.5, 1.1)), fx=[FOG]), pause=0.8)
B("Desde esa noche, el callejón se volvió su secreto.",
  S("alley_low", L("l_kiss_balc"), cam=((0.5, 0.45, 1.15), (0.5, 0.45, 1.35)), fx=[FOG], tr="xfade", tl=0.6),
  music="hope")
B("Imagina cómo era: la ciudad en silencio, el olor a tierra mojada que baja de los cerros, la luz amarilla de un farol allá abajo. Y dos personas, cada una en su casa, tan cerca que podían sentir el calor de la otra.",
  S("balcony_pov", L("l_carmen_window_far", depth=1.03), cam=((0.5, 0.6, 1.05), (0.52, 0.45, 1.3)), fx=[FOG, "fireflies"]),
  amb=["night", "crickets"])
B("Cuando la ciudad dormía, los dos se asomaban. Hablaban en susurros, para que nadie los oyera. Se tomaban de las manos sobre el vacío.",
  S("hands_reach", cam=((0.4, 0.5, 1.35), (0.55, 0.48, 1.25)), fx=["dust"]),
  S("balcony_close", L("l_couple_talk"), cam=((0.5, 0.48, 1.15), (0.5, 0.46, 1.35)), fx=[FOG], w=1.2),
  sfx=[X("whisper", 0.5, -16, dur=5)])
B("Y en ese pedacito de aire, entre dos paredes de piedra… se besaban.",
  S("balcony_close", L("l_kiss_far"), cam=((0.5, 0.45, 1.25), (0.5, 0.42, 1.6)), fx=[FOG, "fireflies"]), pause=1.0)
B("Él le prometía que juntaría dinero, que se la llevaría lejos de Guanajuato, a donde nadie los conociera. Y ella le creía. Porque en ese callejón, por primera vez, alguien le hablaba de futuro.",
  S("luis_portrait", cam=((0.5, 0.45, 1.4), (0.5, 0.45, 1.2)), fx=["dust"], grade="moon"),
  S("carmen_portrait", cam=((0.5, 0.45, 1.25), (0.5, 0.44, 1.35)), fx=["dust"], grade="moon", tr="xfade", tl=0.6))
B("Abajo, Brígida vigilaba la escalera, con una vela en la mano. Cada ruido la hacía saltar.",
  S("stairs_interior", L("l_brigida", depth=1.05), cam=((0.5, 0.6, 1.1), (0.45, 0.55, 1.3)), fx=[FL, "dust"], grade="candle"),
  music="tension", music_at=2.0)
B("Un crujido de madera. Un perro que ladra a lo lejos. Unos pasos en la calle, que se detienen… y siguen.",
  S("alley_low", L("l_lamp_glow", blend="screen", anim=[{"type": "flicker", "amp": 0.2, "speed": 2}]), cam=((0.5, 0.85, 1.4), (0.5, 0.8, 1.55)), fx=[FOGL]),
  S("alley_steps", L("l_shadow_watcher", depth=1.08, opacity=[0, 0.9], fade_in=1.0), cam=((0.5, 0.55, 1.3), (0.5, 0.55, 1.45)), fx=[FOGL], w=1.2),
  sfx=[X("door", 0.2, -14), X("howl", 1.6, -16), X("footsteps", 3.2, -10, dur=3), X("sting", 6.2, -8)])
B("Durante semanas, el amor de Carmen y Luis vivió así: a sesenta y ocho centímetros de distancia… y a un solo paso de la tragedia.",
  S("balcony_close", L("l_couple_talk"), cam=((0.5, 0.45, 1.1), (0.5, 0.47, 1.3)), fx=[FOG]))
B("Pero en una casa así, los secretos no duran.",
  S("house_facade", cam=((0.5, 0.42, 1.3), (0.5, 0.4, 1.55), "in"), fx=[FOGL], out=0.8), pause=0.9)

# ======================================================================== CAP IV
B("Nadie sabe quién se lo dijo. Tal vez un criado. Tal vez un vecino que vio dos sombras juntas en los balcones.",
  S("alley_low", L("l_kiss_balc"), L("l_shadow_watcher_low", depth=1.15), cam=((0.5, 0.6, 1.1), (0.5, 0.5, 1.3)), fx=[FOGL],
    text=[T("CAPÍTULO IV|La daga", "chapter", 0.4, 4.8)], tr="fade", tl=0.8, w=1.5),
  music="dread", amb=["night", {"name": "wind", "gain": -4}])
B("Lo cierto es que una noche, el padre de Carmen no se fue a dormir. Apagó las velas de la casa, se sentó en su estudio, y sacó de un cajón una daga vieja.",
  S("father_study", L("l_father_back", depth=1.08), FLAME(0, 0), cam=((0.5, 0.5, 1.2), (0.52, 0.48, 1.45)), fx=[FL], grade="candle"),
  sfx=[X("clock", 0.0, -12, dur=6)])
B("Esperó en la oscuridad. Escuchó la ventana abrirse. Escuchó el murmullo de dos voces.",
  S("stairs_interior", cam=((0.5, 0.3, 1.3), (0.5, 0.4, 1.15)), fx=[FL], grade="cold"),
  S("alley_low", L("l_kiss_balc"), cam=((0.5, 0.45, 1.4), (0.5, 0.45, 1.55)), fx=[FOG]),
  sfx=[X("door", 2.0, -12), X("whisper", 3.6, -12, dur=3)])
B("Y entonces… subió.",
  S("stairs_interior", L("l_father_climb", depth=1.05, anim=[{"type": "drift", "dx": 0.02, "dy": -0.03}]),
    cam=((0.45, 0.6, 1.2), (0.45, 0.5, 1.35)), fx=[FL, "dust"], grade="candle"),
  pause=0.7, sfx=[X("footsteps", 0.2, -6, dur=4), X("heartbeat", 0.2, -8, dur=10, bpm=88)])
B("Imagina los escalones de madera, uno por uno. La vela apagada. La mano apretando la empuñadura.",
  S("stairs_interior", L("l_father_climb", depth=1.05), cam=((0.55, 0.45, 1.5), (0.55, 0.42, 1.7)), fx=[FL], grade="cold"),
  S("dagger_bg", cam=((0.4, 0.5, 1.5), (0.45, 0.5, 1.25)), fx=[FL], grade="candle"),
  sfx=[X("riser", 3.0, -8, dur=4)])
B("Brígida lo vio primero. Quiso gritar, quiso correr a avisar… pero él la apartó de un empujón.",
  S("door_burst", L("l_father_door", depth=1.04), cam=((0.5, 0.5, 1.15), (0.5, 0.5, 1.35)), fx=[FL, "dust"], grade="candle"),
  S("brigida_portrait", tr="flash", tl=0.3, cam=((0.5, 0.45, 1.4), (0.5, 0.45, 1.3)), fx=[SH(0, 0.6, 10)], dur=1.4),
  sfx=[X("boom", 4.9, -3), X("sting", 4.9, -5)])
B("Carmen sintió la puerta abrirse a su espalda. Se dio la vuelta.",
  S("carmen_room_red", L("l_carmen_window", depth=1.05), cam=((0.5, 0.5, 1.2), (0.5, 0.48, 1.45)), fx=[FL, SH(0, 0.4, 5)]),
  S("carmen_portrait_fear", cam=((0.5, 0.43, 1.25), (0.5, 0.42, 1.55), "in"), fx=["dust"], grade="blood"),
  sfx=[X("door", 0.0, -2), X("heartbeat", 1.0, -6, dur=4, bpm=110)])
B("Su padre estaba ahí. Con la daga en la mano. Y en los ojos, algo que ya no parecía de este mundo.",
  S("carmen_room_red", L("l_father_dagger", depth=1.04, anim=[{"type": "scale", "from": 1.0, "to": 1.06, "pivot": [0.5, 0.9]}]),
    cam=((0.5, 0.5, 1.15), (0.5, 0.45, 1.35)), fx=[FL]),
  S("father_portrait_red", tr="flash", tl=0.25, cam=((0.5, 0.42, 1.3), (0.5, 0.4, 1.6), "in"), fx=[SH(0, 0.7, 10), {"type": "pulse", "bpm": 110, "amp": 0.12}], dur=2.4),
  sfx=[X("sting", 4.0, -2), X("boom", 4.0, -4)])
B("Luis, desde su balcón, lo vio todo, sin poder cruzar. Sesenta y ocho centímetros… y de pronto eran un abismo.",
  S("alley_low_red", L("l_luis_balc"), cam=((0.6, 0.45, 1.5), (0.6, 0.45, 1.7)), fx=[FOG]),
  S("alley_low_red", L("l_luis_balc"), cam=((0.5, 0.7, 1.05), (0.5, 0.5, 1.25)), fx=[FOG, "ash"]),
  music="climax", sfx=[X("riser", 2.5, -6, dur=5)])
B("La hoja brilló una sola vez.",
  S("dagger_bg", cam=((0.5, 0.5, 1.6), (0.5, 0.5, 1.8), "linear"), fx=[FL], grade="blood", dur=2.2),
  S("alley_low_red", tr="flash", tl=0.2, cam=((0.5, 0.45, 1.3), (0.5, 0.45, 1.35)), fx=[SH(0, 0.8, 12)], dur=1.6),
  pause=0.3, sfx=[X("whoosh", 1.6, -4), X("sting", 2.2, -1), X("boom", 2.2, -2)])
B("",
  S("empty_balcony", cam=((0.5, 0.5, 1.2), (0.5, 0.5, 1.3)), fx=[FOG], grade="cold", tr="fade", tl=0.5),
  pause=3.0, music="silence", amb=["wind"])
B("Cuando el padre bajó la mirada, entendió lo que había hecho. Pero ya era tarde.",
  S("carmen_room_red", L("l_father_dagger"), cam=((0.5, 0.35, 1.5), (0.5, 0.38, 1.35)), fx=[FL], grade="cold"),
  music="sad")
B("Carmen se había quedado en el balcón, con el brazo extendido hacia el otro lado del callejón.",
  S("hand_kiss", cam=((0.35, 0.5, 1.3), (0.45, 0.5, 1.15)), fx=["dust"], grade="cold"))
B("Y Luis, del otro lado, seguía sosteniendo su mano.",
  S("hands_reach", cam=((0.5, 0.5, 1.5), (0.5, 0.5, 1.75)), fx=["dust"], grade="cold"), pause=0.9)
B("Cuentan que no la soltó. Que se quedó ahí, en la oscuridad, y le dio un último beso en la mano… mientras la ciudad entera dormía.",
  S("hand_kiss", cam=((0.55, 0.45, 1.5), (0.55, 0.45, 1.2)), fx=["dust", FOG], grade="cold", w=1.3),
  S("gto_panorama", cam=((0.5, 0.5, 1.05), (0.5, 0.5, 1.15)), fx=[FOGL], grade="cold",
    text=[T("EL ÚLTIMO BESO", "big", 0.4, 3.6)], out=1.2),
  pause=1.4, sfx=[X("bell", 6.0, -12, freq=120)])

# ======================================================================== CAP V
B("Lo que pasó después, nadie lo cuenta igual.",
  S("gto_dawn", cam=((0.4, 0.5, 1.2), (0.55, 0.5, 1.05)), fx=[FOGL],
    text=[T("CAPÍTULO V|Lo que queda en el callejón", "chapter", 0.4, 4.6)], tr="fade", tl=1.0, w=1.5),
  music="mystery", amb=[{"name": "wind", "gain": -6}, "city"])
B("Hay otra versión, que se cuenta menos: que Carmen no murió esa noche, sino que su padre la mandó lejos, a un convento, y que Luis la buscó por todos los caminos de la Nueva España sin encontrarla. Pero la versión que repiten los guanajuatenses… es la de la daga.",
  S("temple_facade", cam=((0.5, 0.5, 1.2), (0.5, 0.45, 1.05)), fx=[FOGL], grade="cold"),
  S("dagger_bg", cam=((0.5, 0.5, 1.15), (0.55, 0.5, 1.3)), fx=[FL], grade="candle", tr="xfade", tl=0.5, w=0.6))
B("Algunos dicen que el padre terminó sus días encerrado en esa casa, hablando solo, perseguido por el ruido de una ventana que se abre.",
  S("father_study", cam=((0.5, 0.5, 1.4), (0.5, 0.5, 1.1)), fx=[FL, "dust"], grade="cold"),
  sfx=[X("door", 5.0, -12)])
B("De Luis, dicen que la tristeza lo fue apagando. Que volvió a la mina, a lo más hondo de la sierra… y que nadie lo volvió a ver salir.",
  S("mine", L("l_fog", depth=1.2, anim=[{"type": "drift", "dx": -0.04}]), cam=((0.5, 0.55, 1.3), (0.5, 0.6, 1.6), "in"), fx=["dust"], grade="cold"),
  pause=0.8)
B("Y del callejón… dicen que no se quedó vacío.",
  S("alley_low", cam=((0.5, 0.75, 1.1), (0.5, 0.5, 1.3)), fx=[FOGL]), music="dread")
B("Vecinos y guías de la ciudad cuentan que, en algunas noches sin luna, se ven dos sombras asomadas a los balcones, inclinadas una hacia la otra.",
  S("alley_low", L("l_ghosts", blend="screen", opacity=[0, 0.85], fade_in=2.0, anim=FLOAT(0.005, 5)), cam=((0.5, 0.5, 1.2), (0.5, 0.45, 1.45)), fx=[FOG, FL], grade="cold", w=1.3))
B("Y que, a veces, cuando el viento baja por la cañada, se oye una voz de mujer que repite un nombre.",
  S("balcony_close", L("l_ghosts_close", blend="screen", opacity=[0.0, 0.8], fade_in=1.5, anim=FLOAT(0.006, 4)), cam=((0.5, 0.5, 1.1), (0.45, 0.45, 1.4)), fx=[FOG], grade="cold"),
  sfx=[X("gust", 0.5, -6)])
B("Luis…",
  S("carmen_portrait_ghost", tr="flash", tl=0.3, cam=((0.5, 0.45, 1.3), (0.5, 0.42, 1.5)), fx=[FL, SH(0, 0.5, 6)], grade="cold"),
  voice="ef_dora", speed=0.72, fx="eco", pre=0.3, pause=1.2, sfx=[X("sting", 0.0, -3), X("whisper", 0.4, -10, dur=3)])
B("Ahora, lo que dice la historia.",
  S("docs", cam=((0.5, 0.5, 1.1), (0.5, 0.5, 1.25)), fx=["dust", FL], grade="sepia",
    text=[T("Guanajuato, hoy|Lo que es historia y lo que es leyenda", "date", 0.3, 3.8)]),
  music="calm", amb=["city"])
B("El callejón existe. Está en el centro de Guanajuato, a unos pasos de la Plazuela de los Ángeles, y sus balcones de verdad casi se tocan.",
  S("plazuela", cam=((0.4, 0.55, 1.2), (0.55, 0.5, 1.1)), fx=[FOGL, "dust"]),
  S("balcony_close", cam=((0.5, 0.5, 1.0), (0.5, 0.48, 1.2)), fx=[FOG], tr="xfade", tl=0.6))
B("Lo que no existe es un documento que pruebe que Carmen, Luis o su padre vivieron ahí. Su historia se fue contando de boca en boca, de abuelos a nietos, hasta volverse la leyenda más famosa de la ciudad.",
  S("docs", cam=((0.4, 0.45, 1.4), (0.6, 0.55, 1.4), "linear"), fx=["dust"], grade="sepia", w=1.2),
  S("gto_panorama", cam=((0.6, 0.5, 1.3), (0.5, 0.5, 1.1)), fx=[FOGL], tr="xfade", tl=0.6))
B("Pero hay algo que sí es real: en el Guanajuato de la plata, era común que las familias ricas arreglaran el matrimonio de sus hijas para unir fortunas. La leyenda, como tantas otras, se construyó sobre algo que de verdad pasaba.",
  S("suitor_portrait", cam=((0.5, 0.5, 1.05), (0.5, 0.45, 1.2)), fx=["dust"], grade="sepia"),
  S("coins", cam=((0.5, 0.5, 1.2), (0.5, 0.5, 1.05)), fx=["dust"], grade="sepia", tr="xfade", tl=0.6))
B("Hoy, Guanajuato es Patrimonio de la Humanidad, y ese callejón angosto es uno de los rincones más visitados de México. Las parejas hacen fila para subir sus escalones y darse un beso bajo los balcones.",
  S("gto_dawn", cam=((0.5, 0.5, 1.05), (0.6, 0.45, 1.3)), fx=[FOGL]),
  S("alley_modern", cam=((0.5, 0.6, 1.1), (0.5, 0.5, 1.3)), fx=["dust"], tr="xfade", tl=0.6, w=1.2),
  amb=["city", {"name": "wind", "gain": -10}])
B("Y aquí está lo que te prometí al principio.",
  S("alley_steps", L("l_step_glow", blend="screen"), cam=((0.5, 0.5, 1.05), (0.5, 0.62, 1.3)), fx=[FOGL]),
  music="tension")
B("La tradición dice que si subes con tu pareja y se besan en el tercer escalón, tendrán siete años de felicidad. Hay quien dice que hasta quince.",
  S("alley_steps", L("l_step_glow", blend="screen", anim=[{"type": "pulse", "amp": 0.1, "period": 2.5}]), L("l_couple_steps", depth=1.05),
    cam=((0.5, 0.65, 1.25), (0.5, 0.72, 1.55)), fx=[FOGL, "fireflies"],
    text=[T("TERCER ESCALÓN|siete años de felicidad", "big", 4.0, 8.0)], w=1.2))
B("Por eso, en ese escalón, nunca falta quien se ría nervioso… y bese a su pareja. Por si acaso.",
  S("alley_modern", cam=((0.5, 0.65, 1.4), (0.5, 0.6, 1.6)), fx=["dust"]))
B("Pero si pasas por ese escalón con tu pareja… y no la besas…",
  S("alley_low", cam=((0.5, 0.8, 1.3), (0.5, 0.75, 1.5), "in"), fx=[FOGL, {"type": "pulse", "bpm": 70, "amp": 0.1}]),
  pause=0.4, sfx=[X("heartbeat", 0.2, -8, dur=5, bpm=70), X("riser", 1.0, -6, dur=3)])
B("te esperan siete años de mala suerte.",
  S("alley_low_red", L("l_ghosts", blend="screen", opacity=[0.8, 0.8]), tr="flash", tl=0.25, cam=((0.5, 0.45, 1.4), (0.5, 0.45, 1.6)), fx=[SH(0, 0.7, 10)],
    text=[T("7 AÑOS|de mala suerte", "big", 0.3, 3.0)]),
  pause=0.9, sfx=[X("sting", 0.0, -1), X("boom", 0.0, -3)])
B("Dicen que es una forma de honrar a Carmen y a Luis. De devolverles, en cada beso, el que a ellos les quitaron.",
  S("balcony_close", L("l_kiss_far", opacity=[0.6, 0.6]), cam=((0.5, 0.45, 1.1), (0.5, 0.45, 1.35)), fx=[FOG, "fireflies"]),
  music="sad")
B("Así que, si algún día subes a ese callejón de noche, y sientes que alguien te mira desde arriba…",
  S("alley_low", L("l_ghosts", blend="screen", opacity=[0, 0.6], fade_in=2.5), cam=((0.5, 0.85, 1.2), (0.5, 0.5, 1.35)), fx=[FOGL]),
  music="dread")
B("no te detengas en el tercer escalón sin besar a quien va contigo. Porque ahí, a sesenta y ocho centímetros… alguien sigue esperando el suyo.",
  S("empty_balcony", cam=((0.5, 0.5, 1.1), (0.5, 0.55, 1.4), "in"), fx=[FOG, "dust"], grade="cold", w=1.2),
  S("carmen_portrait_ghost", tr="flash", tl=0.25, cam=((0.5, 0.42, 1.4), (0.5, 0.42, 1.55)), fx=[FL], grade="cold", dur=2.4),
  pause=1.2, sfx=[X("whisper", 1.0, -14, dur=4), X("sting", -1.5, -4)])
B("Y tú… ¿te atreverías a subir sin dar el beso? Te leo en los comentarios.",
  S("moon_sky", CLOUDS, cam=((0.5, 0.5, 1.05), (0.5, 0.45, 1.2)), fx=[FOG], tr="fade", tl=0.8),
  music="mystery")
B("En el próximo video: dos volcanes que fueron amantes. La leyenda del Popocatépetl y la Iztaccíhuatl, el guerrero que todavía vela el sueño de su princesa.",
  S("volcanoes", CLOUDS, cam=((0.5, 0.55, 1.15), (0.5, 0.5, 1.0)), fx=[FOGL, "embers"],
    text=[T("PRÓXIMO VIDEO|Popocatépetl e Iztaccíhuatl", "big", 1.0, 6.0)], out=2.0, w=1.0),
  pause=1.0, music="hope")

story = {"title": "El Callejón del Beso: la leyenda que exige un beso en el tercer escalón", "voice": "em_alex", "speed": 0.88,
         "sentence_gap": 0.24, "key": "D", "seed": 7, "grade": "night", "vignette": 0.58, "outro": 5.0,
         "music_gain": -15, "amb_gain": -21, "sfx_gain": -9, "beats": BEATS}
json.dump(story, open(os.path.join(HERE, "story.json"), "w"), ensure_ascii=False, indent=1)

# script.md
words = 0; out = ["# El Callejón del Beso — guion\n"]
for b in BEATS:
    for sc in b["scenes"]:
        for t in sc.get("text", []):
            if t["style"] in ("chapter", "title"): out.append(f"\n## {t['str'].replace('|', ' — ')}\n")
    if b["text"]:
        who = {"ef_dora": "CARMEN: ", "em_santa": "PADRE: "}.get(b.get("voice"), "")
        out.append(who + b["text"]); words += len(b["text"].split())
open(os.path.join(HERE, "script.md"), "w").write("\n\n".join(out) + "\n")
arts = sorted({l["src"] for b in BEATS for sc in b["scenes"] for l in sc["layers"]})
print(f"beats {len(BEATS)}  scenes {sum(len(b['scenes']) for b in BEATS)}  words {words}  art {len(arts)}")
print(" ".join(a[4:-4] for a in arts))
