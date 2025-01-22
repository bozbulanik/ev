from modules.base_module import BaseModule
from pathlib import Path
import json
from datetime import datetime

class ShoppingListModule(BaseModule):
    """Shopping List Module

Usage: sl [command] <args>

Examples:
sl create <name>                        Create a new shopping list.
sl add <item> <sl_id>                   Add a new item to a shopping list.
sl remove <item_id> <sl_id>             Remove an item from a shopping list.
sl edit <item_id> <sl_id> <item>        Edit an item in a shopping list.
sl list                                 List all the shopping lists.
sl list <sl_id>                         List a shopping list.
"""

    def __init__(self):
        self.sls_file = Path(__file__).parent.parent / "data" / "shoppinglists.json"
        self.sls = self._load_sls()

    def _load_sls(self):
        if self.shoppinglists_file.exists():
            try:
                with open(self.sls_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                return []
        else:
            return []

    def _save_sls(self):
        with open(self.tasks_file, 'w') as f:
            json.dump(self.tasks, f, indent=2)

    def execute(self, *args):
        if args:
            match args[0]:

                case _:
                    return self.__class__.__doc__
        else:
            return self.__class__.__doc__