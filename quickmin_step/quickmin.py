# -*- coding: utf-8 -*-

"""Non-graphical part of the QuickMin step in a SEAMM flowchart
"""

import os
import sys
import threading
import time

import logging
from pathlib import Path
import pkg_resources
import pprint  # noqa: F401
import shutil
import string
import subprocess

from openbabel import openbabel

import molsystem
import quickmin_step
import seamm
from seamm_util import ureg, Q_  # noqa: F401
import seamm_util.printing as printing
from seamm_util.printing import FormattedText as __

# Add this modules properties to the standard properties
path = Path(pkg_resources.resource_filename(__name__, "data/"))
csv_file = path / "properties.csv"
if path.exists():
    molsystem.add_properties_from_file(csv_file)

if "OpenBabel_version" not in globals():
    OpenBabel_version = None


class OutputGrabber(object):
    """Class used to grab standard output or another stream.

    see https://stackoverflow.com/questions/24277488/in-python-how-to-capture-the-stdout-from-a-c-shared-library-to-a-variable/29834357#29834357  # noqa: E501
    """

    escape_char = "\b"

    def __init__(self, stream=None, threaded=False):
        self.origstream = stream
        self.threaded = threaded
        if self.origstream is None:
            self.origstream = sys.stdout
        self.origstreamfd = self.origstream.fileno()
        self.capturedtext = ""
        # Create a pipe so the stream can be captured:
        self.pipe_out, self.pipe_in = os.pipe()

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, type, value, traceback):
        self.stop()

    def start(self):
        """
        Start capturing the stream data.
        """
        self.capturedtext = ""
        # Save a copy of the stream:
        self.streamfd = os.dup(self.origstreamfd)
        # Replace the original stream with our write pipe:
        os.dup2(self.pipe_in, self.origstreamfd)
        if self.threaded:
            # Start thread that will read the stream:
            self.workerThread = threading.Thread(target=self.readOutput)
            self.workerThread.start()
            # Make sure that the thread is running and os.read() has executed:
            time.sleep(0.01)

    def stop(self):
        """
        Stop capturing the stream data and save the text in `capturedtext`.
        """
        # Print the escape character to make the readOutput method stop:
        self.origstream.write(self.escape_char)
        # Flush the stream to make sure all our data goes in before
        # the escape character:
        self.origstream.flush()
        if self.threaded:
            # wait until the thread finishes so we are sure that
            # we have until the last character:
            self.workerThread.join()
        else:
            self.readOutput()
        # Close the pipe:
        os.close(self.pipe_in)
        os.close(self.pipe_out)
        # Restore the original stream:
        os.dup2(self.streamfd, self.origstreamfd)
        # Close the duplicate stream:
        os.close(self.streamfd)

    def readOutput(self):
        """
        Read the stream data (one byte at a time)
        and save the text in `capturedtext`.
        """
        while True:
            char = os.read(self.pipe_out, 1).decode(self.origstream.encoding)
            if not char or self.escape_char in char:
                break
            self.capturedtext += char


# In addition to the normal logger, two logger-like printing facilities are
# defined: "job" and "printer". "job" send output to the main job.out file for
# the job, and should be used very sparingly, typically to echo what this step
# will do in the initial summary of the job.
#
# "printer" sends output to the file "step.out" in this steps working
# directory, and is used for all normal output from this step.

logger = logging.getLogger(__name__)
job = printing.getPrinter()
printer = printing.getPrinter("QuickMin")


class QuickMin(seamm.Node):
    """
    The non-graphical part of a QuickMin step in a flowchart.

    Attributes
    ----------
    parser : configargparse.ArgParser
        The parser object.

    options : tuple
        It contains a two item tuple containing the populated namespace and the
        list of remaining argument strings.

    subflowchart : seamm.Flowchart
        A SEAMM Flowchart object that represents a subflowchart, if needed.

    parameters : QuickMinParameters
        The control parameters for QuickMin.

    See Also
    --------
    TkQuickMin,
    QuickMin, QuickMinParameters
    """

    def __init__(self, flowchart=None, title="QuickMin", extension=None, logger=logger):
        """A step for QuickMin in a SEAMM flowchart.

        You may wish to change the title above, which is the string displayed
        in the box representing the step in the flowchart.

        Parameters
        ----------
        flowchart: seamm.Flowchart
            The non-graphical flowchart that contains this step.

        title: str
            The name displayed in the flowchart.
        extension: None
            Not yet implemented
        logger : Logger = logger
            The logger to use and pass to parent classes

        Returns
        -------
        None
        """
        logger.debug(f"Creating QuickMin {self}")

        super().__init__(
            flowchart=flowchart,
            title="QuickMin",
            extension=extension,
            module=__name__,
            logger=logger,
        )  # yapf: disable

        self._metadata = quickmin_step.metadata
        self.parameters = quickmin_step.QuickMinParameters()

    @property
    def version(self):
        """The semantic version of this module."""
        return quickmin_step.__version__

    @property
    def git_revision(self):
        """The git version of this module."""
        return quickmin_step.__git_revision__

    def description_text(self, P=None):
        """Create the text description of what this step will do.
        The dictionary of control values is passed in as P so that
        the code can test values, etc.

        Parameters
        ----------
        P: dict
            An optional dictionary of the current values of the control
            parameters.
        Returns
        -------
        str
            A description of the current step.
        """
        if P is None:
            P = self.parameters.values_to_dict()

        n_steps = P["n_steps"]
        forcefield = P["forcefield"]
        if forcefield == "best available":
            ff_name = "the best available forcefield"
        else:
            ff_name = forcefield.split()[0]

        text = f"Minimizing the structure with {ff_name}, with a maximum of "
        text += f"{n_steps} steps."

        if "Create" in P["structure handling"]:
            text += " The optimized structure will be put in a new configuration "
        else:
            text += " The optimized structure will overwrite the current configuration "

        confname = P["configuration name"]
        if confname == "use SMILES string":
            text += "using SMILES as its name."
        elif confname == "use Canonical SMILES string":
            text += "using canonical SMILES as its name."
        elif confname == "keep current name":
            text += "keeping the current name."
        elif confname == "optimized with <Forcefield>":
            if forcefield == "best available":
                text += (
                    "with 'optimized with <the name of the forcefield used>' as its"
                    " name."
                )
            else:
                text += f"with 'optimized with {ff_name}' as its name."
        elif confname == "use configuration number":
            text += "using the index of the configuration (1, 2, ...) as its name."
        else:
            confname = confname.replace("<Forcefield>", ff_name)
            text += f"with '{confname}' as its name."

        return self.header + "\n" + __(text, **P, indent=4 * " ").__str__()

    def run(self):
        """Run a QuickMin step.

        Parameters
        ----------
        None

        Returns
        -------
        seamm.Node
            The next node object in the flowchart.
        """
        global OpenBabel_version

        next_node = super().run(printer)
        # Get the values of the parameters, dereferencing any variables
        P = self.parameters.current_values_to_dict(
            context=seamm.flowchart_variables._data
        )

        # Print what we are doing
        printer.important(__(self.description_text(P), indent=self.indent))

        # Add the citations for Open Babel
        self.references.cite(
            raw=self._bibliography["openbabel"],
            alias="openbabel_jcinf",
            module="quickmin_step",
            level=1,
            note="The principle Open Babel citation.",
        )

        # See if we can get the version of obabel
        if OpenBabel_version is None:
            path = shutil.which("obabel")
            if path is not None:
                path = Path(path).expanduser().resolve()
                try:
                    result = subprocess.run(
                        [str(path), "--version"],
                        stdin=subprocess.DEVNULL,
                        capture_output=True,
                        text=True,
                    )
                except Exception:
                    OpenBabel_version = "unknown"
                else:
                    OpenBabel_version = "unknown"
                    lines = result.stdout.splitlines()
                    for line in lines:
                        line = line.strip()
                        tmp = line.split()
                        if len(tmp) == 9 and tmp[0] == "Open":
                            OpenBabel_version = {
                                "version": tmp[2],
                                "month": tmp[4],
                                "year": tmp[6],
                            }
                        break

        if isinstance(OpenBabel_version, dict):
            try:
                template = string.Template(self._bibliography["obabel"])

                citation = template.substitute(
                    month=OpenBabel_version["month"],
                    version=OpenBabel_version["version"],
                    year=OpenBabel_version["year"],
                )

                self.references.cite(
                    raw=citation,
                    alias="obabel-exe",
                    module="quickmin_step",
                    level=1,
                    note="The principle citation for the Open Babel executables.",
                )
            except Exception:
                pass
        # Add the citations for Open Babel
        self.references.cite(
            raw=self._bibliography["bs93"],
            alias="PATTY",
            module="quickmin_step",
            level=1,
            note="The atom typer in OpenBabel.",
        )

        directory = Path(self.directory)
        directory.mkdir(parents=True, exist_ok=True)

        # Get the current system and configuration (ignoring the system...)
        system, configuration = self.get_system_configuration(None)

        obmol = configuration.to_OBMol()

        if P["forcefield"] == "best available":
            for ff_name in ("GAFF", "MMFF94s", "Ghemical", "UFF"):
                obFF = openbabel.OBForceField.FindForceField(ff_name)

                if obFF is None:
                    self.logger.warning(f"Couldn't find forcefield '{ff_name}'")
                    continue

                obFF.SetLogToStdErr()
                obFF.SetLogLevel(1)
                # see https://stackoverflow.com/questions/50978464/redirect-logs-to-file-in-pybel  # noqa: E501
                out = OutputGrabber(sys.stderr)
                with out:
                    if not obFF.Setup(obmol):
                        if ff_name == "UFF":
                            raise RuntimeError(
                                "Could not find a forcefield for the molecule"
                            )
                        continue
                    obFF.ConjugateGradients(P["n_steps"])

                    energy = obFF.Energy(False)
                    units = obFF.GetUnit()

                path = Path(self.directory) / "min.out"
                path.write_text(out.capturedtext)
                break
        else:
            ff_name = P["forcefield"].split()[0]
            obFF = openbabel.OBForceField.FindForceField(ff_name)

            if obFF is None:
                raise RuntimeError(f"Couldn't find forcefield '{ff_name}'")

            obFF.SetLogToStdErr()
            obFF.SetLogLevel(1)
            # see https://stackoverflow.com/questions/50978464/redirect-logs-to-file-in-pybel  # noqa: E501
            out = OutputGrabber(sys.stderr)
            with out:
                if not obFF.Setup(obmol):
                    raise RuntimeError(
                        f"Could not assign forcefield {ff_name} to the molecule"
                    )
                obFF.ConjugateGradients(P["n_steps"])

                energy = obFF.Energy(False)
                units = obFF.GetUnit()

            path = Path(self.directory) / "min.out"
            path.write_text(out.capturedtext)

        # Set the model chemistry to the forcefield name.
        self._model = ff_name

        # Check for convergence
        lines = out.capturedtext.splitlines()
        tmp = lines[-2].split()
        if len(tmp) == 3:
            n_iterations = tmp[0]
        else:
            n_iterations = "unknown"
        converged = "HAS CONVERGED" in lines[-1]

        # Set up the results data
        data = {}
        if units == "kJ/mol":
            data["total energy"] = energy
        else:
            data["total energy"] = Q_(energy, units).m_as("kJ/mol")

        if converged:
            text = (
                f"The minimization converged in {n_iterations} steps to "
                f"{energy:.3f} {units}."
            )
        else:
            text = (
                f"The minimization did not converge in {n_iterations} steps! "
                f"The final energy was {energy:.3f} {units}."
            )

        # Save the structure
        if (
            "structure handling" in P
            and P["structure handling"] == "Create a new configuration"
        ):
            configuration = system.create_configuration(
                periodicity=configuration.periodicity,
                atomset=configuration.atomset,
                bondset=configuration.bondset,
                cell_id=configuration.cell_id,
            )
            text += " The final structure was saved in the new configuration "
        else:
            text += " The final structure replaced the original configuration "

        configuration.from_OBMol(obmol)

        # And the name of the configuration.
        if "configuration name" in P:
            if P["configuration name"] == "optimized with <Forcefield>":
                configuration.name = f"optimized with {ff_name}"
            elif P["configuration name"] == "keep current name":
                pass
            elif P["configuration name"] == "use SMILES string":
                configuration.name = configuration.smiles
            elif P["configuration name"] == "use Canonical SMILES string":
                configuration.name = configuration.canonical_smiles
            elif P["configuration name"] == "use configuration number":
                configuration.name = str(configuration.n_configurations)

        name = configuration.name
        if len(name) > 30:
            name = name[0:30] + "..."
        text += f"named '{name}'."

        printer.normal(__(text, indent=self.indent))
        printer.normal("")

        # Add the citation(s) for the forcefield
        if "MMFF94" in ff_name:
            self.references.cite(
                raw=self._bibliography["MMFF94-1"],
                alias="MMFF94-1",
                module="quickmin_step",
                level=1,
                note="The main MMFF94 citation.",
            )
            if ff_name == "MMFF94s":
                self.references.cite(
                    raw=self._bibliography["MMFF94s"],
                    alias="MMFF94s",
                    module="quickmin_step",
                    level=1,
                    note="The main MMFF94, static version, citation.",
                )
            # The remaining MMF94 citations
            for i in range(2, 6):
                citation = f"MMFF94-{i}"
                self.references.cite(
                    raw=self._bibliography[citation],
                    alias=citation,
                    module="quickmin_step",
                    level=2,
                    note=f"The MMFF94 citation #{i}.",
                )
        else:
            self.references.cite(
                raw=self._bibliography[ff_name],
                alias=ff_name,
                module="quickmin_step",
                level=1,
                note=f"The main {ff_name} citation.",
            )

        # Put any requested results into variables or tables
        self.store_results(
            configuration=configuration,
            data=data,
        )

        # Add other citations here or in the appropriate place in the code.
        # Add the bibtex to data/references.bib, and add a self.reference.cite
        # similar to the above to actually add the citation to the references.

        return next_node
