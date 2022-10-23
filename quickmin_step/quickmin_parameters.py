# -*- coding: utf-8 -*-
"""
Control parameters for the QuickMin step in a SEAMM flowchart
"""

import logging
import seamm
import pprint  # noqa: F401

logger = logging.getLogger(__name__)


class QuickMinParameters(seamm.Parameters):
    """
    The control parameters for QuickMin.

    The developer will add a dictionary of Parameters to this class.
    The keys are parameters for the current plugin, which themselves
    might be dictionaries.

    You need to replace the "time" example below with one or more
    definitions of the control parameters for your plugin and application.

    Examples
    --------
    ::

        parameters = {
            "time": {
                "default": 100.0,
                "kind": "float",
                "default_units": "ps",
                "enumeration": tuple(),
                "format_string": ".1f",
                "description": "Simulation time:",
                "help_text": ("The time to simulate in the dynamics run.")
            },
        }

    parameters : {str: {str: str}}
        A dictionary containing the parameters for the current step.
        Each key of the dictionary is a dictionary that contains the
        the following keys:

    parameters["default"] :
        The default value of the parameter, used to reset it.

    parameters["kind"] : enum()
        Specifies the kind of a variable. One of  "integer", "float", "string",
        "boolean", or "enum"

        While the "kind" of a variable might be a numeric value, it may still have
        enumerated custom values meaningful to the user. For instance, if the parameter
        is a convergence criterion for an optimizer, custom values like "normal",
        "precise", etc, might be adequate. In addition, any parameter can be set to a
        variable of expression, indicated by having "$" as the first character in the
        field. For example, $OPTIMIZER_CONV.

    parameters["default_units"] : str
        The default units, used for resetting the value.

    parameters["enumeration"]: tuple
        A tuple of enumerated values.

    parameters["format_string"]: str
        A format string for "pretty" output.

    parameters["description"]: str
        A short string used as a prompt in the GUI.

    parameters["help_text"]: str
        A longer string to display as help for the user.

    See Also
    --------
    QuickMin, TkQuickMin, QuickMin, QuickMinParameters, QuickMinStep
    """

    parameters = {
        "forcefield": {
            "default": "best available",
            "kind": "enum",
            "enumeration": (
                "best available",
                "GAFF -- General Amber Force Field",
                "Ghemical -- Ghemical force field",
                "MMFF94 -- MMFF94 force field",
                "MMFF94s -- MMFF94s force field for minimization",
                "UFF -- Universal Force Field",
            ),
            "format_string": "",
            "description": "Forcefield:",
            "help_text": "The forcefield to use.",
        },
        "n_steps": {
            "default": 1000,
            "kind": "integer",
            "default_units": "",
            "enumeration": tuple(),
            "format_string": "",
            "description": "Maximum steps:",
            "help_text": "The maximum number of steps to run.",
        },
        # Put in the configuration handling options needed
        "structure handling": {
            "default": "Create a new configuration",
            "kind": "enum",
            "default_units": "",
            "enumeration": (
                "Overwrite the current configuration",
                "Create a new configuration",
            ),
            "format_string": "s",
            "description": "Configuration handling:",
            "help_text": (
                "Whether to overwrite the current configuration, or create a new "
                "configuration or system and configuration for the new structure"
            ),
        },
        "configuration name": {
            "default": "optimized with <Forcefield>",
            "kind": "string",
            "default_units": "",
            "enumeration": (
                "optimized with <Forcefield>",
                "keep current name",
                "use SMILES string",
                "use Canonical SMILES string",
                "use configuration number",
            ),
            "format_string": "s",
            "description": "Configuration name:",
            "help_text": "The name for the new configuration",
        },
        # Results handling
        "results": {
            "default": {},
            "kind": "dictionary",
            "default_units": "",
            "enumeration": tuple(),
            "format_string": "",
            "description": "results",
            "help_text": "The results to save to variables or in tables.",
        },
    }

    def __init__(self, defaults={}, data=None):
        """
        Initialize the parameters, by default with the parameters defined above

        Parameters
        ----------
        defaults: dict
            A dictionary of parameters to initialize. The parameters
            above are used first and any given will override/add to them.
        data: dict
            A dictionary of keys and a subdictionary with value and units
            for updating the current, default values.

        Returns
        -------
        None
        """

        logger.debug("QuickMinParameters.__init__")

        super().__init__(
            defaults={**QuickMinParameters.parameters, **defaults}, data=data
        )
