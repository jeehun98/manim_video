from pathlib import Path
ROOT=Path(__file__).resolve().parent
p=ROOT/'build.py';p.write_text(p.read_text(encoding='utf-8').replace('evdsvd06_reconstruction','evdsvd07_inverse'),encoding='utf-8')
p=ROOT/'verify_final.py';s=p.read_text(encoding='utf-8').replace('evdsvd06_reconstruction','evdsvd07_inverse').replace('133','142').replace('3990','4260')
a=s.index('    for t,name in ');b=s.index(':\n        target=',a)
s=s[:a]+"    for t,name in [(11.5,'ellipse'),(17.5,'restore'),(55.,'svdinverse'),(66.5,'collapse'),(69.5,'overlap'),(92.,'nullspace'),(101.5,'notmagic'),(109.5,'minnorm'),(114.5,'systems'),(141.5,'score')]"+s[b:]
p.write_text(s,encoding='utf-8')
