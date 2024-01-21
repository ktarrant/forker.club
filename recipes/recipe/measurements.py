from pint import UnitRegistry

ureg = UnitRegistry()

supported_units = [
    # imperial
    ureg.tablespoon, ureg.teaspoon, ureg.fluid_ounce,
    ureg.gallon, ureg.quart, ureg.pint, ureg.cup,
    # metric
    ureg.milliliter, ureg.liter,
    # imperial
    ureg.ounce, ureg.pound,
    # metric
    ureg.gram, ureg.kilogram,
]

good_categories = [
    "produce",      # Fruits and Vegetables. Fresh Mushrooms.
    "pantry",       # Canned and Jarred. Pasta, Rice & Cereal. Baking.
    "dairy",        # Butter, Cheese, Eggs, Milk, Yogurt.
    "meat",         # Chicken, Beef, Pork, Fish, Seafood.
    "condiments",   # Ketchup, Mayo, Soy Sauce, Oyster Sauce.
    "oils",         # Extra-Virgin Olive Oil, Vegetable Oil, Coconut Oil.
    "spices",       # Black pepper, Oregano, Cinnamon, Sugar (dried only)
    "bakery",       # Bread, Tortillas, Bagels
    "frozen",       # Frozen Vegetables, Pizza Dough, Fish
]
