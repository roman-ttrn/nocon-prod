from django.shortcuts import render, redirect
from django.contrib import messages

from .models import *
from .forms import *

# Create your views here.
def characters(req):
    if not req.user.is_authenticated:
        return redirect('home')
    
    characters_list = Character.objects.all()
    return render(req, 'lists/characters.html', {'characters': characters_list})

def create_character(request):
    if not request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = CharacterForm(request.POST, request.FILES)
        if form.is_valid():
            character = form.save(commit=False)

            # Повторная серверная проверка (на всякий случай, если кто-то подменил данные на фронте)
            stat_fields = ['danger', 'power', 'health', 'speed', 'intelligence', 'luck']
            for field in stat_fields:
                value = getattr(character, field)
                if not (1 <= value <= 100):
                    messages.error(request, f"Недопустимое значение для {field}: {value}")
                    return render(request, 'lists/character_create.html', {'form': form})
            
            if len(request.POST.get('name')) > 255:
                messages.error(request, f"Недопустимая длина имени")
                return render(request, 'lists/character_create.html', {'form': form})

            character.save()
            messages.success(request, "Персонаж успешно создан.")
            return redirect('characters')
        else:
            messages.error(request, 'Форма содержит ошибки.')
            return render(request, 'lists/character_create.html', {'form': form})

    form = CharacterForm()
    return render(request, 'lists/character_create.html', {'form': form})

def plans(req):
    if not req.user.is_authenticated:
        return redirect('home')
    plans = Plan.objects.all()
    return render(req, 'lists/plans.html', {'plans': plans})

def plan_create(request):
    if not request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = PlanForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('plans')
        else:
            messages.error(request, 'Форма содержит ошибки.')
            return redirect('plan_create')
        
    else:
        form = PlanForm()
    return render(request, 'lists/plan_form.html', {'form': form})
