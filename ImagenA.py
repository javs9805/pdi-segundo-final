from utilities import *


def genImagenA(imagen): 
    resultado = None
    marker = generate_marker(imagen)
    # Llamar a la función de reconstrucción morfológica
    reconstructed = morphological_reconstruction(marker,imagen)


    # Calcular el complemento y Convertir la imagen reconstruida a formato 8-bit para visualización
    rellenada = (reconstructed * 255).astype(np.uint8)
    
    resultado = invertir_imagen(imagen - operacion_and(imagen, rellenada))
    
    return resultado



if __name__ == "__main__":
    imagen = cv2.imread('PlacaCircuito.bmp', cv2.IMREAD_GRAYSCALE)
    imagenA = genImagenA(imagen)
    cv2.imshow('Imagen A', imagenA)
    cv2.waitKey(0)
    cv2.destroyAllWindows()