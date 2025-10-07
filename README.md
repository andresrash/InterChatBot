# InterChatBot
Fail -  Chat de whatsapp API para contextar mensajes
Fail - Conectar con Inteligencia Artificial 
ok - Automatizador de Consultas de Guías - Interrapidísimo
Este script de Python automatiza el proceso de consultar múltiples números de guía en la plataforma web de Interrapidísimo. Lee una lista de guías desde un archivo Excel, busca cada una en la web, extrae la información relevante y guarda los resultados de nuevo en el mismo archivo Excel.

🚀 Características
Lectura Automatizada desde Excel: Lee todos los números de guía desde la primera columna de un archivo .xlsx.
Login Automático: Inicia sesión en la plataforma de Interrapidísimo sin intervención manual.
Procesamiento por Lotes: Recorre cada guía, la busca y extrae los datos necesarios.
Escritura de Resultados: Guarda la información obtenida (estado, teléfono, dirección, etc.) en las columnas correspondientes del archivo Excel.
Robustez y Reanudación: Si una guía falla, el script continúa con la siguiente. Está diseñado para saltar las guías que ya han sido procesadas (si la columna de resultados ya contiene datos), permitiendo reanudar el trabajo fácilmente en caso de interrupción.
Manejo de Errores: Gestiona excepciones comunes para evitar que el programa se detenga inesperadamente.
📋 Prerrequisitos
Antes de ejecutar el script, asegúrate de tener instalado:

Python 3.7 o superior.
Navegador Google Chrome (actualizado).
El archivo de Excel con las guías a consultar.
Instala las dependencias necesarias
pip install openpyxl selenium webdriver-manager 

🤝 Contribuciones
Las sugerencias y pull requests son bienvenidos. Para cambios mayores, por favor, abre un issue primero para discutir qué te gustaría modificar.

📝 Licencia
Este proyecto es para uso personal o interno.