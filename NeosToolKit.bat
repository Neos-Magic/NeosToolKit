@echo off
title Iniciando Neos Toolkit...
cls

echo ==================================================
echo           INICIANDO NEOS TOOLKIT
echo ==================================================
echo.

:: Validar si Python esta instalado
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python no se encuentra instalado o no esta en el PATH.
    echo Por favor, instala Python y marca la casilla "Add Python to PATH".
    echo.
    pause
    exit
)

:: Validar e instalar customtkinter si hace falta
echo [1/2] Verificando dependencias de Python...
python -c "import customtkinter" >nul 2>&1
if %errorlevel% neq 0 (
    echo [INFO] 'customtkinter' no esta instalado. Instalando ahora...
    python -m pip install customtkinter
    if %errorlevel% neq 0 (
        echo [ERROR] No se pudo instalar 'customtkinter' automaticamente.
        echo Revisa tu conexion a Internet o ejecuta: pip install customtkinter
        pause
        exit
    )
) else (
    echo [OK] Dependencias verificadas correctamente.
)

echo.
echo [2/2] Lanzando la aplicacion grafica (NeosToolKit.py)...
echo No cierres esta ventana mientras uses el programa.
echo --------------------------------------------------

:: Ejecutar el script actualizado
python "%~dp0NeosToolKit.py"

if %errorlevel% neq 0 (
    echo.
    echo [AVISO] La aplicacion se cerro con un codigo de error.
    pause
)