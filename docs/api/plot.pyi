"""Design stubs only. These functions are not installed or implemented."""
from typing import Any
from numpy.random import Generator
from pandas import Series
from ._types import PlotResult

def triangle(*, ax: Any = None) -> PlotResult:
    """Draw the AR(2) stability triangle and labelled boundary, returning figure and axes without automatic file output.

    Requires: None or a supported Matplotlib Axes.
    Raises: ValueError, TypeError.
    Planned checks: test_triangle_plot_coordinates,test_plot_no_implicit_save.
    Acceptance mapping: plot contract; geometry from AT-7.
    """
    ...

def argand(roots: Any, *, ax: Any = None) -> PlotResult:
    """Plot supplied roots with the unit circle and equal aspect, retaining plotted-data provenance.

    Requires: finite 1D complex roots; None or supported Axes.
    Raises: ValueError, TypeError.
    Planned checks: test_argand_coordinates_equal_aspect,test_plot_input_unchanged.
    Acceptance mapping: plot contract.
    """
    ...

def root_path(path: Any, *, ax: Any = None) -> PlotResult:
    """Display chronological root sets; do not connect across undefined gaps or imply unprovided root identities.

    Requires: validated indexed root sets; declared warm-up; tracking identities for connected curves.
    Raises: ValueError, TypeError.
    Planned checks: test_root_path_gaps,test_root_path_identity_required.
    Acceptance mapping: plot contract; causal index convention.
    """
    ...

