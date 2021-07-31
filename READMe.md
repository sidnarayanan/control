# Control - a simple personal voice assistant 

## Installation

```bash
$ git clone git@github.com:sidnarayanan/control.git
$ cd control
$ pip install . 
```

## Usage

There are three primary executables. `add_keyword` lets the user define a new keyword.

```bash
$ add_keyword --keyword kitchen_light --n_samples 10
# user will be asked to repeat the keyword 10 times to build a reference library
``` 

To remove an unneeded keyword:
```bash
$ remove_keyword --keyword kitchen_lights
```

The agent is started by simply calling `agent`. TODO: implement a daemon mode.


## Configuration

There are two configuration files you can create.

The first is `~/.control/config.yaml`. It overrides settings defined in `control/config.py`. The most important setting to set is `control_wakeword`, which is used to wake the agent into active-listening mode. TODO: write proper documentation.

The second is `~/.control/actions.yaml`. It is used to define [Home Assistant](https://www.home-assistant.io/getting-started) actions. For example:
```yaml
kitchen_lights:
    action: light_toggle 
    entity: lights.kitchen_lights
```
Assume the above is in your `actions.yaml`, and you have defined a `"kitchen_lights"` keyword above. Then, upon hearing the corresponding keyword, the agent will call `control.hass.light_toggle(entity="lights.kitchen_lights")`. The list of currently-supported HASS actions are available in `control/hass.py`. TODO: write proper documentation.


## Nomenclature

Control was originally named after [Stephen Fry's character](https://www.youtube.com/watch?v=QkKSRPOe72M), but it turns out that "control" is a horrible wakeword. It's too easily confused with other English words, like "hello"
