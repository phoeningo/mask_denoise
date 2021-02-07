import numpy as np
#gpu_array volume input ,cpu array return
from cupy import fft
import cupy as cp

def zslice(volume):
  x,y,z=volume.shape
  ftvolume=np.fft.fftshift(np.fft.fftn(volume))
  ftslice=ftvolume[int(x/2),:,:]
  rslice=np.float32(np.abs(  np.fft.ifftn(np.fft.ifftshift(ftslice))))
  
  return rslice

def gslice(volume):
  x,y,z=volume.shape

  with cp.cuda.Device(3):
    gvolume=cp.asarray(volume)
  #md=cp.get_array_module(volume)
    ftvolume=fft.fftshift(fft.fftn(gvolume))
    ftslice=ftvolume[int(x/2),:,:]
    rslice=np.float32(np.abs( cp.asnumpy (fft.ifftn(fft.ifftshift(ftslice)))))
  return rslice
