from .bot import Bot


class SimpleBot(Bot):
    @property
    def name(self):
        return "SimpleBot"

    @property
    def contributor(self):
        return "Nobleo"

    def compute_commands(self):
        return 0.5, 0.5
