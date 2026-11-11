from etl_wore.transformers.scale_numbers import ScaleNumbers
from etl_wore.transformers.clamp_numbers import ClampNumbers
from etl_wore.transformers.round_numbers import RoundNumbers
from etl_wore.transformers.sort_arrays import SortArrays
def test_large_integers_do_not_require_lossy_float_conversion():
    number = 10**400
    assert ScaleNumbers(['x'], factor=2).transform({'x': number})['x'] == number*2
    assert ClampNumbers(['x'], maximum=number).transform({'x': number+1})['x'] == number
    assert RoundNumbers(['x']).transform({'x': number})['x'] == number
    assert SortArrays(['x']).transform({'x': [number, -number]})['x'] == [-number, number]
