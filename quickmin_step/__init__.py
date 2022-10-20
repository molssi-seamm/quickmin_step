# -*- coding: utf-8 -*-

"""
quickmin_step
A SEAMM plug-in for simple, quick minimization
"""

# Bring up the classes so that they appear to be directly in
# the quickmin_step package.

from quickmin_step.quickmin import QuickMin  # noqa: F401, E501
from quickmin_step.quickmin_parameters import QuickMinParameters  # noqa: F401, E501
from quickmin_step.quickmin_step import QuickMinStep  # noqa: F401, E501
from quickmin_step.tk_quickmin import TkQuickMin  # noqa: F401, E501

# Handle versioneer
from ._version import get_versions

__author__ = "Paul Saxe"
__email__ = "psaxe@molssi.org"
versions = get_versions()
__version__ = versions["version"]
__git_revision__ = versions["full-revisionid"]
del get_versions, versions
