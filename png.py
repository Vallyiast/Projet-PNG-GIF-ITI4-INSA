import matplotlib.pyplot as plt
import deflate
from PIL import Image
import numpy as np
import time

image = [
    [[2,221,111],[22,22,11],[22,22,11]],
    [[22,22,11],[2,221,111],[2,22,111]],
    [[22,22,11],[2,22,111],[2,221,111]]  ,
    [[22,22,11],[2,22,111],[2,221,111]]     ,
    [[22,22,11],[2,22,111],[2,221,111]]        
]

def preparation_deflate(image,filtre_type=0):
    flux = []
    for i_l,ligne in enumerate(image):
    
        for i_e,e in enumerate(ligne):
            flux.extend(e)
    return flux


rose = Image.open("./rose2.jpg")
rose_array = np.array(rose)
print("taille",rose_array.shape)
t1 = time.time()
result = deflate.deflate(preparation_deflate(rose_array))
t2 = time.time()
print("temps (s)",t2-t1)

array = bytearray([int(result[i:i+7],2) for i in range(0,len(result),8)])
with open("result.txt", "wb") as binary_file:
  
    binary_file.write(array)