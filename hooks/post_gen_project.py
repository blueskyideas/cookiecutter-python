import cairosvg
import os

print("converting logo to png")
cairosvg.svg2png(url='docs/_static/logo_full.svg', write_to='docs/_static/logo_full.png')
os.remove('docs/_static/logo_full.svg')
print("...done")
