#!/usr/bin/env python
# -*- coding: utf-8
# pytest unit tests for assign-reviewers.main
import os
import sys
import pytest

from assign_reviewers import *


def test_select_from_pool():
    list_reviewers = [[0, 1], [0, 2], [3], [], []]
    reviewers = select_from_pool(list_reviewers, [0, 1, 2, 3], 3)
    assert reviewers == [1, 2, 3]
    # Make reviewer 1 not illegible
    reviewers = select_from_pool(list_reviewers, [0, 2, 3], 3)
    assert reviewers == [2, 3, 0]


def test_remove_same_affiliation():
    eligible_rev = remove_same_affiliation(
        'blabla',
        [['aff1'], ['aff2'], ['aff3', 'blabla']]
        )
    assert eligible_rev == [0, 1]
    eligible_rev = remove_same_affiliation(
        'hehehe',
        [['aff1'], ['aff2'], ['aff3', 'blabla']]
        )
    assert eligible_rev == [0, 1, 2]
