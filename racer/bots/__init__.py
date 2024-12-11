from .bram import BrumBot
from .daniel import Racinator
from .example import SimpleBot
from .ferry import FurStappen, Schummi
from .gitplant import Lombardi
from .hein import ShadowFax
from .ivo import DaBullet
from .jerrel import DK
from .keyboard_bot import KeyboardBot
from .lewie import Gonzales
from .mahmoud import ComplicatedBot
from .matthijsfh import MatthijsRacer
from .mukunda import AutoSoori
from .niekdt import MinVerstappen
from .paul import PaulBot
from .rayman import RoadRunner, RoadSprinter
from .rein.bot import ReinzorBot

all_bots = [
    # Default bots
    KeyboardBot,
    SimpleBot,

    # Player bots
    BrumBot,
    DaBullet,
    Gonzales,
    ComplicatedBot,
    AutoSoori,
    ReinzorBot,
    DK,
    MatthijsRacer,
    FurStappen,
    Schummi,
    Racinator,
    Lombardi,
    PaulBot,
    RoadRunner,
    ShadowFax,
    MinVerstappen,
    RoadSprinter,

    # These bots are excluded because they use the unmodified default template
    # Lightyear,
    # LilRacer,
    # Bottas,

    # Banned for cheating
    # SmoothSailing,
    # PedaltotheMetal,
]
