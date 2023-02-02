import numpy as np
from plotoptix import TkOptiX
from plotoptix import NpOptiX
import matplotlib.pyplot as plt

nu = 50
nv = 50
    
def displayResults(rt):

    print("Launch finished.")

    hitPositionsData = rt._hit_pos
    xHitPositions = hitPositionsData[:, :, 0]
    yHitPositions = hitPositionsData[:, :, 1]
    zHitPositions = hitPositionsData[:, :, 2]
    dHitPositions = hitPositionsData[:, :, 3]

    hitTriangle   = rt._geo_id[:, :, 1].reshape(rt._height, rt._width)

    print("Shape of rays array is {}.".format(xHitPositions.shape))

    xHitPositions = xHitPositions[hitTriangle < 0xFFFFFFFF]
    yHitPositions = yHitPositions[hitTriangle < 0xFFFFFFFF]
    dHitPositions[np.where(hitTriangle >= 0xFFFFFFFF)] = -1
    hitTriangle[np.where(hitTriangle >= 0xFFFFFFFF)] = 3

    print("Shape of hitting rays array is {}.".format(xHitPositions.shape))

    plt.plot(xHitPositions, yHitPositions, 'bo')
    plt.show()

    plt.imshow(dHitPositions)
    plt.colorbar()
    plt.show()

    plt.imshow(hitTriangle)
    plt.colorbar()
    plt.show()

    plt.draw()


verticesTriangle    = np.array([[-2, -2, 0], [2, -2, 0], [-2, 2, 0], [2,  2, 0]])
faceTriangle        = np.array([[0, 1, 2], [1, 2, 3]])

rt                  = NpOptiX(on_rt_accum_done = displayResults, width = nu, height = nv)
#rt                  = NpOptiX(width = nu, height = nv)

rt.set_mesh("Mesh", verticesTriangle, faceTriangle)

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
 
rt.setup_camera("custom_cam", cam_type = "CustomProjXYZtoDir", textures = ["origins", "directions"])

rt.set_param(max_accumulation_frames = 1)

rt.start()

#rt.close()
