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

supported_goods = [
    # Produce
    dict(name="tomato", package="whole", quantity=1, unit="cup"),
    dict(name="lemon", package="whole", quantity=2.5, unit="tablespoon"),
    dict(name="garlic", package="whole", quantity=10, unit="teaspoon"),
    dict(name="fresh basil leaves", package="whole", quantity=2, unit="teaspoon"),
    # Pantry
    dict(name="dried chantarelle", package="16 ounce bag", quantity=16.0, unit="ounce"),
    dict(name="dry penne pasta", package="16 ounce box", quantity=16.0, unit="ounce"),
    dict(name="pine nuts", package="8 ounce bag", quantity=8, unit="ounce"),
    dict(name="sea salt", package="24 fluid ounce can", quantity=24, unit="fluid ounce"),
    dict(name="black pepper", package="3 ounce grinder", quantity=3, unit="ounce"),
    # Oils
    dict(name="extra-virgin olive oil", package="16 fluid ounce bottle", quantity=16.0, unit="fluid ounce"),
    # Dairy
    dict(name="butter", package="stick", quantity=8, unit="tablespoon"),
    dict(name="parmesan cheese", package="wedge", quantity=4, unit="ounce"),
]
