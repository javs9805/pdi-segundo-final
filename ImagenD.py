from utilities import *
from ImagenA import genImagenA
from ImagenB import genImagenB
from ImagenC import genImagenC

def genImagenD(imagen,imagenC):
    imagenA = genImagenA_2(imagen)    
    resultado = imagen - imagenC
    resultado = resultado - imagenA
    #TENEMOS QUE QUITAR EL PUNTITO 23
    return resultado

def genImagenA_2(imagen): 
    resultado = None
    marker = generate_marker(imagen)
    # Llamar a la función de reconstrucción morfológica
    reconstructed = morp_reconstruction_2(marker,imagen)


    # Calcular el complemento y Convertir la imagen reconstruida a formato 8-bit para visualización
    rellenada = (reconstructed * 255).astype(np.uint8)
    
    resultado = invertir_imagen(imagen - operacion_and(imagen, rellenada))
    
    return resultado



if __name__ == "__main__":
    imagen = cv2.imread('PlacaCircuito.bmp', cv2.IMREAD_GRAYSCALE)
    imagenC = genImagenC(imagen,genImagenB(imagen))
    imagenD = genImagenD(imagen,imagenC)
    cv2.imshow('Imagen D', imagenD)
    cv2.waitKey(0)
    cv2.destroyAllWindows()