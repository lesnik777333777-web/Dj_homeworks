from django.shortcuts import render

# База данных рецептов (как указано в задании)
DATA = {
    'omlet': {
        'яйца, шт': 2,
        'молоко, л': 0.1,
        'соль, ч.л.': 0.5,
    },
    'pasta': {
        'макароны, г': 0.3,
        'сыр, г': 0.05,
    }
}

def show_recipe(request, recipe_name):
    # 1. Получаем параметр servings из URL, по умолчанию '1'
    servings_str = request.GET.get('servings', '1')

    # 2. Преобразуем строку в число. Если передан некорректный текст, считаем как 1
    try:
        servings = int(servings_str)
        if servings < 1:
            servings = 1
    except ValueError:
        servings = 1

    # 3. Получаем базовый рецепт. Если имя не найдено, вернется пустой словарь
    base_recipe = DATA.get(recipe_name, {})

    # 4. Формируем контекст, умножая количество на число порций
    context = {
        'recipe': {
            ingredient: amount * servings
            for ingredient, amount in base_recipe.items()
        }
    }

    # 5. Отправляем данные в шаблон
    return render(request, 'recipes/recipe.html', context)

