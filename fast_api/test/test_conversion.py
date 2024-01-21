from ..util import conversion


def test_inches_to_feet():
    result = conversion.inches_to_feet("50")
    assert result == "4'2\""
