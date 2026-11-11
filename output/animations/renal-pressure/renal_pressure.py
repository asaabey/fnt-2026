"""Qualitative renal haemodynamics: medicines, mediators and clinical context.

Manim Community 0.22.1. Scene text and state transitions are in storyboard.json.
Arteriolar calibre is illustrated; indicators are not calibrated measurements.
"""
from manim import *
from pathlib import Path as FilePath
import json
import os
import numpy as np

BG='#10151F'; INK='#EDF3FA'; MUTED='#A4B3C5'
BLOOD='#EC6174'; LUMEN='#6D2336'; WALL='#CB5269'
GOLD='#F2C66D'; TEAL='#65D4C2'
STORY=json.loads(FilePath(__file__).with_name('storyboard.json').read_text())


def label(text,size=22,color=INK,at=None,max_width=None):
    obj=Text(text or '·',font='Avenir Next',font_size=size,color=color,line_spacing=.8)
    if not text:
        obj.set_opacity(0)
    if max_width and obj.width>max_width:
        obj.scale_to_fit_width(max_width)
    if at is not None:
        obj.move_to(at)
    return obj


def vessel(x0,x1,y,width,centre,tone):
    xs=np.linspace(x0,x1,64)
    half=width*(1-.65*tone*np.exp(-((xs-centre)/.60)**4))
    points=[[x,y+r,0] for x,r in zip(xs,half)]
    points += [[x,y-r,0] for x,r in reversed(list(zip(xs,half)))]
    m=VMobject(stroke_color=WALL,stroke_width=2.4,fill_color=LUMEN,fill_opacity=1)
    m.set_points_as_corners(points+[points[0]])
    return m


class RenalPressure(Scene):
    def construct(self):
        self.camera.background_color=BG
        aff=ValueTracker(0); eff=ValueTracker(0)
        pressure=ValueTracker(.64); filtration=ValueTracker(.64)
        flow=ValueTracker(.8); clock=ValueTracker(0)
        clock.add_updater(lambda m,dt:m.increment_value(dt*flow.get_value()))
        self.add(clock)

        title=label(STORY['title'],34).to_edge(UP,buff=.30)
        incoming=always_redraw(lambda:vessel(-6.2,-1.25,.55,.25,-3.4,aff.get_value()))
        outgoing=always_redraw(lambda:vessel(.85,6.15,.55,.21,2.8,eff.get_value()))
        capsule=Circle(radius=1.08,stroke_color='#43526A',stroke_width=2.4).move_to([-.25,.55,0])
        glow=always_redraw(lambda:Circle(radius=.94,stroke_width=0,fill_color=GOLD,
             fill_opacity=.02+.1*pressure.get_value()).move_to([-.25,.55,0]))
        path=VMobject().set_points_smoothly([
            [-6.2,.55,0],[-2,.55,0],[-1.2,.55,0],[-.8,1.12,0],
            [.1,1.2,0],[.5,.82,0],[.1,.5,0],[-.65,.8,0],[-.85,.43,0],
            [-.5,.03,0],[.28,.12,0],[.6,.46,0],[1.12,.55,0],[6.15,.55,0]])
        tuft=VMobject().set_points_smoothly([
            [-1.25,.55,0],[-.8,1.12,0],[.1,1.2,0],[.5,.82,0],
            [.1,.5,0],[-.65,.8,0],[-.85,.43,0],[-.5,.03,0],
            [.28,.12,0],[.6,.46,0],[.85,.55,0]]).set_stroke(WALL,width=15)
        tuft_inner=tuft.copy().set_stroke(LUMEN,width=10)
        tuft_other=VMobject().set_points_smoothly([
            [-1.1,.56,0],[-.65,.16,0],[-.2,.33,0],[.2,.95,0],[.7,.58,0]])
        tuft_other.set_stroke(WALL,width=7,opacity=.75)
        names=VGroup(label('Afferent',20,MUTED,[-3.65,-.06,0]),
                     label('Glomerulus',21,INK,[-.25,1.92,0]),
                     label('Efferent',20,MUTED,[3.6,-.06,0]))
        arrows=VGroup(*[Arrow([x-.25,.55,0],[x+.25,.55,0],buff=0,
                 max_tip_length_to_length_ratio=.25,stroke_width=2,color=MUTED)
                 for x in [-5.3,-2.1,1.4,5.3]])
        aff_drug=label('',25,TEAL,[-3.65,1.98,0],4.7)
        eff_drug=label('',25,TEAL,[3.6,1.98,0],4.7)
        aff_action=label('',18,MUTED,[-3.65,1.46,0],4.7)
        eff_action=label('',18,MUTED,[3.6,1.46,0],4.7)
        drug_labels=VGroup(aff_drug,eff_drug,aff_action,eff_action)

        filtrate_path=VMobject().set_points_smoothly([
            [-.25,-.2,0],[-.25,-.95,0],[-.25,-1.48,0],[.32,-1.62,0],[.9,-1.62,0]])
        filtrate_path.set_stroke(GOLD,width=2.2,opacity=.45)
        filter_mark=DashedLine([-.9,-.42,0],[.38,-.42,0],dash_length=.07,
                              stroke_color=GOLD,stroke_width=1.4)
        filtrate_label=label('Filtrate',20,GOLD,[.05,-2.02,0])

        def meter(y,tracker,color):
            track=RoundedRectangle(width=3.15,height=.16,corner_radius=.05,
                   stroke_width=0,fill_color='#2A3444',fill_opacity=1).move_to([4.05,y,0])
            fill=always_redraw(lambda:Rectangle(width=max(.03,3.15*tracker.get_value()),
                 height=.16,stroke_width=0,fill_color=color,fill_opacity=1)
                 .move_to([2.475+3.15*tracker.get_value()/2,y,0]))
            return VGroup(track,fill)
        pressure_meter=meter(-1.25,pressure,GOLD)
        gfr_meter=meter(-2.12,filtration,TEAL)
        gauges=VGroup(label('Glomerular pressure',19,INK,[4.05,-.87,0]),pressure_meter,
                      label('GFR',19,INK,[4.05,-1.75,0]),gfr_meter)
        ref_body=label('Typical perfusion',19,MUTED,[-4.05,-1.45,0],4.7)
        reference=VGroup(ref_body)
        outcome=label('',20,TEAL,[-4.05,-2.22,0],4.7)
        caption=label('Inlet and outlet resistance influence filtration pressure.',21,INK,[0,-2.98,0],12.7)
        context=label('Qualitative effects',15,MUTED,[0,-3.38,0],12.7)

        self.play(FadeIn(title),run_time=1)
        diagram=VGroup(incoming,outgoing,capsule,glow,tuft,tuft_inner,tuft_other,
                       names,arrows,filtrate_path,filter_mark,filtrate_label)
        self.play(FadeIn(diagram),FadeIn(gauges),FadeIn(reference),
                  FadeIn(caption),FadeIn(context),run_time=1.3)
        self.add(drug_labels,outcome)
        cells=VGroup()
        for i in range(22):
            dot=Dot(radius=.047,color=BLOOD)
            def update_cell(m,dt,offset=i/22):
                m.move_to(path.point_from_proportion((clock.get_value()*.13+offset)%1))
            dot.add_updater(update_cell);cells.add(dot)
        drops=VGroup()
        for i in range(11):
            dot=Dot(radius=.032,color=GOLD)
            def update_drop(m,dt,offset=i/11):
                m.move_to(filtrate_path.point_from_proportion((self.time*.53+offset)%1))
                m.set_opacity(1 if offset<filtration.get_value() else 0)
            dot.add_updater(update_drop);drops.add(dot)
        self.add(cells,drops)
        self.wait(4)

        trackers=[aff,eff,pressure,filtration,flow]
        def text_to(old,text,size=21,color=INK,max_width=12.7):
            return Transform(old,label(text,size,color,old.get_center(),max_width))
        timings=[]
        review_case=os.environ.get('RENAL_REVIEW_CASE')
        cases=[c for c in STORY['scenes'] if not review_case or c['id']==review_case]
        for case in cases:
            start=self.time
            layout=case['layout']
            self.play(*[tracker.animate.set_value(value)
                        for tracker,value in zip(trackers,case['baseline'])],
                      text_to(aff_drug,layout['afferentMedicine'],25,TEAL,4.7),
                      text_to(eff_drug,layout['efferentMedicine'],25,TEAL,4.7),
                      text_to(aff_action,'',18,MUTED,4.7),
                      text_to(eff_action,'',18,MUTED,4.7),
                      text_to(ref_body,case['reference'],19,MUTED,4.7),
                      text_to(caption,'',20,MUTED),
                      text_to(context,'',15,MUTED),
                      text_to(outcome,'',20,TEAL,4.7),run_time=.9)
            self.wait(.8)
            self.play(*[tracker.animate.set_value(value)
                        for tracker,value in zip(trackers,case['effect'])],
                      text_to(aff_action,layout['afferentAction'],18,GOLD,4.7),
                      text_to(eff_action,layout['efferentAction'],18,GOLD,4.7),
                      text_to(caption,layout['caption'],21,INK),
                      text_to(context,layout['context'],16,MUTED),
                      text_to(outcome,layout.get('clinicalOutcome',''),20,TEAL,4.7),run_time=2)
            self.wait(case['hold'])
            timings.append({'id':case['id'],'start':round(start,2),
                            'effectEstablished':round(start+3.7,2),
                            'end':round(self.time,2)})
        if review_case:
            return
        cells.clear_updaters(recursive=True);drops.clear_updaters(recursive=True)
        self.play(FadeOut(gauges),FadeOut(reference),FadeOut(drug_labels),FadeOut(outcome),
                  text_to(caption,'ACE inhibitors, ARBs and SGLT2i can reduce albuminuria.',20,INK),
                  text_to(context,'An early haemodynamic GFR dip is not necessarily structural injury.',16,MUTED),
                  *[tracker.animate.set_value(value)
                    for tracker,value in zip(trackers,[0,0,.64,.64,.8])],run_time=1)
        # Keep every medicine on its relevant side in the closing view too.
        aff_summary=label('NSAIDs · constriction\nProstaglandins · dilation\nSGLT2i · feedback-mediated tone ↑',17,INK,[-3.65,-1.65,0],5.4)
        eff_summary=label('ACE inhibitors / ARBs · dilation\nAngiotensin II · constriction\nSGLT2i · may dilate, context-dependent',17,INK,[3.60,-1.65,0],5.4)
        self.play(FadeIn(aff_summary),FadeIn(eff_summary),run_time=1)
        self.wait(8)
        FilePath(__file__).with_name('chapter-times.json').write_text(
            json.dumps({'chapters':timings,'durationSeconds':round(self.time,2)},indent=2)+'\n')
