"""Coordinated storage and voiding; a qualitative schematic, not a circuit map.

Manim Community 0.22.1. Palette and local labels match renal-pressure and
urine-concentration. Neural activity, shape and flow are illustrative only.
"""
from manim import *
from pathlib import Path as FilePath
import json
import os
import numpy as np

BG='#10151F'; INK='#EDF3FA'; MUTED='#A4B3C5'
GOLD='#F2C66D'; TEAL='#65D4C2'; CORAL='#EC6174'
WALL='#5E8EAD'; LUMEN='#172B3E'


def label(text, size=22, color=INK, at=None, max_width=None):
    obj=Text(text or '·',font='Avenir Next',font_size=size,color=color,line_spacing=.85)
    if not text: obj.set_opacity(0)
    if max_width and obj.width>max_width: obj.scale_to_fit_width(max_width)
    if at is not None: obj.move_to(at)
    return obj


class Micturition(Scene):
    def construct(self):
        self.camera.background_color=BG
        review=os.environ.get('MICTURITION_REVIEW')
        chapters=[]
        clock=ValueTracker(0)
        clock.add_updater(lambda m,dt:m.increment_value(dt))
        self.add(clock)
        size=ValueTracker(.84)
        opening=ValueTracker(0)
        flow=ValueTracker(0)
        sympathetic=ValueTracker(.85)
        pelvic=ValueTracker(.13)
        pudendal=ValueTracker(.90)
        cx=2.55

        title=label('How the bladder switches from storage to voiding',32,INK,
                    max_width=12.8).to_edge(UP,buff=.30)
        phase=label('Storage',24,GOLD,[5.25,2.59,0],2.5)
        caption=label('Store urine with a relaxed bladder and a closed outlet.',21,INK,[0,-3.17,0],12.7)
        context=label('',16,MUTED,[0,-3.58,0],12.7)

        def bladder_shape():
            s=size.get_value()
            w=1.05+.47*s
            top=.63+1.35*s
            middle=-.13+.52*s
            shape=VMobject().start_new_path(np.array([cx-.21,-1.0,0]))
            shape.add_cubic_bezier_curve_to(np.array([cx-.35,-.64,0]),np.array([cx-w,-.65,0]),np.array([cx-w,middle,0]))
            shape.add_cubic_bezier_curve_to(np.array([cx-w,top+.38,0]),np.array([cx+w,top+.38,0]),np.array([cx+w,middle,0]))
            shape.add_cubic_bezier_curve_to(np.array([cx+w,-.65,0]),np.array([cx+.35,-.64,0]),np.array([cx+.21,-1.0,0]))
            shape.set_stroke(interpolate_color(ManimColor(WALL),ManimColor(TEAL),flow.get_value()),width=8)
            shape.set_fill(LUMEN,opacity=1)
            return shape
        bladder=always_redraw(bladder_shape)
        # Anatomical relations are schematic; the bladder neck is not drawn
        # as a universal discrete internal sphincter in both sexes.
        def urethra_shape():
            gap=.045+.15*opening.get_value()
            return VGroup(*[Line([cx+side*.21,-.99,0],[cx+side*gap,-1.45,0],color=WALL,stroke_width=4)
                              for side in [-1,1]],
                          *[Line([cx+side*gap,-1.45,0],[cx+side*gap,-2.47,0],color=WALL,stroke_width=4)
                              for side in [-1,1]])
        urethra=always_redraw(urethra_shape)
        def muscle_pair(y,width,height,color):
            gap=.018+.20*opening.get_value()
            return VGroup(*[RoundedRectangle(width=width,height=height,corner_radius=.045,
                         stroke_color=color,stroke_width=1.5,fill_color=color,
                         fill_opacity=.70-.30*opening.get_value())
                         .move_to([cx+side*(width/2+gap),y,0]) for side in [-1,1]])
        neck=always_redraw(lambda:muscle_pair(-1.18,.24,.17,GOLD))
        external=always_redraw(lambda:muscle_pair(-1.97,.30,.28,CORAL))
        bladder_name=label('Detrusor',19,MUTED,[5.18,1.03,0],2.5)
        bladder_state=label('relaxed',22,GOLD,[5.18,.63,0],2.5)
        neck_name=label('Bladder outlet',18,MUTED,[5.18,-.78,0],2.85)
        neck_state=label('closed',21,GOLD,[5.18,-1.15,0],2.5)
        ext_name=label('External sphincter',18,MUTED,[5.18,-1.91,0],2.9)
        ext_state=label('contracted',21,CORAL,[5.18,-2.28,0],2.5)
        leaders=VGroup(Line([3.91,.85,0],[4.13,.85,0],color='#43526A',stroke_width=1),
                       Line([3.02,-1.15,0],[3.99,-1.15,0],color='#43526A',stroke_width=1),
                       Line([3.10,-1.98,0],[3.80,-1.98,0],color='#43526A',stroke_width=1))
        urine_label=label('Urine',17,TEAL,[cx,-2.78,0],1.5).set_opacity(0)
        urine_arrow=Arrow([cx,-2.37,0],[cx,-2.66,0],buff=0,color=TEAL,
                          stroke_width=2,max_tip_length_to_length_ratio=.25).set_opacity(0)

        # Neural lanes use the same local-label placement as the prior clips.
        pons_frame=RoundedRectangle(width=3.9,height=.63,corner_radius=.16,
                    stroke_color=WALL,stroke_width=1.5,fill_color=LUMEN,fill_opacity=1)
        pons_frame.move_to([-4.15,2.36,0])
        pons_name=label('Pontine coordination',22,INK,[-4.15,2.36,0],3.5)
        spine=Line([-6.30,2.36,0],[-6.30,-2.12,0],color='#43526A',stroke_width=2)
        top_link=Line([-6.30,2.36,0],[-6.10,2.36,0],color='#43526A',stroke_width=2)
        nerves=VGroup()
        paths=[]
        trackers=[sympathetic,pelvic,pudendal]
        colors=[GOLD,TEAL,CORAL]
        for name,detail,y,color,end in [
            ('Hypogastric','Sympathetic',.83,GOLD,[1.16,.37,0]),
            ('Pelvic','Parasympathetic · S2–S4',-.52,TEAL,[1.12,-.40,0]),
            ('Pudendal','Somatic · S2–S4',-1.87,CORAL,[2.20,-1.97,0])]:
            nerves.add(label(name,23,color,[-4.30,y+.39,0],3.1),
                       label(detail,16,MUTED,[-4.30,y+.06,0],3.45))
            path=VMobject().set_points_as_corners([
                np.array([-6.30,y-.27,0]),np.array([-2.30,y-.27,0]),np.array(end)])
            path.set_stroke(color,width=2.2).set_fill(opacity=0)
            paths.append(path)
        indicators=[label('active',17,GOLD,[-1.69,1.05,0],1.5),
                    label('low',17,TEAL,[-1.69,-.30,0],1.5),
                    label('active',17,CORAL,[-1.69,-1.65,0],1.5)]
        pathways=VGroup(*paths)
        for path,activity in zip(paths,trackers):
            path.add_updater(lambda m,dt,activity=activity:m.set_stroke(opacity=.12+.70*activity.get_value()))

        sensory_path=VMobject().start_new_path(np.array([2.64,1.94,0]))
        sensory_path.add_cubic_bezier_curve_to(np.array([2.1,2.93,0]),np.array([-.8,2.80,0]),np.array([-2.17,2.36,0]))
        sensory_path.set_stroke(MUTED,width=1.4,opacity=.65)
        sensory_tip=Arrow([-1.78,2.49,0],[-2.15,2.37,0],buff=0,color=MUTED,
                     stroke_width=1.4,max_tip_length_to_length_ratio=.25)
        sensory_label=label('Filling signals',17,MUTED,[.31,2.95,0],2.5)
        sensory=VGroup(sensory_path,sensory_tip,sensory_label)

        self.play(FadeIn(title),run_time=1)
        self.play(FadeIn(bladder),FadeIn(urethra),FadeIn(neck),FadeIn(external),
                  FadeIn(bladder_name),FadeIn(bladder_state),FadeIn(neck_name),FadeIn(neck_state),
                  FadeIn(ext_name),FadeIn(ext_state),FadeIn(leaders),FadeIn(phase),FadeIn(caption),run_time=2)
        self.add(context,urine_label,urine_arrow)
        # Fluid dots represent stored urine, not a quantitative volume scale.
        fluid=VGroup()
        for row in range(5):
            for col in range(5):
                xx=(col-2)*.35
                yy=-.30+row*.34
                if (xx/.95)**2+((yy-.4)/1.0)**2>1:continue
                dot=Dot(radius=.035,color=TEAL)
                def update_fluid(m,dt,xx=xx,yy=yy,row=row,col=col):
                    s=size.get_value()
                    m.move_to([cx+xx*(.7+.3*s),-.43+(yy+.43)*(.4+.6*s),0])
                    m.set_opacity(.65 if (row*5+col)/25 < .25+.75*s else .08)
                dot.add_updater(update_fluid);fluid.add(dot)
        self.add(fluid)
        self.play(FadeIn(pons_frame),FadeIn(pons_name),Create(spine),Create(top_link),
                  FadeIn(nerves),Create(pathways),*[FadeIn(x) for x in indicators],run_time=2)
        pulses=VGroup()
        for path,activity,color in zip(paths,trackers,colors):
            for i in range(6):
                dot=Dot(radius=.035,color=color)
                def update_pulse(m,dt,path=path,activity=activity,offset=i/6):
                    t=(clock.get_value()*(.10+.18*activity.get_value())+offset)%1
                    m.move_to(path.point_from_proportion(t))
                    # Reduced activity remains low, rather than anatomically severed.
                    m.set_opacity(activity.get_value() if offset<activity.get_value() else .025)
                dot.add_updater(update_pulse);pulses.add(dot)
        for i in range(9):
            dot=Dot(radius=.032,color=TEAL)
            def update_urine(m,dt,offset=i/9):
                t=(clock.get_value()*.67+offset)%1
                m.move_to([cx,-.80-1.91*t,0])
                m.set_opacity(flow.get_value())
            dot.add_updater(update_urine);pulses.add(dot)
        self.add(pulses)

        def text_to(old,text,size=21,color=INK,max_width=12.7):
            return Transform(old,label(text,size,color,old.get_center(),max_width))
        start=self.time
        self.play(size.animate.set_value(1),run_time=4)
        self.wait(6)
        chapters.append({'id':'storage','start':round(start,2),'end':round(self.time,2)})
        if review=='storage':return
        start=self.time
        self.play(Create(sensory_path),FadeIn(sensory_tip),FadeIn(sensory_label),
                  text_to(caption,'Bladder filling sends sensory information to the brain.'),
                  text_to(context,'Higher centres allow voiding when the time and place are appropriate.',16,MUTED),run_time=2)
        self.wait(6)
        self.play(pons_frame.animate.set_stroke(TEAL,width=2.4),
                  Indicate(pons_name,color=TEAL),
                  text_to(caption,'Pontine circuits coordinate the switch to voiding.'),run_time=1.5)
        self.wait(4)
        chapters.append({'id':'filling-and-permission','start':round(start,2),'end':round(self.time,2)})
        start=self.time
        self.play(FadeOut(sensory),sympathetic.animate.set_value(.12),pelvic.animate.set_value(.96),
                  pudendal.animate.set_value(.09),
                  text_to(indicators[0],'↓',22,GOLD,1.5),
                  text_to(indicators[1],'↑',22,TEAL,1.5),
                  text_to(indicators[2],'↓',22,CORAL,1.5),
                  text_to(phase,'Switch',24,TEAL,2.5),
                  text_to(caption,'Pelvic activity rises. Sympathetic and pudendal activity fall.'),
                  text_to(context,'These changes prepare the bladder and outlet to work together.',16,MUTED),run_time=3)
        self.wait(4)
        chapters.append({'id':'neural-switch','start':round(start,2),'end':round(self.time,2)})
        start=self.time
        self.play(opening.animate.set_value(1),size.animate.set_value(.96),
                  text_to(phase,'Voiding',24,TEAL,2.5),
                  text_to(bladder_state,'contracting',22,TEAL,2.5),
                  text_to(neck_state,'relaxed',21,TEAL,2.5),
                  text_to(ext_state,'relaxed',21,TEAL,2.5),
                  text_to(caption,'The outlet relaxes as detrusor contraction begins.'),
                  text_to(context,'Reduced pudendal drive lets the external sphincter relax.',16,MUTED),run_time=2)
        self.play(flow.animate.set_value(.95),size.animate.set_value(.88),
                  urine_arrow.animate.set_opacity(1),urine_label.animate.set_opacity(1),run_time=2)
        self.play(size.animate.set_value(.30),
                  text_to(caption,'Bladder pressure drives urine through a low-resistance outlet.'),
                  text_to(context,'Detrusor contraction and outlet relaxation permit efficient emptying.',16,MUTED),run_time=8)
        self.wait(5)
        chapters.append({'id':'coordinated-emptying','start':round(start,2),'end':round(self.time,2)})
        if review=='voiding':return
        start=self.time
        self.play(Indicate(paths[1],color=TEAL),Indicate(external,color=TEAL),
                  text_to(caption,'Normal voiding requires coordinated bladder and sphincter activity.'),
                  text_to(context,'Pelvic ↑  ·  Pudendal ↓  ·  Sympathetic ↓',16,MUTED),run_time=1.5)
        self.wait(6)
        chapters.append({'id':'take-home','start':round(start,2),'end':round(self.time,2)})
        FilePath(__file__).with_name('chapter-times.json').write_text(
            json.dumps({'chapters':chapters,'durationSeconds':round(self.time,2)},indent=2)+'\n')
