"""Water loading, vasopressin suppression and dilute urine.

Manim Community 0.22.1. Shares the established renal-animation palette and
collecting-duct style. Indicators, particles and timings are qualitative.
"""
from manim import *
from pathlib import Path as FilePath
import json
import os
import numpy as np

BG='#10151F'; INK='#EDF3FA'; MUTED='#A4B3C5'
GOLD='#F2C66D'; TEAL='#65D4C2'; CORAL='#EC6174'
WALL='#5E8EAD'; LUMEN='#172B3E'


def label(text,size=22,color=INK,at=None,max_width=None):
    obj=Text(text or '·',font='Avenir Next',font_size=size,color=color,line_spacing=.85)
    if not text: obj.set_opacity(0)
    if max_width and obj.width>max_width: obj.scale_to_fit_width(max_width)
    if at is not None: obj.move_to(at)
    return obj


class WaterLoad(Scene):
    def construct(self):
        self.camera.background_color=BG
        review=os.environ.get('WATER_LOAD_REVIEW')
        chapters=[]
        clock=ValueTracker(0)
        clock.add_updater(lambda m,dt:m.increment_value(dt))
        # Display units only: no numerical physiological scale is implied.
        water_level=ValueTracker(.73)
        permeability=ValueTracker(.76)
        insertion=ValueTracker(1)
        urine_volume=ValueTracker(.32)
        urine_osmolality=ValueTracker(.69)
        inflow=ValueTracker(0)
        self.add(clock,water_level,permeability,insertion,urine_volume,urine_osmolality,inflow)

        title=label('How a water load produces dilute urine',32,INK,max_width=12.8).to_edge(UP,buff=.30)
        water_label=label('',24,TEAL,[-4.52,2.55,0],3.0)
        adh=label('Vasopressin',23,TEAL,[1.25,2.55,0],3.4)
        plasma_name=label('Plasma',19,MUTED,[-4.52,1.59,0],2.3)
        plasma_frame=RoundedRectangle(width=2.36,height=3.18,corner_radius=.13,
                     stroke_color=WALL,stroke_width=2,fill_color=LUMEN,fill_opacity=1).move_to([-4.52,-.25,0])
        # A fixed set of sodium symbols illustrates dilution as water expands.
        # It is not a one-compartment fluid distribution model.
        bottom=-1.75
        plasma_fill=always_redraw(lambda:Rectangle(width=2.17,
             height=water_level.get_value()-bottom,stroke_width=0,
             fill_color=TEAL,fill_opacity=.14).move_to([-4.52,(water_level.get_value()+bottom)/2,0]))
        surface=always_redraw(lambda:Line([-5.60,water_level.get_value(),0],[-3.44,water_level.get_value(),0],color=TEAL,stroke_width=1.3))
        sodium=VGroup()
        for row in range(4):
            for col in range(5):
                dot=Dot(radius=.044,color=GOLD)
                def sodium_position(m,dt,row=row,col=col):
                    fraction=.16+.22*row
                    m.move_to([-5.34+.41*col,bottom+.16+(water_level.get_value()-bottom-.36)*fraction,0])
                dot.add_updater(sodium_position);sodium.add(dot)
        sodium_legend=VGroup(Dot(radius=.044,color=GOLD).move_to([-5.15,-1.49,0]),
                            label('Na⁺',17,GOLD,[-4.73,-1.49,0],.8))
        osmo_name=label('Plasma osmolality',18,MUTED,[-4.52,-2.10,0],3.2)
        osmo_state=label('Baseline',21,INK,[-4.52,-2.49,0],3.2)
        water_input=VGroup()
        for i in range(8):
            dot=Dot(radius=.034,color=TEAL)
            def input_position(m,dt,offset=i/8):
                t=(clock.get_value()*.71+offset)%1
                m.move_to([-5.22+.10*np.sin(offset*19),2.10-(2.10-water_level.get_value())*t,0])
                m.set_opacity(inflow.get_value())
            dot.add_updater(input_position);water_input.add(dot)
        control_arrow=Arrow([-3.10,2.55,0],[-.54,2.55,0],buff=0,color=MUTED,
                            stroke_width=1.3,max_tip_length_to_length_ratio=.08).set_opacity(0)

        # Magnified collecting duct: lumen, principal cells and interstitium.
        bands=VGroup()
        for i in range(15):
            depth=(i+1)/15
            bands.add(Rectangle(width=3.85,height=.23,stroke_width=0,
                      fill_color=GOLD,fill_opacity=.015+.085*depth)
                      .move_to([1.79,1.24-i*.23,0]))
        duct_name=label('Collecting duct',19,MUTED,[1.32,2.00,0],3.1)
        duct_lumen=Rectangle(width=.60,height=3.55,stroke_width=0,
                    fill_color=LUMEN,fill_opacity=1).move_to([.50,-.28,0])
        walls=VGroup(Line([.20,1.50,0],[.20,-2.06,0],color=WALL,stroke_width=4),
                     Line([.80,1.50,0],[.80,-2.06,0],color=WALL,stroke_width=4))
        rows=[.94,.14,-.66,-1.46]
        cells=VGroup(*[Rectangle(width=1.60,height=.75,stroke_color=WALL,stroke_width=1.4,
                      fill_color=LUMEN,fill_opacity=.95).move_to([1.60,y,0]) for y in rows])
        aqp_name=label('AQP2',18,TEAL,[1.56,1.50,0],1.6)
        channel_paths=VGroup()
        channels=VGroup()
        for i,y in enumerate(rows):
            path=DashedLine([.86,y,0],[1.61,y,0],dash_length=.065,color=MUTED,stroke_width=.8)
            path.add_updater(lambda m,dt:m.set_stroke(opacity=.55*(1-insertion.get_value())))
            if i<3: channel_paths.add(path)
            ch=RoundedRectangle(width=.15,height=.105,corner_radius=.02,stroke_width=0,
                    fill_color=TEAL,fill_opacity=1)
            def channel_position(m,dt,i=i,y=y):
                # Three channels internalise; one remains to avoid implying zero permeability.
                travel=(1-insertion.get_value()) if i<3 else 0
                m.move_to([.80+.81*travel,y,0])
                m.set_opacity(1 if i==3 else .35+.65*insertion.get_value())
            ch.add_updater(channel_position);channels.add(ch)
        vesicles=VGroup()
        for i in range(3):
            ring=Circle(radius=.145,stroke_color=TEAL,stroke_width=1,fill_opacity=0)
            def vesicle_position(m,dt,i=i):
                m.move_to(channels[i].get_center())
                m.set_stroke(opacity=.40*(1-insertion.get_value()))
            ring.add_updater(vesicle_position);vesicles.add(ring)
        # Basolateral water paths are retained; only the apical regulated population moves.
        basal=VGroup(*[RoundedRectangle(width=.15,height=.105,corner_radius=.02,stroke_width=0,
                        fill_color=TEAL,fill_opacity=.7).move_to([2.40,y,0]) for y in rows])
        flow_arrow=Arrow([.50,1.35,0],[.50,.97,0],buff=0,color=MUTED,
                         stroke_width=1.5,max_tip_length_to_length_ratio=.22)
        output=Arrow([.50,-2.10,0],[.50,-2.47,0],buff=0,color=TEAL,
                     stroke_width=2,max_tip_length_to_length_ratio=.23)
        output_label=label('Urine',18,MUTED,[.50,-2.68,0],2.5)
        water_recovery=label('Water reabsorbed',17,TEAL,[3.00,-2.20,0],2.5)
        medulla=label('Medulla',14,MUTED,[3.27,1.52,0],1.3)

        def meter(y,tracker,color):
            track=RoundedRectangle(width=2.65,height=.15,corner_radius=.04,stroke_width=0,
                    fill_color='#2A3444',fill_opacity=1).move_to([5.25,y,0])
            fill=always_redraw(lambda:Rectangle(width=max(.03,2.65*tracker.get_value()),height=.15,
                    stroke_width=0,fill_color=color,fill_opacity=1)
                    .move_to([3.925+2.65*tracker.get_value()/2,y,0]))
            return VGroup(track,fill)
        gauges=VGroup(label('Water permeability',18,INK,[5.25,1.05,0],2.9),
                      meter(.68,permeability,TEAL),
                      label('Urine volume',18,INK,[5.25,-.03,0],2.9),
                      meter(-.40,urine_volume,TEAL),
                      label('Urine osmolality',18,INK,[5.25,-1.11,0],2.9),
                      meter(-1.48,urine_osmolality,GOLD))
        caption=label('Vasopressin regulates how much water leaves the collecting duct.',21,INK,[0,-3.17,0],12.7)
        context=label('Teal: water   ·   Gold: sodium in the plasma compartment',16,MUTED,[0,-3.58,0],12.7)
        self.play(FadeIn(title),run_time=1)
        self.play(FadeIn(plasma_frame),FadeIn(plasma_fill),FadeIn(surface),FadeIn(sodium),
                  FadeIn(sodium_legend),FadeIn(plasma_name),FadeIn(osmo_name),FadeIn(osmo_state),
                  FadeIn(bands),FadeIn(duct_name),FadeIn(duct_lumen),FadeIn(walls),FadeIn(cells),
                  FadeIn(aqp_name),FadeIn(channels),FadeIn(basal),FadeIn(adh),FadeIn(medulla),
                  FadeIn(flow_arrow),FadeIn(output),FadeIn(output_label),FadeIn(water_recovery),
                  FadeIn(gauges),FadeIn(caption),FadeIn(context),run_time=2)
        self.add(water_label,water_input,control_arrow,channel_paths,vesicles)

        particles=VGroup()
        for i in range(28):
            dot=Dot(radius=.029,color=TEAL)
            def update_lumen(m,dt,i=i):
                offset=i/28
                t=(clock.get_value()*(.18+.12*urine_volume.get_value())+offset)%1
                lane=(i%3)-1
                m.move_to([.50+.15*lane,1.47-3.97*t,0])
                # More water is retained in the lumen as permeability falls.
                retained=.30+.64*(1-permeability.get_value())
                m.set_opacity(1 if offset<retained else .09)
            dot.add_updater(update_lumen);particles.add(dot)
        for row,y in enumerate(rows):
            for i in range(6):
                dot=Dot(radius=.031,color=TEAL)
                def update_water(m,dt,offset=i/6,y=y,row=row):
                    t=(clock.get_value()*.42+offset+row*.08)%1
                    m.move_to([.73+2.65*t,y,0])
                    m.set_opacity(permeability.get_value() if offset<permeability.get_value() else .025)
                dot.add_updater(update_water);particles.add(dot)
        self.add(particles)
        self.wait(5)
        if review=='before':return
        def change(old,text,size=21,color=INK,max_width=12.7):
            return Transform(old,label(text,size,color,old.get_center(),max_width))
        start=self.time
        self.play(inflow.animate.set_value(1),water_level.animate.set_value(.96),
                  change(water_label,'Water load',24,TEAL,3),
                  change(osmo_state,'Falls slightly',21,TEAL,3.2),
                  change(caption,'Added water lowers plasma osmolality and dilutes plasma sodium.'),
                  change(context,'The sodium symbols stay the same; the amount of water increases.',16,MUTED),run_time=3)
        self.play(inflow.animate.set_value(0),run_time=1)
        self.wait(5)
        chapters.append({'id':'water-load','start':round(start,2),'end':round(self.time,2)})
        start=self.time
        self.play(control_arrow.animate.set_opacity(.6),
                  change(adh,'Vasopressin ↓',23,TEAL,3.4),
                  change(caption,'Lower plasma osmolality suppresses vasopressin release.'),
                  change(context,'Osmotic sensing changes the hormonal signal to the collecting duct.',16,MUTED),run_time=2)
        self.wait(6)
        chapters.append({'id':'vasopressin-suppression','start':round(start,2),'end':round(self.time,2)})
        start=self.time
        self.play(insertion.animate.set_value(.08),permeability.animate.set_value(.18),
                  change(caption,'AQP2 channels move away from the apical membrane into the cells.'),
                  change(context,'Collecting-duct water permeability falls.',16,MUTED),run_time=4)
        self.wait(7)
        chapters.append({'id':'aqp2-and-permeability','start':round(start,2),'end':round(self.time,2)})
        start=self.time
        self.play(urine_volume.animate.set_value(.87),urine_osmolality.animate.set_value(.16),
                  change(output_label,'Dilute urine',18,TEAL,2.5),
                  change(water_recovery,'Less water reabsorbed',17,TEAL,3.0),
                  change(caption,'Less water leaves the duct. More remains in the urine.'),
                  change(context,'Urine volume rises while urine osmolality falls.',16,MUTED),run_time=3)
        self.wait(8)
        chapters.append({'id':'dilute-urine','start':round(start,2),'end':round(self.time,2)})
        if review=='after':return
        start=self.time
        self.play(water_level.animate.set_value(.81),
                  change(osmo_state,'Towards baseline',21,TEAL,3.2),
                  change(caption,'Excreting excess water helps restore plasma sodium concentration.'),
                  change(context,'This response limits the dilution caused by the water load.',16,MUTED),run_time=5)
        self.wait(6)
        chapters.append({'id':'negative-feedback','start':round(start,2),'end':round(self.time,2)})
        start=self.time
        self.play(change(caption,'Water load → vasopressin ↓ → water permeability ↓ → dilute urine.'),
                  change(context,'Plasma sodium concentration depends on water balance as well as sodium content.',16,MUTED),run_time=1.5)
        self.wait(7)
        chapters.append({'id':'take-home','start':round(start,2),'end':round(self.time,2)})
        FilePath(__file__).with_name('chapter-times.json').write_text(
            json.dumps({'chapters':chapters,'durationSeconds':round(self.time,2)},indent=2)+'\n')
