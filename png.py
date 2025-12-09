import matplotlib.pyplot as plt
import deflate
from PIL import Image
import numpy as np

image = [
    [[2,221,111],[22,22,11],[22,22,11]],
    [[22,22,11],[2,221,111],[2,22,111]],
    [[22,22,11],[2,22,111],[2,221,111]]     
]

def preparation_deflate(image,filtre_type=0):
    flux = []
    for i_l,ligne in enumerate(image):
    
        for i_e,e in enumerate(ligne):
            flux.extend(e)
    return flux


rose = Image.open("./test_repetitive.bmp")
rose_array = np.array(rose)
deflate.deflate(preparation_deflate(rose_array))