"""Minimal three-panel Edelman-Rose Gamblegram.

Persistent SIADH, DI and one grouped oedematous-disorders panel. Original
Manim Community drawing; fixed K segment, separately normalised body-amount
bars, calculated illustrative concentrations. No narrative captions or resets.
"""
from manim import *
from pathlib import Path as FilePath
import json
import os
import numpy as np

BG='#10151F'; INK='#EDF3FA'; MUTED='#A4B3C5'
GOLD='#F2C66D'; TEAL='#65D4C2'; CORAL='#EC6174'; K_COLOR='#526178'
DATA=json.loads(FilePath(__file__).with_name('cases.json').read_text())


def label(text,size=22,color=INK,at=None,max_width=None):
    m=Text(text,font='Avenir Next',font_size=size,color=color,line_spacing=.85)
    if max_width and m.width>max_width:m.scale_to_fit_width(max_width)
    if at is not None:m.move_to(at)
    return m


def block(x,width,bottom,height,color,opacity=1):
    return Rectangle(width=width,height=max(.001,height),stroke_width=0,
        fill_color=color,fill_opacity=opacity).move_to([x,bottom+height/2,0])


def hatched_region(x,width,y0,y1,color):
    height=max(.001,y1-y0)
    group=VGroup(Rectangle(width=width,height=height,stroke_color=color,stroke_width=1,
        fill_color=color,fill_opacity=.10).move_to([x,(y0+y1)/2,0]))
    left=x-width/2
    for s in np.arange(-height,width+.01,.13):
        low=max(0,-s/height);high=min(1,(width-s)/height)
        if low>=high:continue
        group.add(Line([left+s+height*low,y0+height*low,0],
            [left+s+height*high,y0+height*high,0],color=color,stroke_width=1.2,stroke_opacity=.85))
    return group


class EdelmanGamblegrams(Scene):
    def construct(self):
        self.camera.background_color=BG
        review=os.environ.get('GAMBLEGRAM_REVIEW')
        base=DATA['baseline'];c0=base['sodium']+base['potassium'];w0=base['water']
        bottom=-1.28;height=2.40;width=.76;offset=.64
        title=label(DATA['title'],34,INK,max_width=12.8).to_edge(UP,buff=.30)
        panels=VGroup();controls={};chapters=[]
        for case in DATA['panels']:
            x=case['x'];na=ValueTracker(base['sodium']);water=ValueTracker(w0)
            self.add(na,water)
            controls[case['id']]={'na':na,'water':water}
            xc=x-offset;xw=x+offset
            k_bar=block(xc,width,bottom,height*base['potassium']/c0,K_COLOR)
            na_bar=always_redraw(lambda xc=xc,na=na:block(xc,width,bottom+height*base['potassium']/c0,
                height*na.get_value()/c0,GOLD,.95))
            w_bar=always_redraw(lambda xw=xw,water=water:block(xw,width,bottom,height*water.get_value()/w0,TEAL,.57))
            reference=DashedLine([x-1.25,bottom+height,0],[x+1.25,bottom+height,0],
                dash_length=.095,color=MUTED,stroke_width=1)
            baseline=Line([x-1.25,bottom,0],[x+1.25,bottom,0],color='#43526A',stroke_width=1)
            name=label(case['title'],27 if case['id']!='oedematous' else 22,INK,[x,2.40,0],4.15)
            bars=VGroup(k_bar,na_bar,w_bar,reference,baseline,name)
            if case.get('qualifier'):
                bars.add(label(case['qualifier'],16,MUTED,[x,1.87,0],3.5))
            def difference(xw=xw,na=na,water=water):
                c=height*(na.get_value()+base['potassium'])/c0
                w=height*water.get_value()/w0
                if abs(c-w)<.006:return VGroup()
                return hatched_region(xw,width,bottom+min(c,w),bottom+max(c,w),TEAL if w>c else CORAL)
            bars.add(always_redraw(difference))
            number=label('140',43,INK,[x,-2.06,0],3.4)
            state={'last':140}
            def update_number(m,dt,x=x,na=na,water=water,state=state):
                value=round((na.get_value()+base['potassium'])/water.get_value())
                color=CORAL if value<135 or value>145 else INK
                if value!=state['last']:
                    m.become(label(str(value),43,color,[x,-2.06,0],3.4));state['last']=value
                m.set_color(color)
            number.add_updater(update_number);bars.add(number)
            panels.add(bars)
        unit=label('Plasma [Na⁺] · mmol/L',17,MUTED,[0,-2.73,0],5.2)
        # One compact shared key replaces all per-bar labels and commentary.
        key=VGroup()
        for x,text,color in [(-1.65,'Na⁺',GOLD),(0,'K⁺',K_COLOR),(1.65,'H₂O',TEAL)]:
            chip=Square(side_length=.12,stroke_width=0,fill_color=color,fill_opacity=1).move_to([x-.32,-3.35,0])
            key.add(chip,label(text,16,MUTED,[x+.13,-3.35,0],1.0))
        self.play(FadeIn(title),run_time=.8)
        self.play(FadeIn(panels),FadeIn(unit),FadeIn(key),run_time=1.2)
        self.wait(2)
        if review=='baseline':return
        start=self.time
        case=DATA['panels'][0]
        self.play(controls['siadh']['water'].animate.set_value(case['water']),run_time=5)
        self.wait(7)
        chapters.append({'id':'siadh','start':round(start,2),'end':round(self.time,2),'illustrativePlasmaSodium':128})
        if review=='siadh':return
        start=self.time
        case=DATA['panels'][1]
        self.play(controls['di']['water'].animate.set_value(case['water']),run_time=5)
        self.wait(7)
        chapters.append({'id':'di','start':round(start,2),'end':round(self.time,2),'illustrativePlasmaSodium':160})
        if review=='di':return
        start=self.time
        case=DATA['panels'][2];intermediate=case['intermediate']
        self.play(controls['oedematous']['na'].animate.set_value(intermediate['sodium']),
                  controls['oedematous']['water'].animate.set_value(intermediate['water']),run_time=5)
        self.wait(6)
        chapters.append({'id':'oedematous-retention','start':round(start,2),'end':round(self.time,2),
                         'illustrativePlasmaSodium':140})
        if review=='retention':return
        start=self.time
        self.play(controls['oedematous']['water'].animate.set_value(case['water']),run_time=5)
        chapters.append({'id':'oedematous-hyponatraemia','start':round(start,2),'end':round(self.time,2),
                         'illustrativePlasmaSodium':128})
        start=self.time
        self.wait(10)
        chapters.append({'id':'comparison','start':round(start,2),'end':round(self.time,2)})
        FilePath(__file__).with_name('chapter-times.json').write_text(
            json.dumps({'chapters':chapters,'durationSeconds':round(self.time,2)},indent=2)+'\n')
