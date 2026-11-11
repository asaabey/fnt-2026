"""Sparse-label RAAS animation; schematic anatomy and qualitative ion movement."""
from manim import *
from pathlib import Path
import json
import numpy as np

BG='#10151F'; INK='#EDF3FA'; MUTED='#A4B3C5'; WALL='#5E8EAD'
BLUE='#75B5ED'; GOLD='#F2C66D'; TEAL='#65D4C2'; CORAL='#EC6174'; PURPLE='#BD95ED'


def txt(s, size=23, color=INK, at=None, width=None):
    m=Text(s,font='Avenir Next',font_size=size,color=color,line_spacing=.85)
    if width and m.width>width:m.scale_to_fit_width(width)
    if at is not None:m.move_to(at)
    return m


def arrow(a,b,color=MUTED):
    return Arrow(a,b,buff=.05,color=color,stroke_width=2,tip_length=.14,max_tip_length_to_length_ratio=.30)


def kidney(at,scale=1):
    # Reniform outline, medial hilum opening to the right.
    pts=[[-.05,.68,0],[-.54,.61,0],[-.72,.14,0],[-.58,-.51,0],[-.16,-.68,0],
         [.24,-.50,0],[.26,-.23,0],[.03,-.06,0],[.24,.16,0],[.27,.46,0],[-.05,.68,0]]
    shape=VMobject(stroke_color=WALL,stroke_width=2,fill_color=WALL,fill_opacity=.16)
    shape.set_points_smoothly(pts)
    return VGroup(shape).scale(scale).move_to(at)


def liver(at):
    p=VMobject(stroke_color=CORAL,stroke_width=2,fill_color=CORAL,fill_opacity=.13)
    p.set_points_smoothly([[-.9,.27,0],[-.47,.51,0],[.51,.41,0],[.88,.12,0],
                          [.45,-.12,0],[-.35,-.48,0],[-.83,-.31,0],[-.9,.27,0]])
    return VGroup(p).move_to(at)


def lungs(at):
    left=Ellipse(width=.67,height=1.03,stroke_color=BLUE,stroke_width=2,
                 fill_color=BLUE,fill_opacity=.12).move_to([-.43,0,0]).rotate(-.12)
    right=left.copy().rotate(.24).move_to([.43,0,0])
    bronchi=VGroup(Line([0,.68,0],[0,.10,0]),Line([0,.10,0],[-.35,-.10,0]),
                    Line([0,.10,0],[.35,-.10,0])).set_stroke(MUTED,2)
    return VGroup(left,right,bronchi).move_to(at)


def adrenal(at):
    k=kidney([0,-.16,0],.70)
    cortex=Polygon([-.55,.55,0],[.04,.88,0],[.53,.52,0],stroke_color=PURPLE,
                   stroke_width=5,fill_color=PURPLE,fill_opacity=.12)
    return VGroup(k,cortex).move_to(at)


class RAAS(Scene):
    def construct(self):
        self.camera.background_color=BG
        chapters=[]
        title=txt('Renin → Angiotensin II → Aldosterone',29,at=[0,3.45,0])
        self.play(FadeIn(title),run_time=1)

        # Juxtaglomerular apparatus: macula densa is distinct from renin cells.
        capsule=Circle(radius=.96,color=WALL,stroke_width=1.7).move_to([-.55,.15,0])
        loops=VGroup(*[Circle(radius=.39,color=CORAL,stroke_width=1.5)
                      .move_to([-.88+.37*(i%3),-.08+.38*(i//3),0]) for i in range(6)])
        afferent=VGroup(Line([-5.15,.48,0],[-1.43,.48,0]),
                         Line([-5.15,.12,0],[-1.43,.12,0])).set_stroke(CORAL,2.5)
        inflow=arrow([-4.8,.30,0],[-3.8,.30,0],CORAL)
        tubule=VGroup(Line([-4.55,1.32,0],[-1.70,1.32,0]),
                      Line([-4.55,1.75,0],[-1.70,1.75,0])).set_stroke(WALL,2)
        md=VGroup(*[RoundedRectangle(width=.20,height=.30,corner_radius=.03,
                   stroke_color=TEAL,fill_color=TEAL,fill_opacity=.35,stroke_width=1)
                   .move_to([-2.97+i*.22,1.30,0]) for i in range(5)])
        jg=VGroup(*[Circle(radius=.105,stroke_color=GOLD,fill_color=GOLD,fill_opacity=.55)
                    .move_to([-2.95+i*.24,.59,0]) for i in range(4)])
        na=VGroup(*[Dot([-4.25+i*.33,1.53,0],radius=.036,color=GOLD) for i in range(3)])
        labels=VGroup(txt('↓ Perfusion',23,CORAL,[-4.15,-.37,0]),
                      txt('β₁ ↑',24,BLUE,[-4.05,-1.43,0]),
                      txt('NaCl ↓',23,TEAL,[-3.85,2.16,0]),
                      txt('Macula densa',20,TEAL,[-.14,2.06,0]),
                      txt('JG granular cells',20,GOLD,[-1.77,-1.28,0]))
        leaders=VGroup(Line([-.89,1.91,0],[-2.3,1.49,0],color=TEAL,stroke_width=1),
                       Line([-1.83,-1.04,0],[-2.48,.44,0],color=GOLD,stroke_width=1))
        signals=VGroup(arrow([-3.56,-1.25,0],[-2.85,.43,0],BLUE),
                       arrow([-2.50,1.08,0],[-2.50,.77,0],TEAL))
        renin=txt('Renin',30,GOLD,[3.35,.37,0])
        release=arrow([-2.00,.57,0],[2.50,.37,0],GOLD)
        kidney_scene=VGroup(capsule,loops,afferent,inflow,tubule,md,jg,na,labels,leaders,signals,renin,release)
        self.play(FadeIn(VGroup(capsule,loops,afferent,inflow,tubule,md,jg,na)),run_time=1.5)
        self.play(FadeIn(labels),Create(leaders),Create(signals),run_time=1.5)
        self.play(Create(release),FadeIn(renin),Indicate(jg,color=GOLD),run_time=2)
        self.wait(3)
        chapters.append({'id':'renin-release','start':0,'end':round(self.time,2)})

        # Circulating cascade. Enzymes sit ABOVE reaction arrows, not in the substrate chain.
        start=self.time
        self.play(FadeOut(kidney_scene),run_time=.8)
        li=liver([-4.85,2.0,0]); lu=lungs([1.05,2.0,0]); ki=kidney([-2.75,-1.22,0],.78)
        ad=adrenal([3.45,-1.35,0])
        ag=txt('Angiotensinogen',25,at=[-4.85,.30,0],width=3.1)
        ai=txt('Angiotensin I',25,at=[-.80,.30,0],width=2.8)
        aii=txt('Angiotensin II',27,CORAL,[3.35,.30,0],2.9)
        r=txt('Renin',22,GOLD,[-2.8,.85,0])
        ace=txt('ACE',22,BLUE,[1.18,.85,0])
        first=arrow([-3.25,.30,0],[-2.13,.30,0],GOLD)
        second=arrow([.51,.30,0],[1.94,.30,0],BLUE)
        cascade=VGroup(li,lu,ki,ad,ag,ai,aii,r,ace,first,second)
        liver_label=txt('Liver',18,MUTED,[-4.85,2.86,0])
        kidney_label=txt('Kidney',18,MUTED,[-2.75,-2.0,0])
        lung_label=txt('Vascular endothelium',17,MUTED,[1.05,2.92,0])
        adrenal_label=txt('Adrenal cortex',19,PURPLE,[3.45,-2.33,0])
        zone=txt('Zona glomerulosa',16,MUTED,[3.45,-2.68,0])
        organ_labels=VGroup(liver_label,kidney_label,lung_label,adrenal_label,zone)
        liver_arrow=arrow([-4.85,1.48,0],[-4.85,.68,0],CORAL)
        renin_arrow=arrow([-2.75,-.56,0],[-2.75,.02,0],GOLD)
        ace_arrow=arrow([1.05,1.33,0],[1.12,1.05,0],BLUE)
        aldo_arrow=arrow([3.35,-.10,0],[3.35,-.60,0],PURPLE)
        self.play(FadeIn(li),FadeIn(liver_label),Create(liver_arrow),FadeIn(ag),
                  FadeIn(ki),FadeIn(kidney_label),run_time=1.5)
        self.play(Create(renin_arrow),FadeIn(r),Create(first),FadeIn(ai),run_time=2)
        self.play(FadeIn(lu),FadeIn(lung_label),Create(ace_arrow),FadeIn(ace),
                  Create(second),FadeIn(aii),run_time=2)
        self.play(Create(aldo_arrow),FadeIn(ad),FadeIn(adrenal_label),FadeIn(zone),run_time=1.5)
        aldo=txt('Aldosterone',27,PURPLE,[3.45,-3.25,0])
        self.play(FadeIn(aldo),Indicate(ad[1],color=PURPLE),run_time=1.5)
        self.wait(2)
        # Direct Ang II effects remain separate from the aldosterone branch.
        vessel=VGroup(Line([-.84,-1.10,0],[.68,-1.10,0]),
                      Line([-.84,-1.65,0],[.68,-1.65,0])).set_stroke(CORAL,2)
        constricted=VGroup(Line([-.84,-1.22,0],[.68,-1.22,0]),
                          Line([-.84,-1.53,0],[.68,-1.53,0])).set_stroke(CORAL,2)
        branch=arrow([2.10,.05,0],[.34,-.91,0],CORAL)
        constriction_label=txt('Vasoconstriction',19,CORAL,[-.1,-1.99,0])
        prox=txt('Proximal Na⁺ reabsorption ↑',19,GOLD,[-.1,-2.65,0],4.1)
        self.play(Create(branch),FadeIn(vessel),FadeIn(constriction_label),run_time=1)
        self.play(Transform(vessel,constricted),FadeIn(prox),run_time=1.5)
        self.wait(2.5)
        chapters.append({'id':'angiotensin-and-aldosterone','start':start,'end':round(self.time,2)})

        overview=VGroup(cascade,organ_labels,liver_arrow,renin_arrow,ace_arrow,aldo_arrow,aldo,
                        vessel,branch,constriction_label,prox)
        start=self.time
        self.play(FadeOut(overview),run_time=.8)
        # Principal cell: urine at left; interstitial/blood compartment at right.
        cell=RoundedRectangle(width=3.7,height=3.50,corner_radius=.12,
                              stroke_color=WALL,stroke_width=2,fill_color=WALL,fill_opacity=.10)
        cell.move_to([0,-.1,0])
        cell_name=txt('Principal cell',23,at=[0,2.03,0])
        urine_label=txt('Tubular lumen',23,MUTED,[-4.6,1.93,0])
        blood_label=txt('Blood',23,MUTED,[4.70,1.93,0])
        apical=txt('ENaC ↑',23,GOLD,[-2.60,1.12,0])
        pump_label=txt('Na⁺/K⁺-ATPase ↑',22,GOLD,[3.70,.92,0],4.2)
        enac=RoundedRectangle(width=.22,height=.48,corner_radius=.04,
                              stroke_color=GOLD,fill_color=BG,fill_opacity=1).move_to([-1.85,.5,0])
        pump=RoundedRectangle(width=.32,height=1.20,corner_radius=.06,
                              stroke_color=GOLD,fill_color=BG,fill_opacity=1).move_to([1.85,.10,0])
        kchannel=RoundedRectangle(width=.22,height=.40,corner_radius=.04,
                                 stroke_color=TEAL,fill_color=BG,fill_opacity=1).move_to([-1.85,-1.2,0])
        incoming=arrow([-4.95,.5,0],[-.45,.5,0],GOLD)
        outgoing=arrow([.40,.5,0],[5.12,.5,0],GOLD)
        kentry=arrow([4.85,-.30,0],[.30,-.30,0],TEAL)
        kexit=arrow([-.30,-1.20,0],[-5.05,-1.20,0],TEAL)
        nalabel=txt('Na⁺',24,GOLD,[-4.7,.95,0])
        klabel=txt('K⁺',24,TEAL,[-4.7,-.76,0])
        minus=txt('−',29,TEAL,[-2.70,-.38,0])
        aldo_cell=txt('Aldosterone',26,PURPLE,[0,2.78,0])
        stimulus=arrow([0,2.51,0],[0,2.20,0],PURPLE)
        self.play(FadeIn(cell),FadeIn(cell_name),FadeIn(urine_label),FadeIn(blood_label),
                  FadeIn(enac),FadeIn(pump),FadeIn(kchannel),FadeIn(aldo_cell),Create(stimulus),run_time=1.5)
        self.play(FadeIn(apical),FadeIn(pump_label),Create(incoming),Create(outgoing),
                  FadeIn(nalabel),run_time=1.5)
        self.play(Create(kentry),Create(kexit),FadeIn(klabel),FadeIn(minus),run_time=1.5)
        # Staged particle trajectories show the pump taking K into the cell,
        # followed by its secretion through an apical K channel.
        for _ in range(2):
            na1=Dot([-4.8,.5,0],radius=.065,color=GOLD)
            na2=Dot([.30,.5,0],radius=.065,color=GOLD)
            potassium=Dot([4.7,-.30,0],radius=.065,color=TEAL)
            self.add(na1,na2,potassium)
            self.play(na1.animate.move_to([-.35,.5,0]),na2.animate.move_to([4.9,.5,0]),
                      potassium.animate.move_to([.15,-.30,0]),run_time=1.15,rate_func=linear)
            self.play(potassium.animate.move_to([-.45,-1.20,0]),FadeOut(na1),FadeOut(na2),run_time=.45)
            self.play(potassium.animate.move_to([-4.8,-1.20,0]),run_time=1,rate_func=linear)
            self.remove(potassium)
        net=txt('Na⁺ retained     ·     K⁺ excreted',26,at=[0,-2.72,0])
        self.play(FadeIn(net),run_time=.7)
        self.wait(2.5)
        chapters.append({'id':'principal-cell','start':start,'end':round(self.time,2)})

        start=self.time
        all_cell=VGroup(cell,cell_name,urine_label,blood_label,enac,pump,kchannel,aldo_cell,stimulus,
                        apical,pump_label,incoming,outgoing,kentry,kexit,nalabel,klabel,minus,net)
        self.play(FadeOut(all_cell),run_time=.8)
        # Regulation: normal feedback, then autonomous adrenal secretion.
        k=kidney([-4.3,.6,0],1.1)
        ad2=adrenal([3.7,.6,0])
        ren=txt('Renin ↑',26,GOLD,[-4.3,-.68,0])
        ang=txt('Angiotensin II ↑',25,CORAL,[-.4,.55,0])
        ald=txt('Aldosterone ↑',26,PURPLE,[3.7,-.75,0])
        links=VGroup(arrow([-3.3,.6,0],[-2.05,.6,0],GOLD),
                     arrow([1.25,.6,0],[2.85,.6,0],CORAL))
        volume=txt('Volume & BP restored',26,at=[-.30,-2.13,0])
        feedback=CurvedArrow([-2.5,-2.13,0],[-4.3,-1.05,0],angle=-.6,
                             color=TEAL,stroke_width=2,tip_length=.13)
        potassium_drive=txt('K⁺',23,TEAL,[5.15,2.04,0])
        potassium_arrow=arrow([4.95,1.78,0],[4.10,1.35,0],TEAL)
        self.play(FadeIn(k),FadeIn(ad2),FadeIn(ren),FadeIn(ang),FadeIn(ald),Create(links),
                  FadeIn(potassium_drive),Create(potassium_arrow),run_time=1.5)
        self.play(FadeIn(volume),Create(feedback),run_time=1)
        self.play(Transform(ren,txt('Renin ↓',26,GOLD,ren.get_center())),
                  Transform(ang,txt('Angiotensin II ↓',25,CORAL,ang.get_center())),
                  Transform(ald,txt('Aldosterone ↓',26,PURPLE,ald.get_center())),run_time=1.5)
        self.wait(2)
        chapters.append({'id':'negative-feedback','start':start,'end':round(self.time,2)})

        start=self.time
        autonomous=txt('Autonomous aldosterone',26,PURPLE,[0,2.50,0])
        outcome=txt('BP ↑     ·     Plasma K⁺ ↓',28,at=[0,-2.13,0])
        self.play(FadeOut(feedback),FadeOut(potassium_drive),FadeOut(potassium_arrow),
                  FadeIn(autonomous),links.animate.set_opacity(.20),
                  Transform(volume,outcome),
                  Transform(ald,txt('Aldosterone ↑',26,PURPLE,ald.get_center())),
                  Indicate(ad2[1],color=PURPLE),run_time=1.5)
        self.wait(4)
        chapters.append({'id':'autonomous-aldosterone','start':start,'end':round(self.time,2)})
        Path(__file__).with_name('chapter-times.json').write_text(json.dumps(
            {'durationSeconds':round(self.time,2),'chapters':chapters},indent=2)+'\n')
