from .example import SimpleBot
from .keyboard_bot import KeyboardBot
from .bram import BrumBot
from .ivo import DaBullet
from .jono import Lightyear
from .richard import LilRacer
from .stefan import Bottas
from .lewie import Gonzales
from .mahmoud import ComplicatedBot
from .hein import ShadowFax
from .paul import PaulBot
from .mukunda import AutoSoori
from .rein.bot import ReinzorBot
from .jerrel import DK
from .matthijsfh import MatthijsRacer
from .ferry import FurStappen, Schummi
from .rayman import RoadRunner
from .daniel import Racinator
from .gitplant import Lombardi
from .mhoogesteger import SmoothSailing, PedaltotheMetal

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

    # Non competing bots
    # RoadRunner,
    # ShadowFax,

    # These bots are excluded because they use the unmodified default template
    # Lightyear,
    # LilRacer,
    # Bottas,

    # Banned for cheating
    # SmoothSailing,
    # PedaltotheMetal,
]
