"""This file contains metadata describing the results from {{ cookiecutter.class_name }}

`metadata["results"]` describes the results that this step can produce. It is a
dictionary where the keys are the internal names of the results within this step, and
the values are a dictionary describing the result. For example:

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
            "property": "total energy#{{ cookiecutter.class_name }}#{model}",
            "type": "float",
            "units": "E_h",
        },
    }

The keys for the metadata are the following:

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

metadata = {}

"""Properties that QuickMin produces."""
metadata["results"] = {
    "total energy": {
        "description": "The total energy",
        "dimensionality": "scalar",
        "property": "total energy#QuickMin#{model}",
        "type": "float",
        "units": "kJ/mol",
    },
}
