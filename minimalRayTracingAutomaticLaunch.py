import  numpy               as      np
from    plotoptix           import  NpOptiX
import  matplotlib.pyplot   as      plt
import  threading

class params:
    done = threading.Event()

verticesTriangle1   = np.array([[-1, -1, 0], [1, -1, 0], [-1, 1, 0]])
verticesTriangle2   = np.array([[1, -1, 0], [1, 1, 0], [-1, 1, 0]])
faceTriangle1       = np.array([0, 1, 2])
faceTriangle2       = np.array([0, 1, 2])

rt                  = NpOptiX(width = 20, height = 20)

rt.set_mesh("Mesh1", verticesTriangle1, faceTriangle1)
rt.set_mesh("Mesh2", verticesTriangle2, faceTriangle2)

rt.setup_camera("Cam", eye = [0, 0, 2], fov = 10)

rt.start()

# --- https://superfastpython.com/thread-event-object-in-python/
if params.done.wait(3):
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