@echo off
call "C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Auxiliary\Build\vcvars64.bat" >nul
nvcc -arch=sm_86 -O3 -Xcompiler /utf-8 --ptxas-options=-v longforms\gpuh08_global_memory\global_examples.cu -o longforms\gpuh08_global_memory\global_examples.exe > longforms\gpuh08_global_memory\cuda_compile.log 2>&1
if errorlevel 1 exit /b 1
longforms\gpuh08_global_memory\global_examples.exe longforms\gpuh08_global_memory\cuda_trace.json > longforms\gpuh08_global_memory\cuda_validation.txt
