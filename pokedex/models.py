import csv
import json
import os
import re
from functools import lru_cache
from urllib.request import Request, urlopen

from django.db import models

# Evolution chains mapping
EVOLUTION_CHAINS = {
    # Gen 1 starters
    1: [1, 2, 3],      # Bulbasaur line
    2: [1, 2, 3],
    3: [1, 2, 3],
    4: [4, 5, 6],      # Charmander line
    5: [4, 5, 6],
    6: [4, 5, 6],
    7: [7, 8, 9],      # Squirtle line
    8: [7, 8, 9],
    9: [7, 8, 9],
    # Caterpie line
    10: [10, 11, 12],
    11: [10, 11, 12],
    12: [10, 11, 12],
    # Weedle line
    13: [13, 14, 15],
    14: [13, 14, 15],
    15: [13, 14, 15],
    # Pidgey line
    16: [16, 17, 18],
    17: [16, 17, 18],
    18: [16, 17, 18],
    # Rattata line
    19: [19, 20],
    20: [19, 20],
    # Spearow line
    21: [21, 22],
    22: [21, 22],
    # Ekans line
    23: [23, 24],
    24: [23, 24],
    # Pikachu line
    25: [25, 26],
    26: [25, 26],
    # Sandshrew line
    27: [27, 28],
    28: [27, 28],
    # Nidoran lines
    29: [29, 30, 31],
    30: [29, 30, 31],
    31: [29, 30, 31],
    32: [32, 33, 34],  # Nidoran male line
    33: [32, 33, 34],
    34: [32, 33, 34],
    # More lines from Gen 1
    35: [35, 36],      # Clefairy line
    36: [35, 36],
    37: [37, 38],      # Vulpix line
    38: [37, 38],
    39: [39, 40],      # Jigglypuff line
    40: [39, 40],
    41: [41, 42],      # Zubat line
    42: [41, 42],
    43: [43, 44, 45],  # Oddish line
    44: [43, 44, 45],
    45: [43, 44, 45],
    46: [46, 47],      # Paras line
    47: [46, 47],
    48: [48, 49],      # Venonat line
    49: [48, 49],
    50: [50, 51],      # Diglett line
}


SPECIAL_NAME_MAP = {
    'mr-mime': 'mrmime',
    'mime-jr': 'mimejr',
    'farfetchd': 'farfetchd',
    'nidoran-f': 'nidoranf',
    'nidoran-m': 'nidoranm',
    'type-null': 'typenull',
    'jangmo-o': 'jangmoo',
    'hakamo-o': 'hakamoo',
    'kommo-o': 'kommoo',
    'tapu-koko': 'tapukoko',
    'tapu-lele': 'tapulele',
    'tapu-bulu': 'tapubulu',
    'tapu-fini': 'tapufini',
}


def _normalize_name(name):
    normalized = name.strip().lower()
    normalized = normalized.replace('♀', '-f').replace('♂', '-m').replace('é', 'e')
    normalized = re.sub(r"[^a-z0-9]+", "-", normalized)
    normalized = normalized.strip('-')
    return SPECIAL_NAME_MAP.get(normalized, normalized.replace('-', ''))


def _collect_species_names(chain_node, names):
    species_name = chain_node.get('species', {}).get('name')
    if species_name:
        names.append(species_name)
    for next_node in chain_node.get('evolves_to', []):
        _collect_species_names(next_node, names)


@lru_cache(maxsize=1024)
def _fetch_json(url):
    request = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urlopen(request, timeout=5) as response:
        return json.loads(response.read().decode('utf-8'))


@lru_cache(maxsize=1024)
def _fetch_evolution_species_names(pokedex_number):
    try:
        species_data = _fetch_json(f'https://pokeapi.co/api/v2/pokemon-species/{pokedex_number}/')
        evolution_url = species_data.get('evolution_chain', {}).get('url')
        if not evolution_url:
            return ()

        evolution_data = _fetch_json(evolution_url)
        names = []
        _collect_species_names(evolution_data.get('chain', {}), names)
        return tuple(names)
    except Exception:
        return ()


class Pokemon(models.Model):
    pokedex_number = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    type1 = models.CharField(max_length=50)
    type2 = models.CharField(max_length=50, blank=True)
    hp = models.IntegerField()
    attack = models.IntegerField()
    defense = models.IntegerField()
    sp_attack = models.IntegerField()
    sp_defense = models.IntegerField()
    speed = models.IntegerField()
    base_total = models.IntegerField()
    height_m = models.FloatField()
    weight_kg = models.FloatField()
    classfication = models.CharField(max_length=100)
    capture_rate = models.IntegerField()
    
    class Meta:
        ordering = ['pokedex_number']
    
    def __str__(self):
        return f"#{self.pokedex_number} {self.name}"
    
    def get_evolution_line(self):
        """Get all Pokemon in this Pokemon's evolution line."""
        # Fast local map for lines already declared in project.
        chain_ids = EVOLUTION_CHAINS.get(self.pokedex_number)
        if chain_ids:
            return Pokemon.objects.filter(pokedex_number__in=chain_ids).order_by('pokedex_number')

        species_names = _fetch_evolution_species_names(self.pokedex_number)
        if not species_names:
            return Pokemon.objects.filter(pokedex_number=self.pokedex_number)

        normalized_to_id = {
            _normalize_name(pokemon.name): pokemon.pokedex_number
            for pokemon in Pokemon.objects.only('name', 'pokedex_number')
        }
        fetched_ids = [
            normalized_to_id.get(_normalize_name(species_name))
            for species_name in species_names
        ]
        resolved_ids = [pokemon_id for pokemon_id in fetched_ids if pokemon_id is not None]

        if not resolved_ids:
            return Pokemon.objects.filter(pokedex_number=self.pokedex_number)

        return Pokemon.objects.filter(pokedex_number__in=resolved_ids).order_by('pokedex_number')
