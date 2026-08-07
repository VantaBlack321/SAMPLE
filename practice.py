# Source - https://stackoverflow.com/a/49738373
# Posted by handle, modified by community. See post 'Timeline' for change history
# Retrieved 2026-08-07, License - CC BY-SA 3.0

import numpy as np
from PIL import Image # Pillow

w, h, d = 2,2,3
x,y = 0,1

grid = np.zeros((w, h, d), dtype=np.uint8) # NumPyarray for image data
#test = np.zeros(w*h*d, dtype=np.uint8).reshape(w, h, d)
#print(np.array_equal(grid,test)) # => True

# red pixel with NumPy
grid[x, y] = [255, 0, 0]

print(grid[::])

# green pixel with Pillow
img = Image.fromarray(grid, 'RGB')
pixels = img.load()
pixels[x,y] = (0, 255, 0)

# display temporary image file with default application
scale = 100
img.resize((w*scale,h*scale)).show()
