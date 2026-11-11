"""Single graph with separate ADH, urine osmolarity and relative thirst scales."""
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


def label(s, size=23, color=INK):
    return Text(s, font='Avenir Next', font_size=size, color=color)


def adh(x):
    return .35 + .55 * max(0, x - 280)


def urine(x):
    t = np.clip((x - 280) / 13, 0, 1)
    return 80 + 1120 * (3*t*t - 2*t*t*t)


def thirst(x):
    return .05 * max(0, x - 290)


class Osmoregulation(Scene):
    def construct(self):
        self.camera.background_color = BG
        value = ValueTracker(272)
        extent = ValueTracker(272.02)
        self.add(value, extent)
        left, right, bottom, top = -5.35, 3.65, -2.45, 2.55
        thirst_axis = 5.43

        def point(x, y, maximum):
            return np.array([left + (x-272)/26*(right-left),
                             bottom + y/maximum*(top-bottom), 0])

        axes = VGroup(
            Line([left, bottom, 0], [right, bottom, 0], color=MUTED, stroke_width=1.5),
            Line([left, bottom, 0], [left, top, 0], color=BLUE, stroke_width=1.8),
            Line([right, bottom, 0], [right, top, 0], color=ORANGE, stroke_width=1.8),
            Line([thirst_axis, bottom, 0], [thirst_axis, top, 0], color=PURPLE, stroke_width=1.8),
        )
        for x in [272, 275, 280, 284, 288, 292, 295, 298]:
            p = point(x, 0, 10)
            axes.add(Line(p, p+DOWN*.08, color=MUTED, stroke_width=1.2),
                     label(str(x), 20, MUTED).next_to(p, DOWN, buff=.15))
        for maximum, values, xpos, side, color in [
            (10, [0, 2, 4, 6, 8, 10], left, LEFT, BLUE),
            (1400, [0, 200, 400, 600, 800, 1000, 1200, 1400], right, RIGHT, ORANGE),
            (1, [0, .2, .4, .6, .8, 1], thirst_axis, RIGHT, PURPLE),
        ]:
            for y in values:
                p = np.array([xpos, bottom + y/maximum*(top-bottom), 0])
                axes.add(Line(p, p+side*.07, color=color, stroke_width=1.2),
                         label(f'{y:g}', 19, color).next_to(p, side, buff=.12))
        axes.add(label('Plasma osmolality (mOsm/kg H₂O)', 27).move_to([-.85, -3.28, 0]))
        axes.add(label('ADH concentration (ng/L)', 23, BLUE).rotate(PI/2).move_to([-6.47, .05, 0]))
        axes.add(label('Urine osmolarity (mOsm/L)', 23, ORANGE).rotate(PI/2).move_to([4.78, .05, 0]))
        axes.add(label('Thirst (relative intensity)', 23, PURPLE).rotate(PI/2).move_to([6.48, .05, 0]))

        readout_label = label('Plasma osmolality', 25).move_to([-1.78, 3.25, 0])
        number = always_redraw(lambda: label(str(round(value.get_value())), 29).move_to([.39, 3.25, 0]))
        units = label('mOsm/kg', 22, MUTED).move_to([1.95, 3.25, 0])
        normal_color = '#65D4C2'
        band_left = point(275, 0, 10)[0]
        band_right = point(295, 0, 10)[0]
        normal_band = Rectangle(width=band_right-band_left, height=top-bottom,
                                stroke_width=0, fill_color=normal_color, fill_opacity=.09)
        normal_band.move_to([(band_left+band_right)/2, (top+bottom)/2, 0])
        band_edges = VGroup(*[Line([x, bottom, 0], [x, top, 0],
            color=normal_color, stroke_width=1).set_opacity(.35) for x in [band_left, band_right]])
        band_label = label('Normal range 275–295', 18, normal_color)
        band_label.move_to([(band_left+band_right)/2, 2.79, 0])
        self.play(FadeIn(normal_band), FadeIn(band_edges), FadeIn(band_label),
                  FadeIn(axes), FadeIn(readout_label), FadeIn(number), FadeIn(units), run_time=1.5)

        curves = VGroup()
        dots = VGroup()
        for fn, maximum, color in [(adh, 10, BLUE), (urine, 1400, ORANGE), (thirst, 1, PURPLE)]:
            def make_curve(fn=fn, maximum=maximum, color=color):
                xs = np.linspace(272, max(272.02, extent.get_value()), 230)
                return VMobject(stroke_color=color, stroke_width=4).set_points_as_corners(
                    [point(x, fn(x), maximum) for x in xs])
            curves.add(always_redraw(make_curve))
            dots.add(always_redraw(lambda fn=fn, maximum=maximum, color=color:
                Dot(point(value.get_value(), fn(value.get_value()), maximum), radius=.065, color=color)))
        cursor = always_redraw(lambda: DashedLine(
            point(value.get_value(), 0, 10), point(value.get_value(), 10, 10),
            color=INK, stroke_width=1.3, dash_length=.09).set_opacity(.5))
        self.add(cursor, curves, dots)
        self.wait(1.5)
        chapters = [{'id': 'axes', 'start': 0, 'end': round(self.time, 2)}]

        start = self.time
        self.play(value.animate.set_value(293), extent.animate.set_value(293),
                  run_time=15, rate_func=linear)
        self.wait(2)
        chapters.append({'id': 'rising-osmolarity', 'start': start, 'end': round(self.time, 2)})
        start = self.time
        self.play(value.animate.set_value(296), extent.animate.set_value(296),
                  run_time=4, rate_func=linear)
        self.wait(4)
        chapters.append({'id': 'urine-plateau', 'start': start, 'end': round(self.time, 2)})
        start = self.time
        self.play(value.animate.set_value(286), run_time=8, rate_func=smooth)
        self.wait(4)
        chapters.append({'id': 'falling-osmolarity', 'start': start, 'end': round(self.time, 2)})
        Path(__file__).with_name('chapter-times.json').write_text(json.dumps(
            {'durationSeconds': round(self.time, 2), 'chapters': chapters}, indent=2)+'\n')
