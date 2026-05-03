from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Pokemon


def index(request):
    """Display all Pokemon"""
    pokemon_list = Pokemon.objects.all()
    return render(request, 'pokedex/index.html', {'pokemon_list': pokemon_list})


def pokemon_detail(request, pk):
    """Display a single Pokemon and its evolution line"""
    pokemon = get_object_or_404(Pokemon, pokedex_number=pk)
    evolution_line = pokemon.get_evolution_line()
    
    stats = {
        'HP': pokemon.hp,
        'Attack': pokemon.attack,
        'Defense': pokemon.defense,
        'Sp. Atk': pokemon.sp_attack,
        'Sp. Def': pokemon.sp_defense,
        'Speed': pokemon.speed,
    }
    
    context = {
        'pokemon': pokemon,
        'evolution_line': evolution_line,
        'stats': stats,
    }
    return render(request, 'pokedex/detail.html', context)
