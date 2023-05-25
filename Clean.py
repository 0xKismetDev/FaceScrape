# Clean out images not useful for facial recognition (eg facivon, svgs...)
import os, glob
for file in glob.glob("presidents/*.svg"):
    #if "some string" not in file:
        os.remove(file)

