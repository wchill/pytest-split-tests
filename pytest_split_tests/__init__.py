# -*- coding: utf-8 -*-
from random import Random
import json
import math

from _pytest.config import create_terminal_writer
import pytest


def get_group_size(total_items, total_groups):
    """Return the group size."""
    return int(math.ceil(float(total_items) / total_groups))


def get_group(items, group_size, group_id):
    """Get the items from the passed in group based on group size."""
    start = group_size * (group_id - 1)
    end = start + group_size

    if start >= len(items) or start < 0:
        raise ValueError("Invalid test-group argument")

    return items[start:end]


def pytest_addoption(parser):
    group = parser.getgroup('split your tests into evenly sized groups and run them')
    group.addoption('--test-group-count', dest='test-group-count', type=int,
                    help='The number of groups to split the tests into')
    group.addoption('--test-group', dest='test-group', type=int,
                    help='The group of tests that should be executed')
    group.addoption('--test-group-random-seed', dest='random-seed', type=int,
                    help='Integer to seed pseudo-random test selection')
    group.addoption('--test-group-prescheduled', dest='prescheduled', type=str,
                    help='Path to JSON file containing which tests to run.')


@pytest.hookimpl(hookwrapper=True)
def pytest_collection_modifyitems(session, config, items):
    yield
    group_count = config.getoption('test-group-count')
    group_id = config.getoption('test-group')
    seed = config.getoption('random-seed', False)
    prescheduled_path = config.getoption('prescheduled', None)

    if not group_count or not group_id:
        return

    test_dict = {item.name: item for item in items}
    original_order = {item: index for index, item in enumerate(items)}

    # schema: prescheduled_data[node_id] = [*test_names]
    prescheduled_data = [[] for _ in range(group_count)]
    if prescheduled_path:
        try:
            with open(prescheduled_path, 'r') as f:
                prescheduled_data = json.load(f)
                if len(prescheduled_data) != group_count:
                    print('WARNING: Prescheduled tests do not match up with the group count. '
                          'Prescheduling will be skipped.')
        except Exception:
            print('WARNING: Unable to load prescheduled tests. Prescheduling will be skipped.')

    all_prescheduled_tests = [test_dict[test_name]
                              for sublist in prescheduled_data
                              for test_name in sublist
                              if test_name in test_dict]
    prescheduled_tests = [test_dict[test_name]
                          for test_name in prescheduled_data[group_id - 1]
                          if test_name in test_dict]
    unscheduled_tests = [item for item in items if item not in all_prescheduled_tests]

    if seed is not False:
        seeded = Random(seed)
        seeded.shuffle(unscheduled_tests)

    total_unscheduled_items = len(unscheduled_tests)

    group_size = get_group_size(total_unscheduled_items, group_count)
    tests_in_group = get_group(unscheduled_tests, group_size, group_id)
    items[:] = tests_in_group + prescheduled_tests

    items.sort(key=original_order.__getitem__)

    terminal_reporter = config.pluginmanager.get_plugin('terminalreporter')
    if terminal_reporter is not None:
        terminal_writer = create_terminal_writer(config)
        message = terminal_writer.markup(
            '\nRunning test group #{0} ({1} tests)\n'.format(
                group_id,
                len(items)
            ),
            yellow=True
        )
        terminal_reporter.write(message)
        message = terminal_writer.markup(
            '\n'.join([item.name for item in items])+'\n',
            yellow=True
        )
        terminal_reporter.write(message)
