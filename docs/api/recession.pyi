"""Design stubs only. These functions are not installed or implemented."""
from typing import Any
from numpy.random import Generator
from pandas import Series
from ._types import EpisodeSet

def episodes(g: Any, rule: str = 'two_negative', merge: int = 8) -> EpisodeSet:
    """Return retrospective strictly-negative runs merged from the preceding qualifying run's end, retaining the first onset.

    Requires: finite 1D; valid ordered index; only two_negative rule; nonnegative integer merge.
    Raises: ValueError.
    Planned checks: test_episode_zero_break,test_episode_chain_merge,test_isolated_negative_no_clock_reset.
    Acceptance mapping: registered episode convention.
    """
    ...

