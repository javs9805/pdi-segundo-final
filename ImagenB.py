from utilities import *


def genImagenB(imagen):

    resultado = None
    marker = generate_marker(imagen)

    # Llamar a la función de reconstrucción morfológica
    reconstructed = morphological_reconstruction(marker,invertir_imagen(imagen))


    # Calcular el complemento y Convertir la imagen reconstruida a formato 8-bit para visualización
    rellenada = (255- reconstructed * 255).astype(np.uint8)
    
    resultado = operacion_nand(invertir_imagen(imagen), rellenada)
    
    return resultado


if __name__ == "__main__":
    imagen = cv2.imread('PlacaCircuito.bmp', cv2.IMREAD_GRAYSCALE)
    imagenB = genImagenB(imagen)
    cv2.imshow('Imagen B', imagenB)
    cv2.waitKey(0)
    cv2.destroyAllWindows()