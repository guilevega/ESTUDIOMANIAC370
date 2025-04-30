@echo off

:: install.bat

:: Verificar si Node.js está instalado
where node >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo Error: Node.js no esta instalado.
    echo Por favor, instala Node.js antes de continuar.
    echo Puedes descargarlo desde https://nodejs.org/
    pause
    exit /b 1
)

:: Crear el directorio del proyecto
set PROJECT_DIR=%USERPROFILE%\EstudioManiac370
if exist "%PROJECT_DIR%" (
    echo El directorio %PROJECT_DIR% ya existe. Por favor, elimina o renombra la carpeta antes de continuar.
    pause
    exit /b 1
)

mkdir "%PROJECT_DIR%"
echo Creando directorio del proyecto en %PROJECT_DIR%...

:: Copiar los archivos al directorio del proyecto
copy index.html "%PROJECT_DIR%"
copy indexestrategias.html "%PROJECT_DIR%"
copy estrategias-redes-sociales.html "%PROJECT_DIR%"
copy estado-contables.html "%PROJECT_DIR%"
copy plan-negocios.html "%PROJECT_DIR%"
copy resumen-ejecutivo.html "%PROJECT_DIR%"
copy analisis-mercado.html "%PROJECT_DIR%"
copy estrategia-marketing.html "%PROJECT_DIR%"
copy plan-operativo.html "%PROJECT_DIR%"
copy proyecciones-financieras.html "%PROJECT_DIR%"
copy estrategia-crecimiento.html "%PROJECT_DIR%"
copy header-menu.html "%PROJECT_DIR%"
copy right-sidebar-menu.html "%PROJECT_DIR%"
copy left-sidebar-menu.html "%PROJECT_DIR%"
copy styles.css "%PROJECT_DIR%"
copy scripts.js "%PROJECT_DIR%"
copy load-menus.js "%PROJECT_DIR%"
copy server.js "%PROJECT_DIR%"
echo Archivos copiados a %PROJECT_DIR%...

:: Cambiar al directorio del proyecto
cd /d "%PROJECT_DIR%"

:: Iniciar el servidor
echo Iniciando el servidor...
start /b node server.js

:: Mostrar instrucciones
echo Instalacion completada!
echo El sitio web esta corriendo en http://localhost:3000
echo Para detener el servidor, cierra esta ventana o presiona Ctrl+C.
echo Para modificar los menus, edita los archivos header-menu.html, right-sidebar-menu.html o left-sidebar-menu.html en %PROJECT_DIR%.
pause