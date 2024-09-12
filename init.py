import numpy as np

memory = np.ones((92,2),dtype=np.int32)
np.save("memory.npy",memory)