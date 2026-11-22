from pathlib import Path
import importlib.util
s=importlib.util.spec_from_file_location('shared_classical_quantum',Path(__file__).resolve().parents[1]/'chapter_06/mechanics.py')
m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
MODEL,I,A,EC,H,field,contour,packet,INITIAL,X,psi=m.MODEL,m.I,m.A,m.EC,m.H,m.field,m.contour,m.packet,m.INITIAL,m.X,m.psi
