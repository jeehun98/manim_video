from pathlib import Path
R=Path(__file__).resolve().parent
source=(R.parent/'singular-values-ch0/finish.py').read_text(encoding='utf-8')
source=source.replace('range(11)',"range(len(data['ends']))").replace("'-t','63'","'-t','121'").replace('singular-values-ch0.mp4','singular-values-ch2.mp4')
exec(compile(source,str(R/'finish.py'),'exec'))
