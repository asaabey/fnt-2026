"""One persistent nephron: eight diuretic mechanisms, with local target insets.
Schematic anatomy and qualitative transport; Manim Community 0.22.1.
"""
from manim import *
from pathlib import Path
import json
import os

BG='#10151F'; INK='#EDF3FA'; MUTED='#A4B3C5'; WALL='#6485A3'
TEAL='#65D4C2'; GOLD='#F2C66D'; CORAL='#EC6174'; PURPLE='#BD95ED'; BLUE='#75B5ED'
CASES=[
 dict(id='osmotic',drug='Mannitol',family='Osmotic diuretic',site='Proximal tubule + descending limb',target='Luminal osmoles',line='Retains water in tubular fluid',effect='Osmotic diuresis',note='Acts in water-permeable segments; no receptor blockade.',segments=['pct','desc'],symbol='Osmole',color=PURPLE),
 dict(id='carbonic-anhydrase',drug='Acetazolamide',family='Carbonic anhydrase inhibitor',site='Proximal tubule',target='Carbonic anhydrase',line='Less NaHCO₃ reabsorption',effect='Bicarbonaturia + natriuresis',note='The target is an enzyme, not a sodium channel.',segments=['pct'],symbol='CA',color=BLUE),
 dict(id='sglt2',drug='SGLT2 inhibitors',family='Example: empagliflozin',site='Proximal tubule',target='Apical SGLT2',line='Less Na⁺–glucose cotransport',effect='Glycosuria → osmotic diuresis',note='Also alters sodium handling; natriuresis varies over time.',segments=['pct'],symbol='SGLT2',color=GOLD),
 dict(id='loop',drug='Loop diuretics',family='Furosemide · bumetanide',site='Thick ascending limb',target='Apical NKCC2',line='Less Na⁺ / K⁺ / 2Cl⁻ reabsorption',effect='Natriuresis + weaker medullary gradient',note='This limb stays water-impermeable; concentrating capacity falls.',segments=['tal'],symbol='NKCC2',color=CORAL),
 dict(id='thiazide',drug='Thiazide / thiazide-like',family='Hydrochlorothiazide · indapamide',site='Distal convoluted tubule',target='Apical NCC',line='Less Na⁺–Cl⁻ reabsorption',effect='Natriuresis',note='NCC is distinct from NKCC2 in the loop.',segments=['dct'],symbol='NCC',color=GOLD),
 dict(id='mineralocorticoid',drug='Spironolactone · eplerenone',family='Mineralocorticoid receptor antagonists',site='Aldosterone-sensitive distal nephron',target='Intracellular MR',line='Less aldosterone-driven Na⁺ transport',effect='Natriuresis + potassium sparing',note='MR blockade changes transport regulation; it does not plug ENaC.',segments=['cnt','cdtop'],symbol='MR',color=PURPLE),
 dict(id='enac',drug='Amiloride · triamterene',family='ENaC blockers',site='Aldosterone-sensitive distal nephron',target='Apical ENaC',line='Directly reduces Na⁺ entry',effect='Natriuresis + potassium sparing',note='Less electrogenic Na⁺ uptake reduces the drive for K⁺ secretion.',segments=['cnt','cdtop'],symbol='ENaC',color=TEAL),
 dict(id='v2',drug='Tolvaptan',family='Vasopressin V₂ receptor antagonist',site='Collecting duct',target='Basolateral V₂ receptor',line='Less signalling for apical AQP2 insertion',effect='Aquaresis: predominantly water loss',note='V₂ is the direct target; AQP2 is the downstream water channel.',segments=['cdtop','cdbottom'],symbol='V₂',color=BLUE),
]

def text(s,size=22,color=INK,at=None,width=None):
    m=Text(s,font='Avenir Next',font_size=size,color=color,line_spacing=.85)
    if width and m.width>width:m.scale_to_fit_width(width)
    if at is not None:m.move_to(at)
    return m

def linepath(points,color=WALL,width=17):
    return VMobject().set_points_smoothly(points).set_stroke(color,width=width)

def arr(a,b,color=GOLD):
    return Arrow(a,b,buff=.03,color=color,stroke_width=2.5,tip_length=.14,max_tip_length_to_length_ratio=.24)

def block(at,color=CORAL):
    x,y=at
    return VGroup(Line([x-.12,y-.20,0],[x+.12,y+.20,0],color=color,stroke_width=4))

def gate(at,tag,color=GOLD):
    x,y=at
    return VGroup(RoundedRectangle(width=.27,height=.40,corner_radius=.07,stroke_color=color,fill_color=BG,fill_opacity=1,stroke_width=2).move_to([x,y,0]))

class DiureticsNephron(Scene):
    def construct(self):
        self.camera.background_color=BG
        title=text('Diuretics: one nephron, different targets',32,at=[0,3.5,0],width=13)
        split=Line([1.47,-2.85,0],[1.47,2.95,0],color='#334253',stroke_width=1)
        cortex=Rectangle(width=7.95,height=2.73,stroke_width=0,fill_color='#192330',fill_opacity=.70).move_to([-2.76,1.48,0])
        medulla=Rectangle(width=7.95,height=2.85,stroke_width=0,fill_color='#15252B',fill_opacity=.70).move_to([-2.76,-1.32,0])
        boundary=DashedLine([-6.7,.1,0],[1.18,.1,0],color='#41576A',stroke_width=1,dash_length=.09)
        region=VGroup(text('CORTEX',13,MUTED,[-6.13,.34,0]),text('MEDULLA',13,MUTED,[-6.03,-.15,0]))
        geometry={
         'pct':[[-5.12,2.0,0],[-4.85,2.0,0],[-4.82,1.44,0],[-4.26,1.43,0],[-4.12,2.12,0],[-3.53,2.10,0],[-3.65,1.38,0],[-3.1,1.2,0]],
         'desc':[[-3.1,1.2,0],[-3.1,.3,0],[-3.1,-.85,0],[-3.1,-2.0,0]],
         'bend':[[-3.1,-2.0,0],[-3.0,-2.5,0],[-2.3,-2.68,0],[-1.55,-2.5,0],[-1.45,-2.0,0]],
         'thin':[[-1.45,-2.0,0],[-1.45,-1.15,0]],
         'tal':[[-1.45,-1.15,0],[-1.45,0,0],[-1.45,1.25,0]],
         'dct':[[-1.45,1.25,0],[-1.65,2.20,0],[-1.0,2.35,0],[-.8,1.80,0],[-.23,1.9,0],[-.22,2.45,0],[.34,2.4,0],[.3,1.4,0]],
         'cnt':[[.3,1.4,0],[.63,1.24,0],[.65,.85,0]],
         'cdtop':[[.65,.85,0],[.65,.1,0],[.65,-.55,0]],
         'cdbottom':[[.65,-.55,0],[.65,-1.65,0],[.65,-2.65,0]],
        }
        segments={k:linepath(v,width=12 if k in ['desc','bend','thin'] else 19) for k,v in geometry.items()}
        lumens=VGroup(*[linepath(v,color='#142332',width=5 if k in ['desc','bend','thin'] else 9) for k,v in geometry.items()])
        capsule=Circle(radius=.56,stroke_color=WALL,stroke_width=2).move_to([-5.69,2,0])
        tuft=VGroup(*[Circle(radius=.19,color=CORAL,stroke_width=2).move_to([-5.9+.22*(i%3),1.87+.23*(i//3),0]) for i in range(6)])
        inlet=Line([-6.65,2.15,0],[-6.14,2.15,0],color=CORAL,stroke_width=6)
        outlet=Line([-6.65,1.85,0],[-6.14,1.85,0],color=CORAL,stroke_width=4)
        names=VGroup(text('Glomerulus',17,MUTED,[-5.76,2.8,0]),text('Proximal tubule',18,INK,[-3.92,2.8,0],2.2),text('Distal convoluted\ntubule',17,INK,[-.48,2.98,0],2.2),text('Descending\nlimb',16,MUTED,[-4.08,-.85,0],1.6),text('Thick\nascending\nlimb',16,INK,[-2.23,.68,0],1.4),text('Thin limb',13,MUTED,[-2.27,-1.8,0],1.2),text('Collecting\nduct',17,INK,[-.18,-1.05,0],1.45))
        sites=VGroup(text('Site I',12,MUTED,[-3.95,2.49,0]),text('Site II',12,MUTED,[-2.22,-.10,0]),text('Site III',12,MUTED,[-.55,2.54,0]),text('Site IV',12,MUTED,[-.08,.83,0]))
        flowarrows=VGroup(arr([-3.1,.4,0],[-3.1,-.05,0],MUTED),arr([-1.45,-.7,0],[-1.45,-.22,0],MUTED),arr([.65,-1.85,0],[.65,-2.35,0],MUTED))
        flowarrows.set_opacity(.8)
        footer=text('Follow the segment → identify the target → predict the effect.',21,at=[0,-3.3,0],width=13)
        self.add(cortex,medulla,boundary,region)
        self.play(FadeIn(title),FadeIn(split),FadeIn(capsule),FadeIn(tuft),FadeIn(inlet),FadeIn(outlet),*[Create(m) for m in segments.values()],FadeIn(lumens),run_time=1.6)
        self.play(FadeIn(names),FadeIn(sites),FadeIn(flowarrows),FadeIn(footer),run_time=1)
        overview=text('Enzyme · cotransporters\nchannels · receptors\n\nOne shared nephron map',25,at=[4.13,.6,0],width=4.9)
        self.play(FadeIn(overview),run_time=.6);self.wait(3)
        self.play(FadeOut(overview),run_time=.5)
        chapters=[]
        selected=os.environ.get('DIURETIC_REVIEW')
        cases=[c for c in CASES if not selected or c['id']==selected]
        for c in cases:
            start=self.time
            detail=self.detail(c)
            for mark in detail.block_marks:mark.set_opacity(0)
            for flux in detail.flux_arrows:flux.set_opacity(1)
            if detail.aqp2 is not None:detail.aqp2.move_to([3.04,-.14,0])
            colors=[m.animate.set_stroke(c['color'] if k in c['segments'] else WALL,opacity=1 if k in c['segments'] else .48) for k,m in segments.items()]
            self.play(*colors,FadeIn(detail),Transform(footer,text(c['note'],19,MUTED,[0,-3.3,0],13)),run_time=.8)
            # Transport change is qualitative, independent for every drug class.
            if c['id']=='osmotic':
                osmoles=VGroup(*[Dot(segments['pct'].point_from_proportion(.10+.17*i),radius=.035,color=PURPLE) for i in range(5)],*[Dot(segments['desc'].point_from_proportion(.30+.16*i),radius=.035,color=PURPLE) for i in range(4)])
                self.play(FadeIn(osmoles),*[m.animate.set_opacity(1) for m in detail.block_marks],*[m.animate.set_opacity(.25) for m in detail.flux_arrows],run_time=.6);self.wait(1.5);self.play(*[Indicate(dot,color=PURPLE,scale_factor=1.4) for dot in osmoles],run_time=1);self.wait(5.5)
                self.play(FadeOut(osmoles),run_time=.4)
            else:
                anims=[Indicate(detail.target_icon,color=c['color'],scale_factor=1.12),*[m.animate.set_opacity(1) for m in detail.block_marks],*[m.animate.set_opacity(.3) for m in detail.flux_arrows]]
                if detail.aqp2 is not None:anims.append(detail.aqp2.animate.move_to([3.79,-.14,0]))
                self.play(*anims,run_time=1)
                self.wait(7.6)
            chapters.append(dict(id=c['id'],start=round(start,2),end=round(self.time,2),drug=c['drug'],target=c['target']))
            if selected:return
            self.play(FadeOut(detail),run_time=.4)
        self.play(*[m.animate.set_stroke(WALL,opacity=1) for m in segments.values()],Transform(footer,text('Natriuresis: Na⁺ excretion.   Aquaresis: predominantly water excretion.',20,INK,[0,-3.3,0],13)),run_time=.7)
        summary=self.summary()
        self.play(FadeIn(summary),run_time=.8);self.wait(10)
        chapters.append(dict(id='summary',start=round(self.time-10.8,2),end=round(self.time,2)))
        Path(__file__).with_name('chapter-times.json').write_text(json.dumps(dict(durationSeconds=round(self.time,2),chapters=chapters),indent=2)+'\n')

    def detail(self,c):
        color=c['color']; g=VGroup(); bmarks=[]; fluxes=[]; aqp2=None
        def inhibition(at):
            m=block(at);bmarks.append(m);return m
        def flux(a,b,color):
            m=arr(a,b,color);fluxes.append(m);return m
        g.add(text(c['drug'],25,color,[4.12,2.69,0],5),text(c['family'],16,MUTED,[4.12,2.24,0],5),text(c['site'],17,INK,[4.12,1.83,0],5))
        # All cell insets keep luminal/apical left and interstitial/basolateral right.
        cell=RoundedRectangle(width=2.16,height=1.62,corner_radius=.12,stroke_color=WALL,stroke_width=1.3,fill_color='#203042',fill_opacity=.50).move_to([4.12,.32,0])
        g.add(cell,text('Tubular fluid',13,MUTED,[2.37,1.23,0],1.45),text('Cell',13,MUTED,[4.12,1.23,0]),text('Interstitium',13,MUTED,[5.92,1.23,0],1.45))
        if c['id']=='osmotic':
            icon=VGroup(*[Dot([2.25+.20*(i%3),.38+.22*(i//3),0],radius=.055,color=color) for i in range(6)])
            g.add(icon,text('Osmoles',14,color,[2.45,-.18,0]),text('H₂O',19,TEAL,[2.44,-.64,0]))
            water=flux([2.53,.05,0],[4.35,.05,0],TEAL).set_opacity(.25);g.add(water)
        elif c['id']=='carbonic-anhydrase':
            icon=VGroup(Circle(radius=.27,stroke_color=color,fill_color=BG,fill_opacity=1).move_to([3.15,.34,0]),text('CA',17,color,[3.15,.34,0]))
            g.add(icon,inhibition((3.15,.34)),flux([2.12,-.10,0],[4.35,-.10,0],GOLD).set_opacity(.3),text('NaHCO₃',16,GOLD,[4.13,.57,0]))
        elif c['id']=='mineralocorticoid':
            icon=VGroup(Circle(radius=.28,stroke_color=color,fill_color=BG,fill_opacity=1).move_to([4.12,.23,0]),text('MR',17,color,[4.12,.23,0]))
            g.add(icon,arr([6.25,.23,0],[4.48,.23,0],PURPLE),text('Aldosterone',13,PURPLE,[5.86,.66,0],1.5),inhibition((4.65,.23)),gate((3.04,.51),'ENaC',TEAL),text('ENaC',12,TEAL,[3.26,.91,0]),flux([2.2,.51,0],[3.81,.51,0],GOLD).set_opacity(.30),flux([3.82,-.24,0],[2.2,-.24,0],TEAL).set_opacity(.30),text('Na⁺',14,GOLD,[2.29,.82,0]),text('K⁺',14,TEAL,[2.3,-.53,0]))
        elif c['id']=='v2':
            icon=VGroup(gate((5.2,.44),'V2',color),text('V₂',14,color,[4.88,.77,0]))
            aqp2=gate((3.79,-.14),'AQP2',TEAL)
            g.add(icon,arr([6.35,.44,0],[5.37,.44,0],BLUE),text('ADH',14,BLUE,[6.03,.79,0]),inhibition((5.55,.44)),DashedLine([4.93,.43,0],[3.78,.04,0],color=MUTED,stroke_width=1.4),Circle(radius=.25,color=TEAL,stroke_width=1.5).move_to([3.79,-.14,0]),aqp2,text('AQP2',12,TEAL,[3.81,-.60,0]),text('Less apical insertion',13,TEAL,[4.18,-.95,0],4.7))
        else:
            icon=gate((3.04,.35),c['symbol'],color)
            cargo={'sglt2':'Na⁺ + glucose','loop':'Na⁺ + K⁺ + 2Cl⁻','thiazide':'Na⁺ + Cl⁻','enac':'Na⁺'}[c['id']]
            g.add(icon,text(c['symbol'],16,color,[3.86,.79,0],2.2),flux([2.1,.35,0],[4.43,.35,0],GOLD).set_opacity(.30),inhibition((3.04,.35)),text(cargo,15,GOLD,[4.16,-.18,0],2.6))
            if c['id']=='enac':g.add(flux([4.25,-.28,0],[2.15,-.28,0],TEAL).set_opacity(.3),text('K⁺ secretion ↓',13,TEAL,[4.11,-.77,0],4.6))
        target_y=-1.25 if c['id']=='v2' else -1.04
        g.add(text(c['target'],22,color,[4.12,target_y,0],4.9),text(c['line'],19,INK,[4.12,-1.65,0],4.95),text(c['effect'],20,color,[4.12,-2.23,0],4.95))
        g.target_icon=icon; g.block_marks=bmarks; g.flux_arrows=fluxes; g.aqp2=aqp2
        return g

    def summary(self):
        rows=[('Mannitol','Luminal osmoles'),('Acetazolamide','Carbonic anhydrase'),('SGLT2 inhibitors','SGLT2'),('Loop diuretics','NKCC2'),('Thiazides','NCC'),('Spironolactone','MR'),('Amiloride','ENaC'),('Tolvaptan','V₂ → AQP2')]
        g=VGroup(text('Site + molecular target',25,at=[4.12,2.66,0],width=4.9))
        for i,(drug,target) in enumerate(rows):
            y=1.98-i*.48
            a=text(drug,17,INK,width=2.7);a.move_to([1.78+a.width/2,y,0])
            b=text(target,17,CASES[i]['color'],width=2.1);b.move_to([6.55-b.width/2,y,0])
            g.add(a,b)
        g.add(text('Same nephron. Different mechanisms.',17,MUTED,[4.12,-2.53,0],4.9))
        return g
