"""Design stubs only. These functions are not installed or implemented."""
from typing import Any
from numpy.random import Generator
from pandas import Series
from ._types import CSDResult

def csd_test(g: Any, window: int, lookback: int, B: int, rng: Generator, onsets: str = 'endogenous', *, merge: int = 8, innovation: str = 'residual') -> CSDResult:
    """Return observed pre-onset changes and a tie-inclusive plus-one fitted-null comparison with every attempt accounted for.

    Requires: rolling and episode contracts; positive lookback/B; Generator; endogenous/fixed modes; registered retained-sample rules.
    Raises: ValueError, NullModelError, RollingFitError.
    Planned checks: test_csd_plus_one_ties,test_csd_no_episode_denominator,test_csd_failures_invalidate_p,test_csd_frozen_h1_reference.
    Acceptance mapping: AT-14; AT-15; AT-16.
    """
    ...

