from utilities import *
from ImagenE import genImagenE


def genImagenF(imagen, imagenE):
    resultado = None
    inverted_image = invertir_imagen(imagen)
    resultado = imagen - imagenE
    marker3 = np.zeros_like(imagen)
    marker3[:, 0] = inverted_image[:, 0]
    marker3[:, -1] = inverted_image[:, -1]
    w = morphological_reconstruction(marker3,resultado)
    w = (w*255).astype(np.uint8)
    resultado = w
    return resultado


if __name__ == "__main__":
    imagen = cv2.imread("PlacaCircuito.bmp", cv2.IMREAD_GRAYSCALE)
    imagenE = genImagenE(imagen)
    imagenF = genImagenF(imagen, imagenE)
    cv2.imshow("Imagen F", imagenF)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    