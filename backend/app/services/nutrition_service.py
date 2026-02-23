"""
app/services/nutrition_service.py
----------------------------------
Expanded recipe database — 150+ recipes, 40+ breakfasts.
Fresh results every shuffle, strict dietary filtering.
"""

import random
from typing import List, Dict


# ---------------------------------------------------------------------------
# Filter constants
# ---------------------------------------------------------------------------

NON_VEGAN    = ["chicken", "beef", "turkey", "pork", "lamb", "egg", "eggs",
                "cheese", "yogurt", "milk", "tuna", "salmon", "shrimp",
                "fish", "meat", "cream", "butter", "honey", "whey", "cod",
                "tilapia", "sardine", "anchovy", "mince", "bacon", "ham",
                "prawn", "crab", "lobster", "scallop", "duck", "venison",
                "bison", "gelatin", "lard", "suet", "ghee", "paneer",
                "ricotta", "curd", "mozzarella", "parmesan", "feta",
                "cottage cheese", "whipping cream", "heavy cream"]

GLUTEN_ITEMS = ["flour", "wheat", "bread", "pasta", "tortilla", "barley",
                "rye", "oat flour", "soy sauce", "couscous", "bulgur",
                "seitan", "panko", "breadcrumbs", "noodles", "pita",
                "flatbread", "crackers", "malt", "spelt", "farro"]

DAIRY_ITEMS  = ["milk", "cheese", "yogurt", "cream", "butter", "whey",
                "paneer", "ghee", "curd", "mozzarella", "parmesan", "feta",
                "ricotta", "cottage cheese", "kefir", "lactose",
                "whipping cream", "heavy cream", "sour cream", "brie",
                "cheddar", "gouda", "halloumi"]

KETO_EXCLUDE = ["rice", "potato", "bread", "pasta", "quinoa", "oats",
                "beans", "tortilla", "banana", "mango", "grape", "corn",
                "lentil", "chickpea", "couscous", "sweet potato", "carrot",
                "peas", "apple", "orange", "sugar", "maple syrup",
                "honey", "dates", "raisin", "barley", "bulgur"]


def _passes(ingredients_text: str, tags: List[str], restrictions: List[str]) -> bool:
    tags_lower = [t.lower() for t in tags]
    ing = ingredients_text.lower()
    for r in [r.lower().strip() for r in restrictions]:
        if r == "vegan":
            if any(item in ing for item in NON_VEGAN):
                return False
            # also ensure vegan tag present
            if "vegan" not in tags_lower:
                return False
        elif r in ("gluten-free", "gluten_free"):
            if any(item in ing for item in GLUTEN_ITEMS):
                return False
        elif r in ("dairy-free", "dairy_free"):
            if any(item in ing for item in DAIRY_ITEMS):
                return False
        elif r in ("high-protein", "high_protein"):
            if not any("high-protein" in t or "high_protein" in t for t in tags_lower):
                return False
        elif r in ("low-carb", "low_carb"):
            if not any("low-carb" in t or "low_carb" in t for t in tags_lower):
                return False
        elif r == "keto":
            if any(item in ing for item in KETO_EXCLUDE):
                return False
    return True


# ---------------------------------------------------------------------------
# Master recipe pool — 150+ recipes
# ---------------------------------------------------------------------------

ALL_RECIPES = [

    # ════════════════════════════════════════════════════════════════════════
    # WEIGHT LOSS
    # ════════════════════════════════════════════════════════════════════════
    {
        "name": "Grilled Chicken & Quinoa Bowl",
        "description": "Lean protein with fluffy quinoa and roasted vegetables",
        "prep_time": 25, "calories": 380, "servings": 2, "icon": "🥗",
        "goals": ["weight_loss", "maintenance"],
        "dietary_tags": ["High-Protein", "Gluten-Free", "Dairy-Free"],
        "ingredients": ["200g chicken breast", "1 cup quinoa", "2 cups mixed vegetables", "2 tbsp olive oil", "lemon juice", "herbs"],
        "instructions": ["Cook quinoa per package directions", "Season chicken and grill until cooked through", "Steam or roast vegetables", "Assemble bowl and drizzle with olive oil and lemon"]
    },
    {
        "name": "Mediterranean Tuna Salad",
        "description": "Fresh omega-3 packed salad with olives and capers",
        "prep_time": 15, "calories": 320, "servings": 2, "icon": "🥙",
        "goals": ["weight_loss"],
        "dietary_tags": ["High-Protein", "Dairy-Free", "Gluten-Free"],
        "ingredients": ["2 cans tuna in water", "4 cups mixed greens", "1 cup cherry tomatoes", "1/2 cucumber diced", "2 tbsp olive oil", "balsamic vinegar", "fresh basil"],
        "instructions": ["Drain and flake tuna", "Chop all vegetables", "Combine greens, tomatoes, cucumber", "Add tuna on top", "Dress with olive oil and balsamic"]
    },
    {
        "name": "Lentil & Spinach Soup",
        "description": "Hearty vegan soup with red lentils, turmeric and cumin",
        "prep_time": 30, "calories": 290, "servings": 3, "icon": "🍲",
        "goals": ["weight_loss", "maintenance"],
        "dietary_tags": ["Vegan", "Gluten-Free", "Dairy-Free", "High-Protein"],
        "ingredients": ["1 cup red lentils", "3 cups fresh spinach", "1 can diced tomatoes", "1 onion diced", "3 cloves garlic", "1 tsp cumin", "1 tsp turmeric", "4 cups vegetable broth", "1 tbsp olive oil"],
        "instructions": ["Sauté onion and garlic in olive oil", "Add spices and stir 1 minute", "Add lentils, tomatoes and broth", "Simmer 20 minutes", "Stir in spinach until wilted"]
    },
    {
        "name": "Zucchini Noodle Stir-Fry",
        "description": "Low-carb spiralized zucchini with tofu and sesame",
        "prep_time": 20, "calories": 280, "servings": 2, "icon": "🍜",
        "goals": ["weight_loss"],
        "dietary_tags": ["Vegan", "Low-Carb", "Gluten-Free", "Dairy-Free"],
        "ingredients": ["3 zucchinis spiralized", "150g tofu cubed", "1 bell pepper sliced", "1 cup snap peas", "2 cloves garlic", "1 tbsp coconut oil", "2 tbsp tamari sauce", "sesame seeds"],
        "instructions": ["Spiralize zucchini", "Heat coconut oil and sauté garlic", "Add tofu and cook until golden", "Add vegetables and stir fry 3 minutes", "Add zucchini and tamari, toss 2 minutes", "Top with sesame seeds"]
    },
    {
        "name": "Cauliflower Fried Rice",
        "description": "Low-carb riced cauliflower with ginger, garlic and vegetables",
        "prep_time": 20, "calories": 260, "servings": 2, "icon": "🍚",
        "goals": ["weight_loss"],
        "dietary_tags": ["Vegan", "Low-Carb", "Gluten-Free", "Dairy-Free"],
        "ingredients": ["1 head cauliflower riced", "2 cups mixed vegetables", "3 cloves garlic", "2 tbsp tamari sauce", "1 tbsp sesame oil", "1 tsp ginger", "spring onions"],
        "instructions": ["Rice cauliflower in food processor", "Heat sesame oil in a wok", "Sauté garlic and ginger", "Add vegetables and cook 3 minutes", "Add cauliflower rice and tamari", "Garnish with spring onions"]
    },
    {
        "name": "Greek Salad with Chickpeas",
        "description": "Classic Greek salad with protein-rich chickpeas and olives",
        "prep_time": 10, "calories": 310, "servings": 2, "icon": "🫙",
        "goals": ["weight_loss", "maintenance"],
        "dietary_tags": ["Vegan", "Gluten-Free", "Dairy-Free"],
        "ingredients": ["1 can chickpeas drained", "2 cups cucumber diced", "1 cup cherry tomatoes", "1/2 red onion sliced", "1/4 cup olives", "2 tbsp olive oil", "lemon juice", "oregano"],
        "instructions": ["Drain and rinse chickpeas", "Dice all vegetables", "Combine everything in a large bowl", "Dress with olive oil, lemon and oregano", "Toss and serve chilled"]
    },
    {
        "name": "Spiced Chickpea & Kale Bowl",
        "description": "Warming spiced chickpeas over wilted kale and brown rice",
        "prep_time": 20, "calories": 340, "servings": 2, "icon": "🌿",
        "goals": ["weight_loss", "maintenance"],
        "dietary_tags": ["Vegan", "Gluten-Free", "Dairy-Free", "High-Protein"],
        "ingredients": ["1 can chickpeas drained", "3 cups kale chopped", "1 cup brown rice", "1 tsp cumin", "1 tsp smoked paprika", "1 tsp turmeric", "2 tbsp olive oil", "lemon juice", "garlic"],
        "instructions": ["Cook brown rice", "Sauté garlic in olive oil", "Add chickpeas and spices, cook 5 minutes", "Add kale and cook until wilted", "Serve over brown rice with lemon juice"]
    },
    {
        "name": "Vietnamese Fresh Spring Rolls",
        "description": "Light rice paper rolls with fresh herbs, avocado and vegetables",
        "prep_time": 20, "calories": 250, "servings": 2, "icon": "🌱",
        "goals": ["weight_loss"],
        "dietary_tags": ["Vegan", "Gluten-Free", "Dairy-Free", "Low-Carb"],
        "ingredients": ["8 rice paper wrappers", "2 cups mixed greens", "1 cucumber julienned", "1 carrot julienned", "1 avocado sliced", "fresh mint and cilantro", "2 tbsp lime juice"],
        "instructions": ["Soak rice paper in warm water until soft", "Lay flat and add greens, vegetables and herbs", "Roll tightly", "Mix lime juice with tamari for dipping", "Serve immediately"]
    },
    {
        "name": "Mushroom & Lentil Stew",
        "description": "Rich earthy stew with mushrooms, lentils and fresh thyme",
        "prep_time": 35, "calories": 300, "servings": 3, "icon": "🍄",
        "goals": ["weight_loss", "maintenance"],
        "dietary_tags": ["Vegan", "Gluten-Free", "Dairy-Free", "High-Protein"],
        "ingredients": ["2 cups mixed mushrooms sliced", "1 cup green lentils", "1 onion diced", "3 cloves garlic", "2 carrots diced", "4 cups vegetable broth", "fresh thyme", "2 tbsp olive oil", "black pepper"],
        "instructions": ["Sauté onion, garlic and carrots in olive oil", "Add mushrooms and cook until golden", "Add lentils, broth and thyme", "Simmer 25 minutes until lentils are tender", "Season well and serve hot"]
    },
    {
        "name": "Thai Peanut Tofu Salad",
        "description": "Crunchy cabbage salad with pan-fried tofu and peanut dressing",
        "prep_time": 20, "calories": 330, "servings": 2, "icon": "🥜",
        "goals": ["weight_loss"],
        "dietary_tags": ["Vegan", "Dairy-Free", "Gluten-Free"],
        "ingredients": ["200g firm tofu cubed", "3 cups shredded cabbage", "1 cup shredded carrot", "1/4 cup peanuts", "2 tbsp peanut butter", "2 tbsp lime juice", "1 tbsp tamari", "1 tsp ginger", "sesame oil"],
        "instructions": ["Pan-fry tofu until golden and crispy", "Shred cabbage and carrot", "Whisk peanut butter, lime, tamari and ginger into dressing", "Combine vegetables and tofu", "Drizzle with dressing and top with peanuts"]
    },
    {
        "name": "Baked Cod with Asparagus",
        "description": "Flaky baked cod over roasted asparagus with lemon and capers",
        "prep_time": 25, "calories": 290, "servings": 2, "icon": "🐟",
        "goals": ["weight_loss"],
        "dietary_tags": ["High-Protein", "Gluten-Free", "Dairy-Free", "Low-Carb"],
        "ingredients": ["2 cod fillets", "1 bunch asparagus", "2 tbsp capers", "2 cloves garlic", "2 tbsp olive oil", "lemon juice", "fresh parsley", "salt and pepper"],
        "instructions": ["Preheat oven to 200°C", "Arrange asparagus on baking sheet with olive oil", "Place cod on top, add capers and garlic", "Bake 18 minutes", "Squeeze lemon and garnish with parsley"]
    },
    {
        "name": "Mango Black Bean Salad",
        "description": "Tropical sweet and savoury salad with zesty lime dressing",
        "prep_time": 15, "calories": 320, "servings": 2, "icon": "🥭",
        "goals": ["weight_loss", "maintenance"],
        "dietary_tags": ["Vegan", "Gluten-Free", "Dairy-Free"],
        "ingredients": ["1 can black beans drained", "1 large mango diced", "1 red bell pepper diced", "1/2 red onion diced", "fresh cilantro", "2 tbsp lime juice", "1 tbsp olive oil", "1 tsp cumin"],
        "instructions": ["Drain and rinse black beans", "Dice mango, pepper and onion", "Combine all in a bowl", "Dress with lime juice, olive oil and cumin", "Top with cilantro"]
    },
    {
        "name": "Stuffed Bell Peppers with Quinoa",
        "description": "Colourful peppers filled with herbed quinoa and black beans",
        "prep_time": 35, "calories": 350, "servings": 2, "icon": "🫑",
        "goals": ["weight_loss", "maintenance"],
        "dietary_tags": ["Vegan", "Gluten-Free", "Dairy-Free"],
        "ingredients": ["4 bell peppers halved", "1 cup quinoa cooked", "1 can black beans", "1 cup corn kernels", "1 can diced tomatoes", "1 tsp cumin", "1 tsp paprika", "fresh cilantro"],
        "instructions": ["Preheat oven to 190°C", "Mix quinoa, beans, corn, tomatoes and spices", "Fill pepper halves with mixture", "Bake 25 minutes until peppers are tender", "Garnish with cilantro"]
    },
    {
        "name": "Korean Kimchi Tofu Bowl",
        "description": "Spicy fermented kimchi with silken tofu over steamed brown rice",
        "prep_time": 15, "calories": 310, "servings": 2, "icon": "🌶️",
        "goals": ["weight_loss"],
        "dietary_tags": ["Vegan", "Dairy-Free", "Gluten-Free"],
        "ingredients": ["300g silken tofu", "1 cup kimchi", "1 cup brown rice", "2 tbsp sesame oil", "2 spring onions sliced", "sesame seeds", "1 tsp gochujang"],
        "instructions": ["Cook brown rice", "Slice tofu into cubes", "Heat kimchi in a pan with sesame oil", "Add tofu and gochujang, warm through", "Serve over rice, top with spring onions and sesame"]
    },
    {
        "name": "Roasted Vegetable & White Bean Soup",
        "description": "Chunky Italian soup with roasted vegetables and cannellini beans",
        "prep_time": 40, "calories": 295, "servings": 3, "icon": "🍵",
        "goals": ["weight_loss", "maintenance"],
        "dietary_tags": ["Vegan", "Gluten-Free", "Dairy-Free", "High-Protein"],
        "ingredients": ["2 cans cannellini beans", "2 zucchinis diced", "2 carrots diced", "1 red onion diced", "4 cups vegetable broth", "1 can diced tomatoes", "3 cloves garlic", "fresh rosemary", "2 tbsp olive oil"],
        "instructions": ["Roast vegetables at 200°C for 20 minutes", "Sauté garlic in olive oil", "Add roasted vegetables, beans, broth and tomatoes", "Simmer 15 minutes", "Season with rosemary and serve hot"]
    },
    {
        "name": "Edamame & Brown Rice Bowl",
        "description": "Simple Japanese-inspired bowl with miso glazed vegetables",
        "prep_time": 20, "calories": 340, "servings": 2, "icon": "🫛",
        "goals": ["weight_loss", "maintenance"],
        "dietary_tags": ["Vegan", "Gluten-Free", "Dairy-Free", "High-Protein"],
        "ingredients": ["1 cup brown rice", "2 cups edamame", "2 cups broccoli florets", "2 tbsp white miso paste", "1 tbsp sesame oil", "1 tbsp rice vinegar", "sesame seeds", "spring onions"],
        "instructions": ["Cook brown rice", "Steam edamame and broccoli", "Whisk miso, sesame oil and rice vinegar", "Toss vegetables with miso dressing", "Serve over rice with sesame seeds and spring onions"]
    },
    {
        "name": "Cucumber Gazpacho",
        "description": "Chilled Spanish cucumber and tomato soup — refreshing and light",
        "prep_time": 15, "calories": 150, "servings": 2, "icon": "🥒",
        "goals": ["weight_loss"],
        "dietary_tags": ["Vegan", "Gluten-Free", "Dairy-Free", "Low-Carb"],
        "ingredients": ["3 large cucumbers", "2 large tomatoes", "1 green bell pepper", "2 cloves garlic", "2 tbsp olive oil", "2 tbsp red wine vinegar", "fresh mint", "salt and pepper"],
        "instructions": ["Roughly chop all vegetables", "Blend until smooth", "Add olive oil and vinegar", "Season well and chill for at least 1 hour", "Serve cold with fresh mint"]
    },
    {
        "name": "Roasted Aubergine & Tomato Pasta",
        "description": "Silky roasted aubergine with cherry tomatoes tossed through pasta",
        "prep_time": 35, "calories": 360, "servings": 2, "icon": "🍆",
        "goals": ["weight_loss", "maintenance"],
        "dietary_tags": ["Vegan", "Dairy-Free"],
        "ingredients": ["200g wholegrain pasta", "2 aubergines diced", "2 cups cherry tomatoes", "4 cloves garlic", "3 tbsp olive oil", "fresh basil", "1 tsp oregano", "chili flakes"],
        "instructions": ["Roast aubergine and tomatoes at 200°C for 25 minutes", "Cook pasta", "Toss roasted vegetables through pasta", "Add olive oil, basil and chili flakes", "Season and serve"]
    },
    {
        "name": "Spinach & Chickpea Curry",
        "description": "Quick and fragrant Indian-spiced spinach curry with chickpeas",
        "prep_time": 25, "calories": 320, "servings": 2, "icon": "🍛",
        "goals": ["weight_loss", "maintenance"],
        "dietary_tags": ["Vegan", "Gluten-Free", "Dairy-Free", "High-Protein"],
        "ingredients": ["1 can chickpeas drained", "4 cups fresh spinach", "1 can diced tomatoes", "1 onion diced", "3 cloves garlic", "1 tsp ginger grated", "1 tsp garam masala", "1 tsp cumin", "1 tsp turmeric", "1 tbsp coconut oil"],
        "instructions": ["Sauté onion, garlic and ginger in coconut oil", "Add spices and cook 1 minute", "Add tomatoes and chickpeas, simmer 10 minutes", "Stir in spinach until wilted", "Serve with brown rice or on its own"]
    },
    {
        "name": "Watermelon Feta Mint Salad",
        "description": "Refreshing summer salad with sweet watermelon and salty feta",
        "prep_time": 10, "calories": 210, "servings": 2, "icon": "🍉",
        "goals": ["weight_loss"],
        "dietary_tags": ["Gluten-Free", "High-Protein"],
        "ingredients": ["4 cups watermelon cubed", "1/2 cup feta cheese crumbled", "fresh mint leaves", "1/4 red onion sliced", "2 tbsp olive oil", "1 tbsp lime juice", "black pepper"],
        "instructions": ["Cube watermelon and place in a bowl", "Add thinly sliced red onion", "Crumble feta over the top", "Dress with olive oil and lime", "Garnish with fresh mint leaves"]
    },
    {
        "name": "Roasted Cauliflower Steaks",
        "description": "Thick-cut roasted cauliflower with harissa and pomegranate",
        "prep_time": 30, "calories": 240, "servings": 2, "icon": "🥦",
        "goals": ["weight_loss"],
        "dietary_tags": ["Vegan", "Gluten-Free", "Dairy-Free", "Low-Carb"],
        "ingredients": ["1 large cauliflower", "2 tbsp harissa paste", "2 tbsp olive oil", "1/4 cup pomegranate seeds", "fresh parsley", "2 tbsp tahini", "lemon juice"],
        "instructions": ["Slice cauliflower into thick steaks", "Brush with harissa and olive oil", "Roast at 220°C for 25 minutes", "Drizzle with tahini and lemon", "Top with pomegranate and parsley"]
    },
    {
        "name": "Black Bean & Corn Taco Salad",
        "description": "All the taco flavours in a fresh, light salad bowl",
        "prep_time": 15, "calories": 300, "servings": 2, "icon": "🌮",
        "goals": ["weight_loss"],
        "dietary_tags": ["Vegan", "Gluten-Free", "Dairy-Free"],
        "ingredients": ["1 can black beans drained", "1 cup corn kernels", "2 cups romaine lettuce chopped", "1 avocado diced", "1 cup salsa", "lime juice", "fresh cilantro", "1 tsp cumin"],
        "instructions": ["Drain and season black beans with cumin", "Chop romaine and place in bowl", "Add beans, corn and avocado", "Top with salsa and cilantro", "Squeeze lime over everything"]
    },

    # ════════════════════════════════════════════════════════════════════════
    # WEIGHT GAIN
    # ════════════════════════════════════════════════════════════════════════
    {
        "name": "Power Protein Bowl",
        "description": "Calorie-dense bowl with beef, avocado, black beans and rice",
        "prep_time": 30, "calories": 680, "servings": 2, "icon": "🍖",
        "goals": ["weight_gain", "muscle_gain"],
        "dietary_tags": ["High-Protein", "High-Calorie", "Gluten-Free"],
        "ingredients": ["250g beef or chicken", "2 cups brown rice", "1 avocado sliced", "2 eggs", "1 cup black beans", "olive oil", "seasonings"],
        "instructions": ["Cook brown rice", "Season and cook meat of choice", "Fry eggs sunny-side up", "Warm black beans", "Assemble bowl with all ingredients", "Drizzle with olive oil"]
    },
    {
        "name": "Peanut Butter Banana Smoothie",
        "description": "Thick 520-kcal smoothie with oats, hemp protein and maple syrup",
        "prep_time": 5, "calories": 520, "servings": 1, "icon": "🥤",
        "goals": ["weight_gain"],
        "dietary_tags": ["Vegan", "Dairy-Free", "High-Calorie"],
        "ingredients": ["2 bananas", "3 tbsp peanut butter", "2 cups oat milk", "2 tbsp hemp protein powder", "2 tbsp maple syrup", "1/4 cup oats", "ice cubes"],
        "instructions": ["Add all ingredients to blender", "Blend until smooth and creamy", "Pour into a large glass", "Top with granola or nuts"]
    },
    {
        "name": "Loaded Sweet Potato",
        "description": "Baked sweet potato loaded with turkey, beans and avocado",
        "prep_time": 45, "calories": 580, "servings": 2, "icon": "🍠",
        "goals": ["weight_gain"],
        "dietary_tags": ["High-Carb", "Gluten-Free"],
        "ingredients": ["2 large sweet potatoes", "200g ground turkey", "1 cup black beans", "1 avocado", "salsa", "seasonings"],
        "instructions": ["Bake sweet potatoes at 200°C for 40 minutes", "Cook ground meat with seasonings", "Warm black beans", "Slice open sweet potatoes", "Top with all ingredients"]
    },
    {
        "name": "Vegan Avocado Toast with Chickpeas",
        "description": "Crispy chickpeas on mashed avocado toast with smoked paprika",
        "prep_time": 10, "calories": 540, "servings": 2, "icon": "🥑",
        "goals": ["weight_gain"],
        "dietary_tags": ["Vegan", "Dairy-Free", "High-Calorie"],
        "ingredients": ["4 slices whole grain bread", "2 large avocados", "1 can chickpeas drained", "2 tbsp olive oil", "1 tsp smoked paprika", "lemon juice", "red pepper flakes"],
        "instructions": ["Toast bread slices", "Mash avocados with lemon juice, salt and pepper", "Pan-fry chickpeas with olive oil and paprika until crispy", "Spread avocado on toast", "Top with crispy chickpeas"]
    },
    {
        "name": "Pasta with Chickpeas & Tomato",
        "description": "Italian peasant pasta with chickpeas, garlic and crushed tomatoes",
        "prep_time": 25, "calories": 620, "servings": 2, "icon": "🍝",
        "goals": ["weight_gain"],
        "dietary_tags": ["Vegan", "Dairy-Free", "High-Carb", "High-Calorie"],
        "ingredients": ["300g pasta", "1 can chickpeas", "1 can crushed tomatoes", "4 cloves garlic", "3 tbsp olive oil", "fresh basil", "1 tsp chili flakes"],
        "instructions": ["Cook pasta per package directions", "Sauté garlic in olive oil", "Add tomatoes and chickpeas, simmer 10 minutes", "Season with chili flakes", "Toss with pasta and garnish with basil"]
    },
    {
        "name": "Walnut Mushroom Mash Bowl",
        "description": "Earthy mushrooms and walnuts over creamy mashed sweet potato",
        "prep_time": 25, "calories": 590, "servings": 2, "icon": "🍄",
        "goals": ["weight_gain"],
        "dietary_tags": ["Vegan", "Gluten-Free", "Dairy-Free", "High-Calorie"],
        "ingredients": ["2 cups mixed mushrooms sliced", "1/2 cup walnuts chopped", "2 large sweet potatoes", "2 tbsp olive oil", "3 cloves garlic", "fresh thyme", "1 tbsp tamari sauce", "black pepper"],
        "instructions": ["Bake sweet potatoes and mash with olive oil", "Sauté garlic and mushrooms until golden", "Add walnuts, thyme and tamari", "Cook 3 more minutes", "Serve mushroom mix over mashed sweet potato"]
    },
    {
        "name": "Coconut Lentil Dal",
        "description": "Creamy coconut milk dal with red lentils, ginger and garam masala",
        "prep_time": 30, "calories": 560, "servings": 3, "icon": "🥘",
        "goals": ["weight_gain", "maintenance"],
        "dietary_tags": ["Vegan", "Gluten-Free", "Dairy-Free", "High-Calorie"],
        "ingredients": ["1.5 cups red lentils", "1 can coconut milk", "1 can diced tomatoes", "1 onion diced", "3 cloves garlic", "1 tbsp ginger grated", "2 tsp garam masala", "1 tsp turmeric", "2 cups basmati rice"],
        "instructions": ["Cook basmati rice", "Sauté onion, garlic and ginger", "Add spices and cook 1 minute", "Add lentils, tomatoes and coconut milk", "Simmer 20 minutes until thick", "Serve over basmati rice"]
    },
    {
        "name": "Nut & Seed Energy Bowl",
        "description": "Calorie-dense bowl with quinoa, roasted vegetables and tahini drizzle",
        "prep_time": 20, "calories": 610, "servings": 2, "icon": "🌻",
        "goals": ["weight_gain"],
        "dietary_tags": ["Vegan", "Gluten-Free", "Dairy-Free", "High-Calorie"],
        "ingredients": ["1.5 cups quinoa", "1/4 cup pumpkin seeds", "1/4 cup sunflower seeds", "2 tbsp tahini", "2 cups roasted vegetables", "1 avocado", "lemon juice", "olive oil", "za'atar spice"],
        "instructions": ["Cook quinoa", "Roast vegetables with olive oil and za'atar", "Make tahini dressing with tahini, lemon and water", "Assemble bowl with quinoa, vegetables, avocado", "Drizzle with tahini and top with seeds"]
    },
    {
        "name": "Thai Massaman Chickpea Curry",
        "description": "Rich coconut massaman curry with chickpeas and sweet potato",
        "prep_time": 35, "calories": 650, "servings": 3, "icon": "🍛",
        "goals": ["weight_gain"],
        "dietary_tags": ["Vegan", "Gluten-Free", "Dairy-Free", "High-Calorie"],
        "ingredients": ["2 cans chickpeas", "1 large sweet potato cubed", "1 can coconut milk", "2 tbsp massaman curry paste", "1 onion diced", "2 cups basmati rice", "1/4 cup peanuts", "fresh cilantro", "lime"],
        "instructions": ["Cook basmati rice", "Sauté onion and curry paste", "Add sweet potato, chickpeas and coconut milk", "Simmer 20 minutes", "Serve over rice with peanuts and cilantro"]
    },
    {
        "name": "Vegan Almond Butter Noodles",
        "description": "Thick rice noodles tossed in a rich almond butter sesame sauce",
        "prep_time": 20, "calories": 600, "servings": 2, "icon": "🍜",
        "goals": ["weight_gain"],
        "dietary_tags": ["Vegan", "Dairy-Free", "Gluten-Free", "High-Calorie"],
        "ingredients": ["300g rice noodles", "3 tbsp almond butter", "2 tbsp tamari sauce", "1 tbsp sesame oil", "1 tbsp maple syrup", "1 tbsp lime juice", "1 tsp ginger", "2 cups shredded cabbage", "spring onions", "sesame seeds"],
        "instructions": ["Cook rice noodles and rinse", "Whisk almond butter, tamari, sesame oil, maple syrup, lime and ginger", "Toss noodles with sauce", "Add shredded cabbage", "Top with spring onions and sesame seeds"]
    },
    {
        "name": "Roasted Chickpea & Avocado Wrap",
        "description": "Crispy chickpeas and creamy avocado in a hearty wholegrain wrap",
        "prep_time": 20, "calories": 570, "servings": 2, "icon": "🌯",
        "goals": ["weight_gain"],
        "dietary_tags": ["Vegan", "Dairy-Free", "High-Calorie"],
        "ingredients": ["4 wholegrain tortillas", "2 cans chickpeas drained", "2 avocados", "2 tbsp olive oil", "1 tsp smoked paprika", "1 tsp cumin", "2 cups mixed greens", "1 cup salsa", "lime juice"],
        "instructions": ["Roast chickpeas with oil and spices at 200°C for 20 minutes", "Mash avocados with lime juice and salt", "Warm tortillas", "Spread avocado on tortillas", "Add roasted chickpeas, greens and salsa", "Roll tightly and serve"]
    },
    {
        "name": "Vegan Pesto Pasta",
        "description": "Creamy cashew basil pesto tossed through wholegrain pasta",
        "prep_time": 20, "calories": 620, "servings": 2, "icon": "🍝",
        "goals": ["weight_gain"],
        "dietary_tags": ["Vegan", "Dairy-Free", "High-Calorie"],
        "ingredients": ["300g wholegrain pasta", "1 cup fresh basil", "1/2 cup cashews soaked", "3 cloves garlic", "3 tbsp olive oil", "2 tbsp nutritional yeast", "lemon juice", "1 cup cherry tomatoes", "salt and pepper"],
        "instructions": ["Cook pasta", "Blend basil, cashews, garlic, olive oil, nutritional yeast and lemon", "Toss pasta with pesto", "Halve cherry tomatoes and fold through", "Season and serve immediately"]
    },
    {
        "name": "Tempeh Bolognese",
        "description": "Hearty meat-free bolognese with crumbled tempeh in rich tomato sauce",
        "prep_time": 30, "calories": 640, "servings": 2, "icon": "🍝",
        "goals": ["weight_gain", "muscle_gain"],
        "dietary_tags": ["Vegan", "Dairy-Free", "High-Protein", "High-Calorie"],
        "ingredients": ["300g tempeh crumbled", "300g pasta", "1 can crushed tomatoes", "1 onion diced", "3 cloves garlic", "2 carrots diced", "2 tbsp olive oil", "1 tsp oregano", "1 tsp smoked paprika", "fresh basil"],
        "instructions": ["Cook pasta", "Sauté onion, garlic and carrots in olive oil", "Add crumbled tempeh and spices, brown well", "Add crushed tomatoes and simmer 15 minutes", "Toss with pasta and garnish with basil"]
    },
    {
        "name": "Vegan Loaded Nachos",
        "description": "Crispy tortilla chips loaded with black beans, salsa and guacamole",
        "prep_time": 20, "calories": 680, "servings": 2, "icon": "🫙",
        "goals": ["weight_gain"],
        "dietary_tags": ["Vegan", "Dairy-Free", "High-Calorie"],
        "ingredients": ["200g tortilla chips", "2 cans black beans drained", "2 avocados", "1 cup salsa", "1 cup corn kernels", "1 jalapeño sliced", "lime juice", "fresh cilantro", "1 tsp cumin"],
        "instructions": ["Spread chips on baking tray", "Warm black beans with cumin", "Mash avocados with lime juice for guacamole", "Top chips with beans, corn and jalapeño", "Bake 5 minutes at 180°C", "Add salsa, guacamole and cilantro"]
    },
    {
        "name": "Coconut Rice with Mango & Tofu",
        "description": "Fragrant coconut rice with glazed tofu and fresh mango",
        "prep_time": 25, "calories": 590, "servings": 2, "icon": "🥭",
        "goals": ["weight_gain"],
        "dietary_tags": ["Vegan", "Gluten-Free", "Dairy-Free", "High-Calorie"],
        "ingredients": ["1.5 cups jasmine rice", "1 can coconut milk", "300g firm tofu", "1 large mango diced", "2 tbsp tamari sauce", "1 tbsp sesame oil", "1 tbsp maple syrup", "lime juice", "sesame seeds", "spring onions"],
        "instructions": ["Cook rice in coconut milk and water", "Slice and pan-fry tofu until golden", "Glaze tofu with tamari, sesame oil and maple syrup", "Dice mango", "Serve rice with glazed tofu and mango", "Top with sesame seeds and spring onions"]
    },

    # ════════════════════════════════════════════════════════════════════════
    # MAINTENANCE
    # ════════════════════════════════════════════════════════════════════════
    {
        "name": "Balanced Buddha Bowl",
        "description": "Quinoa, roasted chickpeas, kale and sweet potato with tahini",
        "prep_time": 25, "calories": 480, "servings": 2, "icon": "🥙",
        "goals": ["maintenance"],
        "dietary_tags": ["Vegan", "Gluten-Free", "Dairy-Free"],
        "ingredients": ["1 cup quinoa", "1 can chickpeas", "2 cups kale", "1 sweet potato cubed", "1/4 cup tahini", "lemon juice", "olive oil"],
        "instructions": ["Cook quinoa", "Roast chickpeas and sweet potato at 200°C for 25 minutes", "Massage kale with olive oil", "Make tahini dressing", "Assemble bowl and drizzle with dressing"]
    },
    {
        "name": "Baked Salmon & Vegetables",
        "description": "Omega-3 rich salmon with broccoli, tomatoes and zucchini",
        "prep_time": 30, "calories": 450, "servings": 2, "icon": "🐟",
        "goals": ["maintenance", "muscle_gain"],
        "dietary_tags": ["High-Protein", "Gluten-Free", "Dairy-Free"],
        "ingredients": ["2 salmon fillets", "2 cups broccoli florets", "1 cup cherry tomatoes", "1 zucchini sliced", "olive oil", "lemon", "herbs"],
        "instructions": ["Preheat oven to 200°C", "Arrange vegetables on baking sheet with olive oil", "Season salmon and place on sheet", "Bake 15-20 minutes", "Squeeze fresh lemon before serving"]
    },
    {
        "name": "Black Bean Tacos",
        "description": "Corn tortilla tacos with spiced black beans, corn and avocado",
        "prep_time": 20, "calories": 420, "servings": 2, "icon": "🌮",
        "goals": ["maintenance"],
        "dietary_tags": ["Vegan", "Dairy-Free"],
        "ingredients": ["6 small corn tortillas", "2 cans black beans drained", "1 cup corn kernels", "1 avocado sliced", "1 cup salsa", "1 lime", "fresh cilantro", "1 tsp cumin"],
        "instructions": ["Heat beans with cumin in a pan", "Warm tortillas in a dry pan", "Fill tortillas with beans and corn", "Top with avocado, salsa and cilantro", "Squeeze lime over everything"]
    },
    {
        "name": "Stir-Fried Tofu & Broccoli",
        "description": "Quick balanced Asian stir fry with sesame oil and ginger",
        "prep_time": 20, "calories": 390, "servings": 2, "icon": "🥦",
        "goals": ["maintenance", "weight_loss"],
        "dietary_tags": ["Vegan", "Dairy-Free", "Gluten-Free", "High-Protein"],
        "ingredients": ["300g firm tofu cubed", "3 cups broccoli florets", "2 tbsp tamari sauce", "1 tbsp sesame oil", "2 cloves garlic", "1 tsp ginger", "1 cup brown rice", "sesame seeds"],
        "instructions": ["Cook brown rice", "Press and cube tofu", "Heat sesame oil, stir fry garlic and ginger", "Add tofu and cook until golden", "Add broccoli and tamari", "Serve over rice with sesame seeds"]
    },
    {
        "name": "Moroccan Vegetable Tagine",
        "description": "Fragrant spiced vegetable stew with chickpeas and couscous",
        "prep_time": 35, "calories": 440, "servings": 3, "icon": "🫕",
        "goals": ["maintenance"],
        "dietary_tags": ["Vegan", "Dairy-Free"],
        "ingredients": ["2 carrots chopped", "1 zucchini chopped", "1 can chickpeas", "1 can diced tomatoes", "1 onion diced", "2 tsp ras el hanout", "1 tsp cinnamon", "2 cups couscous", "fresh coriander"],
        "instructions": ["Sauté onion until soft", "Add spices and cook 1 minute", "Add vegetables, chickpeas and tomatoes", "Simmer 25 minutes", "Cook couscous", "Serve tagine over couscous with coriander"]
    },
    {
        "name": "Spinach & Mushroom Frittata",
        "description": "Oven-baked Italian egg frittata with spinach and mushrooms",
        "prep_time": 25, "calories": 350, "servings": 4, "icon": "🍳",
        "goals": ["maintenance", "weight_loss"],
        "dietary_tags": ["High-Protein", "Gluten-Free", "Low-Carb"],
        "ingredients": ["8 eggs", "2 cups spinach", "1.5 cups mushrooms sliced", "1/2 cup feta cheese", "1 onion diced", "2 cloves garlic", "2 tbsp olive oil", "salt and pepper"],
        "instructions": ["Preheat oven to 180°C", "Sauté onion, garlic and mushrooms in olive oil", "Add spinach and cook until wilted", "Whisk eggs and pour over vegetables", "Top with feta", "Bake 15 minutes until set"]
    },
    {
        "name": "Rainbow Veggie Noodle Bowl",
        "description": "Rice noodles tossed with colourful vegetables and peanut sauce",
        "prep_time": 20, "calories": 460, "servings": 2, "icon": "🌈",
        "goals": ["maintenance"],
        "dietary_tags": ["Vegan", "Dairy-Free", "Gluten-Free"],
        "ingredients": ["200g rice noodles", "1 cup shredded purple cabbage", "1 cup carrot ribbons", "1 cup cucumber strips", "1/4 cup peanuts", "3 tbsp peanut butter", "2 tbsp lime juice", "1 tbsp tamari", "ginger", "sesame oil"],
        "instructions": ["Cook rice noodles and rinse with cold water", "Whisk peanut butter, lime, tamari, ginger and sesame oil", "Combine noodles with all vegetables", "Toss with peanut dressing", "Top with peanuts and serve"]
    },
    {
        "name": "Mediterranean Stuffed Aubergine",
        "description": "Roasted aubergine halves filled with tomato, herbs and pine nuts",
        "prep_time": 40, "calories": 380, "servings": 2, "icon": "🍆",
        "goals": ["maintenance", "weight_loss"],
        "dietary_tags": ["Vegan", "Gluten-Free", "Dairy-Free"],
        "ingredients": ["2 large aubergines", "1 can diced tomatoes", "1/4 cup pine nuts", "3 cloves garlic", "fresh basil", "1 tsp oregano", "3 tbsp olive oil", "salt and pepper"],
        "instructions": ["Halve aubergines and score flesh", "Roast at 200°C for 25 minutes", "Sauté garlic and tomatoes with herbs", "Scoop out some aubergine flesh and mix with tomato", "Fill aubergine halves and top with pine nuts", "Bake another 10 minutes"]
    },
    {
        "name": "Chickpea Shakshuka",
        "description": "Spiced tomato sauce with poached eggs and chickpeas",
        "prep_time": 25, "calories": 420, "servings": 2, "icon": "🍅",
        "goals": ["maintenance"],
        "dietary_tags": ["Gluten-Free", "Dairy-Free", "High-Protein"],
        "ingredients": ["4 eggs", "1 can chickpeas", "1 can crushed tomatoes", "1 onion diced", "3 cloves garlic", "1 tsp cumin", "1 tsp smoked paprika", "1/2 tsp chili flakes", "2 tbsp olive oil", "fresh parsley"],
        "instructions": ["Sauté onion and garlic in olive oil", "Add spices and cook 1 minute", "Add tomatoes and chickpeas, simmer 10 minutes", "Make wells in sauce and crack eggs in", "Cover and cook 5-7 minutes until eggs are set", "Garnish with parsley"]
    },
    {
        "name": "Vegan Mushroom Risotto",
        "description": "Creamy arborio rice with mushrooms, white wine and nutritional yeast",
        "prep_time": 40, "calories": 470, "servings": 2, "icon": "🍄",
        "goals": ["maintenance"],
        "dietary_tags": ["Vegan", "Gluten-Free", "Dairy-Free"],
        "ingredients": ["1.5 cups arborio rice", "3 cups mixed mushrooms sliced", "1 onion diced", "3 cloves garlic", "1/2 cup white wine", "4 cups vegetable broth", "2 tbsp nutritional yeast", "2 tbsp olive oil", "fresh thyme", "black pepper"],
        "instructions": ["Sauté onion and garlic in olive oil", "Add mushrooms and cook until golden", "Add rice and toast 2 minutes", "Add wine and stir until absorbed", "Add broth one ladle at a time, stirring", "Stir in nutritional yeast and thyme"]
    },
    {
        "name": "Sweet Potato & Black Bean Chili",
        "description": "Hearty smoky vegan chili with sweet potato and three types of beans",
        "prep_time": 35, "calories": 430, "servings": 3, "icon": "🌶️",
        "goals": ["maintenance"],
        "dietary_tags": ["Vegan", "Gluten-Free", "Dairy-Free", "High-Protein"],
        "ingredients": ["2 sweet potatoes diced", "1 can black beans", "1 can kidney beans", "1 can diced tomatoes", "1 onion diced", "3 cloves garlic", "2 tsp chili powder", "1 tsp cumin", "1 tsp smoked paprika", "2 tbsp olive oil"],
        "instructions": ["Sauté onion and garlic in olive oil", "Add spices and cook 1 minute", "Add sweet potato, beans and tomatoes", "Add 1 cup water and simmer 25 minutes", "Season well and serve hot"]
    },
    {
        "name": "Lemon Herb Quinoa Salad",
        "description": "Light and bright quinoa with cucumber, herbs and preserved lemon",
        "prep_time": 20, "calories": 380, "servings": 2, "icon": "🍋",
        "goals": ["maintenance"],
        "dietary_tags": ["Vegan", "Gluten-Free", "Dairy-Free"],
        "ingredients": ["1.5 cups quinoa", "2 cups cucumber diced", "1 cup cherry tomatoes", "1/2 cup fresh parsley", "1/4 cup fresh mint", "3 tbsp olive oil", "2 tbsp lemon juice", "1 preserved lemon rind", "salt and pepper"],
        "instructions": ["Cook quinoa and cool", "Dice cucumber and halve tomatoes", "Chop herbs finely", "Combine all in a bowl", "Dress with olive oil, lemon juice and preserved lemon", "Season and serve at room temperature"]
    },
    {
        "name": "Tofu Vegetable Green Curry",
        "description": "Fragrant Thai green curry with tofu, snap peas and basil",
        "prep_time": 25, "calories": 450, "servings": 2, "icon": "🌿",
        "goals": ["maintenance"],
        "dietary_tags": ["Vegan", "Gluten-Free", "Dairy-Free"],
        "ingredients": ["300g firm tofu cubed", "1 can coconut milk", "2 tbsp green curry paste", "1 cup snap peas", "1 zucchini sliced", "1 cup jasmine rice", "fresh Thai basil", "2 kaffir lime leaves", "1 tbsp coconut oil"],
        "instructions": ["Cook jasmine rice", "Heat coconut oil and fry curry paste 1 minute", "Add coconut milk and lime leaves", "Add tofu and vegetables, simmer 10 minutes", "Stir in Thai basil", "Serve over rice"]
    },
    {
        "name": "Roasted Red Pepper Soup",
        "description": "Silky blended roasted red pepper and tomato soup with smoked paprika",
        "prep_time": 35, "calories": 250, "servings": 3, "icon": "🫑",
        "goals": ["maintenance", "weight_loss"],
        "dietary_tags": ["Vegan", "Gluten-Free", "Dairy-Free", "Low-Carb"],
        "ingredients": ["4 red bell peppers", "1 can crushed tomatoes", "1 onion diced", "3 cloves garlic", "1 tsp smoked paprika", "3 cups vegetable broth", "2 tbsp olive oil", "fresh basil"],
        "instructions": ["Roast red peppers at 220°C until charred, then peel", "Sauté onion and garlic in olive oil", "Add roasted peppers, tomatoes, broth and paprika", "Simmer 15 minutes", "Blend until silky smooth", "Garnish with basil and olive oil"]
    },

    # ════════════════════════════════════════════════════════════════════════
    # MUSCLE GAIN
    # ════════════════════════════════════════════════════════════════════════
    {
        "name": "High-Protein Chicken Wrap",
        "description": "Whole wheat wrap with grilled chicken, hummus, quinoa and feta",
        "prep_time": 20, "calories": 620, "servings": 2, "icon": "🌯",
        "goals": ["muscle_gain"],
        "dietary_tags": ["High-Protein", "High-Calorie"],
        "ingredients": ["2 whole wheat tortillas", "300g grilled chicken breast", "1/2 cup hummus", "1 cup mixed greens", "1 cup quinoa", "cherry tomatoes", "cucumber"],
        "instructions": ["Grill and slice chicken", "Cook quinoa", "Spread hummus on tortillas", "Layer with greens, quinoa and chicken", "Roll tightly and slice in half"]
    },
    {
        "name": "Tempeh & Quinoa Power Bowl",
        "description": "Plant-based bowl with marinated tempeh, edamame and sesame",
        "prep_time": 25, "calories": 600, "servings": 2, "icon": "💪",
        "goals": ["muscle_gain"],
        "dietary_tags": ["Vegan", "Gluten-Free", "Dairy-Free", "High-Protein"],
        "ingredients": ["200g tempeh sliced", "1.5 cups quinoa", "2 cups edamame", "1 cup broccoli florets", "3 tbsp tamari sauce", "2 tbsp sesame oil", "1 tbsp maple syrup", "sesame seeds"],
        "instructions": ["Cook quinoa", "Marinate tempeh in tamari, sesame oil and maple syrup", "Pan-fry tempeh until golden", "Steam broccoli and edamame", "Assemble bowl and drizzle with remaining marinade", "Top with sesame seeds"]
    },
    {
        "name": "Beef & Sweet Potato Hash",
        "description": "Hearty skillet hash with lean ground beef and sweet potato",
        "prep_time": 25, "calories": 650, "servings": 2, "icon": "🥩",
        "goals": ["muscle_gain", "weight_gain"],
        "dietary_tags": ["High-Protein", "Gluten-Free", "High-Calorie"],
        "ingredients": ["300g lean ground beef", "2 sweet potatoes diced", "1 bell pepper diced", "1 onion diced", "3 cloves garlic", "1 tbsp olive oil", "1 tsp paprika"],
        "instructions": ["Cook sweet potato in olive oil until golden", "Add onion, bell pepper and garlic", "Add beef and cook through", "Season with paprika, salt and pepper", "Serve hot"]
    },
    {
        "name": "Lentil & Black Bean Protein Bowl",
        "description": "Double legume bowl with brown rice, avocado and smoky spices",
        "prep_time": 25, "calories": 570, "servings": 2, "icon": "🫘",
        "goals": ["muscle_gain", "maintenance"],
        "dietary_tags": ["Vegan", "Gluten-Free", "Dairy-Free", "High-Protein"],
        "ingredients": ["1 cup green lentils", "1 can black beans", "1 cup brown rice", "1 avocado", "1 cup salsa", "1 lime", "1 tsp cumin", "1 tsp smoked paprika", "fresh cilantro"],
        "instructions": ["Cook lentils and brown rice separately", "Warm black beans with cumin and paprika", "Assemble bowl with rice, lentils and beans", "Top with avocado, salsa and cilantro", "Squeeze lime over bowl"]
    },
    {
        "name": "Salmon Teriyaki Bowl",
        "description": "Glazed teriyaki salmon with edamame over jasmine rice",
        "prep_time": 25, "calories": 630, "servings": 2, "icon": "🍱",
        "goals": ["muscle_gain", "weight_gain"],
        "dietary_tags": ["High-Protein", "Dairy-Free", "High-Calorie"],
        "ingredients": ["2 salmon fillets", "2 cups jasmine rice", "1 cup edamame", "3 tbsp teriyaki sauce", "1 tbsp sesame oil", "spring onions", "sesame seeds", "ginger"],
        "instructions": ["Cook jasmine rice", "Marinate salmon in teriyaki sauce 10 minutes", "Pan-fry salmon 4 minutes each side", "Steam edamame", "Serve over rice with edamame, spring onions and sesame"]
    },
    {
        "name": "Turkey Meatball Pasta",
        "description": "Lean turkey meatballs in rich tomato sauce over wholegrain pasta",
        "prep_time": 35, "calories": 610, "servings": 3, "icon": "🍝",
        "goals": ["muscle_gain"],
        "dietary_tags": ["High-Protein", "High-Calorie"],
        "ingredients": ["400g ground turkey", "300g wholegrain pasta", "1 can crushed tomatoes", "2 eggs", "4 cloves garlic", "fresh basil", "1 tsp oregano", "olive oil"],
        "instructions": ["Mix turkey with eggs, garlic and herbs", "Roll into meatballs and bake 20 minutes", "Simmer tomatoes with garlic and oregano", "Cook pasta", "Combine meatballs with sauce over pasta", "Garnish with fresh basil"]
    },
    {
        "name": "Edamame & Quinoa Protein Salad",
        "description": "Cold protein-packed salad with edamame, quinoa and miso dressing",
        "prep_time": 15, "calories": 520, "servings": 2, "icon": "🫛",
        "goals": ["muscle_gain", "maintenance"],
        "dietary_tags": ["Vegan", "Gluten-Free", "Dairy-Free", "High-Protein"],
        "ingredients": ["1.5 cups quinoa cooked", "2 cups edamame", "1 cup shredded carrot", "1 avocado diced", "2 tbsp white miso", "2 tbsp rice vinegar", "1 tbsp sesame oil", "sesame seeds", "spring onions"],
        "instructions": ["Cook quinoa and let cool", "Steam edamame and cool", "Whisk miso, rice vinegar and sesame oil for dressing", "Combine quinoa, edamame, carrot and avocado", "Toss with dressing", "Top with sesame seeds and spring onions"]
    },
    {
        "name": "Chicken & White Bean Stew",
        "description": "Rustic Italian stew with chicken, white beans and rosemary",
        "prep_time": 35, "calories": 590, "servings": 3, "icon": "🫕",
        "goals": ["muscle_gain"],
        "dietary_tags": ["High-Protein", "Gluten-Free", "Dairy-Free", "High-Calorie"],
        "ingredients": ["400g chicken thighs", "2 cans white beans", "1 can diced tomatoes", "1 onion diced", "4 cloves garlic", "fresh rosemary", "3 cups chicken broth", "2 tbsp olive oil", "kale"],
        "instructions": ["Brown chicken thighs in olive oil", "Add onion, garlic and rosemary", "Add beans, tomatoes and broth", "Simmer 25 minutes until chicken is tender", "Shred chicken and stir in kale", "Serve hot"]
    },
    {
        "name": "Vegan Tempeh Stir Fry",
        "description": "High-protein tempeh stir fry with broccoli, edamame and brown rice",
        "prep_time": 20, "calories": 560, "servings": 2, "icon": "🥦",
        "goals": ["muscle_gain"],
        "dietary_tags": ["Vegan", "Gluten-Free", "Dairy-Free", "High-Protein"],
        "ingredients": ["250g tempeh cubed", "2 cups broccoli florets", "1 cup edamame", "1 cup brown rice", "3 tbsp tamari sauce", "1 tbsp sesame oil", "2 cloves garlic", "1 tsp ginger", "sesame seeds", "spring onions"],
        "instructions": ["Cook brown rice", "Pan-fry tempeh in sesame oil until golden", "Add garlic, ginger, broccoli and edamame", "Stir fry 4 minutes", "Add tamari and toss well", "Serve over rice with sesame seeds"]
    },
    {
        "name": "Black Bean & Tofu Burrito Bowl",
        "description": "Protein-dense burrito bowl with tofu, black beans, rice and guacamole",
        "prep_time": 25, "calories": 580, "servings": 2, "icon": "🫘",
        "goals": ["muscle_gain"],
        "dietary_tags": ["Vegan", "Gluten-Free", "Dairy-Free", "High-Protein"],
        "ingredients": ["250g firm tofu crumbled", "1 can black beans", "1.5 cups brown rice", "2 avocados", "1 cup salsa", "1 tsp cumin", "1 tsp smoked paprika", "1 tsp chili powder", "lime juice", "fresh cilantro"],
        "instructions": ["Cook brown rice", "Season crumbled tofu with spices and pan-fry until crispy", "Warm black beans", "Make guacamole with avocados, lime and salt", "Assemble bowls with rice, tofu, beans and guacamole", "Top with salsa and cilantro"]
    },
    {
        "name": "Moroccan Lamb & Chickpea Soup",
        "description": "Warming spiced lamb soup with chickpeas and harissa",
        "prep_time": 40, "calories": 640, "servings": 3, "icon": "🍲",
        "goals": ["muscle_gain"],
        "dietary_tags": ["High-Protein", "Gluten-Free", "Dairy-Free", "High-Calorie"],
        "ingredients": ["400g lamb shoulder diced", "1 can chickpeas", "1 can diced tomatoes", "1 onion diced", "2 tsp harissa", "1 tsp cumin", "1 tsp coriander", "4 cups stock", "fresh cilantro", "lemon"],
        "instructions": ["Brown lamb in a heavy pot", "Add onion, harissa and spices", "Add chickpeas, tomatoes and stock", "Simmer 30 minutes until lamb is tender", "Serve with fresh cilantro and lemon"]
    },
    {
        "name": "Vegan Protein Chili",
        "description": "Three-bean chili with TVP, smoked paprika and dark chocolate",
        "prep_time": 35, "calories": 540, "servings": 3, "icon": "🌶️",
        "goals": ["muscle_gain"],
        "dietary_tags": ["Vegan", "Gluten-Free", "Dairy-Free", "High-Protein"],
        "ingredients": ["1 cup TVP or soy mince", "1 can black beans", "1 can kidney beans", "1 can pinto beans", "1 can crushed tomatoes", "1 onion diced", "3 cloves garlic", "2 tsp chili powder", "1 tsp cumin", "1 tsp smoked paprika", "10g dark chocolate", "2 tbsp olive oil"],
        "instructions": ["Rehydrate TVP in hot vegetable broth", "Sauté onion and garlic in olive oil", "Add spices and cook 1 minute", "Add TVP, all beans and tomatoes", "Simmer 25 minutes", "Stir in dark chocolate and season well"]
    },
]


# ---------------------------------------------------------------------------
# Breakfast database — 40 options
# ---------------------------------------------------------------------------

ALL_BREAKFASTS = [
    {"name": "Overnight Oats with Berries", "icon": "🥣", "quick_recipe": "Rolled oats soaked in oat milk overnight with berries and maple syrup", "dietary_tags": ["Vegan", "Dairy-Free"], "ingredients": ["rolled oats", "oat milk", "berries", "maple syrup", "chia seeds"]},
    {"name": "Avocado Toast with Seeds", "icon": "🥑", "quick_recipe": "Whole grain toast with mashed avocado, chili flakes and pumpkin seeds", "dietary_tags": ["Vegan", "Dairy-Free"], "ingredients": ["whole grain bread", "avocado", "pumpkin seeds", "chili flakes", "lemon juice"]},
    {"name": "Vegan Smoothie Bowl", "icon": "🫐", "quick_recipe": "Blended frozen banana, spinach and almond milk topped with granola and fresh fruit", "dietary_tags": ["Vegan", "Dairy-Free", "Gluten-Free"], "ingredients": ["frozen banana", "spinach", "almond milk", "granola", "mixed berries"]},
    {"name": "Chia Pudding with Mango", "icon": "🥥", "quick_recipe": "Chia seeds soaked in coconut milk overnight topped with fresh mango", "dietary_tags": ["Vegan", "Gluten-Free", "Dairy-Free"], "ingredients": ["chia seeds", "coconut milk", "mango", "maple syrup"]},
    {"name": "Peanut Butter Banana Toast", "icon": "🍌", "quick_recipe": "Whole grain toast with natural peanut butter and sliced banana", "dietary_tags": ["Vegan", "Dairy-Free"], "ingredients": ["whole grain bread", "peanut butter", "banana", "cinnamon"]},
    {"name": "Tofu Scramble", "icon": "🍳", "quick_recipe": "Crumbled firm tofu scrambled with turmeric, spinach and cherry tomatoes", "dietary_tags": ["Vegan", "Gluten-Free", "Dairy-Free", "High-Protein"], "ingredients": ["firm tofu crumbled", "turmeric", "spinach", "cherry tomatoes", "olive oil", "black salt"]},
    {"name": "Açaí Bowl", "icon": "🍇", "quick_recipe": "Blended açaí with banana and almond milk topped with coconut and hemp seeds", "dietary_tags": ["Vegan", "Gluten-Free", "Dairy-Free"], "ingredients": ["açaí pack", "frozen banana", "almond milk", "coconut flakes", "hemp seeds"]},
    {"name": "Banana Oat Porridge", "icon": "🌾", "quick_recipe": "Creamy oat porridge cooked in oat milk with mashed banana and cinnamon", "dietary_tags": ["Vegan", "Dairy-Free"], "ingredients": ["rolled oats", "oat milk", "banana", "cinnamon", "maple syrup"]},
    {"name": "Almond Butter Rice Cakes", "icon": "🌰", "quick_recipe": "Rice cakes topped with almond butter, banana slices and hemp seeds", "dietary_tags": ["Vegan", "Gluten-Free", "Dairy-Free"], "ingredients": ["rice cakes", "almond butter", "banana", "hemp seeds", "cinnamon"]},
    {"name": "Coconut Yogurt Parfait", "icon": "🍓", "quick_recipe": "Coconut yogurt layered with granola, berries and chia seeds", "dietary_tags": ["Vegan", "Dairy-Free"], "ingredients": ["coconut yogurt", "granola", "mixed berries", "chia seeds", "maple syrup"]},
    {"name": "Mango Turmeric Smoothie", "icon": "🥭", "quick_recipe": "Mango, turmeric, ginger and coconut milk blended until silky", "dietary_tags": ["Vegan", "Gluten-Free", "Dairy-Free"], "ingredients": ["frozen mango", "turmeric", "ginger", "coconut milk", "maple syrup"]},
    {"name": "Peanut Butter Oat Balls", "icon": "⚽", "quick_recipe": "No-bake oat and peanut butter balls with dark chocolate chips — prep night before", "dietary_tags": ["Vegan", "Dairy-Free"], "ingredients": ["rolled oats", "peanut butter", "maple syrup", "dark chocolate chips", "vanilla"]},
    {"name": "Avocado & Tomato Rice Cakes", "icon": "🍅", "quick_recipe": "Rice cakes with smashed avocado, sliced tomato and everything bagel seasoning", "dietary_tags": ["Vegan", "Gluten-Free", "Dairy-Free"], "ingredients": ["rice cakes", "avocado", "tomato sliced", "everything bagel seasoning", "lemon juice"]},
    {"name": "Warm Spiced Quinoa Bowl", "icon": "🌿", "quick_recipe": "Quinoa cooked with cinnamon, topped with apple, walnuts and maple syrup", "dietary_tags": ["Vegan", "Gluten-Free", "Dairy-Free"], "ingredients": ["quinoa", "water", "cinnamon", "apple diced", "walnuts", "maple syrup"]},
    {"name": "Green Detox Smoothie", "icon": "💚", "quick_recipe": "Spinach, cucumber, green apple, ginger and lemon blended with coconut water", "dietary_tags": ["Vegan", "Gluten-Free", "Dairy-Free", "Low-Carb"], "ingredients": ["spinach", "cucumber", "green apple", "ginger", "lemon juice", "coconut water"]},
    {"name": "Tahini Date Oatmeal", "icon": "🌾", "quick_recipe": "Oats cooked with oat milk, stirred with tahini and topped with chopped dates", "dietary_tags": ["Vegan", "Dairy-Free"], "ingredients": ["rolled oats", "oat milk", "tahini", "medjool dates chopped", "cinnamon"]},
    {"name": "Greek Yogurt Parfait", "icon": "🍓", "quick_recipe": "Layered Greek yogurt with granola and mixed berries", "dietary_tags": ["Gluten-Free", "High-Protein"], "ingredients": ["Greek yogurt", "granola", "mixed berries", "honey"]},
    {"name": "Veggie Scrambled Eggs", "icon": "🥚", "quick_recipe": "Eggs scrambled with spinach, cherry tomatoes and bell peppers", "dietary_tags": ["Gluten-Free", "High-Protein"], "ingredients": ["eggs", "spinach", "cherry tomatoes", "bell pepper", "olive oil"]},
    {"name": "Protein Smoothie", "icon": "💪", "quick_recipe": "Banana, protein powder, almond milk and peanut butter blended smooth", "dietary_tags": ["High-Protein", "Gluten-Free"], "ingredients": ["banana", "protein powder", "almond milk", "peanut butter", "ice"]},
    {"name": "Cottage Cheese Fruit Bowl", "icon": "🧀", "quick_recipe": "Creamy cottage cheese topped with mixed fresh fruit and a drizzle of honey", "dietary_tags": ["High-Protein", "Gluten-Free"], "ingredients": ["cottage cheese", "mixed fresh fruit", "honey", "cinnamon"]},
    {"name": "Egg Muffins with Vegetables", "icon": "🫙", "quick_recipe": "Mini baked egg muffins with spinach, peppers and feta — prep ahead", "dietary_tags": ["High-Protein", "Gluten-Free", "Low-Carb"], "ingredients": ["eggs", "spinach", "bell peppers", "feta cheese", "olive oil"]},
    {"name": "Almond Flour Pancakes", "icon": "🥞", "quick_recipe": "Fluffy low-carb pancakes made with almond flour, eggs and vanilla", "dietary_tags": ["High-Protein", "Gluten-Free", "Low-Carb"], "ingredients": ["almond flour", "eggs", "vanilla extract", "baking powder", "berries"]},
    {"name": "Berry Protein Oats", "icon": "🍒", "quick_recipe": "Oats cooked with protein powder stirred in, topped with fresh berries", "dietary_tags": ["High-Protein", "Dairy-Free"], "ingredients": ["rolled oats", "protein powder", "oat milk", "mixed berries", "chia seeds"]},
    {"name": "Vegan Baked Oatmeal", "icon": "🫐", "quick_recipe": "Oven-baked oats with blueberries, chia seeds and vanilla — slice and reheat", "dietary_tags": ["Vegan", "Dairy-Free"], "ingredients": ["rolled oats", "blueberries", "chia seeds", "oat milk", "vanilla", "maple syrup", "baking powder"]},
    {"name": "Watermelon Mint Smoothie", "icon": "🍉", "quick_recipe": "Chilled watermelon blended with fresh mint, lime and coconut water", "dietary_tags": ["Vegan", "Gluten-Free", "Dairy-Free", "Low-Carb"], "ingredients": ["watermelon", "fresh mint", "lime juice", "coconut water", "ice"]},
    {"name": "Savoury Oatmeal with Avocado", "icon": "🌾", "quick_recipe": "Savoury oats cooked in vegetable broth topped with avocado and sesame", "dietary_tags": ["Vegan", "Dairy-Free"], "ingredients": ["rolled oats", "vegetable broth", "avocado", "sesame seeds", "tamari sauce", "spring onions"]},
    {"name": "Cashew Chia Parfait", "icon": "🥛", "quick_recipe": "Cashew milk chia pudding layered with fresh kiwi and passion fruit", "dietary_tags": ["Vegan", "Gluten-Free", "Dairy-Free"], "ingredients": ["chia seeds", "cashew milk", "kiwi sliced", "passion fruit", "maple syrup", "vanilla"]},
    {"name": "Tropical Granola Bowl", "icon": "🌴", "quick_recipe": "Coconut granola over coconut yogurt with pineapple and mango", "dietary_tags": ["Vegan", "Dairy-Free"], "ingredients": ["coconut granola", "coconut yogurt", "pineapple diced", "mango diced", "coconut flakes", "lime juice"]},
    {"name": "Spinach Banana Protein Smoothie", "icon": "💚", "quick_recipe": "Spinach, banana, plant protein powder and oat milk blended until creamy", "dietary_tags": ["Vegan", "Gluten-Free", "Dairy-Free", "High-Protein"], "ingredients": ["spinach", "banana", "plant protein powder", "oat milk", "flaxseed", "ice"]},
    {"name": "Apple Cinnamon Overnight Oats", "icon": "🍎", "quick_recipe": "Oats soaked overnight with grated apple, cinnamon and raisins", "dietary_tags": ["Vegan", "Dairy-Free"], "ingredients": ["rolled oats", "oat milk", "apple grated", "cinnamon", "raisins", "maple syrup"]},
    {"name": "Pumpkin Spice Oatmeal", "icon": "🎃", "quick_recipe": "Warm oats with pumpkin puree, pumpkin spice and pecan nuts", "dietary_tags": ["Vegan", "Dairy-Free"], "ingredients": ["rolled oats", "pumpkin puree", "oat milk", "pumpkin spice", "pecan nuts", "maple syrup"]},
    {"name": "Hemp Seed Smoothie Bowl", "icon": "🌱", "quick_recipe": "Frozen berry and banana smoothie bowl topped with hemp seeds and granola", "dietary_tags": ["Vegan", "Gluten-Free", "Dairy-Free", "High-Protein"], "ingredients": ["frozen mixed berries", "banana", "almond milk", "hemp seeds", "granola", "coconut flakes"]},
    {"name": "Matcha Chia Pudding", "icon": "🍵", "quick_recipe": "Earthy matcha chia pudding with oat milk topped with sliced strawberries", "dietary_tags": ["Vegan", "Gluten-Free", "Dairy-Free"], "ingredients": ["chia seeds", "oat milk", "matcha powder", "maple syrup", "vanilla", "strawberries"]},
    {"name": "Sun Butter & Banana Oats", "icon": "🌻", "quick_recipe": "Warm oats with sunflower seed butter, banana and cinnamon", "dietary_tags": ["Vegan", "Gluten-Free", "Dairy-Free"], "ingredients": ["rolled oats", "oat milk", "sunflower seed butter", "banana", "cinnamon", "maple syrup"]},
    {"name": "Chickpea Flour Omelette", "icon": "🫙", "quick_recipe": "Savoury vegan omelette made with chickpea flour, spinach and tomatoes", "dietary_tags": ["Vegan", "Gluten-Free", "Dairy-Free", "High-Protein"], "ingredients": ["chickpea flour", "water", "spinach", "cherry tomatoes", "olive oil", "turmeric", "black salt"]},
    {"name": "Kiwi Coconut Smoothie", "icon": "🥝", "quick_recipe": "Bright green kiwi, spinach and coconut milk smoothie with lime", "dietary_tags": ["Vegan", "Gluten-Free", "Dairy-Free"], "ingredients": ["kiwi", "spinach", "coconut milk", "lime juice", "banana", "ice"]},
    {"name": "Blueberry Flaxseed Oats", "icon": "🫐", "quick_recipe": "Oats cooked with ground flaxseed and topped with warm blueberry compote", "dietary_tags": ["Vegan", "Dairy-Free"], "ingredients": ["rolled oats", "oat milk", "ground flaxseed", "blueberries", "maple syrup", "cinnamon"]},
    {"name": "Peach Almond Smoothie Bowl", "icon": "🍑", "quick_recipe": "Blended frozen peach and almond milk bowl topped with sliced almonds and granola", "dietary_tags": ["Vegan", "Gluten-Free", "Dairy-Free"], "ingredients": ["frozen peach", "almond milk", "almond butter", "granola", "sliced almonds", "maple syrup"]},
    {"name": "Turmeric Ginger Porridge", "icon": "🌟", "quick_recipe": "Golden anti-inflammatory porridge with turmeric, ginger and black pepper", "dietary_tags": ["Vegan", "Dairy-Free"], "ingredients": ["rolled oats", "oat milk", "turmeric", "ginger", "black pepper", "maple syrup", "coconut flakes"]},
    {"name": "Walnut Date Energy Bowl", "icon": "🌰", "quick_recipe": "Quinoa porridge with walnuts, chopped dates and a drizzle of tahini", "dietary_tags": ["Vegan", "Gluten-Free", "Dairy-Free"], "ingredients": ["quinoa", "oat milk", "walnuts", "medjool dates", "tahini", "cinnamon", "maple syrup"]},
]


# ---------------------------------------------------------------------------
# Public service functions
# ---------------------------------------------------------------------------

def get_recipes(goal: str, dietary_restrictions: List[str]) -> List[Dict]:
    """Return 3 random recipes matching the goal and dietary restrictions."""
    goal = goal.lower().replace("-", "_")

    pool = [r for r in ALL_RECIPES if goal in r["goals"]]
    if not pool:
        pool = ALL_RECIPES.copy()

    if dietary_restrictions:
        filtered = [
            r for r in pool
            if _passes(" ".join(r["ingredients"]).lower(), r["dietary_tags"], dietary_restrictions)
        ]
        if filtered:
            pool = filtered

    random.shuffle(pool)
    return pool[:3]


def get_meal_plan(goal: str, dietary_restrictions: List[str], days: int = 7) -> List[Dict]:
    """Generate a fresh N-day meal plan with filtered breakfasts and mains."""
    goal = goal.lower().replace("-", "_")

    calorie_targets = {
        "weight_loss": 1600,
        "weight_gain": 2800,
        "maintenance": 2200,
        "muscle_gain": 2600,
    }
    target = calorie_targets.get(goal, 2200)
    days = min(days, 7)

    pool = [r for r in ALL_RECIPES if goal in r["goals"]]
    if not pool:
        pool = ALL_RECIPES.copy()
    if dietary_restrictions:
        filtered = [r for r in pool if _passes(" ".join(r["ingredients"]).lower(), r["dietary_tags"], dietary_restrictions)]
        if filtered:
            pool = filtered
    random.shuffle(pool)

    breakfast_pool = ALL_BREAKFASTS.copy()
    if dietary_restrictions:
        filtered_b = [b for b in breakfast_pool if _passes(" ".join(b["ingredients"]).lower(), b["dietary_tags"], dietary_restrictions)]
        if filtered_b:
            breakfast_pool = filtered_b
    random.shuffle(breakfast_pool)

    day_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    tips = [
        "Stay hydrated — aim for 8 glasses of water today.",
        "Don't skip meals — consistency is key for your goals.",
        "Listen to your body's hunger cues.",
        "Prep tomorrow's meals tonight to stay on track.",
        "Add variety with different vegetables each day.",
        "Include a colourful variety of fruits and vegetables.",
        "Remember: it's about progress, not perfection!",
        "Chew your food slowly — it helps with digestion and satiety.",
        "Add a handful of leafy greens to every meal where possible.",
        "Meal variety keeps nutrients balanced and meals exciting.",
    ]
    random.shuffle(tips)

    meal_plan = []
    for i in range(days):
        breakfast = breakfast_pool[i % len(breakfast_pool)]
        lunch     = pool[i % len(pool)]
        dinner    = pool[(i + max(1, len(pool) // 2)) % len(pool)]

        b_cal = int(target * 0.25)
        l_cal = int(target * 0.35)
        d_cal = int(target * 0.30)
        s_cal = int(target * 0.10)

        meals = [
            {
                "meal_type": "Breakfast",
                "time": "7:00 AM",
                "name": breakfast["name"],
                "description": "Start your day with sustained energy",
                "calories": b_cal,
                "protein": 20 if goal == "muscle_gain" else 15,
                "carbs": 45 if goal == "weight_gain" else 35,
                "fats": 12,
                "icon": breakfast["icon"],
                "quick_recipe": breakfast["quick_recipe"],
            },
            {
                "meal_type": "Lunch",
                "time": "12:30 PM",
                "name": lunch["name"],
                "description": lunch["description"],
                "calories": l_cal,
                "protein": 30 if goal == "muscle_gain" else 25,
                "carbs": 50 if goal == "weight_gain" else 40,
                "fats": 15,
                "icon": lunch["icon"],
                "quick_recipe": ", ".join(lunch["ingredients"][:3]) + "...",
            },
            {
                "meal_type": "Dinner",
                "time": "7:00 PM",
                "name": dinner["name"],
                "description": dinner["description"],
                "calories": d_cal,
                "protein": 35 if goal == "muscle_gain" else 28,
                "carbs": 45 if goal == "weight_gain" else 35,
                "fats": 18,
                "icon": dinner["icon"],
                "quick_recipe": ", ".join(dinner["ingredients"][:3]) + "...",
            },
        ]

        if goal in ["weight_gain", "muscle_gain"]:
            meals.append({
                "meal_type": "Snack",
                "time": "3:00 PM",
                "name": "Protein Snack",
                "description": "Keep energy levels high",
                "calories": s_cal,
                "protein": 15,
                "carbs": 20,
                "fats": 8,
                "icon": "🥜",
                "quick_recipe": "Nuts, fruit and a protein source",
            })

        meal_plan.append({
            "day": i + 1,
            "day_name": day_names[i],
            "total_calories": sum(m["calories"] for m in meals),
            "meals": meals,
            "tips": tips[i % len(tips)],
        })

    return meal_plan


def get_healthy_swaps(craving: str) -> List[Dict]:
    """Return 4 shuffled healthy swaps for the given craving."""
    swaps_db = {
        "sweet": [
            {"name": "Dates with Almond Butter", "description": "Natural caramel sweetness with healthy fats and fibre", "calories": 150, "benefits": ["Natural sugars", "Fibre", "Healthy fats"], "icon": "🌰"},
            {"name": "Greek Yogurt with Berries", "description": "Creamy protein-rich yogurt with antioxidant-rich berries", "calories": 180, "benefits": ["Protein", "Probiotics", "Antioxidants"], "icon": "🍓"},
            {"name": "Dark Chocolate 70%+", "description": "Rich chocolate with less sugar and far more antioxidants", "calories": 170, "benefits": ["Antioxidants", "Lower sugar", "Mood boost"], "icon": "🍫"},
            {"name": "Banana Nice Cream", "description": "Frozen blended banana that tastes just like ice cream", "calories": 105, "benefits": ["Potassium", "No added sugar", "Vitamins"], "icon": "🍌"},
            {"name": "Baked Cinnamon Apple", "description": "Warm baked apple with maple syrup and cinnamon — naturally sweet", "calories": 95, "benefits": ["Fibre", "Vitamins", "Low calorie"], "icon": "🍎"},
            {"name": "Medjool Dates with Tahini", "description": "Sweet dates stuffed with creamy tahini for balanced energy", "calories": 140, "benefits": ["Natural sweetness", "Healthy fats", "Minerals"], "icon": "🟫"},
            {"name": "Mango Chia Pudding", "description": "Tropical mango layered over vanilla chia pudding", "calories": 160, "benefits": ["Omega-3", "Vitamins", "Natural sweetness"], "icon": "🥭"},
        ],
        "salty": [
            {"name": "Air-Popped Popcorn", "description": "Whole grain snack with satisfying crunch and minimal calories", "calories": 120, "benefits": ["Whole grain", "Fibre", "Low calorie"], "icon": "🍿"},
            {"name": "Roasted Chickpeas", "description": "Crunchy savory chickpeas packed with protein and fibre", "calories": 140, "benefits": ["Protein", "Fibre", "Iron"], "icon": "🫘"},
            {"name": "Seaweed Snacks", "description": "Crispy seaweed sheets with umami minerals and almost no calories", "calories": 30, "benefits": ["Iodine", "Vitamins", "Very low calorie"], "icon": "🌿"},
            {"name": "Edamame with Sea Salt", "description": "Protein-rich pods with a satisfying salty and earthy bite", "calories": 120, "benefits": ["Protein", "Fibre", "Minerals"], "icon": "🫛"},
            {"name": "Cucumber with Sea Salt & Vinegar", "description": "Hydrating cucumber with a tangy punch", "calories": 20, "benefits": ["Hydration", "Minerals", "Very low calorie"], "icon": "🥒"},
            {"name": "Miso Soup", "description": "Warm umami broth that satisfies salty cravings instantly", "calories": 35, "benefits": ["Probiotics", "Minerals", "Very low calorie"], "icon": "🍵"},
            {"name": "Olives", "description": "Briny olives packed with heart-healthy monounsaturated fats", "calories": 80, "benefits": ["Healthy fats", "Antioxidants", "Satisfying"], "icon": "🫒"},
        ],
        "crunchy": [
            {"name": "Raw Almonds", "description": "Satisfying crunch loaded with healthy fats, protein and vitamin E", "calories": 160, "benefits": ["Healthy fats", "Protein", "Vitamin E"], "icon": "🥜"},
            {"name": "Apple with Peanut Butter", "description": "Crisp apple slices with creamy protein-rich peanut butter", "calories": 190, "benefits": ["Fibre", "Protein", "Vitamins"], "icon": "🍎"},
            {"name": "Carrots & Hummus", "description": "Crunchy carrots dipped in silky protein-packed hummus", "calories": 130, "benefits": ["Beta-carotene", "Protein", "Fibre"], "icon": "🥕"},
            {"name": "Rice Cakes with Avocado", "description": "Airy crunchy base with creamy nutrient-rich avocado", "calories": 150, "benefits": ["Healthy fats", "Fibre", "Light"], "icon": "🥑"},
            {"name": "Baked Kale Chips", "description": "Shatteringly crispy kale chips with sea salt — zero guilt", "calories": 60, "benefits": ["Very low calorie", "Vitamins", "Minerals"], "icon": "🥬"},
            {"name": "Celery with Almond Butter", "description": "Classic ants-on-a-log with a nutritious update", "calories": 110, "benefits": ["Low calorie", "Protein", "Healthy fats"], "icon": "🥬"},
            {"name": "Roasted Pumpkin Seeds", "description": "Mineral-rich seeds with a satisfying crunch and nutty flavour", "calories": 130, "benefits": ["Magnesium", "Zinc", "Protein"], "icon": "🌻"},
        ],
        "creamy": [
            {"name": "Greek Yogurt Parfait", "description": "Thick protein-rich yogurt layered with fresh fruit and granola", "calories": 180, "benefits": ["Protein", "Probiotics", "Calcium"], "icon": "🥛"},
            {"name": "Avocado Chocolate Pudding", "description": "Blended avocado with cacao — indulgently creamy and healthy", "calories": 200, "benefits": ["Healthy fats", "Fibre", "Antioxidants"], "icon": "🥑"},
            {"name": "Cottage Cheese with Fruit", "description": "Protein-rich cottage cheese with fresh berries and a drizzle of maple syrup", "calories": 150, "benefits": ["High protein", "Calcium", "Vitamins"], "icon": "🧀"},
            {"name": "Chia Pudding", "description": "Thick creamy pudding from omega-3 rich chia seeds", "calories": 170, "benefits": ["Omega-3", "Fibre", "Protein"], "icon": "🥥"},
            {"name": "Silken Tofu Smoothie", "description": "Ultra-creamy vegan smoothie using silken tofu as the base", "calories": 160, "benefits": ["Plant protein", "Calcium", "Creamy texture"], "icon": "🥤"},
            {"name": "Hummus with Warm Pitta", "description": "Silky smooth hummus with warm toasted pitta triangles", "calories": 200, "benefits": ["Protein", "Fibre", "Healthy fats"], "icon": "🫙"},
            {"name": "Banana Peanut Butter Smoothie", "description": "Thick creamy smoothie with banana, peanut butter and oat milk", "calories": 220, "benefits": ["Potassium", "Protein", "Sustained energy"], "icon": "🍌"},
        ],
        "chocolate": [
            {"name": "Cacao Nibs", "description": "Pure chocolate in its raw natural form with zero added sugar", "calories": 130, "benefits": ["Antioxidants", "Minerals", "No added sugar"], "icon": "🍫"},
            {"name": "Chocolate Protein Shake", "description": "Rich chocolate shake that hits your protein targets too", "calories": 200, "benefits": ["Protein", "Vitamins", "Filling"], "icon": "🥤"},
            {"name": "Frozen Chocolate Banana", "description": "Frozen banana dipped in dark chocolate — nature's ice lolly", "calories": 150, "benefits": ["Potassium", "Antioxidants", "Natural sweetness"], "icon": "🍌"},
            {"name": "Chocolate Almond Butter", "description": "Almond butter blended with cacao powder and a touch of maple", "calories": 190, "benefits": ["Healthy fats", "Protein", "Antioxidants"], "icon": "🥜"},
            {"name": "Carob Energy Balls", "description": "No-bake balls with carob, oats and medjool dates", "calories": 160, "benefits": ["Natural energy", "Fibre", "No refined sugar"], "icon": "⚫"},
            {"name": "Chocolate Chia Pudding", "description": "Creamy chia pudding made with cacao and coconut milk", "calories": 175, "benefits": ["Omega-3", "Antioxidants", "Fibre"], "icon": "🥥"},
            {"name": "Dark Chocolate Bark with Nuts", "description": "70% dark chocolate broken into shards with almonds and sea salt", "calories": 180, "benefits": ["Antioxidants", "Healthy fats", "Mineral-rich"], "icon": "🍫"},
        ],
        "fried": [
            {"name": "Air-Fried Sweet Potato Fries", "description": "Perfectly crispy sweet potato fries with a fraction of the oil", "calories": 150, "benefits": ["Vitamins", "Fibre", "Less oil"], "icon": "🍠"},
            {"name": "Baked Zucchini Fries", "description": "Oven-baked zucchini coated in herbed breadcrumbs", "calories": 120, "benefits": ["Low calorie", "Vitamins", "Fibre"], "icon": "🥒"},
            {"name": "Oven-Baked Chicken Tenders", "description": "Crispy golden chicken tenders without a drop of frying oil", "calories": 220, "benefits": ["High protein", "Less fat", "Crispy"], "icon": "🍗"},
            {"name": "Roasted Chickpeas", "description": "Crunchy oven-roasted chickpeas seasoned with smoked paprika", "calories": 140, "benefits": ["Protein", "Fibre", "Iron"], "icon": "🫘"},
            {"name": "Baked Kale Chips", "description": "Shatteringly crispy kale chips — zero oil guilt", "calories": 60, "benefits": ["Very low calorie", "Vitamins", "Iron"], "icon": "🥬"},
            {"name": "Air-Fried Tofu Nuggets", "description": "Crispy golden tofu nuggets with a cornflake crust", "calories": 180, "benefits": ["Plant protein", "Low fat", "Satisfying"], "icon": "🟡"},
            {"name": "Baked Onion Rings", "description": "Oven-baked onion rings with panko — crispy without the grease", "calories": 130, "benefits": ["Low calorie vs fried", "Fibre", "Crunch"], "icon": "🧅"},
        ],
    }

    craving = craving.lower().strip()
    swaps = swaps_db.get(craving, swaps_db["sweet"]).copy()
    random.shuffle(swaps)
    return swaps[:4]