import matplotlib.pyplot as plt
import deflate


image = [
    [[2,221,111],[22,22,11],[22,22,11]],
    [[22,22,11],[2,221,111],[2,22,111]],
    [[22,22,11],[2,22,111],[2,221,111]]     
]

def preparation_deflate(image,filtre_type=0):
    flux = []
    for i_l,ligne in enumerate(image):
        flux.append(0)
        for i_e,e in enumerate(ligne):
            flux.extend(e)
    return flux

print(preparation_deflate(image))


deflate.deflate(preparation_deflate(image))