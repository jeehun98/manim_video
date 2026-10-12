import subprocess,sys
for n in [5,6,7]:subprocess.run([sys.executable,'longforms/mm01_cubic_question/build.py','--scene',str(n)],check=True)
subprocess.run([sys.executable,'longforms/mm01_cubic_question/build.py','--concat-only'],check=True)
subprocess.run([sys.executable,'longforms/mm01_cubic_question/make_short.py'],check=True)
