"""61-second standalone tier-list short; timings are user supplied."""
import json
import os
from pathlib import Path
from manim import *

config.pixel_width = int(os.getenv('VIDEO_WIDTH',1080))
config.pixel_height = int(os.getenv('VIDEO_HEIGHT',1920))
config.frame_width=9
config.frame_height=16
config.frame_rate=30
config.background_color='#0C1020'
FONT='Malgun Gothic'
COLORS={'S':'#FFD56A','A':'#FF9478','B':'#7CDDC9','C':'#7FAAF5','D':'#BB9BEF'}
DATA=[
 ('LU','LU 분해','선형방정식 해결사','PA = LU','A',2,5.3),
 ('QR','QR 분해','조용한 실력자','최소제곱 · 고윳값 계산','S',6,10.3),
 ('Cholesky','촐레스키 분해','조건부 미친 효율','대칭 양의 정부호','A',11,16.3),
 ('EVD','고윳값 분해','수학적 낭만','대각화 가능한 행렬','A',17,23.3),
 ('SVD','특이값 분해','사기 캐릭터','직사각형 · 특이행렬 · 차원 축소','S',24,31.3),
 ('NMF','비음수 행렬 분해','해석력은 인정','비음수 데이터 · 부분의 조합','C',32,37.3),
 ('Polar','극분해','회전과 변형을 분리','회전·반사 / 늘이기','B',38,43.3),
 ('Schur','슈어 분해','수치선형대수의 핵심','B… 아니, A?','B',44,47),
 ('LDLᵀ','LDLᵀ 분해','까다로운 문제도 처리','부정부호 가능 · 피벗/블록 D','B',50,55.3),
 ('Jordan','조르당 표준형','수학적으로는 전설','컴퓨터 계산에서는…','D',56,60),
]

def label(s,size=30,color=WHITE,max_width=7.6):
    m=Text(s,font=FONT,font_size=size,color=color)
    if m.width>max_width:m.scale_to_fit_width(max_width)
    return m

class MatrixDecompositionTierList(Scene):
    def construct(self):
        self.add(label('MATRIX DECOMPOSITION',19,'#8793B3').move_to([0,6.85,0]))
        self.add(label('행렬 분해 티어리스트',39).move_to([0,6.2,0]))
        self.add(label('실전 활용 기준 · 주관적 랭킹',18,'#A9B2CC').move_to([0,5.55,0]))
        ys={tier:4.45-i*1.04 for i,tier in enumerate('SABCD')}
        for tier,y in ys.items():
            row=RoundedRectangle(width=7.7,height=.93,corner_radius=.12,stroke_width=1,stroke_color='#333E5B',fill_color='#161D31',fill_opacity=1).move_to([0,y,0])
            box=RoundedRectangle(width=.8,height=.85,corner_radius=.09,stroke_width=0,fill_color=COLORS[tier],fill_opacity=1).move_to([-3.4,y,0])
            self.add(row,box,label(tier,30,'#151626').move_to(box))
        self.add(Line([-3.8,-.65,0],[3.8,-.65,0],color='#303A56'))
        self.add(label('10 DECOMPOSITIONS / 61 SECONDS',16,'#7684A5').move_to([0,-6.9,0]))
        counts={t:0 for t in 'SABCD'};chips={};current=None;caption=None
        segments=json.loads(Path(__file__).with_name('timing.json').read_text(encoding='utf-8'))['segments']
        events=[]
        for seg in segments:events.append((seg['start'],'caption',seg['text']))
        for item in DATA:
            events.append((item[5],'card',item));events.append((item[6],'rank',item))
        events.append((49,'promote',None))
        events.sort(key=lambda e:e[0])
        for when,kind,payload in events:
            if self.time<when:self.wait(when-self.time)
            if kind=='caption':
                if caption:self.remove(caption)
                # Wrap by punctuation/length, keeping provided sentence boundaries.
                s=payload;lines=[];line=''
                for word in s.split():
                    if len(line+' '+word)>23 and line:lines.append(line);line=word
                    else:line=(line+' '+word).strip()
                if line:lines.append(line)
                caption=VGroup(*[label(x,27,max_width=7.3) for x in lines]).arrange(DOWN,buff=.13).move_to([0,-5.65,0])
                self.add(caption)
            elif kind=='card':
                if current:self.remove(current)
                key,name,tag,detail,tier,*_=payload
                panel=RoundedRectangle(width=7.4,height=3.25,corner_radius=.24,stroke_color=COLORS[tier],stroke_width=2,fill_color='#171F36',fill_opacity=1).move_to([0,-2.6,0])
                current=VGroup(panel,label(key,55,COLORS[tier],6.7).move_to([0,-1.65,0]),label(name,24,'#B7C2DF').move_to([0,-2.45,0]),label(tag,32).move_to([0,-3.15,0]),label(detail,20,'#9CAACC').move_to([0,-3.85,0]))
                self.play(FadeIn(current,shift=UP*.15),run_time=.2)
            elif kind in ('rank','promote'):
                if kind=='promote':
                    key='Schur';tier='A';self.remove(chips[key]);counts['B']-=1
                else:key=payload[0];tier=payload[4]
                x=-2.05+counts[tier]*1.65;counts[tier]+=1
                chip=VGroup(RoundedRectangle(width=1.52,height=.65,corner_radius=.09,stroke_width=0,fill_color=COLORS[tier],fill_opacity=1),label(key,19,'#101628',1.35)).move_to([0,-2.6,0])
                self.add(chip)
                self.play(chip.animate.move_to([x,ys[tier],0]),run_time=.4,rate_func=rush_into if tier=='D' else smooth)
                chips[key]=chip
        if self.time<61:self.wait(61-self.time)
