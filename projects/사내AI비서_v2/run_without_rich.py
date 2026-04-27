import sys
import runpy

from rich import box
import rich.console
import rich.table

# Monkey patch console rule to just print the title
original_rule = rich.console.Console.rule
def new_rule(self, title="", *args, **kwargs):
    pass
rich.console.Console.rule = new_rule

# Monkey patch Table init to remove borders
original_init = rich.table.Table.__init__
def new_init(self, *args, **kwargs):
    kwargs['box'] = None  # Removes outer border
    kwargs['show_edge'] = False
    original_init(self, *args, **kwargs)
rich.table.Table.__init__ = new_init

if __name__ == "__main__":
    import os
    if len(sys.argv) < 2:
        sys.exit(1)
    
    # Add cwd to sys.path so that 'tuning' module can be found
    sys.path.insert(0, os.getcwd())
    
    # sys.argv[0] is run_without_rich.py
    # sys.argv[1] is the module to run
    module_name = sys.argv[1]
    
    # Adjust sys.argv so the target module sees its own args
    sys.argv = [module_name] + sys.argv[2:]
    
    runpy.run_module(module_name, run_name="__main__")
