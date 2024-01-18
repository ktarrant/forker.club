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
    dict(name="tomato", package="whole", volume_quantity=1, volume_unit="cup", weight_quantity=5, weight_unit="ounce"),
    dict(name="lemon", package="whole", volume_quantity=2.5, volume_unit="tablespoon", weight_quantity=1.3, weight_unit="ounce"),
    dict(name="garlic", package="whole", volume_quantity=10, volume_unit="teaspoon", weight_quantity=4, weight_unit="ounce"),
    dict(name="fresh basil leaves", package="whole", volume_quantity=2, volume_unit="teaspoon", weight_quantity=0.5, weight_unit="ounce"),
    # Pantry
    dict(name="dried chantarelle", package="16 ounce bag", volume_quantity=2, volume_unit='quart', weight_quantity=16.0, weight_unit="ounce"),
    dict(name="dry penne pasta", package="16 ounce box", volume_quantity=1.5, volume_unit='quart', weight_quantity=16.0, weight_unit="ounce"),
    dict(name="pine nuts", package="8 ounce bag", volume_quantity=1, volume_unit='pint', weight_quantity=8, weight_unit="ounce"),
    dict(name="sea salt", package="24 fluid ounce can", volume_quantity=1.5, volume_unit='pint', weight_quantity=24, weight_unit="ounce"),
    dict(name="black pepper", package="3 ounce grinder", volume_quantity=1, volume_unit='cup', weight_quantity=3, weight_unit="ounce"),
    # Oils
    dict(name="extra-virgin olive oil", package="16 fluid ounce bottle", volume_quantity=16.0, volume_unit="fluid ounce", weight_quantity=13, weight_unit='ounce'),
    # Dairy
    dict(name="butter", package="stick", volume_quantity=8, volume_unit="tablespoon", weight_quantity=8, weight_unit='ounce'),
    dict(name="parmesan cheese", package="wedge", volume_quantity=3, volume_unit="cup", weight_quantity=4, weight_unit="ounce"),
]
