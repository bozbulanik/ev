from modules.base_module import BaseModule
from pathlib import Path
import json
from datetime import datetime
import os


class TaskModule(BaseModule):
    """Task Module

Usage: task [command] <args>

Examples:
task add <task> <due_to>            Add a new task.
task remove <task_id(s)>            Remove task(s).
task edit <task_id> <task>          Edit a task.
task complete <task_id(s)>          Mark task(s) as complete.
task undo <task_id(s)>              Undo task(s).
task list                           List all the tasks.
    """

    def __init__(self):
        self.tasks_file = Path(__file__).parent.parent / "data" / "tasks.json"
        self.tasks = self._load_tasks()

    def _load_tasks(self):
        if self.tasks_file.exists():
            try:
                with open(self.tasks_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                return []
        else:
            return []

    def _save_tasks(self):
        with open(self.tasks_file, 'w') as f:
            json.dump(self.tasks, f, indent=2)
            
 
    def _add_task(self, content, due_to):
        if not content:
            return "Please provide the task content."
        content = " ".join(content)
        task = {
            'id': len(self.tasks) + 1,
            'content': content,
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'completed': False,
            'due_to': due_to
        }
        self.tasks.append(task)
        self._reindex_tasks()
        self._save_tasks()
        return f"Task added: {content}"
    
    def _list_tasks(self):
        if not self.tasks:
            return "No tasks found."
        
        longest_element = max(self.tasks, key=lambda task: len(task['content']))
        longest_element_len = (
            len(str(longest_element['id'])) +
            len(str(longest_element['content'])) +
            len(str(longest_element['created_at'])) + 10
        )
        term_size = os.get_terminal_size()[0]
        hr_size = min(longest_element_len, term_size)

        task_list = ["\nYour Tasks:", "-" * hr_size]
        for task in self.tasks:
            status = "x" if task['completed'] else " "
            task_list.append(f"{task['id']}. [{status}] - {task['content']} ({task['created_at']})")
        task_list.append("-" * hr_size)
        
        return "\n".join(task_list)

    def _complete_task(self, *task_ids):
        if not task_ids:
            return "Please provide at least one task ID."
        
        valid = []
        invalid = []
        
        for task_id in task_ids:
            try:
                task_id = int(task_id)
            except ValueError:
                invalid.append(task_id)
                continue
            
            task_found = False
            for task in self.tasks:
                if task['id'] == task_id:
                    task['completed'] = True
                    valid.append(task_id)
                    task_found = True
                    break
            
            if not task_found:
                invalid.append(str(task_id))
                        
        self._save_tasks()
        result = []
        if valid:
            result.append(f"Tasks {', '.join(map(str, valid))} marked as complete!")
        if invalid:
            result.append(f"Tasks with IDs {', '.join(invalid)} not found.")

        return "\n".join(result)
    
    def _undo_task(self, *task_ids):
        if not task_ids:
            return "Please provide at least one task ID."
        
        valid = []
        invalid = []
        
        for task_id in task_ids:
            try:
                task_id = int(task_id)
            except ValueError:
                invalid.append(task_id)
                continue
            
            task_found = False
            for task in self.tasks:
                if task['id'] == task_id:
                    task['completed'] = False
                    valid.append(task_id)
                    task_found = True
                    break
            
            if not task_found:
                invalid.append(str(task_id))
                        
        self._save_tasks()
        result = []
        if valid:
            result.append(f"Tasks {', '.join(map(str, valid))} undone!")
        if invalid:
            result.append(f"Tasks with IDs {', '.join(invalid)} not found.")

        return "\n".join(result)
    
    def _reindex_tasks(self):
        for index, task in enumerate(self.tasks, 1):
            task['id'] = index

    def _remove_task(self, *task_ids):
        if not task_ids:
            return "Please provide at least one task ID."
        valid = []
        invalid = []
        
        for task_id in task_ids:
            try:
                task_id = int(task_id)
            except ValueError:
                invalid.append(task_id)
                continue
            
            task_found = False
            for task in self.tasks:
                if task['id'] == task_id:
                    self.tasks.remove(task)
                    valid.append(task_id)
                    task_found = True
                    break
            
            if not task_found:
                invalid.append(str(task_id))
        
        self._reindex_tasks()
        self._save_tasks()
        result = []
        if valid:
            result.append(f"Tasks {', '.join(map(str, valid))} removed.")
        if invalid:
            result.append(f"Tasks with IDs {', '.join(invalid)} not found.")

        return "\n".join(result)
    

    def _edit_task(self, task_id, content):
        try:
            task_id = int(task_id)
        except ValueError:
            return f"{task_id} is not a valid task ID."
        content = " ".join(content)
        for task in self.tasks:
            if task['id'] == task_id:
                task['content'] = content
                self._save_tasks()
                return f"Task {task_id} edited!"
        return f"Task with ID {task_id} not found."
    
    def execute(self, *args):
        if args:
            match args[0]:
                case "add":
                    return self._add_task(args[1:])
                case "list":
                    return self._list_tasks()
                case "complete":
                    return self._complete_task(*args[1:])
                case "undo":
                    return self._undo_task(*args[1:])
                case "remove":
                    return self._remove_task(*args[1:])
                case "edit":
                    return self._edit_task(args[1], args[2:])
                case _:
                    return self.__class__.__doc__
        else:
            return self.__class__.__doc__