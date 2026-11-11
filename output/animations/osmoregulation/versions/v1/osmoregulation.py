"""Captioned osmoregulation teaching animation; all response curves schematic."""
from manim import *
from pathlib import Path
import json
import numpy as np

BG = '#10151F'
INK = '#EDF3FA'
MUTED = '#A4B3C5'
BLUE = '#75B5ED'
ORANGE = '#F2AB66'
PURPLE = '#BD95ED'
TEAL = '#65D4C2'
GOLD = '#F2C66D'
TRACK = '#2A3444'


def text(s, size=22, color=INK, at=None, width=None):
    m = Text(s, font='Avenir Next', font_size=size, color=color)
    if width and m.width > width:
        m.scale_to_fit_width(width)
    if at is not None:
        m.move_to(at)
    return m


def avp(x):
    return .35 + .55 * max(0, x - 280)


def urine(x):
    t = np.clip((x - 280) / 13, 0, 1)
    return 80 + 1120 * (3*t*t - 2*t*t*t)


def thirst(x):
    return max(0, (x - 290) / 6)


class Osmoregulation(Scene):
    def construct(self):
        self.camera.background_color = BG
        osm = ValueTracker(278)
        revealed = ValueTracker(278.02)
        self.add(osm, revealed)
        chapters = []

        title = text('Water balance defends plasma sodium concentration', 31).to_edge(UP, buff=.28)
        subtitle = text('Vasopressin conserves water. Thirst replaces water.', 22, MUTED, [0, 2.97, 0])
        stage = text('Start at low plasma osmolality', 21, TEAL, [0, 2.43, 0])
        self.play(FadeIn(title), FadeIn(subtitle), FadeIn(stage), run_time=1.5)

        # Three independent response scales, one shared osmolality coordinate.
        axes = []
        plot_group = VGroup()
        specs = [
            ('Vasopressin', 'ng/L', BLUE, [0, 10, 5], avp, 1.60),
            ('Urine osmolality', 'mOsm/kg H₂O', ORANGE, [0, 1200, 600], urine, .00),
            ('Thirst', 'relative intensity', PURPLE, [0, 1, .5], thirst, -1.60),
        ]
        for name, unit, color, yrange, fn, cy in specs:
            ax = Axes(x_range=[278, 298, 2], y_range=yrange,
                      x_length=6.2, y_length=1.0, tips=False,
                      axis_config={'color': MUTED, 'stroke_width': 1.2,
                                   'include_ticks': False})
            ax.move_to([-1.80, cy, 0])
            axes.append(ax)
            name_label = text(name.replace('Urine osmolality', 'Urine\nosmolality'), 18, color, [-6.08, cy+.19, 0], 1.63)
            unit_label = text(unit, 12, MUTED, [-6.08, cy-.27, 0], 1.63)
            plot_group.add(ax, name_label, unit_label)
            # Only endpoint scale labels are needed: avoid visual clutter.
            for v in [yrange[0], yrange[1]]:
                lab = text(str(v), 14, MUTED)
                lab.next_to(ax.c2p(278, v), LEFT, buff=.09)
                plot_group.add(lab)
            curve = always_redraw(lambda ax=ax, fn=fn, color=color:
                ax.plot(fn, x_range=[278, max(278.02, revealed.get_value()), .08],
                        color=color, stroke_width=3.3, use_smoothing=False))
            dot = always_redraw(lambda ax=ax, fn=fn, color=color:
                Dot(ax.c2p(osm.get_value(), fn(osm.get_value())), radius=.057, color=color))
            cursor = always_redraw(lambda ax=ax:
                DashedLine(ax.c2p(osm.get_value(), 0),
                           ax.c2p(osm.get_value(), ax.y_range[1]),
                           color=INK, stroke_width=1.2, dash_length=.055).set_opacity(.65))
            plot_group.add(curve, cursor, dot)

        for x in [280, 284, 288, 292, 296]:
            tick = text(str(x), 16, MUTED).next_to(axes[2].c2p(x, 0), DOWN, buff=.12)
            plot_group.add(tick)
        plot_group.add(text('Plasma osmolality (mOsm/kg H₂O)', 19, INK, [-2.05, -2.67, 0]))
        # Thresholds reflect the supplied classic schematic, not diagnostic cutoffs.
        for ax, x, color in [(axes[0], 280, BLUE), (axes[2], 290, PURPLE)]:
            plot_group.add(DashedLine(ax.c2p(x, 0), ax.c2p(x, ax.y_range[1]),
                                      color=color, stroke_width=1, dash_length=.05).set_opacity(.35))

        divider = Line([1.86, 2.03, 0], [1.86, -2.73, 0], color=TRACK, stroke_width=1.5)
        right_title = text('Water relative to sodium', 21, INK, [4.30, 1.93, 0], 4.2)
        # One qualitative body-water compartment. Solute count remains fixed.
        bx = 3.32
        bottom = -.57
        def level():
            return 1.12 - (osm.get_value()-278)/18*.62
        vessel = RoundedRectangle(width=1.67, height=1.90, corner_radius=.10,
                                  stroke_color=MUTED, stroke_width=1.5).move_to([bx, .32, 0])
        water = always_redraw(lambda: Rectangle(width=1.52, height=level()-bottom,
            stroke_width=0, fill_color=TEAL, fill_opacity=.18)
            .move_to([bx, (level()+bottom)/2, 0]))
        surface = always_redraw(lambda: Line([bx-.76, level(), 0], [bx+.76, level(), 0],
                                             color=TEAL, stroke_width=1.6))
        sodium = VGroup()
        for row in range(4):
            for col in range(4):
                dot = Dot(radius=.035, color=GOLD)
                dot.add_updater(lambda m, dt, row=row, col=col: m.move_to([
                    bx-.54+.36*col, bottom+.12+(level()-bottom-.23)*(row/3), 0]))
                sodium.add(dot)
        legend = text('● Na⁺  ·  fixed amount', 15, GOLD, [bx, -.91, 0], 2.5)
        water_label = text('Body water', 18, TEAL, [bx, -1.24, 0])

        # Water intake is revealed at the high-osmolality end of the sweep.
        glass = VGroup(Line([5.15, 1.20, 0], [5.23, .50, 0]),
                       Line([5.23, .50, 0], [5.78, .50, 0]),
                       Line([5.78, .50, 0], [5.86, 1.20, 0]))
        glass.set_stroke(TEAL, 2)
        glass_water = Polygon([5.21, .96, 0], [5.80, .96, 0],
                              [5.75, .55, 0], [5.27, .55, 0],
                              stroke_width=0, fill_color=TEAL, fill_opacity=.35)
        glass_label = text('Drink water', 18, TEAL, [5.50, .14, 0], 1.9)
        intake = VGroup(glass, glass_water, glass_label).set_opacity(0)
        intake_arrow = CurvedArrow([5.12, .40, 0], [4.16, .60, 0],
                                   color=TEAL, angle=-.45, stroke_width=2).set_opacity(0)

        meter_label = text('Renal water conservation', 19, ORANGE, [4.35, -1.72, 0], 4.2)
        track = Rectangle(width=3.45, height=.12, stroke_width=0,
                          fill_color=TRACK, fill_opacity=1).move_to([4.35, -2.06, 0])
        meter = always_redraw(lambda: Rectangle(
            width=max(.025, 3.45*urine(osm.get_value())/1200), height=.12,
            stroke_width=0, fill_color=ORANGE, fill_opacity=1)
            .move_to([2.625+3.45*urine(osm.get_value())/2400, -2.06, 0]))
        urine_state = text('Large volume · dilute urine', 17, MUTED, [4.35, -2.45, 0], 4.3)
        caption = text('At low osmolality, vasopressin is suppressed and urine is dilute.',
                       23, INK, [0, -3.14, 0], 13)
        foot = text('Schematic responses, not a time axis. Thresholds vary; thirst and AVP can overlap.',
                    14, MUTED, [0, -3.65, 0], 13)
        self.play(FadeIn(plot_group), FadeIn(divider), FadeIn(right_title),
                  FadeIn(vessel), FadeIn(water), FadeIn(surface), FadeIn(sodium),
                  FadeIn(legend), FadeIn(water_label), FadeIn(meter_label), FadeIn(track),
                  FadeIn(meter), FadeIn(urine_state), FadeIn(caption), FadeIn(foot), run_time=2)
        self.add(intake, intake_arrow)
        self.wait(3)

        def change(obj, s, color=INK):
            return Transform(obj, text(s, 23 if obj is caption else 21,
                                       color, obj.get_center(), 13 if obj is caption else 11))

        def sweep(value, duration):
            self.play(osm.animate.set_value(value), revealed.animate.set_value(value),
                      run_time=duration, rate_func=linear)

        chapters.append({'id': 'low-osmolality', 'start': 0, 'end': self.time})
        start = self.time
        self.play(change(stage, 'Water loss → rising plasma osmolality', TEAL),
                  change(caption, 'Water falls relative to sodium. The sodium amount stays the same.'), run_time=1)
        sweep(280, 2)
        self.wait(1)
        self.play(change(caption, 'Vasopressin rises, increasing renal water conservation.'), run_time=1)
        sweep(288, 8)
        self.play(Transform(urine_state, text('Smaller volume · concentrated urine', 17, ORANGE,
                                            urine_state.get_center(), 4.3)), run_time=1)
        self.wait(2)
        chapters.append({'id': 'conserve-water', 'start': start, 'end': self.time})

        start = self.time
        self.play(change(stage, 'Further water loss recruits thirst', PURPLE),
                  change(caption, 'Thirst adds a second response: seek and drink water.'), run_time=1)
        sweep(293, 5)
        self.wait(2)
        chapters.append({'id': 'thirst', 'start': start, 'end': self.time})

        start = self.time
        plateau = SurroundingRectangle(
            Line(axes[1].c2p(292.7, 1200), axes[1].c2p(296.5, 1200)),
            buff=.10, color=ORANGE, stroke_width=2)
        self.play(change(stage, 'The kidney reaches its concentrating limit', ORANGE),
                  change(caption, 'Vasopressin can keep rising after urine concentration reaches its ceiling.'),
                  Create(plateau), run_time=1.5)
        sweep(296, 4)
        self.wait(4)
        chapters.append({'id': 'renal-ceiling', 'start': start, 'end': self.time})

        start = self.time
        self.play(change(stage, 'Drinking replaces the missing water', TEAL),
                  change(caption, 'After water is absorbed, plasma osmolality moves back toward baseline.'),
                  intake.animate.set_opacity(1), intake_arrow.animate.set_opacity(1),
                  FadeOut(plateau), run_time=1.5)
        self.wait(2)
        self.play(osm.animate.set_value(286), run_time=9, rate_func=smooth)
        self.play(intake_arrow.animate.set_opacity(0), run_time=.5)
        self.wait(2)
        chapters.append({'id': 'water-intake-and-feedback', 'start': start, 'end': self.time})

        start = self.time
        self.play(change(stage, 'Negative feedback reduces the drive to retain and drink water', TEAL),
                  change(caption, 'Vasopressin conserves water. Thirst replaces water.'),
                  Transform(urine_state, text('Conservation eases as osmolality falls', 17, MUTED,
                                            urine_state.get_center(), 4.3)), run_time=1.5)
        self.wait(5)
        chapters.append({'id': 'take-home', 'start': start, 'end': self.time})
        Path(__file__).with_name('chapter-times.json').write_text(
            json.dumps({'durationSeconds': self.time, 'chapters': chapters}, indent=2)+'\n')
