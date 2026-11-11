"""Loop diuretics, the medullary gradient and water recovery.

Manim Community 0.22.1. Qualitative directions and indicators, not a calibrated
transport model. Vasopressin-driven permeability remains high after blockade.
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
    obj=Text(text or '·',font='Avenir Next',font_size=size,color=color,line_spacing=.8)
    if not text:obj.set_opacity(0)
    if max_width and obj.width>max_width:obj.scale_to_fit_width(max_width)
    if at is not None:obj.move_to(at)
    return obj


class UrineConcentration(Scene):
    def construct(self):
        self.camera.background_color=BG
        gradient=ValueTracker(.22)
        salt_transport=ValueTracker(.95)
        ability=ValueTracker(.28)
        clock=ValueTracker(0)
        clock.add_updater(lambda m,dt:m.increment_value(dt))
        self.add(clock)
        review=os.environ.get('URINE_REVIEW')
        chapters=[]
        dx,ax,cx=-4.6,-2.15,1.75

        title=label('Why loop diuretics limit urine concentration',32,INK,
                    max_width=12.8).to_edge(UP,buff=.30)
        loop=VMobject().start_new_path(np.array([dx,1.5,0]))
        loop.add_line_to(np.array([dx,-1.40,0]))
        loop.add_cubic_bezier_curve_to(np.array([dx,-2.23,0]),np.array([ax,-2.23,0]),np.array([ax,-1.40,0]))
        loop.add_line_to(np.array([ax,1.5,0]))
        loop.set_stroke(WALL,width=22)
        loop_inner=loop.copy().set_stroke(LUMEN,width=14)
        tal=Line([ax,-.40,0],[ax,1.5,0],stroke_color=WALL,stroke_width=30)
        tal_inner=tal.copy().set_stroke(LUMEN,width=19)
        cd=Line([cx,1.5,0],[cx,-2.07,0],stroke_color=WALL,stroke_width=30)
        cd_inner=cd.copy().set_stroke(LUMEN,width=19)

        bands=VGroup()
        for i in range(15):
            depth=(i+1)/15
            band=Rectangle(width=7.5,height=.23,stroke_width=0,
                           fill_color=GOLD,fill_opacity=.02)
            band.move_to([-1.55,1.13-i*.23,0])
            def update_band(m,dt,depth=depth):
                m.set_fill(opacity=.012+(.025+.17*depth)*gradient.get_value())
            band.add_updater(update_band);bands.add(band)
        cortex_boundary=DashedLine([-5.3,1.27,0],[2.20,1.27,0],dash_length=.11,
                                  stroke_color='#43526A',stroke_width=1)
        cortex=label('Cortex',14,MUTED,[-5.9,1.38,0],1.1)
        medulla=label('Medulla',14,MUTED,[-5.9,.87,0],1.1)

        names=VGroup(label('Descending limb',18,MUTED,[dx,1.92,0],2.45),
                     label('Ascending limb',18,MUTED,[ax,1.92,0],2.4),
                     label('Collecting duct',18,MUTED,[cx,1.92,0],2.8))
        adh=label('High vasopressin',22,TEAL,[cx,2.51,0],3.05)
        drug=label('',24,TEAL,[ax,2.51,0],3.6)
        nkcc2=label('NKCC2',19,GOLD,[-3.12,.49,0],1.45)
        pump=RoundedRectangle(width=.18,height=.42,corner_radius=.05,
              stroke_color=GOLD,stroke_width=1.6,fill_color=GOLD,fill_opacity=.25)
        pump.move_to([ax,.49,0])
        nacl=label('NaCl',18,GOLD,[-.76,1.12,0],1)
        water_label=label('Water',18,TEAL,[.69,-1.25,0],1.05)
        arrows=VGroup(Arrow([dx,.94,0],[dx,.51,0],buff=0,color=MUTED,stroke_width=2,
                     max_tip_length_to_length_ratio=.25),
                     Arrow([ax,-.97,0],[ax,-.57,0],buff=0,color=MUTED,stroke_width=2,
                     max_tip_length_to_length_ratio=.25),
                     Arrow([cx,1.1,0],[cx,.72,0],buff=0,color=MUTED,stroke_width=2,
                     max_tip_length_to_length_ratio=.25))
        salt_arrows=VGroup(*[Arrow([ax+.07,y,0],[-.75,y,0],buff=0,
                        color=GOLD,stroke_width=1.4,
                        max_tip_length_to_length_ratio=.12) for y in [-.11,.47,.89]])
        salt_arrows.add_updater(lambda m,dt:m.set_opacity(.1+.65*salt_transport.get_value()))
        # Open water paths remain present throughout, including after NKCC2 blockade.
        channels=VGroup(*[Rectangle(width=.18,height=.09,stroke_width=0,
                         fill_color=TEAL,fill_opacity=1).move_to([cx-.10,y,0])
                         for y in [.63,.05,-.53,-1.11]])
        output=Arrow([cx,-2.12,0],[cx,-2.40,0],buff=0,color=MUTED,
                     stroke_width=2,max_tip_length_to_length_ratio=.25)
        output_label=label('Urine',18,MUTED,[cx,-2.59,0],1.8)
        blocked=VGroup(Line([ax-.18,.76,0],[ax+.18,.22,0],color=CORAL,stroke_width=4),
                       Line([ax-.18,.22,0],[ax+.18,.76,0],color=CORAL,stroke_width=4))
        blocked.set_opacity(0)

        def meter(y,value,color):
            track=RoundedRectangle(width=2.85,height=.16,corner_radius=.05,
                   stroke_width=0,fill_color='#2A3444',fill_opacity=1).move_to([4.75,y,0])
            fill=always_redraw(lambda:Rectangle(width=max(.03,2.85*value.get_value()),
                 height=.16,stroke_width=0,fill_color=color,fill_opacity=1)
                 .move_to([3.325+2.85*value.get_value()/2,y,0]))
            return VGroup(track,fill)
        gauges=VGroup(label('Medullary gradient',18,INK,[4.75,.95,0],3.15),
                      meter(.56,gradient,GOLD),
                      label('Concentrating ability',18,INK,[4.75,-.09,0],3.15),
                      meter(-.48,ability,TEAL))
        caption=label('An osmotic gradient and a water-permeable duct work together.',21,INK,[0,-3.17,0],12.8)
        context=label('',16,MUTED,[0,-3.58,0],12.7)
        self.play(FadeIn(title),run_time=1)
        self.play(FadeIn(bands),Create(cortex_boundary),FadeIn(cortex),FadeIn(medulla),
                  Create(loop),Create(loop_inner),Create(tal),Create(tal_inner),
                  Create(cd),Create(cd_inner),FadeIn(names),FadeIn(adh),FadeIn(nkcc2),
                  FadeIn(pump),FadeIn(nacl),FadeIn(water_label),FadeIn(arrows),
                  FadeIn(salt_arrows),FadeIn(channels),FadeIn(output),FadeIn(output_label),
                  FadeIn(gauges),FadeIn(caption),run_time=2)
        self.add(drug,blocked,context)

        # Moving dots communicate direction, not mass-conserving molecule counts.
        particles=VGroup()
        for i in range(24):
            dot=Dot(radius=.028,color=TEAL)
            def update_flow(m,dt,offset=i/24):
                m.move_to(loop.point_from_proportion((clock.get_value()*.11+offset)%1))
            dot.add_updater(update_flow);particles.add(dot)
        for i in range(16):
            dot=Dot(radius=.033,color=TEAL)
            def update_cd(m,dt,offset=i/16):
                m.move_to(cd.point_from_proportion((clock.get_value()*.21+offset)%1))
                retained=.28+.62*(1-gradient.get_value())
                m.set_opacity(1 if offset<retained else .12)
            dot.add_updater(update_cd);particles.add(dot)
        for row,y in enumerate([-.11,.47,.89]):
            for i in range(5):
                dot=Dot(radius=.037,color=GOLD)
                def update_salt(m,dt,offset=i/5,y=y,row=row):
                    t=(clock.get_value()*.7+offset+row*.1)%1
                    m.move_to([ax+.10+1.27*t,y,0])
                    m.set_opacity(salt_transport.get_value())
                dot.add_updater(update_salt);particles.add(dot)
        for row,y in enumerate([.63,.05,-.53,-1.11]):
            for i in range(4):
                dot=Dot(radius=.033,color=TEAL)
                def update_water(m,dt,offset=i/4,y=y,row=row):
                    t=(clock.get_value()*.48+offset+row*.08)%1
                    m.move_to([cx-.09-1.12*t,y,0])
                    # Water permeability is held high; changing gradient alters flux.
                    m.set_opacity(gradient.get_value() if offset<gradient.get_value() else .02)
                dot.add_updater(update_water);particles.add(dot)
        for row,y in enumerate([.30,-.38,-1.03]):
            for i in range(3):
                dot=Dot(radius=.027,color=TEAL)
                def update_descending(m,dt,offset=i/3,y=y,row=row):
                    t=(clock.get_value()*.42+offset+row*.08)%1
                    m.move_to([dx-.05-.69*t,y,0])
                    m.set_opacity(.7*gradient.get_value() if offset<gradient.get_value() else .02)
                dot.add_updater(update_descending);particles.add(dot)
        self.add(particles)
        self.wait(4)

        def text_to(old,text,size=21,color=INK,max_width=12.7):
            return Transform(old,label(text,size,color,old.get_center(),max_width))
        start=self.time
        self.play(gradient.animate.set_value(.91),ability.animate.set_value(.90),
                  text_to(caption,'Salt leaves the thick ascending limb; water cannot follow.'),
                  run_time=4)
        self.wait(7)
        chapters.append({'id':'build-gradient','start':round(start,2),'end':round(self.time,2)})
        start=self.time
        self.play(Indicate(adh,color=TEAL),
                  text_to(caption,'High vasopressin keeps the collecting duct water-permeable.'),
                  text_to(context,'Water leaves the duct down the medullary osmotic gradient.',16,MUTED),run_time=1.3)
        self.wait(7)
        chapters.append({'id':'vasopressin-and-water','start':round(start,2),'end':round(self.time,2)})
        if review=='before':return

        start=self.time
        self.play(text_to(drug,'Loop diuretic',24,TEAL,3.6),
                  blocked.animate.set_opacity(1),salt_transport.animate.set_value(.07),
                  text_to(caption,'NKCC2 blockade reduces salt reabsorption into the medulla.'),
                  text_to(context,'Vasopressin remains high.',16,MUTED),run_time=2)
        self.wait(4)
        self.play(gradient.animate.set_value(.34),ability.animate.set_value(.37),
                  text_to(caption,'The gradient weakens. Less water is recovered from the collecting duct.'),run_time=5)
        self.wait(7)
        chapters.append({'id':'nkcc2-blockade','start':round(start,2),'end':round(self.time,2)})
        start=self.time
        self.play(Indicate(adh,color=TEAL),Indicate(channels,color=TEAL),
                  text_to(caption,'Open water pathways cannot replace a strong osmotic gradient.'),
                  text_to(context,'High vasopressin does not fully restore the concentrating capacity.',16,MUTED),run_time=1.5)
        self.wait(7)
        chapters.append({'id':'permeability-remains','start':round(start,2),'end':round(self.time,2)})
        if review=='after':return
        start=self.time
        self.play(text_to(caption,'NKCC2 block → weaker medullary gradient → lower concentrating capacity.'),
                  text_to(context,'Reduced concentrating capacity; the medullary gradient is not abolished.',16,MUTED),run_time=1)
        self.wait(7)
        chapters.append({'id':'take-home','start':round(start,2),'end':round(self.time,2)})
        FilePath(__file__).with_name('chapter-times.json').write_text(
            json.dumps({'chapters':chapters,'durationSeconds':round(self.time,2)},indent=2)+'\n')
