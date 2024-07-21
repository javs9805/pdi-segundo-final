from utilities import *

def genImagenE(imagen):
    resultado = None
    inverted_image = invertir_imagen(imagen)

    # Crear la imagen marcador
    marker = np.zeros_like(imagen)
    marker[0, :] = inverted_image[0, :]
    
    x = morphological_reconstruction(marker,imagen)
    x = (x*255).astype(np.uint8)
    marker2 = np.zeros_like(imagen)
    marker2[-1, :] = inverted_image[-1, :]

    marker2 = np.zeros_like(imagen)
    marker2[-1, :] = inverted_image[-1, :]

    y = morphological_reconstruction(marker2,imagen)
    y = (y*255).astype(np.uint8)
    z = cv2.bitwise_and(x,y)
    marker3 = np.zeros_like(imagen)
    marker3[:, -1] = inverted_image[:, -1]
    w = morphological_reconstruction(marker3,imagen)
    w = (w*255).astype(np.uint8)

    resultado = operacion_and(x,w) + z
    return resultado



if __name__ == "__main__":
    imagen = cv2.imread('PlacaCircuito.bmp', cv2.IMREAD_GRAYSCALE)
    imagenE = genImagenE(imagen)
    cv2.imshow('Imagen E', imagenE)
    cv2.waitKey(0)
    cv2.destroyAllWindows()