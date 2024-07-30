import pytest

from pytest_split_tests import get_group


def test_group_is_the_proper_size_no_remainder():
    num_items = 32
    num_groups = 8
    expected_items_per_group = 4
    items = [str(i) for i in range(num_items)]

    for i in range(1, num_groups + 1):
        assert len(get_group(items, num_groups, i)) == expected_items_per_group


def test_group_is_the_proper_size_with_remainder():
    num_items = 32
    num_groups = 5
    expected_base_items_per_group = 6
    items = [str(i) for i in range(num_items)]

    for i in range(1, 3):
        assert len(get_group(items, num_groups, i)) == (
            expected_base_items_per_group + 1
        )

    for i in range(3, num_groups + 1):
        assert len(get_group(items, num_groups, i)) == expected_base_items_per_group


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
