=======
History
=======
2023.10.30 -- Enhanced structure handling.
    Switched to standard handling of structures, which adds ability to name with the
    IUPAC name, InCHI, and InChIKey in addition to previous methods.

2023.1.14 -- Changed documentation to new style and theme.
    Switched the documentation to the MolSSI theme and diátaxis layout, though more work
    is needed.
    
2022.11.7 -- Internal Release
    Switching from LGTM code analysis to GitHub Actions using CodeQL, since LGTM is
    shutting down!
    
2022.10.23 -- Properties added
    Added a single property, 'total energy#QuickMin#<forcefield>', to store the final
    energy in the database. Also added 'total energy' as a result for tables or
    variables.

2022.10.22 -- Documentation!
    Got the documentation into reasonable shape.

2022.10.20 -- Initial Release!
    Provides quick minimization for smaller molecules, using OpenBabel. Probably
    reasonable for some few hundred atoms. Supports the following forcefields:

       1. GAFF
       2. MMFF94 & MMFF94s (which is optimized for minimization)
       3. Ghemical
       4. UFF

    The default is the "best available" forcefield, which tries them in the order given
    above until it finds one that can handle the molecule. 
