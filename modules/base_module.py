class BaseModule:
    def execute(self, *args):
        """Override this method in modules to define their behavior."""
        raise NotImplementedError("Subclasses must implement this method.")
        
    def get_help(self):
        """Returns help information for the module."""
        return self.__class__.__doc__ or "No help information available."
