from modules.base_module import BaseModule

class TestModule(BaseModule):
    """A simple test module that greets users.

    Usage: test [name]
    If no name is provided, defaults to "Stranger"

    Examples:
    > test
    > test Alice
    """

    def execute(self, *args):
        name = args[0] if args else "Stranger"
        return f"Hello, {name}!"
