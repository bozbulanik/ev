from modules.base_module import BaseModule
from modules.utils.tabler import Tabler
from pathlib import Path
import json
import os
import shlex

class ShoppingListModule(BaseModule):
    """Shopping List Module

Usage: sl [command] <args>
    sl add                                  Creates item adding dialogue.
    sl add <name> <quantity>                Adds new item.
    sl add <"name"> <"quantity">            Adds new item with multiple words.
    sl remove                               Queries the desired item ID(s) to remove and removes them.
    sl remove <item_id(s)>                  Removes the item(s) seperated with a comma or space interchangeably. (2, 4 5 is allowed and parsed as 2nd, 4th and 5th element.)
    sl edit                                 Queries for the edit. 
    sl edit <item_id> <name> <quantity>     Edits the desired item. 
    sl edit <item_id> <"name"> <"quantity"> Edits the desired item with multiple words. Using quotation marks without content leaves value unchanged.
    sl clear                                Clear the shopping list.
    sl list                                 Lists the shopping list.
    sl print                                Pretty prints the shopping list.

Examples:
    sl add "Milk" "4L"                      Adds milk item with 4L quantity to the list.
    sl add Butter 2pcs                      Adds butter item with 2pcs quantity to the list.                  
    sl remove 2, 4, 12                      Removes 2nd, 4th and 12th items from the list.
    sl remove 1 7 25                        Removes first, 7th and 25th items from the list.
    sl edit 5 "Rice" ""                     Edits the 5th element's name to "Rice".
    sl edit 8 Bread 1                       Edits the 8th element's name to Bread and quantity to 1.
"""

    def __init__(self):
        self.slitems_file = Path(__file__).parent.parent / "data" / "shoppinglist.json"
        self.slitems = self._load_slitems()

    def _load_slitems(self):
        if self.slitems_file.exists():
            try:
                with open(self.slitems_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                return []
        else:
            return []

    def _save_slitems(self):
        with open(self.slitems_file, 'w') as f:
            json.dump(self.slitems, f, indent=2)

    def _reindex_slitems(self):
        for index, sl in enumerate(self.slitems, 1):
            sl['id'] = index

    def _list_items(self):
        if not self.slitems:
            return "Shopping list is empty."
        item_list = []
        
        term_size = os.get_terminal_size()[0]

        item_list.append("Shopping List".center(term_size))
        item_list.append("─" * term_size)

        term_size_item = (term_size - 3) // 2
        for item in self.slitems:
            item_list.append(f"{(str(item['id']) + ".").ljust(4)}{item['name'].ljust(term_size_item)}{item['quantity'].rjust(term_size_item)}")
        item_list.append("─" * term_size)
        
        return "\n".join(item_list)

    def _print_items(self):
        item_list = []
        if not self.slitems:
            return "Shopping list is empty."
        
        for item in self.slitems:
            item_list.append([item['name'],item['quantity'],"[ ]"])

        sl = Tabler(title="Shopping List", show_date=True, 
                    rows=item_list, 
                    headers=["Item", "Quantity", "Purchased"], 
                    row_paddings=[0,0,0], 
                    row_alignments=["left", "left", "center"], 
                    header_alignments=["center", "center", "center"])
        result = sl.create_table()
        return result

    def _add_item(self, *item_args):
        if(item_args):
            try:
                args = shlex.split(" ".join(item_args))
                if len(args) > 2: # optional. maybe a bit anti-user pattern?
                    return "Error. Please type <help sl> for the correct usage."
                item = {
                    'id': len(self.slitems) + 1,
                    'name': args[0],
                    'quantity': args[1],
                }
                self.slitems.append(item)
                self._reindex_slitems()
                self._save_slitems()
                return f"{args[0]} with quantity of {args[1]} added to the list."
            except (ValueError, IndexError):
                return "Error. Please type <help sl> for the correct usage"
        
        name = input("Name of the item? ")
        quantity = input("Quantity? ")

        item = {
            'id': len(self.slitems) + 1,
            'name': name,
            'quantity': quantity,
        }
        self.slitems.append(item)
        self._reindex_slitems()
        self._save_slitems()
        return f"{name} with quantity of {quantity} added to the list."

    def _remove_item(self, *item_ids):
        if item_ids:
            args = shlex.shlex(" ".join(item_ids))
            args.whitespace += ","
            args.whitespace_split = True
            args = list(args)
            
            valid = []
            invalid = []
            
            for item_id in args:
                try:
                    item_id = int(item_id)
                except ValueError:
                    invalid.append(item_id)
                    continue
                
                item_found = False
                for item in self.slitems:
                    if item['id'] == item_id:
                        self.slitems.remove(item)
                        valid.append(item_id)
                        item_found = True
                        break
                
                if not item_found:
                    invalid.append(str(item_id))
            
            self._reindex_slitems()
            self._save_slitems()
            result = []
            if valid:
                result.append(f"Items {', '.join(map(str, valid))} removed.")
            if invalid:
                result.append(f"Items with IDs {', '.join(invalid)} not found.")

            return "\n".join(result)
        
        ids = input("Enter ID(s) of the item: ")
        ids = shlex.shlex(ids)
        ids.whitespace += ","
        ids.whitespace_split = True
        ids = list(ids)
    
        valid = []
        invalid = []
        
        for item_id in ids:
            try:
                item_id = int(item_id)
            except ValueError:
                invalid.append(item_id)
                continue
            
            item_found = False
            for item in self.slitems:
                if item['id'] == item_id:
                    self.slitems.remove(item)
                    valid.append(item_id)
                    item_found = True
                    break
            
            if not item_found:
                invalid.append(str(item_id))
        
        self._reindex_slitems()
        self._save_slitems()
        result = []
        if valid:
            result.append(f"Items {', '.join(map(str, valid))} removed.")
        if invalid:
            result.append(f"Items with IDs {', '.join(invalid)} not found.")

        return "\n".join(result)
            
    def _edit_item(self, *args):
        if args:
            try:
                args = shlex.split(" ".join(args))
                if len(args) > 3:
                    return "Error. Please type <help sl> for the correct usage." 
                id = 0
                try:
                    id = int(args[0])
                except ValueError:
                    return f"{args[0]} is not a valid ID."
                
                for item in self.slitems:
                    if item['id'] == id:
                        item['name'] = args[1] if args[1] != "" else item['name']
                        item['quantity'] = args[2] if args[2] != "" else item['quantity']
                        self._save_slitems()
                        return f"Item {id} edited!" if args[1] != "" or args[2] != "" else "Nothing changed."
                return f"Item {id} not found."

            except (IndexError, ValueError):
                return "Error. Please type <help sl> for the correct usage"

        id_input = input("Type the item ID: ")
        name_input = input("Type the name (enter to not change): ")
        quantity_input = input("Type the quantity (enter to not change): ")

        if id_input == "":
            return "Please enter a valid ID.\nNothing has changed..."
        try:
            id_input = int(id_input)
        except ValueError:
            return f"{id_input} is not a valid item ID."

        for item in self.slitems:
            if item['id'] == id_input:
                item['name'] = name_input if name_input != "" else item['name']
                item['quantity'] = quantity_input if quantity_input != "" else item['quantity']
                self._save_slitems()

                return f"Item {id_input} edited!" if name_input != "" or quantity_input != "" else "Nothing changed."
        return f"Item {id_input} not found."
    
    def _clear_items(self):
        if self.slitems:
            confirm = input("Clear the shopping list? (Y/n) ")
            if confirm.lower() == "y" or confirm == "":
                self.slitems = []
                self._save_slitems()
                return "Shopping list cleared."
            else:
                return "Action aborted."
        else:
            return "Shopping list is empty."
    
    def execute(self, *args):
        if args:
            match args[0]:
                case 'list':
                    return self._list_items()
                case 'print':
                    return self._print_items()
                case "add":
                    return self._add_item(*args[1:])
                case 'remove':
                    return self._remove_item(*args[1:])
                case 'edit':
                    return self._edit_item(*args[1:])
                case 'clear':
                    return self._clear_items()
                case _:
                    return self.__class__.__doc__
        else:
            return self.__class__.__doc__
        