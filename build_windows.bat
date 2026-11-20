@echo off
setlocal
cd /d "%~dp0"
echo ================================================
echo Goblin Mod - Minecraft 1.21.1 / NeoForge 21.1
echo ================================================
where java >nul 2>nul
if errorlevel 1 (
  echo ERROR: Java was not found. Install a 64-bit Java 21 JDK.
  goto failed
)
java -version
where gradle >nul 2>nul
if errorlevel 1 (
  echo ERROR: Gradle was not found on PATH.
  echo Install Gradle 8.8 or newer, then reopen this window.
  echo The first build also needs internet access to download dependencies.
  goto failed
)
gradle --version
if errorlevel 1 goto failed
gradle clean build
if errorlevel 1 goto failed
echo.
echo BUILD SUCCEEDED. Mod JAR files:
dir /b build\libs\*.jar
goto done
:failed
echo.
echo BUILD NOT COMPLETED. Copy the full error output when asking for help.
:done
pause
