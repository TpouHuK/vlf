# Removing console clutter
import pymunkoptions
pymunkoptions.options["debug"] = False
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

# Actual imports
import engine
import visualise
import sensors
import get_fitness
