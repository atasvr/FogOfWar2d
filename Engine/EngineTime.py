"""Utility helpers for dealing with frame time.

The original implementation stored the timing state as global attributes on the
class and expected ``EngineTime.Update`` to be called with the class itself as
an argument.  Besides being fairly confusing, this caused ``pylint`` style
errors and made it hard to reason about what was shared state versus instance
state.

This module now exposes a small class with class methods that clearly express
the shared nature of the timing state while keeping the public API exactly the
same: ``EngineTime.deltaTime`` continues to expose the elapsed time (in
seconds) since the previous frame.
"""

from __future__ import annotations

from dataclasses import dataclass
import pygame


@dataclass
class _TimingState:
    """Container storing the timestamp of the previous frame."""

    last_ticks: int = 0


class EngineTime:
    """Computes the delta time between frames.

    ``deltaTime`` is exposed as a class attribute so the rest of the code can
    continue to access it without keeping a reference to an ``EngineTime``
    instance.  ``update`` is implemented as a class method, ensuring we don't
    rely on the old ``EngineTime.Update(EngineTime)`` pattern.
    """

    deltaTime: float = 0.0
    _state = _TimingState()

    @classmethod
    def update(cls) -> None:
        """Refresh the ``deltaTime`` value based on the current ticks."""

        current_ticks = pygame.time.get_ticks()
        if cls._state.last_ticks == 0:
            # Skip the large spike on the very first frame and treat it as 0.
            cls.deltaTime = 0.0
        else:
            cls.deltaTime = (current_ticks - cls._state.last_ticks) / 1000.0

        cls._state.last_ticks = current_ticks

    @classmethod
    def reset(cls) -> None:
        """Reinitialize the internal timing state.

        ``EngineTime`` keeps the timestamp of the previous frame around so it
        can compute the delta on the next call to :meth:`update`.  When the game
        is restarted (or a different scene is loaded) we want to clear that
        state so the next ``update`` call measures the time since the restart
        instead of the time since the previous play session.
        """

        cls.deltaTime = 0.0
        cls._state.last_ticks = pygame.time.get_ticks()


# Preserve the legacy name so existing code keeps working without changes.
EngineTime.Update = EngineTime.update



