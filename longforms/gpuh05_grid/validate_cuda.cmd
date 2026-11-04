@echo off
call "C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Auxiliary\Build\vcvars64.bat" >nul
nvcc -arch=sm_86 -O3 -Xcompiler /utf-8 --ptxas-options=-v longforms\gpuh05_grid\grid_examples.cu -o longforms\gpuh05_grid\grid_examples.exe > longforms\gpuh05_grid\cuda_compile.log 2>&1
if errorlevel 1 exit /b 1
longforms\gpuh05_grid\grid_examples.exe longforms\gpuh05_grid\cuda_trace.json > longforms\gpuh05_grid\cuda_validation.txt
