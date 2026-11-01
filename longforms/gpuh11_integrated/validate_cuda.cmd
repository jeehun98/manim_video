@echo off
call "C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Auxiliary\Build\vcvars64.bat" >nul
nvcc -arch=sm_86 -O3 -Xcompiler /utf-8 --ptxas-options=-v longforms\gpuh11_integrated\vector_add.cu -o longforms\gpuh11_integrated\vector_add.exe > longforms\gpuh11_integrated\cuda_compile.log 2>&1
if errorlevel 1 exit /b 1
longforms\gpuh11_integrated\vector_add.exe longforms\gpuh11_integrated\cuda_trace.json > longforms\gpuh11_integrated\cuda_validation.txt
