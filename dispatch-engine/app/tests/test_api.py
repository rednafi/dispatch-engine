from app.apis.api_b.mainmod import main_func as main_func_b
from app.apis.dispatch.mainmod import main_func as main_func_a


def test_func_main_a() -> None:
    seed = 420
    result = main_func_a(seed)
    assert isinstance(result, dict) is True
    assert result.get("seed") == seed


def test_func_main_b() -> None:
    seed = 500
    result = main_func_b(seed)
    assert isinstance(result, dict) is True
    assert result.get("seed") == seed
