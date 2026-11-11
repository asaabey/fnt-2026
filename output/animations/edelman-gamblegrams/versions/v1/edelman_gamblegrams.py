"""Animated, original Edelman–Rose Gamblegrams with a diabetes-insipidus case.

The full cation numerator is retained; K is held fixed as a grey segment.
Amounts are normalised to their own baseline totals. Plasma [Na] readouts
are calculated from the stated illustrative Rose model, not patient forecasts.
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
    m=Text(text or '·',font='Avenir Next',font_size=size,color=color,line_spacing=.85)
    if not text:m.set_opacity(0)
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
    for s in np.arange(-height,width+.01,.16):
        low=max(0,-s/height);high=min(1,(width-s)/height)
        if low>=high:continue
        group.add(Line([left+s+height*low,y0+height*low,0],
                       [left+s+height*high,y0+height*high,0],
                       color=color,stroke_width=1.2,stroke_opacity=.85))
    return group


class EdelmanGamblegrams(Scene):
    def construct(self):
        self.camera.background_color=BG
        review=os.environ.get('GAMBLEGRAM_REVIEW')
        base=DATA['baseline'];c0=base['sodium']+base['potassium'];w0=base['water']
        na=ValueTracker(base['sodium']);potassium=base['potassium'];water=ValueTracker(w0)
        self.add(na,water)
        chapters=[]
        bottom=-1.65;h=2.60;x_c=-3.35;x_w=-.53;width=1.22
        def cat_height():return h*(na.get_value()+potassium)/c0
        def water_height():return h*water.get_value()/w0
        def plasma_na():return (na.get_value()+potassium)/water.get_value()
        title=label('Sodium content, water and concentration',32,INK,max_width=12.8).to_edge(UP,buff=.30)
        equation=label('[Na⁺]plasma ≈ (Naₑ + Kₑ) / TBW',27,INK,[0,2.58,0],11.5)
        k_bar=block(x_c,width,bottom,h*potassium/c0,K_COLOR)
        na_bar=always_redraw(lambda:block(x_c,width,bottom+h*potassium/c0,h*na.get_value()/c0,GOLD,.95))
        w_bar=always_redraw(lambda:block(x_w,width,bottom,water_height(),TEAL,.57))
        k_label=label('K⁺ fixed',17,INK,[x_c,bottom+h*potassium/c0/2,0],1.10)
        na_label=label('Na⁺',20,BG)
        na_label.add_updater(lambda m,dt:m.move_to([x_c,bottom+h*potassium/c0+h*na.get_value()/c0/2,0]))
        w_label=label('H₂O',22,INK)
        w_label.add_updater(lambda m,dt:m.move_to([x_w,bottom+water_height()/2,0]))
        chart_bottom=Line([-4.17,bottom,0],[.31,bottom,0],color='#43526A',stroke_width=1.2)
        baseline_line=DashedLine([-4.17,bottom+h,0],[.31,bottom+h,0],dash_length=.10,color=MUTED,stroke_width=1.2)
        baseline_tag=label('Baseline',14,MUTED,[-5.15,bottom+h,0],1.3)
        c_name=label('Body Na⁺ + K⁺',19,MUTED,[x_c,-2.03,0],2.65)
        w_name=label('Body water',19,MUTED,[x_w,-2.03,0],2.65)
        normalisation=label('Each total is scaled to its own baseline amount.',15,MUTED,[-2.05,-2.57,0],6.9)

        def relative_water():
            c=cat_height();w=water_height()
            if abs(c-w)<.012:return VGroup()
            color=TEAL if w>c else CORAL
            y0=bottom+min(c,w);y1=bottom+max(c,w)
            region=hatched_region(x_w,width,y0,y1,color)
            bracket=VGroup(Line([.22,y0,0],[.37,y0,0],color=color,stroke_width=1.5),
                           Line([.37,y0,0],[.37,y1,0],color=color,stroke_width=1.5),
                           Line([.22,y1,0],[.37,y1,0],color=color,stroke_width=1.5))
            text='Relative water\nexcess' if w>c else 'Relative water\ndeficit'
            tag=label(text,15,color,[1.25,(y0+y1)/2,0],1.65)
            return VGroup(region,bracket,tag)
        water_difference=always_redraw(relative_water)

        scenario=label('Normal reference',23,TEAL,[4.30,1.95,0],4.9)
        readout_name=label('Plasma [Na⁺]',21,MUTED,[4.30,1.16,0],4.6)
        approx=label('≈',29,MUTED,[2.95,.42,0])
        readout=label('140',51,INK,[4.03,.43,0])
        last=[140]
        def update_readout(m,dt):
            value=int(round(plasma_na()))
            color=CORAL if value<135 or value>145 else INK
            if value!=last[0]:
                m.become(label(str(value),51,color,[4.03,.43,0]));last[0]=value
            m.set_color(color)
        readout.add_updater(update_readout)
        units=label('mmol/L',18,MUTED,[5.45,.20,0])
        info=VGroup(label('Sodium stores at baseline',19,GOLD,[4.30,-.43,0],4.9),
                    label('Water at baseline',19,TEAL,[4.30,-.99,0],4.9),
                    label('Illustrative Rose model',17,MUTED,[4.30,-1.58,0],4.9))
        caption=label('Plasma sodium is a ratio, not a measure of sodium stores.',21,INK,[0,-3.17,0],12.7)
        context=label('Gold: exchangeable sodium. Grey: exchangeable potassium, held constant.',16,MUTED,[0,-3.58,0],12.7)
        chart=VGroup(k_bar,na_bar,w_bar,k_label,na_label,w_label,chart_bottom,baseline_line,
                     baseline_tag,c_name,w_name,normalisation,water_difference)
        panel=VGroup(scenario,readout_name,approx,readout,units,info)
        self.play(FadeIn(title),run_time=1)
        self.play(FadeIn(equation),FadeIn(chart),FadeIn(panel),FadeIn(caption),FadeIn(context),run_time=2)
        self.wait(6)
        if review=='baseline':return
        def change(old,text,size=21,color=INK,max_width=12.7):
            return Transform(old,label(text,size,color,old.get_center(),max_width))
        def reset():
            self.play(na.animate.set_value(base['sodium']),water.animate.set_value(w0),
                      change(scenario,'Normal reference',23,TEAL,4.9),
                      change(info[0],'Sodium stores at baseline',19,GOLD,4.9),
                      change(info[1],'Water at baseline',19,TEAL,4.9),
                      change(info[2],'Compare a separate situation',17,MUTED,4.9),
                      change(caption,'Return to the normal reference before the next comparison.'),
                      change(context,'Each example starts independently from this reference.',16,MUTED),run_time=2)
            self.wait(1)
        for i,case in enumerate(DATA['cases']):
            if i:reset()
            start=self.time
            self.play(na.animate.set_value(case['sodium']),water.animate.set_value(case['water']),
                      change(scenario,case['title'],23,CORAL if case['plasmaSodium']>145 else TEAL if case['plasmaSodium']<135 else GOLD,4.9),
                      *[change(info[j],text,19 if j<2 else 17,GOLD if j==0 else TEAL if j==1 else MUTED,4.9)
                        for j,text in enumerate(case['lines'])],
                      change(caption,case['caption']),change(context,case['context'],16,MUTED),run_time=4)
            self.wait(8)
            if case['id']=='sodium-loss':
                self.play(change(caption,'Relative water excess can exist even when total body water has fallen.'),
                          change(context,'Both bars are below baseline, but water exceeds the amount matched to the cations.',16,MUTED),run_time=1)
                self.wait(5)
            if case['id']=='hypotonic-retention':
                self.play(change(caption,'In heart failure, oedema can coexist with reduced effective arterial filling.'),
                          change(context,'Non-osmotic vasopressin can maintain water retention despite low plasma sodium.',16,MUTED),run_time=1)
                self.wait(5)
            chapters.append({'id':case['id'],'start':round(start,2),'end':round(self.time,2),
                             'illustrativePlasmaSodium':case['plasmaSodium']})
            if review==case['id']:return
        start=self.time
        self.play(water.animate.set_value(w0),
                  change(scenario,'DI with water replacement',23,TEAL,4.9),
                  change(info[0],'Sodium stores unchanged',19,GOLD,4.9),
                  change(info[1],'Drinking matches water loss',19,TEAL,4.9),
                  change(info[2],'Dilute polyuria can persist',17,MUTED,4.9),
                  change(caption,'Adequate drinking can preserve plasma sodium despite ongoing DI.'),
                  change(context,'A normal plasma sodium does not exclude diabetes insipidus.',16,MUTED),run_time=4)
        self.wait(6)
        chapters.append({'id':'di-compensated','start':round(start,2),'end':round(self.time,2),
                         'illustrativePlasmaSodium':140})
        if review=='di-compensated':return

        start=self.time
        chart.clear_updaters(recursive=True);panel.clear_updaters(recursive=True)
        self.play(FadeOut(chart),FadeOut(panel),FadeOut(equation),
                  change(caption,'The same low plasma sodium can accompany low, normal or high sodium stores.'),
                  change(context,'DI can raise plasma sodium when water loss is not replaced.',16,MUTED),run_time=1.5)
        summary=VGroup(label('Gold: Na⁺   ·   Grey: K⁺ held fixed   ·   Teal: water',16,MUTED,[0,2.66,0],12.7))
        for x,case in zip([-5.25,-2.625,0,2.625,5.25],DATA['cases']):
            base_y=-.70;mh=1.65;mw=.44
            left=x-.43;right=x+.43
            ch=mh*(case['sodium']+potassium)/c0;wh=mh*case['water']/w0
            group=VGroup(
                label(case['posterTitle'],19,INK,[x,1.99,0],2.42),
                block(left,mw,base_y,mh*potassium/c0,K_COLOR),
                block(left,mw,base_y+mh*potassium/c0,mh*case['sodium']/c0,GOLD,.95),
                block(right,mw,base_y,wh,TEAL,.57),
                DashedLine([x-.79,base_y+mh,0],[x+.79,base_y+mh,0],dash_length=.07,color=MUTED,stroke_width=.8),
                label('Na+K',12,MUTED,[left,-1.01,0],.8),
                label('H₂O',12,MUTED,[right,-1.01,0],.8),
                label(str(case['plasmaSodium']),35,CORAL if case['plasmaSodium']!=140 else INK,[x,-1.65,0],2.2),
                label('mmol/L',14,MUTED,[x,-2.08,0],2.2),
                label(case['posterStores'],15,GOLD,[x,-2.56,0],2.45))
            if abs(ch-wh)>.012:
                group.add(hatched_region(right,mw,base_y+min(ch,wh),base_y+max(ch,wh),TEAL if wh>ch else CORAL))
            summary.add(group)
        self.play(FadeIn(summary),run_time=2)
        self.wait(10)
        chapters.append({'id':'comparison','start':round(start,2),'end':round(self.time,2)})
        FilePath(__file__).with_name('chapter-times.json').write_text(
            json.dumps({'chapters':chapters,'durationSeconds':round(self.time,2)},indent=2)+'\n')
