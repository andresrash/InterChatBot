from selenium import webdriver
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

# --- Configuración Inicial ---
# Instala y configura el servicio de ChromeDriver automáticamente.
# service = ChromeService(executable_path=ChromeDriverManager().install())
# driver = webdriver.Chrome(service=service)

# Variable global para almacenar el número de la guía a buscar.
# Guia = "24003512457"


# URLs utilizadas en el proceso de automatización.
urlEnvios = "http://reportes.interrapidisimo.com/Reportes/ExploradorEnvios/ExploradorEnvios.aspx"
urlAnterior = "https://www3.interrapidisimo.com/SitioLogin/home/aplicaciones"


def login(driver):
    """
    Intenta iniciar sesión en el portal de Interrapidisimo.
    Tiene un mecanismo de reintentos limitado a 3 intentos en caso de fallo.

    Args:
        driver: Instancia del WebDriver de Selenium.
    """
    wait = WebDriverWait(driver, 15)  # Espera explícita hasta 20 segundos

    for intento in range(3):  # Bucle limitado a 3 intentos.
        try:
            print("Iniciando login de usuario")

            UserInter = input("Por favor, ingresa tu nombre: ")
            PassInter = input("ingresa tu Contraseña: ")

            # Espera a que el campo de usuario sea visible
            username_field = wait.until(
                EC.visibility_of_element_located((By.ID, "usernameLogin"))
            )
            username_field.clear()
            username_field.send_keys("LAUNION.VALLE")

            """
            # usar metodo para sistema automatico 
            username_field.clear()
            username_field.send_keys(UserInter)
            """

            # Espera a que el campo de contraseña sea visible
            password_field = wait.until(
                EC.visibility_of_element_located((By.ID, "passwordLogin"))
            )
            password_field.clear()
            password_field.send_keys(PassInter)

            # Espera a que el botón de login esté clickeable
            boton = wait.until(
                EC.element_to_be_clickable((By.ID, "botonLogin"))
            )
            boton.click()

            return  # Si logra loguear, termina la función

        except (NoSuchElementException, TimeoutException, Exception) as e:
            print(f"Error en login, intento {intento + 1}. Ocurrió un error: {e}. Reintentando en 7 segundos...")
            time.sleep(7)



def SelectApliEnvio(driver, buscar=False, Guia=None):
    """
    Navega desde la página principal a la aplicación 'Explorador de Envíos'.
    Maneja el cambio de pestañas y cierra la pestaña anterior.

    Args:
        driver: Instancia del WebDriver de Selenium.
        buscar (bool): Si es True, llama a la función BuscarGuia después de navegar.
        Guia (str): El número de la guía a buscar.
    """
    wait = WebDriverWait(driver, 10)  # Espera explícita hasta 10 segundos

    for intento in range(3):  # Bucle de reintentos
        try:
            print(" Click Explorador Envios")
            # Espera a que el botón por XPATH sea clickeable
            BsButon = wait.until(
                EC.element_to_be_clickable((By.XPATH, '//*[@title="Explorador Envios"]'))
            )
            BsButon.click()

            try:
                WebDriverWait(driver, 20).until(
                    lambda d: len(d.window_handles) == 2
                )
                print("✅ Detectadas 2 pestañas en el navegador.")

                # Cambia el foco del driver a la nueva pestaña
                nueva_pestana = driver.window_handles[1]
                driver.switch_to.window(nueva_pestana)
            except:
                print("⚠️ No se detectaron 2 pestañas dentro del tiempo de espera.")

            # ✅ Espera explícita a que cargue el campo de número de guía
            GuiaTxt = wait.until(
                EC.visibility_of_element_located((By.ID, 'tbxNumeroGuia'))
            )
            print("✅ Cambio de pestaña y carga confirmados")

            # Cierra la pestaña original y mantiene la nueva
            driver.switch_to.window(driver.window_handles[0])
            driver.close()
            driver.switch_to.window(driver.window_handles[0])

            print("Nueva URL:", driver.current_url)

            # Si 'buscar' es True, procede a buscar la guía
            if buscar and Guia:
                BuscarGuia(driver, Guia)

            break  # Sale del bucle si todo salió bien

        except (NoSuchElementException, TimeoutException, Exception) as e:
            print(
                f"Error en SelectApliEnvio, intento {intento + 1}. Ocurrió un error: {e}. Reintentando en 7 segundos..."
            )
            time.sleep(7)


def BuscarGuia(driver, Guia):
    """
    Busca una guía específica en la página del 'Explorador de Envíos' y extrae sus detalles.

    Args:
        driver: Instancia del WebDriver de Selenium.
        Guia (str): El número de la guía a buscar.

    Returns:
        tuple: Una tupla con los detalles de la guía (VerificaGuia, Telefono, CiudadDestino, TipoEntrega, Direccion)
               o None si falla.
    """
    global urlEnvios, urlAnterior
    wait = WebDriverWait(driver, 15)  # Espera explícita de hasta 15 segundos

    for intento in range(3):  # Bucle de reintentos.
        try:
            # Verifica que esté en la URL correcta para realizar la búsqueda
            if driver.current_url == urlEnvios:
                print("Estamos en la URL correcta ✅ para Buscar Guia", Guia)

                # Esperar a que el campo de guía sea visible
                GuiaTxt = wait.until(
                    EC.visibility_of_element_located((By.ID, 'tbxNumeroGuia'))
                )
                GuiaTxt.clear()
                time.sleep(1)
                GuiaTxt.send_keys(Guia)

                # Esperar a que el botón de búsqueda sea clickeable
                GuiaButon = wait.until(
                    EC.element_to_be_clickable((By.ID, 'btnShow'))
                )
                GuiaButon.click()
                time.sleep(1)  # Pausa para esperar los resultados.

                # 🔹 Verificar que la página terminó de cargar
                wait.until(lambda d: d.execute_script("return document.readyState") == "complete")

                # 🔹 Comprobar si aparece el botón emergente "Aceptar" cuando no encuentra el paquete
                try:
                    ButtonAceptar = WebDriverWait(driver, 3).until(
                        EC.element_to_be_clickable((By.ID, 'Button4'))
                    )
                    print("⚠️ Apareció mensaje emergente. Presionando 'Aceptar'...")
                    ButtonAceptar.click()
                    # esperar a que el campo de búsqueda esté otra vez activo
                    wait.until(EC.visibility_of_element_located((By.ID, 'tbxNumeroGuia')))
                    continue  # volver a intentar la búsqueda
                except TimeoutException:
                    # Si no aparece el botón, seguimos normalmente
                    pass

                # Obtener el HTML actual y parsearlo con BeautifulSoup
                html = driver.page_source
                soup = BeautifulSoup(html, "html.parser")

                # Extraer los datos desde el DOM
                VerificaGuia = soup.find(id="tbxNumeroGuia1")["value"]
                Direccion = soup.find(id="tbxDireccionDes")["value"]
                Telefono = soup.find(id="tbxTelefonoDes")["value"]
                TipoEntrega = soup.find(id="tbxTipoEntrega")["value"]
                CiudadDestino = soup.find(id="tbxCiudadDestino")["value"]


                # 🔍 Verificación de consistencia
                if not VerificaGuia or VerificaGuia != str(Guia):
                    raise Exception(f"❌ La guía encontrada ('{VerificaGuia}') no coincide con la buscada ('{Guia}')")

                print("✅ Datos obtenidos:")
                print(" Guia Respuesta", VerificaGuia, "Ciudad Destino:", CiudadDestino)

                return VerificaGuia, Telefono, CiudadDestino, TipoEntrega, Direccion

            # Si por alguna razón volvió a la URL anterior, intenta navegar de nuevo.
            elif driver.current_url == urlAnterior:
                print("❌ Seguimos en la URL anterior, llamando SelectApliEnvio...")
                SelectApliEnvio(driver, True, Guia)


        except (NoSuchElementException, TimeoutException, Exception) as e:
            print(f"Error en BuscarGuia, intento {intento + 1}. Ocurrió un error: {e}. Reintentando en 7 segundos...")
            time.sleep(7)


def Prueba():  # Funcion para Pruebas
    """
    Función principal de prueba, flujo de la automatización:
    1. Inicia el navegador.
    2. Elimina cookies.
    3. Navega a la página de login.
    4. Llama a las funciones de login, navegación y búsqueda.
    5. Imprime los resultados.
    """
    print("Inicia Test")
    # driver.maximize_window() # Opcional: maximizar la ventana.
    driver.delete_all_cookies()
    driver.get("https://www3.interrapidisimo.com/SitioLogin/auth/login")

    print("Inicia el navegador.")
    login(driver)
    print("Ejecutar SelectApliEnvio. ")
    SelectApliEnvio(driver, Guia=Guia)  # Se pasa buscar=True para que se ejecute la búsqueda.
    print("Ejecutar Buscar Guia ")
    # Desempaqueta los resultados devueltos por BuscarGuia.
    VerificaGuia, Telefono, CiudadDestino, TipoEntrega, Direccion = BuscarGuia(driver, Guia)
    print("Termino Buscar Guia ")
    print(Telefono, VerificaGuia, CiudadDestino, TipoEntrega, Direccion)
    print('finaliza test')

# Para ejecutar el script, se debería llamar a la función principal.
# Prueba()