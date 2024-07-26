import pytest

from .bot import Bot


def test_complete_bot():
    class SimpleBot(Bot):
        @property
        def name(self):
            return "SimpleBot"

        @property
        def contributor(self):
            return "Nobleo"

        def compute_commands(self):
            return 0.5, 0.5

    bot = SimpleBot()


def test_missing_compute_commands():
    class Incomplete(Bot):
        @property
        def name(self):
            return "SimpleBot"

        @property
        def contributor(self):
            return "Nobleo"

    with pytest.raises(TypeError):
        Incomplete()


def test_missing_name():
    class Incomplete(Bot):
        @property
        def contributor(self):
            return "Nobleo"

        def compute_commands(self):
            return 0.5, 0.5

    with pytest.raises(TypeError):
        Incomplete()


def test_missing_contributor():
    class Incomplete(Bot):
        @property
        def name(self):
            return "SimpleBot"

        def compute_commands(self):
            return 0.5, 0.5

    with pytest.raises(TypeError):
        Incomplete()
