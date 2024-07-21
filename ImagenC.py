from utilities import *
from ImagenA import genImagenA
from ImagenB import genImagenB

def genImagenC(img0, imgB):
    imgA = genImagenA(img0)

    # Rellenar los huecos de la imagen A
    imgAwithFilledHoles = operacion_xor(imgA, imgB)

    not_B = invertir_imagen(imgB)

    # Reconstruir las islas y las pistas que forman un agujero bien construido de not_B
    rec = morphological_reconstruction(not_B ,imgAwithFilledHoles)
    rec = (rec * 255).astype(np.uint8)
    # Rellenar las pistas y las islas que se formaron con la reconstrucción
    result = operacion_and(rec, imgB)
    return result



if __name__ == "__main__":
    imagen = cv2.imread('PlacaCircuito.bmp', cv2.IMREAD_GRAYSCALE)
    imagenB = genImagenB(imagen)
    imagenC = genImagenC(imagen,imagenB)
    cv2.imshow('Imagen C', imagenC)
    cv2.waitKey(0)
    cv2.destroyAllWindows()