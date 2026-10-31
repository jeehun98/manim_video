@echo off
call "C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Auxiliary\Build\vcvars64.bat" >nul
nvcc -arch=sm_86 -O3 -Xcompiler /utf-8 --ptxas-options=-v longforms\gpuh06_register\register_example.cu -o longforms\gpuh06_register\register_example.exe > longforms\gpuh06_register\cuda_compile.log 2>&1
if errorlevel 1 exit /b 1
longforms\gpuh06_register\register_example.exe longforms\gpuh06_register\cuda_trace.json > longforms\gpuh06_register\cuda_validation.txt
