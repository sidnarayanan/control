import yaml
import os
from dataclasses import dataclass, field
from typing import Dict


@dataclass(frozen=True)
class Config:
    config_path: str

    control_wakeword: str = "watson"
    control_indicator_entity: str = None

    listen_timeout: int = 10
    keyword_match_threshold: float = 7000.0
    hass_auth_key: str = ""
    actions: Dict = field(default_factory=dict)


_home_dir = os.path.expanduser("~")
_cfg_dir = _home_dir + "/.control/"
os.makedirs(_cfg_dir, exist_ok=True)


def get_config() -> Config:
    _cfg_path = _cfg_dir + "/config.yaml"
    kwargs = dict(config_path=_cfg_dir)
    if os.path.exists(_cfg_path):
        with open(_cfg_path) as fcfg:
            content = yaml.load(fcfg, Loader=yaml.SafeLoader)
        kwargs.update(content)

    _action_path = _cfg_dir + "/actions.yaml"
    if os.path.exists(_action_path):
        with open(_action_path) as fcfg:
            content = yaml.load(fcfg, Loader=yaml.SafeLoader)
        kwargs["actions"] = content

    cfg = Config(**kwargs)
    return cfg


global_config = get_config()


def resolve_config(other_config: Config = None) -> Config:
    return other_config or global_config
