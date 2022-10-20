#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `quickmin_step` package."""

import pytest  # noqa: F401
import quickmin_step  # noqa: F401


def test_construction():
    """Just create an object and test its type."""
    result = quickmin_step.QuickMin()
    assert str(type(result)) == "<class 'quickmin_step.quickmin.QuickMin'>"
