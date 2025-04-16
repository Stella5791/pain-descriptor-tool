
import pandas as pd
import tkinter as tk
from tkinter import ttk
import re

METAPHOR_THEMES = {
    "conflict": [
        "battle", "war", "fight", "enemy", "attacked", "struggle", "combat", "warrior"
    ],
    "violent_action": [
        "tearing", "ripping", "twisting", "pulling", "breaking", "crushing", "smashing", "pounding"
    ],
    "external_tools": [
        "knife", "blade", "drill", "piercing", "stabbing", "needle", "dagger", "spear"
    ],
    "weather": [
        "storm", "cloud", "wave", "fog", "rain", "wind", "lightning", "thunder", "tsunami", "whirlwind"
    ],
    "confinement": [
        "trapped", "prison", "cage", "locked", "confined", "chained", "barred", "held"
    ],
    "attacking_agents": [
        "monster", "creature", "beast", "parasite", "demon", "entity", "thing", "it"
    ],
    "weight_pressure": [
        "weight", "heavy", "load", "burden", "crushing", "pressing", "sinking", "bearing"
    ],
    "heat_temperature": [
        "fire", "burning", "molten", "scorching", "ice", "freezing", "boiling", "searing"
    ],
    "motion_violent": [
        "spinning", "crashing", "tumbling", "whirling", "jerking", "convulsing", "exploding"
    ],
    "motion_forceful": [
        "shooting", "surging", "thrusting", "radiating", "pulsing", "moving", "jolting"
    ],
    "transformative_force": [
        "blacking out", "fading", "losing consciousness", "disappearing", "melting away", "detaching"
    ],
    "death_illness": [
        "dying", "decaying", "infected", "poisoned", "rotting", "sickening", "terminal"
    ],
    "injury_medical": [
        "wounded", "broken", "bruised", "bleeding", "scarred", "fractured"
    ],
    "journey": [
        "path", "road", "going through", "stuck", "lost", "crossing", "wandering", "climbing"
    ],
    "childbirth": [
        "contractions", "pushing", "labor", "delivering", "birthing", "giving birth"
    ],
    "organic_entity": [
        "growing inside", "roots", "plant", "spreading", "infesting", "burrowing"
    ]
}
