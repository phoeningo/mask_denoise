import numpy as np


#define a canvas (arr.size*4)
def shift (arr,dx,dy):
  x,y=arr.shape
  expx=int(x/2)
  expy=int(y/2)
  try:
    assert abs(dx)<expx and abs(dy)<expy ," Large image shift.Ignore this one "
  except:
    return arr
  canvas=np.zeros(shape=(x+expx*2,y+expx*2),dtype=arr.dtype)
  canvas[expx:expx+x,expy:expy+y]=arr[:,:]
  output=np.empty_like(arr)
  output[:,:]=canvas[expx+dx:expx+dx+x,expy+dy:expy+dy+y]  
  arr=None
  canvas=None
  return output


def shift3d(arr,dx,dy,dz):
  pass
