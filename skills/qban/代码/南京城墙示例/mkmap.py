import sys; sys.path.insert(0,'/workspace/work/mapref')
from terrain import *
m = Map(118.56, 118.92, 31.97, 32.14, z=13)
print(m.W, m.H, m.dem.min(), m.dem.max())
np.save('dem.npy', m.dem)
