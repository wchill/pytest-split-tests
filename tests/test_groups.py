import pytest

from pytest_split_tests import get_group, get_group_size_and_start


def test_group_params_computed_correctly_for_even_group():
    expected = [(0, 8), (8, 8), (16, 8), (24, 8)]
    actual = [get_group_size_and_start(32, 4, group_id) for group_id in range(1, 5)]  # 32 total tests; 4 groups

    assert expected == actual


def test_group_size_computed_correctly_for_odd_group():
    expected = [(0, 8), (8, 8), (16, 8), (24, 7)]
    actual = [get_group_size_and_start(31, 4, group_id) for group_id in range(1, 5)]  # 32 total tests; 4 groups

    assert expected == actual


def test_group_is_the_proper_size():
    items = [str(i) for i in range(32)]
    group = get_group(items, 4, 1)

    assert len(group) == 8


def test_all_groups_together_form_original_set_of_tests():
    items = [str(i) for i in range(32)]

    groups = [get_group(items, 4, i) for i in range(1, 5)]

    combined = []
    for group in groups:
        combined.extend(group)

    assert combined == items


def test_group_that_is_too_high_raises_value_error():
    items = [str(i) for i in range(32)]

    with pytest.raises(ValueError):
        get_group(items, 4, 5)


def test_group_that_is_too_low_raises_value_error():
    items = [str(i) for i in range(32)]

    with pytest.raises(ValueError):
        get_group(items, 4, 0)
