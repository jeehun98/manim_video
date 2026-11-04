@echo off
call "C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Auxiliary\Build\vcvars64.bat" >nul
nvcc -arch=sm_86 -O3 -Xcompiler /utf-8 --ptxas-options=-v longforms\gpuh09_cache\cache_examples.cu -o longforms\gpuh09_cache\cache_examples.exe > longforms\gpuh09_cache\cuda_compile.log 2>&1
if errorlevel 1 exit /b 1
longforms\gpuh09_cache\cache_examples.exe longforms\gpuh09_cache\cuda_trace.json > longforms\gpuh09_cache\cuda_validation.txt
