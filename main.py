"""
TO-DO:
    [x] - Task module needs error oversight. Look extreme cases and positional argument errors.
    [ ] - Add due to functionality to task module items.
    [ ] - Edit the general help.
"""

import os
import time
import importlib
from pathlib import Path
from modules.base_module import BaseModule
import json

class HomeSystem:
    def __init__(self):
        self.can_run = False
        self.modules = {}
        self.load_modules()
        self.home_data_file = Path(__file__).parent / "data" / "home_data.json"
        self.home_data = {}
  

    def load_modules(self):
        """Dynamically load all modules from the 'modules' folder."""
        modules_dir = Path(__file__).parent / "modules"
        for file in modules_dir.glob("*_module.py"):
            if file.stem == "base_module":
                continue
            
            module_name = file.stem
            try:
                module = importlib.import_module(f"modules.{module_name}")
                for attr in dir(module):
                    obj = getattr(module, attr)
                    if isinstance(obj, type) and issubclass(obj, BaseModule) and obj is not BaseModule:
                        command_name = module_name.replace("_module", "")
                        self.modules[command_name] = obj()
            except Exception as e:
                print(f"Error loading module '{module_name}': {e}")

    def execute_command(self, command_line):
        args = command_line.split()
        if not args:
            return

        command_name, *command_args = args
        
        if command_name == "help":
            if command_args:
                module_name = command_args[0]
                if module_name in self.modules:
                    print(f"Help for '{module_name}' command:")
                    print(self.modules[module_name].get_help())
                else:
                    print(f"Error: Command '{module_name}' not found.")
            else:
                print("Available commands:")
                print(" - help [command]: Show this help message or help for a specific command")
                print(" - list: List all available commands")
                print(" - exit: Exit the system")
                print("\nFor detailed help on a specific command, type: help <command>")
            return

        module = self.modules.get(command_name)
        if not module:
            print(f"Error: Command '{command_name}' not found.")
            return

        try:
            result = module.execute(*command_args)
            print(result)
        except Exception as e:
            print(f"Error executing command '{command_name}': {e}")

    def list_commands(self):
        for module_name in self.modules:
            print(f" - {module_name}")

    def load_home_data(self):
        print("Loading home data...")
        if self.home_data_file.exists():
            with open(self.home_data_file, 'r') as f:
                self.home_data = json.load(f)
                self.can_run = True
                print("Home data loaded successfully.")
        else:
            print("No home data found. Creating one right now...")
            self.create_new_home()

    def create_new_home(self):
        data_dir = self.home_data_file.parent
        if not data_dir.exists():
            data_dir.mkdir(parents=True)

        owner_name = input("What's your name? ")
        home_name = input("Pick a name for your home? ")
        self.home_data = {
            "home_name": home_name,
            "owner_name": owner_name,
        }
        with open(self.home_data_file, 'w') as f:
            json.dump(self.home_data, f)

        print(f"Thank you {owner_name}!\nNew home {home_name} created successfully.")
        self.load_home_data()

    def run(self):
        self.load_home_data()
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"Welcome to {self.home_data["home_name"]}, {self.home_data["owner_name"]}. Type 'help' for assistance or 'exit' to quit.")
        if self.can_run:
            while True:
                try:
                    command_line = input("> ").strip()
                    if command_line == "exit":
                        print(f"Goodbye, {self.home_data["owner_name"]}!")
                        break
                    elif command_line == "list":
                        self.list_commands()
                    else:
                        self.execute_command(command_line)
                except (EOFError, KeyboardInterrupt):
                    print(f"\nGoodbye, {self.home_data["owner_name"]}!")
                    break

if __name__ == "__main__":
    HomeSystem().run()
