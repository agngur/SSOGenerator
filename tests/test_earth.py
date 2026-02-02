from ssogenerator.earth import Earth

main_body = Earth(name="Earth", radius=6378.137)

def test_earth():
    assert isinstance(main_body, Earth)