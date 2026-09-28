"""Design stubs only. These functions are not installed or implemented."""
from typing import Any
from numpy.random import Generator
from pandas import Series
from ._types import SurrogateBatch

def ar_surrogates(x: Any, B: int, rng: Generator, p: int = 2, *, innovation: str = 'residual') -> SurrogateBatch:
    """Attempt B fitted-null paths with explicit random state, fixed initial observations and recorded failures.

    Requires: finite identifiable stable AR(2) null; positive integer B; Generator; supported innovation.
    Raises: ValueError, NullModelError, NotImplementedOrderError.
    Planned checks: test_surrogates_rng_state,test_surrogates_initial_pair,test_surrogates_no_replacement_draw.
    Acceptance mapping: AT-13; RNG extraction contract.
    """
    ...

def var_surrogates(X: Any, B: int, rng: Generator, p: int = 1) -> SurrogateBatch:
    """Generate vector-residual surrogates only after the E2 model and random-stream contract are frozen.

    Requires: finite aligned 2D data; positive B/p; Generator; frozen E2 specification.
    Raises: ValueError, NullModelError, PendingMethodError.
    Planned checks: test_var_whole_residual_vectors,test_var_frozen_e2_reference.
    Acceptance mapping: AT-12; frozen E2 outputs.
    """
    ...

