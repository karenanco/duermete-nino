#!/usr/bin/env python
"""
Generador del fixture folclore_inicial.json para Duérmete Niño.
Genera datos iniciales de arquetipos, países y seres folclóricos.
"""

import json
import os

FIXTURE_DIR = os.path.join(
    os.path.dirname(__file__), "duermete_nino", "fixtures"
)
FIXTURE_PATH = os.path.join(FIXTURE_DIR, "folclore_inicial.json")

# ──────────────────────────────────────────────
# ARQUETIPOS (PK 1-8)
# ──────────────────────────────────────────────
arquetipos = [
    {
        "model": "duermete_nino.arquetipo",
        "pk": 1,
        "fields": {
            "nombre": "La devoradora de niños",
            "descripcion": "Figura que devora, consume o se alimenta de niños como castigo o por naturaleza.",
        },
    },
    {
        "model": "duermete_nino.arquetipo",
        "pk": 2,
        "fields": {
            "nombre": "El secuestrador de niños",
            "descripcion": "Entidad que secuestra, roba o extravía niños, generalmente como castigo por desobediencia.",
        },
    },
    {
        "model": "duermete_nino.arquetipo",
        "pk": 3,
        "fields": {
            "nombre": "El espíritu acuático que atrae niños",
            "descripcion": "Ser que habita ríos, lagos o mares y atrae o arrastra a los niños al agua.",
        },
    },
    {
        "model": "duermete_nino.arquetipo",
        "pk": 4,
        "fields": {
            "nombre": "El niño fantasma o espíritu infantil",
            "descripcion": "Espíritu de niño que interactúa con los vivos, trayendo fortuna, advertencia o consuelo.",
        },
    },
    {
        "model": "duermete_nino.arquetipo",
        "pk": 5,
        "fields": {
            "nombre": "El protector del hogar",
            "descripcion": "Entidad benevolente que protege, cuida o recompensa a los niños y sus hogares.",
        },
    },
    {
        "model": "duermete_nino.arquetipo",
        "pk": 6,
        "fields": {
            "nombre": "Las hadas que roban o cambian bebés",
            "descripcion": "Seres feéricos que sustituyen bebés humanos por criaturas mágicas.",
        },
    },
    {
        "model": "duermete_nino.arquetipo",
        "pk": 7,
        "fields": {
            "nombre": "El espíritu infantil/Pícaro",
            "descripcion": "Entidad traviesa y juguetona que interactúa con niños, a veces ayudando, a veces molestando.",
        },
    },
    {
        "model": "duermete_nino.arquetipo",
        "pk": 8,
        "fields": {
            "nombre": "El secuestrador/Castigador",
            "descripcion": "Figura que castiga rigurosamente las malas conductas mediante secuestro temporal, golpes o sustos.",
        },
    },
]

# ──────────────────────────────────────────────
# PAÍSES ~46 (PK secuencial en el orden listado)
# ──────────────────────────────────────────────
paises_data = [
    # Europa
    ("Islandia", "ISL", "EU"),
    ("Austria", "AUT", "EU"),
    ("Alemania", "DEU", "EU"),
    ("Polonia", "POL", "EU"),
    ("Chequia", "CZE", "EU"),
    ("Reino Unido", "GBR", "EU"),
    ("España", "ESP", "EU"),
    ("Escocia", "SCT", "EU"),
    ("Irlanda", "IRL", "EU"),
    ("Noruega", "NOR", "EU"),
    ("Dinamarca", "DNK", "EU"),
    ("Suecia", "SWE", "EU"),
    ("Francia", "FRA", "EU"),
    ("Italia", "ITA", "EU"),
    ("Rusia", "RUS", "EU"),
    ("Finlandia", "FIN", "EU"),
    # América Latina
    ("México", "MEX", "LA"),
    ("Argentina", "ARG", "LA"),
    ("Colombia", "COL", "LA"),
    ("Paraguay", "PRY", "LA"),
    ("Chile", "CHL", "LA"),
    ("Perú", "PER", "LA"),
    ("Cuba", "CUB", "LA"),
    ("Guatemala", "GTM", "LA"),
    ("Brasil", "BRA", "LA"),
    ("Venezuela", "VEN", "LA"),
    # Norteamérica
    ("Canadá", "CAN", "NA"),
    ("Estados Unidos", "USA", "NA"),
    # Asia
    ("Japón", "JPN", "AS"),
    ("Indonesia", "IDN", "AS"),
    ("Malasia", "MYS", "AS"),
    ("Tailandia", "THA", "AS"),
    ("India", "IND", "AS"),
    ("China", "CHN", "AS"),
    ("Emiratos Árabes", "ARE", "AS"),
    # África
    ("Sudáfrica", "ZAF", "AF"),
    ("Ghana", "GHA", "AF"),
    ("Togo", "TGO", "AF"),
    ("Benín", "BEN", "AF"),
    ("Gambia", "GMB", "AF"),
    ("Nigeria", "NGA", "AF"),
    # Oceanía
    ("Australia", "AUS", "OC"),
    ("Nueva Zelanda", "NZL", "OC"),
    ("Hawái", "HWI", "OC"),
    ("Islas Salomón", "SLB", "OC"),
    ("Groenlandia", "GRL", "OC"),
]

paises = [
    {
        "model": "duermete_nino.pais",
        "pk": i + 1,
        "fields": {
            "nombre": nombre,
            "codigo_iso": iso,
            "continente": cont,
        },
    }
    for i, (nombre, iso, cont) in enumerate(paises_data)
]

# Mapa nombre_pais -> pk
PAIS_PK = {nombre: i + 1 for i, (nombre, _, _) in enumerate(paises_data)}

# ──────────────────────────────────────────────
# SERES FOLCLÓRICOS (100 registros)
# ──────────────────────────────────────────────
# Cada entrada: (nombre, descripcion, pais_nombre, arquetipo_pk)
seres_data = [
    # ─── Europa (20 seres) ───
    (
        "Grýla",
        "Devora de forma implacable a todos los niños desobedientes durante las vísperas navideñas.",
        "Islandia",
        1,
    ),
    (
        "Jólasveinar",
        "Traviesos muchachos que bajan de la montaña durante la Navidad para gastar bromas y, si los niños se portan mal, secuestrarlos.",
        "Islandia",
        7,
    ),
    (
        "Krampus",
        "Criatura que acompaña a San Nicolás y castiga a los niños malos con cadenas y ramas de abedul.",
        "Austria",
        8,
    ),
    (
        "Perchta",
        "Entidad que castiga a los niños desobedientes abriéndoles el vientre para rellenarlos con paja.",
        "Austria",
        8,
    ),
    (
        "Baba Yaga",
        "Anciana bruja que habita en una choza sobre patas de pollo y devora a los niños que se pierden en el bosque.",
        "Rusia",
        1,
    ),
    (
        "Rübezahl",
        "Gigante de las montañas que protege a los pastores y castiga a quienes dañan la naturaleza.",
        "Polonia",
        5,
    ),
    (
        "Black Annis",
        "Bruja de cara azul con garras de hierro que devora a los niños que se acercan a su cueva en los bosques de Leicestershire.",
        "Reino Unido",
        1,
    ),
    (
        "Jenny Greenteeth",
        "Espíritu de río con dientes verdes que atrae a los niños hacia las aguas profundas para ahogarlos.",
        "Reino Unido",
        3,
    ),
    (
        "Bogeyman",
        "Ser misterioso que se esconde en armarios y debajo de camas para llevarse a los niños que no se portan bien.",
        "Reino Unido",
        2,
    ),
    (
        "El Hombre del Saco",
        "Hombre que lleva un saco al hombro para raptar a los niños que se portan mal y llevárselos lejos.",
        "España",
        2,
    ),
    (
        "Coco",
        "Monstruo que se esconde en habitaciones oscuras para llevarse a los niños que no quieren dormir.",
        "España",
        2,
    ),
    (
        "Trasgu",
        "Duende doméstico que ayuda en las tareas del hogar pero también hace travesuras si se le enfada.",
        "España",
        5,
    ),
    (
        "Nuberu",
        "Señor de las tormentas que castiga a los niños y adultos que maltratan la naturaleza lanzando rayos.",
        "España",
        8,
    ),
    (
        "Brownie",
        "Pequeño ser hogareño que realiza labores domésticas durante la noche a cambio de comida y respeto.",
        "Escocia",
        5,
    ),
    (
        "Bean Nighe",
        "Lavandera fantasma que lava las mortajas de quienes van a morir, apareciendo cerca de arroyos solitarios.",
        "Escocia",
        3,
    ),
    (
        "Selkie",
        "Foca que muda su piel para volverse humana y atrae a los niños con su canto hipnótico junto al mar.",
        "Escocia",
        3,
    ),
    (
        "Changeling",
        "Criatura feérica que las hadas dejan en lugar del bebé humano que roban de su cuna.",
        "Irlanda",
        6,
    ),
    (
        "Leshy",
        "Espíritu del bosque que confunde y secuestra a los niños que se adentran demasiado en la foresta.",
        "Rusia",
        2,
    ),
    (
        "Domovói",
        "Espíritu del hogar que protege la casa y a los niños que en ella habitan si se le respeta.",
        "Rusia",
        5,
    ),
    (
        "Tomte",
        "Gnomo anciano que cuida las granjas y protege a los niños de los peligros de la noche.",
        "Suecia",
        5,
    ),
    # ─── América Latina (20 seres) ───
    (
        "La Llorona",
        "Espíritu de madre que llora por sus hijos perdidos y vaga cerca de ríos, atrayendo a los niños con su lamento.",
        "México",
        3,
    ),
    (
        "El Cuco",
        "Monstruo que se oculta en la oscuridad para llevarse a los niños que no obedecen a sus padres.",
        "México",
        2,
    ),
    (
        "El Familiar",
        "Ser nocturno que ataca a los niños que deambulan solos por la noche, robándolos para siempre.",
        "Argentina",
        2,
    ),
    (
        "Patasola",
        "Mujer de una sola pierna que seduce a los niños en la selva para devorarlos en su guarida.",
        "Colombia",
        2,
    ),
    (
        "Madremonte",
        "Guardiana de la naturaleza que castiga a quienes dañan el bosque, especialmente a niños que maltratan animales.",
        "Colombia",
        8,
    ),
    (
        "Mohán",
        "Hechicero acuático de larga cabellera que atrae a los niños a los ríos con su canto hipnótico.",
        "Colombia",
        3,
    ),
    (
        "Pombero",
        "Duende del monte que protege a los animales y a los niños perdidos, guiándolos de vuelta a casa.",
        "Paraguay",
        5,
    ),
    (
        "Kurupí",
        "Ser de los pies hacia atrás que secuestra a los niños que se internan solos en el monte.",
        "Paraguay",
        2,
    ),
    (
        "Yasy Yateré",
        "Duende rubio de los yerbatales que atrae a los niños con silbidos y los pierde en el monte.",
        "Paraguay",
        2,
    ),
    (
        "Pihuchén",
        "Ser alado que chupa la sangre de niños indefensos durante la noche, similar a un vampiro.",
        "Chile",
        1,
    ),
    (
        "Tue-Tué",
        "Bruja que se transforma en ave nocturna y ataca a los niños malos mientras duermen.",
        "Chile",
        8,
    ),
    (
        "Trauco",
        "Duende deforme que habita en los bosques del sur y seduce o secuestra a niños descuidados.",
        "Chile",
        2,
    ),
    (
        "Fiura",
        "Mujer salvaje de largos cabellos que ataca a los niños que desobedecen a sus padres en el bosque.",
        "Chile",
        8,
    ),
    (
        "Caleuche",
        "Barco fantasma que navega por los canales del sur atrayendo a los niños con luces y música.",
        "Chile",
        3,
    ),
    (
        "Chonchón",
        "Cabeza con grandes orejas que vuela emitiendo un canto fúnebre anunciando desgracia a niños desobedientes.",
        "Chile",
        8,
    ),
    (
        "Sachamama",
        "Serpiente gigante de la amazonía que devora a todo aquel que perturbe la selva, incluyendo niños.",
        "Perú",
        1,
    ),
    (
        "Tunche",
        "Espíritu selvático que silba anunciando su presencia y secuestra a los niños que maltratan la naturaleza.",
        "Perú",
        2,
    ),
    (
        "Madre de Agua",
        "Espíritu femenino de ríos y lagunas que atrae a los niños con su belleza para sumergirlos en las aguas.",
        "Colombia",
        3,
    ),
    (
        "Duende de los Cerros",
        "Pequeño ser de los Andes que juega con los niños pero los pierde en las montañas si no lo respetan.",
        "Perú",
        2,
    ),
    (
        "Alux",
        "Pequeño duende maya que protege los hogares y las milpas, recompensando a los niños que ayudan en casa.",
        "México",
        5,
    ),
    # ─── Norteamérica (10 seres) ───
    (
        "Wendigo",
        "Espíritu devorador de los bosques fríos que posee a quienes se entregan al canibalismo, cazando niños.",
        "Canadá",
        1,
    ),
    (
        "Skinwalker",
        "Hechicero que se transforma en animal para acechar y secuestrar a niños que desobedecen las tradiciones.",
        "Estados Unidos",
        2,
    ),
    (
        "Pukwudgie",
        "Pequeño ser pícaro de la tradición algonquina que secuestra niños y juega bromas peligrosas.",
        "Estados Unidos",
        8,
    ),
    (
        "Thunderbird",
        "Ave gigante protectora que ahuyenta a los espíritus malignos y protege a los niños de las tormentas.",
        "Estados Unidos",
        5,
    ),
    (
        "Water Babies",
        "Espíritus de niños fallecidos que habitan en ríos y lagos, atrayendo a otros niños a su morada acuática.",
        "Estados Unidos",
        3,
    ),
    (
        "Rawhead",
        "Monstruo de sangre con cabeza descarnada que acecha los sótanos y armarios para llevarse a niños desobedientes.",
        "Estados Unidos",
        2,
    ),
    (
        "Tommyknocker",
        "Pequeños duendes mineros que protegen a los niños que trabajan en las minas, advirtiendo de peligros.",
        "Estados Unidos",
        5,
    ),
    (
        "Night Hag",
        "Bruja nocturna que se sienta sobre el pecho de los niños mientras duermen, causando pesadillas y parálisis.",
        "Estados Unidos",
        8,
    ),
    (
        "Jersey Devil",
        "Criatura alada que habita los bosques de Nueva Jersey y secuestra a niños que vagan solos de noche.",
        "Estados Unidos",
        2,
    ),
    (
        "Mishipeshu",
        "Pantera acuática con cuernos de ciervo que habita el Lago Superior y atrae a niños a las aguas heladas.",
        "Estados Unidos",
        3,
    ),
    # ─── Asia (20 seres) ───
    (
        "Namahage",
        "Demonios que bajan de las montañas en Año Nuevo para castigar a los niños perezosos y desobedientes.",
        "Japón",
        8,
    ),
    (
        "Kappa",
        "Duende acuático de ríos japoneses que atrae a los niños al agua y los arrastra a su guarida.",
        "Japón",
        3,
    ),
    (
        "Tengu",
        "Criatura alada mitad hombre mitad cuervo que secuestra a niños que se pierden en las montañas.",
        "Japón",
        2,
    ),
    (
        "Yuki-onna",
        "Mujer de nieve que aparece en tormentas invernales y hechiza a los niños para que la sigan a la muerte.",
        "Japón",
        8,
    ),
    (
        "Zashiki-warashi",
        "Espíritu infantil de cabello corto que trae buena fortuna a los hogares donde se le respeta.",
        "Japón",
        4,
    ),
    (
        "Aka Manto",
        "Espíritu que acecha en los baños escolares y ofrece papel rojo o azul a los niños, castigando según su elección.",
        "Japón",
        8,
    ),
    (
        "Pontianak",
        "Espíritu femenino que seduce a los hombres y roba bebés recién nacidos de sus cunas.",
        "Indonesia",
        6,
    ),
    (
        "Toyol",
        "Espíritu de bebé no nacido que es usado como sirviente para robar y asustar a niños vivos.",
        "Malasia",
        4,
    ),
    (
        "Penanggalan",
        "Cabeza voladora con vísceras colgantes que devora a niños recién nacidos y mujeres embarazadas.",
        "Malasia",
        1,
    ),
    (
        "Krasue",
        "Cabeza flotante con órganos internos expuestos que devora niños durante la noche en las aldeas.",
        "Tailandia",
        1,
    ),
    (
        "Phi Krasue",
        "Espíritu femenino flotante que se alimenta de carne y vísceras de niños descuidados.",
        "Tailandia",
        1,
    ),
    (
        "Nang Tani",
        "Espíritu femenino de los árboles de plátano que protege a los niños que juegan cerca de los templos.",
        "Tailandia",
        5,
    ),
    (
        "Rakshasa",
        "Demonio devorador de carne humana que acecha en los bosques para capturar y devorar niños.",
        "India",
        1,
    ),
    (
        "Vetala",
        "Espíritu que posee cuerpos sin vida y castiga a los niños que profanan los lugares sagrados.",
        "India",
        8,
    ),
    (
        "Jinn",
        "Ser de fuego sin humo que protege los hogares y a los niños si se les honra debidamente.",
        "Emiratos Árabes",
        5,
    ),
    (
        "Ghoul",
        "Demonio carroñero que devora niños en cementerios y lugares desolados durante la noche.",
        "Emiratos Árabes",
        1,
    ),
    (
        "Um Al Duwais",
        "Ser que azota a los niños con un látigo si se portan mal o no honran a sus padres.",
        "Emiratos Árabes",
        8,
    ),
    (
        "Huli Jing",
        "Zorro espiritual de nueve colas que seduce y extravía a los niños en los bosques encantados.",
        "China",
        2,
    ),
    (
        "Nian",
        "Bestia devoradora que emerge cada Año Nuevo para devorar niños, ahuyentada por petardos y color rojo.",
        "China",
        1,
    ),
    (
        "Mogwai",
        "Pequeños espíritus traviesos que causan problemas pero también protegen a los niños de peligros mayores.",
        "China",
        7,
    ),
    # ─── África (10 seres) ───
    (
        "Tokoloshe",
        "Duende acuático que secuestra niños que se bañan solos en ríos y lagos durante la noche.",
        "Sudáfrica",
        2,
    ),
    (
        "Grootslang",
        "Serpiente elefante gigante que habita cuevas profundas y devora niños que se aventuran en su territorio.",
        "Sudáfrica",
        1,
    ),
    (
        "Adze",
        "Bruja vampírica que se transforma en luciérnaga y devora niños pequeños durante la noche.",
        "Ghana",
        1,
    ),
    (
        "Asanbosam",
        "Criatura con ganchos de hierro por pies que cuelga de árboles para atrapar y devorar niños.",
        "Ghana",
        1,
    ),
    (
        "Sasabonsam",
        "Murciélago gigante con alas enormes que caza niños desde las copas de los árboles en la selva.",
        "Ghana",
        1,
    ),
    (
        "Abiku",
        "Espíritu de niño que nace y muere repetidamente, atormentando a sus padres con ciclos de pérdida.",
        "Nigeria",
        4,
    ),
    (
        "Mami Wata",
        "Diosa acuática de larga cabellera que atrae a los niños con su canto hacia las profundidades del río.",
        "Nigeria",
        3,
    ),
    (
        "Ninki Nanka",
        "Dragón de los pantanos que secuestra niños que se acercan demasiado a las orillas del río Gambia.",
        "Gambia",
        3,
    ),
    (
        "Impundulu",
        "Pájaro del trueno que ataca a los niños desobedientes con rayos y castigos celestiales.",
        "Sudáfrica",
        8,
    ),
    (
        "Aziza",
        "Pequeños espíritus benévolos del bosque que protegen a los niños cazadores y recolectores.",
        "Benín",
        5,
    ),
    # ─── Oceanía (10 seres) ───
    (
        "Bunyip",
        "Monstruo de los pantanos que emerge del agua para devorar niños que se acercan a sus ciénagas.",
        "Australia",
        3,
    ),
    (
        "Yara-ma-yha-who",
        "Pequeño ser rojo que cae de los árboles para succionar la sangre de niños que pasan bajo su sombra.",
        "Australia",
        2,
    ),
    (
        "Mimi",
        "Espíritus elegantes de las rocas que enseñan a los niños aborígenes a cazar y pintar.",
        "Australia",
        5,
    ),
    (
        "Taniwha",
        "Guardián acuático que protege los ríos y lagos, atrapando a niños que contaminan sus aguas.",
        "Nueva Zelanda",
        3,
    ),
    (
        "Patupaiarehe",
        "Hadas de piel pálida y cabello dorado que cambian bebés maoríes por sus propias crías.",
        "Nueva Zelanda",
        6,
    ),
    (
        "Menehune",
        "Pequeños constructores nocturnos que protegen los hogares y niños hawaiianos con su magia ancestral.",
        "Hawái",
        5,
    ),
    (
        "Mo'o",
        "Lagarto acuático gigante que atrae niños a los estanques sagrados con su canto hipnótico.",
        "Hawái",
        3,
    ),
    (
        "Kakamora",
        "Pequeños seres guerreros de las islas Salomón que viajan en cocos y juegan bromas a los niños.",
        "Islas Salomón",
        7,
    ),
    (
        "Te Wheke",
        "Pulpo gigante de ocho tentáculos que habita las profundidades y atrapa niños cerca de las costas.",
        "Nueva Zelanda",
        3,
    ),
    (
        "Tupilaq",
        "Golem de huesos y piel creado por chamanes para castigar a los niños que rompen tabúes.",
        "Groenlandia",
        8,
    ),
    # ─── Protectores Universales (10 seres) ───
    (
        "Hada Madrina",
        "Hada bondadosa que vela por los niños desde su nacimiento, concediendo dones y protección.",
        "Francia",
        5,
    ),
    (
        "Ángel de la Guarda",
        "Ser celestial asignado a cada niño para guiarlo, protegerlo y alejarlo del peligro.",
        "Italia",
        5,
    ),
    (
        "Ratón Pérez",
        "Pequeño ratón que recoge los dientes de leche caídos y deja monedas o regalos a cambio.",
        "España",
        4,
    ),
    (
        "Sandman",
        "Ser misterioso que arroja arena mágica en los ojos de los niños para inducir sueños placenteros.",
        "Alemania",
        5,
    ),
    (
        "Jack Frost",
        "Espíritu invernal travieso que pinta escarcha en los vidrios y juega con los niños en la nieve.",
        "Noruega",
        7,
    ),
    (
        "Nisse",
        "Gnomo navideño que protege las granjas y deja regalos a los niños que se han portado bien.",
        "Noruega",
        5,
    ),
    (
        "Korrigan",
        "Hada bretona que danza en círculos de piedra y cambia bebés humanos por criaturas feéricas.",
        "Francia",
        6,
    ),
    (
        "Lutín",
        "Duende de las encrucijadas que protege a los niños viajeros señalándoles el camino seguro.",
        "Francia",
        5,
    ),
    (
        "Kobold",
        "Espíritu del hogar que ayuda en las tareas domésticas y protege a los niños de accidentes.",
        "Alemania",
        5,
    ),
    (
        "Duende del Hogar",
        "Pequeño ser doméstico que cuida de los niños mientras duermen y arregla juguetes rotos.",
        "España",
        5,
    ),
]

seres = []
for i, (nombre, desc, pais_nombre, arq_pk) in enumerate(seres_data):
    pais_pk = PAIS_PK[pais_nombre]
    seres.append(
        {
            "model": "duermete_nino.serfolclorico",
            "pk": i + 1,
            "fields": {
                "nombre": nombre,
                "descripcion_breve": desc,
                "descripcion_detallada": "",
                "pais": pais_pk,
                "arquetipo": arq_pk,
            },
        }
    )

# ──────────────────────────────────────────────
# ENSAMBLAR Y GUARDAR
# ──────────────────────────────────────────────
fixture = arquetipos + paises + seres

os.makedirs(FIXTURE_DIR, exist_ok=True)
with open(FIXTURE_PATH, "w", encoding="utf-8") as f:
    json.dump(fixture, f, ensure_ascii=False, indent=2)

print(f"✓ Fixture generado: {FIXTURE_PATH}")
print(f"  Arquetipos: {len(arquetipos)}")
print(f"  Países:     {len(paises)}")
print(f"  Seres:      {len(seres)}")
print(f"  Total:      {len(fixture)}")
