from pathlib import Path
ROOT=Path(__file__).resolve().parent
p=ROOT/'build.py';p.write_text(p.read_text(encoding='utf-8').replace('evdsvd07_inverse','evdsvd08_final_choice'),encoding='utf-8')
p=ROOT/'verify_final.py';s=p.read_text(encoding='utf-8').replace('evdsvd07_inverse','evdsvd08_final_choice').replace('142','149').replace('4260','4470')
a=s.index('    for t,name in ');b=s.index(':\n        target=',a)
s=s[:a]+"    for t,name in [(8.5,'rounds'),(39.5,'negative'),(55.,'powers'),(79.5,'directions'),(85.5,'same_output'),(92.5,'loss'),(97.5,'approximation'),(117.5,'conditions'),(134.5,'champion'),(140.5,'question'),(148.5,'ending')]"+s[b:]
p.write_text(s,encoding='utf-8')
