import sys

from scipy.misc import imread
from scipy.linalg import norm
from scipy import sum, average

def to_grayscale(arr):
    "If arr is a color image (3D array), convert it to grayscale (2D array)."
    if len(arr.shape) == 3:
        return average(arr, -1)  # average over the last axis (color channels)
    else:
        return arr
    
def normalize(arr):
    rng = arr.max()-arr.min()
    amin = arr.min()
    return (arr-amin)*255/rng

#How to compare. img1 and img2 are 2D SciPy arrays here:
def compare_images(img1, img2):
    # normalize to compensate for exposure difference, this may be unnecessary
    # consider disabling it
    img1 = normalize(img1)
    img2 = normalize(img2)
    # calculate the difference and its norms
    diff = img1 - img2  # elementwise for scipy arrays
    m_norm = sum(abs(diff))  # Manhattan norm
    z_norm = norm(diff.ravel(), 0)  # Zero norm
    return (m_norm, z_norm)

img1 = imread('videos\\BIkHTKk2xf0\\frame24300.jpg').astype(float)
img2 = imread('videos\\BIkHTKk2xf0\\frame25200.jpg').astype(float)
img3 = imread('videos\\BIkHTKk2xf0\\frame26100.jpg').astype(float)
img4 = imread('videos\\BIkHTKk2xf0\\frame27000.jpg').astype(float)
img5 = imread('videos\\BIkHTKk2xf0\\frame27900.jpg').astype(float)
img6 = imread('videos\\BIkHTKk2xf0\\frame28800.jpg').astype(float)
n_m, n_0 = compare_images(img1, img2)

#print ("Manhattan norm:", n_m, "/ per pixel:", n_m/img1.size)
#print ("Zero norm:", n_0, "/ per pixel:", n_0*1.0/img1.size)

print(compare_images(img4,img2))
print(compare_images(img4,img3))
print(compare_images(img4,img1))
print(compare_images(img4,img5))
print(compare_images(img4,img6))
