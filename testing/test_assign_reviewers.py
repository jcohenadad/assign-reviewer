#!/usr/bin/env python
# -*- coding: utf-8
# pytest unit tests for assign-reviewers.main
import os
import sys
import pytest

from assign_reviewers import *


def test_select_from_pool():
    list_reviewers = [[0, 1], [0, 2], [3], [], []]
    reviewers = select_from_pool(list_reviewers, 4, 3)
    assert reviewers == [1, 2, 3]
