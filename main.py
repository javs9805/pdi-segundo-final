import numpy as np
from scipy.ndimage import binary_dilation
import cv2


# Función para la reconstrucción de la imagen
def morphological_reconstruction(marker, mask):
    """
    Realiza la reconstrucción morfológica binaria.
    
    :param marker: Imagen binaria que sirve como marcador.
    :param mask: Imagen binaria que sirve como máscara.
    :return: Imagen reconstruida.
    """
    # Verificar que las dimensiones de marker y mask sean las mismas
    if marker.shape != mask.shape:
        raise ValueError("Las dimensiones de marker y mask deben ser iguales.")
    
    # Inicializar la imagen reconstruida
    reconstructed = marker.copy()
    
    while True:
        previous = reconstructed.copy()
        # Aplicar la dilatación a la imagen reconstruida
        dilated = binary_dilation(reconstructed, structure=np.ones((3, 3)))
        # Realizar la intersección con la máscara usando AND lógico
        reconstructed = dilated & mask
        # Comprobar si hay cambios
        if np.array_equal(reconstructed, previous):
            break
    
    return reconstructed

def generate_marker(binary_image):
    
    # Invertir la imagen binaria
    inverted_image = cv2.bitwise_not(binary_image)

    # Crear la imagen marcador
    marker = np.zeros_like(binary_image)
    marker[0, :] = inverted_image[0, :]
    marker[-1, :] = inverted_image[-1, :]
    marker[:, 0] = inverted_image[:, 0]
    marker[:, -1] = inverted_image[:, -1]
    return marker



# Función para la operación lógica AND
def operacion_and(imagen1, imagen2):
    return cv2.bitwise_and(imagen1, imagen2)

# Función para la operación lógica OR
def operacion_or(imagen1, imagen2):
    return cv2.bitwise_or(imagen1, imagen2)

# Función para la operación lógica XOR
def operacion_xor(imagen1, imagen2):
    return cv2.bitwise_xor(imagen1, imagen2)

# Función para la operación lógica NAND
def operacion_nand(imagen1, imagen2):
    return cv2.bitwise_not(cv2.bitwise_and(imagen1, imagen2))

# Función para la operación lógica NOR
def operacion_nor(imagen1, imagen2):
    return cv2.bitwise_not(cv2.bitwise_or(imagen1, imagen2))

# Función para la inversión de la imagen
def invertir_imagen(imagen):
    return cv2.bitwise_not(imagen)

#NO TOCAR YA FUNCIONAN
def genImagenA(imagen): 
    resultado = None
    marker = generate_marker(imagen)
    # Llamar a la función de reconstrucción morfológica
    reconstructed = morphological_reconstruction(marker,imagen)


    # Calcular el complemento y Convertir la imagen reconstruida a formato 8-bit para visualización
    rellenada = (reconstructed * 255).astype(np.uint8)
    
    resultado = invertir_imagen(imagen - operacion_and(imagen, rellenada))
    
    return resultado

def genImagenB(imagen):

    resultado = None
    marker = generate_marker(imagen)

    # Llamar a la función de reconstrucción morfológica
    reconstructed = morphological_reconstruction(marker,invertir_imagen(imagen))


    # Calcular el complemento y Convertir la imagen reconstruida a formato 8-bit para visualización
    rellenada = (255- reconstructed * 255).astype(np.uint8)
    
    resultado = operacion_nand(invertir_imagen(imagen), rellenada)
    
    return resultado


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
#NO TOCAR YA FUNCIONAN


def getImagenD(imagen,imagenC):
    resultado = imagenC - imagen
    return resultado


def genImagenAux(imagen):
    resultado = None
    imagenB = genImagenB(imagen)
    # imagen sin islas ni pistas
    imagenAux = imagen + invertir_imagen(imagenB)
    resultado = imagenAux
    return resultado



def eliminar_no_agujeros_completos(imagen):
    """
    Elimina de una imagen los elementos que no son agujeros completos.
    
    :param imagen: Imagen en blanco y negro.
    :return: Imagen con solo los agujeros completos.
    """
    # Convertir la imagen a binaria
    _, binaria = cv2.threshold(imagen, 127, 1, cv2.THRESH_BINARY)
    
    # Invertir la imagen para que los agujeros sean blancos (1) y el fondo negro (0)
    invertida = invertir_imagen(binaria)
    
    # Crear un marcador inicial con los bordes de la imagen invertida
    marker = generate_marker(invertida)
    
    # Realizar la reconstrucción morfológica
    reconstruida = morphological_reconstruction(marker, invertida)
    # Invertir la imagen reconstruida para obtener los agujeros completos
    agujeros_completos = invertir_imagen(reconstruida)
    
    # Convertir la imagen de agujeros completos a formato 8-bit para visualización   
    return agujeros_completos

# Ejemplo de uso
if __name__ == "__main__":
    imagen = cv2.imread('PlacaCircuito.bmp', cv2.IMREAD_GRAYSCALE)

    imagenA = genImagenA(imagen)
    imagenB = genImagenB(imagen)
    imagenC = genImagenC(imagen,imagenB)
    imagenD = getImagenD(imagen,imagenC)
    imagenAux = genImagenAux(imagen)
    
    # Mostrar resultados
#    cv2.imshow('Imagen Original', imagen)
    cv2.imshow('Imagen A', imagenA)
    cv2.imwrite('ImagenA.png',imagenA)
    cv2.imshow('Imagen B', imagenB)
    cv2.imwrite('ImagenB.png',imagenB)
    cv2.imshow('Imagen C', imagenC)
    cv2.imwrite('ImagenC.png',imagenC)
    cv2.imshow('Imagen D', imagenD)
    cv2.imwrite('ImagenD.png',imagenD)
    cv2.waitKey(0)
    cv2.destroyAllWindows()