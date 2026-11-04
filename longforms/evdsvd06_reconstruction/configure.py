from pathlib import Path
ROOT=Path(__file__).resolve().parent
p=ROOT/'build.py';p.write_text(p.read_text(encoding='utf-8').replace('evdsvd05_future','evdsvd06_reconstruction'),encoding='utf-8')
p=ROOT/'verify_final.py';s=p.read_text(encoding='utf-8').replace('evdsvd05_future','evdsvd06_reconstruction').replace('130','133').replace('3900','3990')
a=s.index('    for t,name in ');b=s.index(':\n        target=',a)
s=s[:a]+"    for t,name in [(21.,'fair'),(42.,'cancel'),(46.,'break'),(67.,'orthogonal'),(74.,'error'),(87.,'optimal'),(102.,'evd'),(108.,'svd'),(114.5,'symmetric'),(132.5,'score')]"+s[b:]
p.write_text(s,encoding='utf-8')
