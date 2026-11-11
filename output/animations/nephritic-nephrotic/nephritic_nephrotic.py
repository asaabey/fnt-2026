"""Illustrated glomerular barrier with two separately evolving injury patterns.

Manim Community 0.22.1. Original layered illustration informed by the user's
reference. This is a schematic capillary cross-section, not a whole glomerulus,
a histological image, or a calibrated filtration/injury model.
"""
from manim import *
from pathlib import Path as FilePath
import json
import os
import numpy as np

BG='#10151F'; INK='#EDF3FA'; MUTED='#A4B3C5'
GOLD='#F2C66D'; TEAL='#65D4C2'; CORAL='#EC6174'
WALL='#5E8EAD'; LUMEN='#172B3E'
ENDO='#BC7B8D'; ENDO_NUCLEUS='#794B63'; GBM='#78B9D1'; PURPLE='#B8A3DB'


def label(text,size=22,color=INK,at=None,max_width=None):
    obj=Text(text or '·',font='Avenir Next',font_size=size,color=color,line_spacing=.85)
    if not text:obj.set_opacity(0)
    if max_width and obj.width>max_width:obj.scale_to_fit_width(max_width)
    if at is not None:obj.move_to(at)
    return obj


def rbc(scale=1,angle=0):
    outer=Ellipse(width=.28*scale,height=.19*scale,stroke_color='#F29AA7',stroke_width=.8,
                  fill_color=CORAL,fill_opacity=.92)
    centre=Ellipse(width=.13*scale,height=.068*scale,stroke_color='#BA526B',stroke_width=.7,
                   fill_color='#BD516A',fill_opacity=.36)
    return VGroup(outer,centre).rotate(angle)


def leader(points):
    return VMobject().set_points_as_corners([np.array(p,dtype=float) for p in points])\
        .set_stroke(MUTED,width=1.1,opacity=.65).set_fill(opacity=0)


class GlomerularInjury(Scene):
    def construct(self):
        self.camera.background_color=BG
        review=os.environ.get('GLOMERULAR_REVIEW')
        chapters=[]
        C=np.array([-2.10,.18,0])
        clock=ValueTracker(0)
        clock.add_updater(lambda m,dt:m.increment_value(dt))
        inflammation=ValueTracker(0)
        disruption=ValueTracker(0)
        effacement=ValueTracker(0)
        protein_leak=ValueTracker(.035)
        filtration=ValueTracker(.86)
        cast_formation=ValueTracker(0)
        self.add(clock,inflammation,disruption,effacement,protein_leak,filtration,cast_formation)
        def polar(radius,degrees):
            a=degrees*DEGREES
            return C+np.array([radius*np.cos(a),radius*np.sin(a),0])

        title=label('Two patterns of glomerular injury',32,INK,max_width=12.8).to_edge(UP,buff=.30)
        phase=label('Healthy barrier',24,TEAL,[-5.03,2.65,0],3.6)
        caption=label('The filtration barrier has three cooperating layers.',21,INK,[0,-3.17,0],12.7)
        context=label('Blood cells and most albumin remain in the capillary.',16,MUTED,[0,-3.58,0],12.7)
        lumen=Circle(radius=1.55,stroke_color='#CB8D9F',stroke_width=.8,
                     fill_color=LUMEN,fill_opacity=1).move_to(C)
        endothelium=VGroup(); basement=VGroup()
        for i in range(36):
            a=i*10
            damaged=230<=a<=260
            en=AnnularSector(inner_radius=1.55,outer_radius=1.73,start_angle=a*DEGREES,
                 angle=10.10*DEGREES,stroke_width=0,fill_color=ENDO,fill_opacity=.88).shift(C)
            bm=AnnularSector(inner_radius=1.745,outer_radius=1.855,start_angle=a*DEGREES,
                 angle=10.10*DEGREES,stroke_width=0,fill_color=GBM,fill_opacity=.96).shift(C)
            if damaged:
                en.add_updater(lambda m,dt:m.set_fill(opacity=.88*(1-.95*disruption.get_value())))
                bm.add_updater(lambda m,dt:m.set_fill(opacity=.96*(1-.98*disruption.get_value())))
            endothelium.add(en);basement.add(bm)
        nuclei=VGroup(*[Ellipse(width=.32,height=.135,stroke_width=0,
                      fill_color=ENDO_NUCLEUS,fill_opacity=.78)
                      .rotate((a+90)*DEGREES).move_to(polar(1.64,a)) for a in [25,145,285]])
        fenestrae=VGroup()
        for a in range(0,360,20):
            if min(abs(a-b) for b in [25,145,285])<17:continue
            hole=Ellipse(width=.070,height=.031,stroke_width=0,fill_color=BG,fill_opacity=.7)
            hole.rotate((a+90)*DEGREES).move_to(polar(1.64,a))
            if 230<=a<=260:
                hole.add_updater(lambda m,dt:m.set_fill(opacity=.70*(1-disruption.get_value())))
            fenestrae.add(hole)
        feet=VGroup();slits=VGroup()
        for i in range(28):
            a=i*360/28
            def foot_shape(a=a):
                e=effacement.get_value()
                opacity=.82*(1-.93*disruption.get_value()) if 230<=a<=265 else .82
                foot=RoundedRectangle(width=.335+.165*e,height=.19-.065*e,corner_radius=.065,
                        stroke_color=GOLD,stroke_width=1,fill_color=GOLD,fill_opacity=opacity)
                foot.rotate((a+90)*DEGREES).move_to(polar(1.973,a))
                foot.set_stroke(opacity=max(.05,opacity))
                return foot
            feet.add(always_redraw(foot_shape))
            mid=a+360/56
            slit=Line(polar(1.925,mid-1.0),polar(1.925,mid+1.0),color=TEAL,stroke_width=1.5)
            def update_slit(m,dt,mid=mid):
                intact=1-.88*effacement.get_value()
                if 230<=mid<=270:intact*=1-disruption.get_value()
                m.set_stroke(opacity=.70*intact)
            slit.add_updater(update_slit);slits.add(slit)

        bodies=VGroup()
        for a,offsets in [(62,[-26,0,26]),(171,[-23,0,23])]:
            body_c=polar(2.31,a)
            branches=VGroup()
            for delta in offsets:
                endpoint=polar(1.98,a+delta)
                path=VMobject().start_new_path(body_c)
                path.add_cubic_bezier_curve_to(polar(2.18,a+delta*.30),polar(2.09,a+delta*.8),endpoint)
                path.set_stroke(GOLD,width=10,opacity=.70).set_fill(opacity=0)
                branches.add(path)
            body=VMobject().start_new_path(np.array([-.54,-.16,0]))
            body.add_cubic_bezier_curve_to(np.array([-.69,.03,0]),np.array([-.46,.30,0]),np.array([-.16,.32,0]))
            body.add_cubic_bezier_curve_to(np.array([.18,.43,0]),np.array([.57,.29,0]),np.array([.62,.03,0]))
            body.add_cubic_bezier_curve_to(np.array([.65,-.17,0]),np.array([.19,-.24,0]),np.array([-.10,-.20,0]))
            body.add_cubic_bezier_curve_to(np.array([-.26,-.19,0]),np.array([-.45,-.24,0]),np.array([-.54,-.16,0]))
            body.close_path().set_stroke(GOLD,width=1.2).set_fill(GOLD,opacity=.67)
            body.rotate((a+90)*DEGREES).move_to(body_c)
            nucleus=Ellipse(width=.34,height=.20,stroke_color='#B48E4C',stroke_width=1,
                         fill_color='#B89B65',fill_opacity=.8).rotate((a+90)*DEGREES).move_to(body_c)
            bodies.add(branches,body,nucleus)

        swelling=AnnularSector(inner_radius=1.26,outer_radius=1.56,start_angle=195*DEGREES,
                   angle=94*DEGREES,stroke_width=0,fill_color=ENDO,fill_opacity=0).shift(C)
        swelling.add_updater(lambda m,dt:m.set_fill(opacity=.70*inflammation.get_value()))
        inflammatory_cells=VGroup()
        for pos,s in [(C+np.array([-.67,-.55,0]),1.0),(C+np.array([-.02,-.94,0]),.80)]:
            cell=VGroup(Circle(radius=.245*s,stroke_color=PURPLE,stroke_width=1,
                        fill_color='#6A607F',fill_opacity=.85))
            for x,y in [(-.075,.065),(.067,.017),(-.025,-.09)]:
                cell.add(Ellipse(width=.16*s,height=.105*s,stroke_width=0,
                    fill_color=PURPLE,fill_opacity=.9).rotate(.4).move_to([x*s,y*s,0]))
            cell.shift(pos)
            cell.add_updater(lambda m,dt:m.set_opacity(inflammation.get_value()))
            inflammatory_cells.add(cell)
        mediators=VGroup()
        for i in range(13):
            a=212+(i%5)*11
            p=polar(1.12+.095*(i//5),a)
            dot=Dot(radius=.022,color=PURPLE).move_to(p)
            dot.add_updater(lambda m,dt:m.set_opacity(.85*inflammation.get_value()))
            mediators.add(dot)
        injury_halo=Arc(radius=1.84,start_angle=229*DEGREES,angle=43*DEGREES,
                        color=CORAL,stroke_width=4).shift(C)
        injury_halo.add_updater(lambda m,dt:m.set_stroke(opacity=.65*disruption.get_value()))
        slit_damage=VGroup(*[Line(polar(1.895,a-2),polar(1.895,a+2),color=CORAL,stroke_width=3)
                            for a in [-35,-10,15,40]])
        slit_damage.add_updater(lambda m,dt:m.set_stroke(opacity=.9*effacement.get_value()))
        anatomy=VGroup(lumen,endothelium,basement,nuclei,fenestrae,feet,slits,bodies,
                      swelling,inflammatory_cells,mediators,injury_halo,slit_damage)

        callouts=VGroup(
            leader([polar(2.31,62),[.10,2.45,0],[1.45,2.10,0]]),
            label('Podocyte and foot processes',21,GOLD,[4.12,2.10,0],4.6),
            leader([polar(1.64,8),[.20,.51,0],[1.45,1.02,0]]),
            label('Fenestrated endothelium',21,ENDO,[4.12,1.02,0],4.6),
            leader([polar(1.80,-28),[.25,-.62,0],[1.45,-.05,0]]),
            label('Glomerular basement membrane',20,GBM,[4.12,-.05,0],4.8))
        filtration_label=label('Filtrate',17,MUTED,[-5.50,-1.58,0],1.5)
        legend=VGroup(rbc(.64).move_to([-5.42,-2.64,0]),
                      label('Red cells',17,CORAL,[-4.51,-2.64,0],1.6),
                      Dot(radius=.042,color=TEAL).move_to([-2.94,-2.64,0]),
                      label('Albumin',17,TEAL,[-2.08,-2.64,0],1.55))

        particles=VGroup()
        for i in range(15):
            cell=rbc(.85,angle=(i*.83)%PI)
            def update_rbc(m,dt,i=i):
                y=-1.13+(i%6)*.43
                half=np.sqrt(max(.10,1.40**2-y*y))
                t=(clock.get_value()*.09+i*.381966)%1
                m.move_to(C+np.array([-half+2*half*t,y,0]))
            cell.add_updater(update_rbc);particles.add(cell)
        for i in range(26):
            dot=Dot(radius=.035,color=TEAL)
            def update_albumin(m,dt,i=i):
                a=clock.get_value()*.085+i*2.39996
                r=.33+(i%6)*.18
                m.move_to(C+np.array([r*np.cos(a),r*np.sin(a),0]))
                m.set_opacity(.88-.48*protein_leak.get_value())
            dot.add_updater(update_albumin);particles.add(dot)
        for row,a in enumerate([70,150,290,345]):
            for i in range(5):
                dot=Dot(radius=.016,color=INK)
                def update_filtrate(m,dt,row=row,a=a,offset=i/5):
                    t=(clock.get_value()*(.20+.23*filtration.get_value())+offset)%1
                    m.move_to(polar(1.43+1.10*t,a))
                    m.set_opacity(.43*filtration.get_value() if offset<filtration.get_value() else .015)
                dot.add_updater(update_filtrate);particles.add(dot)
        for i in range(7):
            cell=rbc(.74,angle=i*.73)
            def update_leaked_rbc(m,dt,i=i):
                t=(clock.get_value()*.19+i/7)%1
                a=238+(i%3)*8
                m.move_to(polar(1.28+1.60*t,a))
                m.set_opacity(disruption.get_value()*min(1,(1-t)*6))
            cell.add_updater(update_leaked_rbc);particles.add(cell)
        for row in range(4):
            for i in range(7):
                dot=Dot(radius=.037,color=TEAL)
                def update_leak(m,dt,row=row,offset=i/7):
                    t=(clock.get_value()*.28+offset+row*.07)%1
                    a=(-35+row*25)*(1-inflammation.get_value())+(235+row*8)*inflammation.get_value()
                    m.move_to(polar(1.27+1.65*t,a))
                    m.set_opacity(protein_leak.get_value() if offset<protein_leak.get_value() else .008)
                dot.add_updater(update_leak);particles.add(dot)

        nephritic_heading=label('Nephritic pattern',26,CORAL,[4.12,2.15,0],4.8)
        nephritic_mechanism=label('Glomerular inflammation',20,INK,[4.12,1.48,0],4.8)
        nephritic_facts=VGroup(
            label('Haematuria · Red-cell casts',20,CORAL,[4.12,.85,0],4.8),
            label('GFR ↓  ·  Blood pressure ↑',20,INK,[4.12,.24,0],4.8),
            label('Protein: 1 g/day',20,TEAL,[4.12,-.34,0],4.8))
        tube_label=label('Downstream tubule',17,MUTED,[4.12,-.98,0],3.8)
        tube=RoundedRectangle(width=3.90,height=.82,corner_radius=.24,
                  stroke_color=WALL,stroke_width=2,fill_color=LUMEN,fill_opacity=1).move_to([4.12,-1.65,0])
        cast_matrix=RoundedRectangle(width=2.52,height=.47,corner_radius=.18,
                    stroke_color='#B67986',stroke_width=1,fill_color='#7C4C60',fill_opacity=.38).move_to([4.21,-1.65,0])
        cast_matrix.add_updater(lambda m,dt:m.set_opacity(cast_formation.get_value()))
        cast_cells=VGroup()
        for i in range(7):
            cell=rbc(.76,angle=(i*.9)%PI)
            target=np.array([3.28+(i%4)*.55,-1.80+(i//4)*.28,0])
            def update_cast(m,dt,i=i,target=target):
                p=cast_formation.get_value()
                start=np.array([2.41+i*.035,-1.65+.15*np.sin(i),0])
                m.move_to(start*(1-p)+target*p)
                m.set_opacity(min(1,p*3))
            cell.add_updater(update_cast);cast_cells.add(cell)
        cast_group=VGroup(tube_label,tube,cast_matrix,cast_cells)
        nephrotic_panel=VGroup(
            label('Nephrotic pattern',26,GOLD,[4.12,2.15,0],4.8),
            label('Podocyte / slit-barrier injury',20,INK,[4.12,1.48,0],4.8),
            label('Heavy proteinuria: 5.2 g/day',20,TEAL,[4.12,.85,0],4.8),
            label('Plasma albumin: 20 g/L',20,INK,[4.12,.24,0],4.8),
            label('Oedema',23,INK,[4.12,-.56,0],4.8),
            label('Hyperlipidaemia',21,MUTED,[4.12,-1.18,0],4.8))
        self.play(FadeIn(title),run_time=1)
        self.play(FadeIn(anatomy),FadeIn(callouts),FadeIn(phase),FadeIn(filtration_label),
                  FadeIn(legend),FadeIn(caption),FadeIn(context),run_time=3)
        self.add(particles)
        self.wait(5)
        if review=='healthy':return
        def change(old,text,size=21,color=INK,max_width=12.7):
            return Transform(old,label(text,size,color,old.get_center(),max_width))
        start=self.time
        self.play(FadeOut(callouts),FadeIn(nephritic_heading),FadeIn(nephritic_mechanism),
                  inflammation.animate.set_value(1),
                  change(phase,'Inflammatory injury',23,CORAL,3.6),
                  change(caption,'Inflammatory cells and mediators injure the glomerular capillary.'),
                  change(context,'This illustrates one inflammatory route to a nephritic presentation.',16,MUTED),run_time=4)
        self.wait(5)
        self.play(disruption.animate.set_value(1),protein_leak.animate.set_value(.25),filtration.animate.set_value(.34),
                  FadeIn(nephritic_facts),
                  change(caption,'Barrier disruption lets red cells and protein enter the filtrate.'),
                  change(context,'Inflammation also reduces filtration; salt and water retention favour hypertension.',16,MUTED),run_time=4)
        self.wait(7)
        chapters.append({'id':'nephritic-injury','start':round(start,2),'end':round(self.time,2)})
        start=self.time
        self.play(FadeIn(tube_label),FadeIn(tube),run_time=1.5)
        self.add(cast_matrix,cast_cells)
        self.play(cast_formation.animate.set_value(1),
                  change(caption,'Downstream, red cells become trapped in a tubular cast.'),
                  change(context,'The cast forms in a tubule after red cells have crossed the injured barrier.',16,MUTED),run_time=4)
        self.wait(5)
        chapters.append({'id':'red-cell-casts','start':round(start,2),'end':round(self.time,2)})
        def snapshot():
            copy=VGroup(anatomy.copy(),particles.copy())
            copy.clear_updaters(recursive=True)
            return copy
        nephritic_snapshot=snapshot()
        if review=='nephritic':return
        start=self.time
        # A visible healthy reset separates the two branches of the explanation.
        cast_group.clear_updaters(recursive=True)
        self.play(FadeOut(nephritic_heading),FadeOut(nephritic_mechanism),FadeOut(nephritic_facts),
                  FadeOut(cast_group),inflammation.animate.set_value(0),disruption.animate.set_value(0),
                  protein_leak.animate.set_value(.035),filtration.animate.set_value(.86),
                  FadeIn(callouts),change(phase,'Healthy reference',23,TEAL,3.6),
                  change(caption,'From the healthy barrier, follow a second pattern of injury.'),
                  change(context,'These are separate pathways; clinical features can overlap.',16,MUTED),run_time=3)
        self.wait(3)
        chapters.append({'id':'healthy-reset','start':round(start,2),'end':round(self.time,2)})
        start=self.time
        self.play(FadeOut(callouts),FadeIn(nephrotic_panel[:2]),effacement.animate.set_value(1),
                  change(phase,'Podocyte injury',23,GOLD,3.6),
                  change(caption,'Podocyte foot processes flatten, with slit-barrier dysfunction.'),
                  change(context,'Podocyte injury is a common route to increased protein permeability.',16,MUTED),run_time=4)
        self.wait(6)
        self.play(protein_leak.animate.set_value(.95),FadeIn(nephrotic_panel[2:4]),
                  change(caption,'More albumin crosses the damaged protein barrier into the filtrate.'),
                  change(context,'Heavy urinary protein loss is a defining feature of the nephrotic pattern.',16,MUTED),run_time=3)
        self.wait(8)
        chapters.append({'id':'podocyte-injury-and-protein-loss','start':round(start,2),'end':round(self.time,2)})
        start=self.time
        self.play(FadeIn(nephrotic_panel[4:]),
                  change(caption,'Protein loss lowers plasma albumin; fluid accumulates in tissues.'),
                  change(context,'Low oncotic pressure and renal sodium retention both contribute to oedema.',16,MUTED),run_time=2)
        self.wait(7)
        chapters.append({'id':'nephrotic-clinical-features','start':round(start,2),'end':round(self.time,2)})
        nephrotic_snapshot=snapshot()
        if review=='nephrotic':return

        start=self.time
        anatomy.clear_updaters(recursive=True);particles.clear_updaters(recursive=True)
        self.play(FadeOut(anatomy),FadeOut(particles),FadeOut(nephrotic_panel),FadeOut(phase),
                  FadeOut(legend),FadeOut(filtration_label),
                  change(caption,'Recognise the dominant pattern, then connect it to the underlying injury.'),
                  change(context,'Nephritic and nephrotic features can overlap in the same disease.',16,MUTED),run_time=1.5)
        # Reuse frozen illustrated states for a matched final comparison.
        nephritic_snapshot.scale_to_fit_height(3.10).move_to([-3.48,.65,0])
        nephrotic_snapshot.scale_to_fit_height(3.10).move_to([3.48,.65,0])
        comparison=VGroup(nephritic_snapshot,nephrotic_snapshot,
            label('Nephritic',26,CORAL,[-3.48,2.62,0],4.8),
            label('Nephrotic',26,GOLD,[3.48,2.62,0],4.8),
            label('Haematuria · Red-cell casts',20,CORAL,[-3.48,-1.40,0],5.6),
            label('1 g/day protein · GFR ↓ · BP ↑',19,INK,[-3.48,-1.97,0],5.8),
            label('Heavy proteinuria',20,TEAL,[3.48,-1.40,0],5.6),
            label('5.2 g/day · Albumin 20 g/L',19,INK,[3.48,-1.97,0],5.8),
            label('Oedema · Hyperlipidaemia',18,MUTED,[3.48,-2.48,0],5.8))
        self.play(FadeIn(comparison),run_time=1.5)
        self.wait(8)
        chapters.append({'id':'comparison','start':round(start,2),'end':round(self.time,2)})
        FilePath(__file__).with_name('chapter-times.json').write_text(
            json.dumps({'chapters':chapters,'durationSeconds':round(self.time,2)},indent=2)+'\n')
