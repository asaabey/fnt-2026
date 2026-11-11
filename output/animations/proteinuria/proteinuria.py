"""Three predominant mechanisms of proteinuria, in a shared nephron schematic.

Manim Community 0.22.1. Particle counts and mesh spacing are illustrative,
not a calibrated size-sieving, receptor-kinetic or mass-conservation model.
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


def polyline(points,color=MUTED,width=2):
    return VMobject().set_points_as_corners([np.array(p,dtype=float) for p in points]).set_stroke(color,width).set_fill(opacity=0)


class Proteinuria(Scene):
    def construct(self):
        self.camera.background_color=BG
        review=os.environ.get('PROTEINURIA_REVIEW')
        chapters=[]
        clock=ValueTracker(0)
        clock.add_updater(lambda m,dt:m.increment_value(dt))
        leak=ValueTracker(.045)
        load=ValueTracker(18)
        capacity=ValueTracker(17)
        injury=ValueTracker(0)
        self.add(clock,leak,load,capacity,injury)

        title=label('Three routes to proteinuria',32,INK,max_width=12.8).to_edge(UP,buff=.30)
        phase=label('Normal handling',26,TEAL,[-4.65,2.55,0],3.9)
        caption=label('Most albumin stays in blood. Filtered small proteins are taken up.',21,INK,[0,-3.17,0],12.7)
        context=label('Protein uptake occurs in proximal tubular cells.',16,MUTED,[0,-3.58,0],12.7)
        blood=label('Blood',19,MUTED,[-5.6,1.08,0],1.6)
        urine=label('Urine',19,MUTED,[5.65,1.08,0],1.6)
        filter_name=label('Glomerular barrier',19,MUTED,[-2.55,1.78,0],3)
        tubule_name=label('Proximal tubule',19,MUTED,[2.34,1.98,0],3)
        blood_lane=VGroup(Line([-6.1,.67,0],[-2.72,.67,0],color='#43526A',stroke_width=1.5),
                          Line([-6.1,-.47,0],[-2.72,-.47,0],color='#43526A',stroke_width=1.5))
        filtrate_lane=VGroup(Line([-2.36,.67,0],[-.73,.67,0],color='#43526A',stroke_width=1.5),
                             Line([-2.36,-.47,0],[-.73,-.47,0],color='#43526A',stroke_width=1.5))
        lumen=Rectangle(width=5.45,height=1.14,stroke_width=0,fill_color=LUMEN,fill_opacity=1).move_to([2.0,.10,0])
        lower_wall=Line([-.73,-.47,0],[4.73,-.47,0],color=WALL,stroke_width=4)
        upper_wall=Line([-.73,.67,0],[4.73,.67,0],color=WALL,stroke_width=4)
        brush=VGroup(*[Line([x,.67,0],[x,.82,0],color=WALL,stroke_width=1.3) for x in np.linspace(-.67,4.67,36)])
        cells=VGroup(*[RoundedRectangle(width=1.21,height=.83,corner_radius=.08,
                       stroke_color=WALL,stroke_width=1.5,fill_color=LUMEN,fill_opacity=1)
                       .move_to([x,1.18,0]) for x in [.65,2.22,3.79]])
        # The mesh is a schematic of selectivity, not literal anatomical holes.
        def barrier_shape():
            h=.13-.07*leak.get_value()
            return VGroup(*[RoundedRectangle(width=.24,height=h,corner_radius=.025,
                       stroke_color=interpolate_color(ManimColor(WALL),ManimColor(CORAL),leak.get_value()),
                       stroke_width=1.5,fill_color=WALL,fill_opacity=.35)
                       .move_to([-2.55,y,0]) for y in np.linspace(-.53,1.12,8)])
        barrier=always_redraw(barrier_shape)
        filter_state=label('Restrictive',20,TEAL,[-2.55,-1.0,0],3.1)
        uptake_state=label('Uptake working',20,TEAL,[2.22,-1.0,0],3.5)
        output_state=label('Very little protein',19,MUTED,[5.49,-1.0,0],2.7)
        output_arrow=Arrow([4.88,.10,0],[6.08,.10,0],buff=0,color=MUTED,
                           stroke_width=1.5,max_tip_length_to_length_ratio=.13)
        uptake_arrows=VGroup(*[Arrow([x,.17,0],[x,1.28,0],buff=0,color=TEAL,
                              stroke_width=1.4,max_tip_length_to_length_ratio=.10) for x in [.65,2.22,3.79]])
        uptake_arrows.add_updater(lambda m,dt:m.set_opacity(.15+.65*(1-injury.get_value())))
        injury_marks=VGroup(*[VGroup(Line([x-.15,1.45,0],[x+.15,.96,0],color=CORAL,stroke_width=3),
                                    Line([x-.15,.96,0],[x+.15,1.45,0],color=CORAL,stroke_width=3)) for x in [.65,2.22,3.79]])
        injury_marks.add_updater(lambda m,dt:m.set_opacity(injury.get_value()))
        albumin_icon=Dot(radius=.09,color=CORAL).move_to([-5.22,-2.0,0])
        small_icon=Dot(radius=.042,color=GOLD).move_to([-.30,-2.0,0])
        albumin_legend=label('Albumin',19,CORAL,[-4.30,-2.0,0],2)
        small_legend=label('Small proteins',19,GOLD,[1.36,-2.0,0],3.5)
        legend=VGroup(albumin_icon,albumin_legend,small_icon,small_legend)
        load_label=label('',19,GOLD,[-5.1,-.98,0],2.1)
        diagram=VGroup(blood,urine,filter_name,tubule_name,blood_lane,filtrate_lane,lumen,
                       lower_wall,upper_wall,brush,cells,barrier,filter_state,uptake_state,
                       output_state,output_arrow,uptake_arrows,injury_marks,legend,load_label,phase)
        self.play(FadeIn(title),run_time=1)
        self.play(FadeIn(diagram),FadeIn(caption),FadeIn(context),run_time=2)

        # A common blood→filtrate→tubule→urine direction is used in all cases.
        # Captured proteins enter epithelial cells and fade there; they are not
        # drawn returning to blood as unchanged intact proteins.
        def route_point(t,y,uptake_x=None,blocked=False):
            if blocked:
                # Retained albumin approaches the barrier and turns back in blood.
                if t<.58:
                    return np.array([-6.0+3.20*t/.58,y,0]),1.0
                q=(t-.58)/.42
                return np.array([-2.80-3.20*q,y+.19,0]),max(0,1-q*.65)
            if uptake_x is None:
                return np.array([-6.0+12.15*t,y,0]),min(1,(1-t)*12)
            if t<.80:
                return np.array([-6.0+(uptake_x+6.0)*t/.80,y,0]),1.0
            q=(t-.80)/.20
            return np.array([uptake_x,y+(1.43-y)*q,0]),max(0,1-(max(0,q-.73)/.27))

        particles=VGroup()
        for i in range(22):
            dot=Dot(radius=.079,color=CORAL)
            def update_albumin(m,dt,i=i):
                t=(clock.get_value()*.135+i/22)%1
                passes=i/22 < leak.get_value()
                # Some filtered albumin is taken up; excess reaches urine.
                captures=passes and i<2
                x=[.65,2.22,3.79][i%3] if captures else None
                y=.10+((i%3)-1)*.22
                p,alpha=route_point(t,y,x,blocked=not passes)
                m.move_to(p).set_opacity(alpha*.92)
            dot.add_updater(update_albumin);particles.add(dot)
        for i in range(50):
            dot=Dot(radius=.039,color=GOLD)
            def update_small(m,dt,i=i):
                t=(clock.get_value()*.143+i*.381966)%1
                visible=np.clip(load.get_value()-i,0,1)
                captured=i<capacity.get_value()
                x=[.65,2.22,3.79][i%3] if captured else None
                y=.10+((i%5)-2)*.11
                p,alpha=route_point(t,y,x)
                m.move_to(p).set_opacity(alpha*visible)
            dot.add_updater(update_small);particles.add(dot)
        self.add(particles)
        start=self.time
        self.wait(9)
        chapters.append({'id':'normal-handling','start':round(start,2),'end':round(self.time,2)})
        if review=='normal': return

        # Keep stable label identities so the diagram can fade as one group.
        def change(old,text,size=21,color=INK,max_width=12.7):
            return Transform(old,label(text,size,color,old.get_center(),max_width))

        start=self.time
        self.play(leak.animate.set_value(.80),
                  change(phase,'Glomerular',26,CORAL,3.9),
                  change(filter_state,'Permeability ↑',20,CORAL,3.1),
                  change(output_state,'Albumin ↑',19,CORAL,2.7),
                  change(caption,'A less selective glomerular barrier lets more albumin enter the filtrate.'),
                  change(context,'Example: diabetic kidney disease with predominantly urinary albumin.',16,MUTED),run_time=3)
        self.wait(12)
        self.play(Indicate(barrier,color=CORAL),run_time=1.2)
        self.wait(3)
        chapters.append({'id':'glomerular-leakage','start':round(start,2),'end':round(self.time,2)})
        if review=='glomerular': return

        start=self.time
        self.play(leak.animate.set_value(.045),capacity.animate.set_value(3),injury.animate.set_value(1),
                  change(phase,'Tubular',26,TEAL,3.9),
                  change(filter_state,'Restrictive',20,TEAL,3.1),
                  change(uptake_state,'Uptake impaired',20,CORAL,3.5),
                  change(output_state,'Small proteins ↑',19,GOLD,2.7),
                  change(caption,'Filtered small proteins escape when proximal tubular uptake is impaired.'),
                  change(context,'Example: proximal tubular injury with low-molecular-weight proteinuria.',16,MUTED),run_time=3)
        self.wait(12)
        self.play(Indicate(injury_marks,color=CORAL),run_time=1.2)
        self.wait(3)
        chapters.append({'id':'tubular-reabsorption-failure','start':round(start,2),'end':round(self.time,2)})
        if review=='tubular': return

        start=self.time
        self.play(capacity.animate.set_value(17),injury.animate.set_value(0),
                  change(phase,'Overflow',26,GOLD,3.9),
                  change(uptake_state,'Uptake working',20,TEAL,3.5),
                  change(small_legend,'Free light chains',19,GOLD,3.5),
                  change(caption,'Excess circulating free light chains increase the filtered protein load.'),
                  change(context,'Example: a plasma-cell disorder producing excess free light chains.',16,MUTED),run_time=2)
        self.play(load.animate.set_value(49),
                  change(load_label,'Protein load ↑',19,GOLD,2.1),
                  change(output_state,'Light chains ↑',19,GOLD,2.7),run_time=4)
        self.wait(6)
        self.play(change(uptake_state,'Capacity exceeded',20,GOLD,3.5),
                  change(caption,'Uptake continues, but the excess load exceeds reabsorptive capacity.'),
                  change(context,'Overflow does not require a primary glomerular leak.',16,MUTED),run_time=1.5)
        self.wait(8)
        chapters.append({'id':'overflow','start':round(start,2),'end':round(self.time,2)})
        if review=='overflow': return

        start=self.time
        # Freeze before fading, so live particle/opacity updaters cannot defeat FadeOut.
        diagram.clear_updaters(recursive=True)
        particles.clear_updaters(recursive=True)
        self.play(FadeOut(diagram),FadeOut(particles),
                  change(caption,'Different protein patterns can reveal different predominant mechanisms.'),
                  change(context,'Mechanisms may coexist in clinical disease.',16,MUTED),run_time=1.5)
        summary=VGroup()
        for x,heading,color,cause,protein,example in [
            (-4.50,'Glomerular',CORAL,'Barrier leak ↑','Albumin','Diabetes'),
            (0,'Tubular',TEAL,'Protein uptake ↓','Small proteins','Proximal tubular injury'),
            (4.50,'Overflow',GOLD,'Filtered load ↑','Free light chains','Plasma-cell disorder')]:
            summary.add(label(heading,26,color,[x,2.12,0],3.8),
                        label(cause,22,INK,[x,.88,0],3.9),
                        Arrow([x,.37,0],[x,-.35,0],buff=0,color=color,stroke_width=2,
                              max_tip_length_to_length_ratio=.18),
                        label(protein,22,color,[x,-.83,0],3.9),
                        label(example,17,MUTED,[x,-1.80,0],3.9))
        self.play(FadeIn(summary),run_time=1.5)
        self.wait(8)
        chapters.append({'id':'comparison','start':round(start,2),'end':round(self.time,2)})
        FilePath(__file__).with_name('chapter-times.json').write_text(
            json.dumps({'chapters':chapters,'durationSeconds':round(self.time,2)},indent=2)+'\n')
