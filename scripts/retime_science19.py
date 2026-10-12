"""Kakeya draft/measured cue timing and Korean TTS pronunciations."""
from pathlib import Path
import sys
import retime_science17 as shared
shared.EP=Path(__file__).resolve().parents[1]/'episodes/science19_kakeya_dimension'
if __name__=='__main__':
 if '--duration' not in sys.argv and '--end-times' not in sys.argv:
  sys.argv.extend(['--duration','175'])
 shared.main()
 p=shared.EP/'tts_script.txt'
 text=p.read_text(encoding='utf-8')
 for src,dst in [('Hong Wang','홍 왕'),('Joshua Zahl','조슈아 잘'),('Hausdorff','하우스도르프'),('Minkowski','민코프스키'),('Kakeya','가케야'),('sticky','스티키')]:text=text.replace(src,dst)
 p.write_text(text,encoding='utf-8')
