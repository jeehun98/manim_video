@echo off
call "C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Auxiliary\Build\vcvars64.bat" >nul
nvcc -arch=sm_86 -O3 --ptxas-options=-v longforms\gpuh04_sm\compute.cu -o longforms\gpuh04_sm\compute.exe
if errorlevel 1 exit /b 1
longforms\gpuh04_sm\compute.exe > longforms\gpuh04_sm\cuda_validation.txt
