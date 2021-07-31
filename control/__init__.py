from .config import get_config, Config, global_config
from .keyword import Keyword, KeywordSet
from .audio import Listener
from .hass import HASS

keywords = KeywordSet(global_config)
hass = HASS(global_config)
listener = Listener(global_config)
