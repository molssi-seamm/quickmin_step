"""This file contains metadata describing the results from QuickMin"""

metadata = {}

"""Properties that QuickMin produces.
`metadata["results"]` describes the results that this step can produce. It is a
dictionary where the keys are the internal names of the results within this step, and
the values are a dictionary describing the result. For example::

    metadata["results"] = {
        "total_energy": {
            "calculation": [
                "energy",
                "optimization",
            ],
            "description": "The total energy",
            "dimensionality": "scalar",
            "methods": [
                "ccsd",
                "ccsd(t)",
                "dft",
                "hf",
            ],
            "property": "total energy#QuickMin#{model}",
            "type": "float",
            "units": "E_h",
        },
    }

Fields
______

calculation : [str]
    Optional metadata describing what subtype of the step produces this result.
    The subtypes are completely arbitrary, but often they are types of calculations
    which is why this is name `calculation`. To use this, the step or a substep
    define `self._calculation` as a value. That value is used to select only the
    results with that value in this field.

description : str
    A human-readable description of the result.

dimensionality : str
    The dimensions of the data. The value can be "scalar" or an array definition
    of the form "[dim1, dim2,...]". Symmetric tringular matrices are denoted
    "triangular[n,n]". The dimensions can be integers, other scalar
    results, or standard parameters such as `n_atoms`. For example, '[3]',
    [3, n_atoms], or "triangular[n_aos, n_aos]".

methods : str
    Optional metadata like the `calculation` data. `methods` provides a second
    level of filtering, often used for the Hamiltionian for *ab initio* calculations
    where some properties may or may not be calculated depending on the type of
    theory.

property : str
    An optional definition of the property for storing this result. Must be one of
    the standard properties defined either in SEAMM or in this steps property
    metadata in `data/properties.csv`.

type : str
    The type of the data: string, integer, or float.

units : str
    Optional units for the result. If present, the value should be in these units.
"""
metadata["results"] = {
    "energy": {
        "description": "The total energy",
        "dimensionality": "scalar",
        "property": "total energy#QuickMin#{model}",
        "type": "float",
        "units": "kJ/mol",
    },
    "gradients": {
        "description": "The gradients",
        "dimensionality": "[3, n_atoms]",
        "type": "float",
        "units": "kJ/mol/Å",
    },
    "forcefield": {
        "description": "The forcefield used",
        "dimensionality": "scalar",
        "type": "string",
    },
    "model": {
        "description": "The model string",
        "dimensionality": "scalar",
        "type": "string",
    },
    "n steps": {
        "description": "The number of optimization steps",
        "dimensionality": "scalar",
        "type": "integer",
    },
    "converged": {
        "description": "Whether the optimization converged",
        "dimensionality": "scalar",
        "type": "boolean",
    },
    "RMSD": {
        "calculation": ["optimization"],
        "description": "RMSD with H removed",
        "dimensionality": "scalar",
        "type": "float",
        "units": "Å",
    },
    "displaced atom": {
        "calculation": ["optimization"],
        "description": "Atom index with largest displacement",
        "dimensionality": "scalar",
        "type": "int",
    },
    "maximum displacement": {
        "calculation": ["optimization"],
        "description": "Maximum displacement of an atom",
        "dimensionality": "scalar",
        "type": "float",
        "units": "Å",
    },
    "RMSD with H": {
        "calculation": ["optimization"],
        "description": "RMSD including H atoms",
        "dimensionality": "scalar",
        "type": "float",
        "units": "Å",
    },
    "displaced atom with H": {
        "calculation": ["optimization"],
        "description": "Atom index with largest displacement, including H",
        "dimensionality": "scalar",
        "type": "int",
    },
    "maximum displacement with H": {
        "calculation": ["optimization"],
        "description": "Maximum displacement of an atom, including H",
        "dimensionality": "scalar",
        "type": "float",
        "units": "Å",
    },
}
