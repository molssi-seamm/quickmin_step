========
History
========

2022.10.22 -- Documentation!
    Got the documentation into reasonable shape.

2022.10.20 -- Initial Release!
    Provides quick minimization for smaller molecules, using OpenBabel. Probably reasonable for some few hundred atoms. Supports the following forcefields:

       1. GAFF
       2. MMFF94 & MMFF94s (which is optimized for minimization)
       3. Ghemical
       4. UFF

    The default is the "best available" forcefield, which tries them in the order given above until it finds one that can handle the molecule.
