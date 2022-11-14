import numpy as np
from plotoptix import TkOptiX
from plotoptix import NpOptiX
import matplotlib.pyplot as plt
#from plotoptix.materials import m_flat

import threading
 
class params:
    done = threading.Event()
 
def wait_for_gpu(rt: NpOptiX) -> None:
    print("gpu done")
    params.done.set()

nu = 20
nv = 20
    
verticesTriangle1   = np.array([[-1, -1, 0], [1, -1, 0], [-1, 1, 0]])
verticesTriangle2   = np.array([[1, -1, 0], [1, 1, 0], [-1, 1, 0]])
faceTriangle1       = np.array([0, 1, 2])
faceTriangle2       = np.array([0, 1, 2])

rt                  = NpOptiX(on_launch_finished = wait_for_gpu, width = nu, height = nv)

rt.set_mesh("Mesh1", verticesTriangle1, faceTriangle1)
rt.set_mesh("Mesh2", verticesTriangle2, faceTriangle2)

u                   = np.linspace(-2, 2, nu)
v                   = np.linspace(-2, 2, nv)
V, U                = np.meshgrid(v, u)
W                   = np.full((nu, nv), -1)
 
originsTexture      = np.stack((U, V, W, np.zeros((nu, nv)))).T
rt.set_texture_2d("origins", originsTexture)
 
cx                  = np.zeros((nu, nv))
cy                  = np.zeros((nu, nv))
cz                  = np.ones((nu, nv))
r                   = np.full((nu, nv), 200)
directionsTexture   = np.stack((cx, cy, cz, r)).T
rt.set_texture_2d("directions", directionsTexture)
 
rt.setup_camera("custom_cam", cam_type = "CustomProjXYZtoDir", textures=["origins", "directions"])

rt.start()

# --- https://superfastpython.com/thread-event-object-in-python/
if params.done.wait(10):
    print("Waiting for event to be set.-.")
else:
    print("Event set. Continue.")

hitPositionsData = rt._hit_pos
xHitPositions = hitPositionsData[:, :, 0]
yHitPositions = hitPositionsData[:, :, 1]
zHitPositions = hitPositionsData[:, :, 2]
dHitPositions = hitPositionsData[:, :, 3]
    
print("Shape of rays array is {}.".format(xHitPositions.shape))

xHitPositions = xHitPositions[dHitPositions < 10]
yHitPositions = yHitPositions[dHitPositions < 10]

print("Shape of hitting rays array is {}.".format(xHitPositions.shape))

plt.plot(xHitPositions, yHitPositions, 'bo')
plt.show()

plt.imshow(dHitPositions)
plt.show()

rt.close()