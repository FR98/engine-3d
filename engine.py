"""
---------------------------------------------------------------------------------------------------
	Author:
	Francisco Rosal 18676
---------------------------------------------------------------------------------------------------
"""

from gl import Render
from color import Color


r = Render.glInit(24, 24)
# r.glCreateWindow(11, 11)
# r.glViewPort(2, 2, 9, 9)

r.glCreateWindow(16, 16)
r.glViewPort(2, 2, 9, 9)

r.glClear()
r.glClearColor(0, 0, 1)
r.glClearBlack()

r.glColor(0, 0, 1)
r.glVertex(-1, -1)
r.glVertex(-1, 1)
r.glVertex(0, 0)
r.glVertex(1, -1)
r.glVertex(1, 1)
r.glFinish()
