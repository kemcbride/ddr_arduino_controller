# testing for script for ddr arduino project
import unittest

import simfile
import lib


class TestFullSmWrites(unittest.TestCase):

    def check_total_duration(self, lines, num_bars, bpm, addl_delay=0):
        line_duration_sum = sum(line.duration for line in lines)
        bar_duration = lib.get_bar_duration(bpm)
        expected_duration_sum = num_bars * bar_duration + addl_delay
        self.assertEqual(line_duration_sum, expected_duration_sum)

    def test_empty_song(self):
        with open("testing/test1.sm", "r") as f:
            sm = simfile.load(f)
        chart = sm.charts[0]
        press_duration = 10
        bpm = lib.get_bpm(sm)
        lines = lib.get_chart_lines(chart.notes, bpm, press_duration)
        self.assertEqual(len(lines), 8)

    def test_single_note_song(self):
        with open("testing/test2.sm", "r") as f:
            sm = simfile.load(f)
        chart = sm.charts[0]
        press_duration = 10
        bpm = lib.get_bpm(sm)

        bars = lib.read_notes(chart.notes)
        self.assertEqual(len(bars), 8)

        leftover_delay = 0.0
        for bar in bars:
            bar_lines, leftover_delay = lib.write_out_bar_code(
                bar, press_duration, bpm, leftover_delay
            )
            self.assertLess(len(bar_lines), 4)

        lines = lib.get_chart_lines(chart.notes, bpm, press_duration)
        self.assertEqual(len(lines), 9)

        self.check_total_duration(lines, 8, bpm)

    def test_simple_multi_note_song(self):
        with open("testing/test3.sm", "r") as f:
            sm = simfile.load(f)
        chart = sm.charts[0]
        press_duration = 10
        bpm = lib.get_bpm(sm)

        bars = lib.read_notes(chart.notes)
        self.assertEqual(len(bars), 8)

        leftover_delay = 0.0
        for bar in bars:
            bar_lines, leftover_delay = lib.write_out_bar_code(
                bar, press_duration, bpm, leftover_delay
            )
            self.assertLess(len(bar_lines), 10)

        lines = lib.get_chart_lines(chart.notes, bpm, press_duration)
        self.assertEqual(len(lines), 32)

        self.check_total_duration(lines, 8, bpm)

    def test_hysteria_maniac_single(self):
        with open("testing/hysteria.sm", "r") as f:
            sm = simfile.load(f)
        chart = sm.charts[2]
        press_duration = 50
        bpm = lib.get_bpm(sm)
        bars = lib.read_notes(chart.notes)
        bar_duration = lib.get_bar_duration(bpm)
        for bar in bars:
            bar_lines, _ = lib.write_out_bar_code(bar, press_duration, bpm)
            bar_line_duration = sum(line.duration for line in bar_lines)
            self.assertEqual(bar_line_duration, bar_duration)
            num_presses = len([
                p for p in bar_lines if isinstance(p, lib.Press)
            ])
            if isinstance(bar_lines[0], lib.Press):
                self.assertEqual(len(bar_lines), num_presses * 2)
            else:
                self.assertEqual(len(bar_lines), 1 + num_presses * 2)

        lib.get_chart_lines(chart.notes, bpm, press_duration)


class TestBarLogic(unittest.TestCase):
    def setUp(self):
        self.press_duration = 10
        self.bpm = 120.0
        self.bar_duration = lib.get_bar_duration(self.bpm)

    def produce_press_absolute_timeline(self, bar_lines):
        time = 0
        press_times = []
        for line in bar_lines:
            if isinstance(line, lib.Press):
                press_times.append(time)
            time += line.duration
        return press_times

    def test_bar_duration(self):
        expected_duration = 2000
        self.assertEqual(self.bar_duration, expected_duration)

    def test_empty_bar(self):
        bar = lib.produce_bar("0000\n0000\n0000\n0000\n")
        bar_duration = lib.get_bar_duration(self.bpm)

        lines, _ = lib.write_out_bar_code(bar, self.press_duration, self.bpm)
        line_duration_sum = sum(line.duration for line in lines)
        self.assertEqual(len(lines), 1)
        self.assertEqual(line_duration_sum, bar_duration)
        for line in lines:
            self.assertGreater(line.duration, 0)

        press_times = self.produce_press_absolute_timeline(lines)
        self.assertEqual(len(press_times), 0)

    def test_singlenote_bar(self):
        bar = lib.produce_bar("0000\n0000\n0000\n1000\n")
        bar_duration = lib.get_bar_duration(self.bpm)

        lines, _ = lib.write_out_bar_code(bar, self.press_duration, self.bpm)
        line_duration_sum = sum(line.duration for line in lines)
        self.assertEqual(len(lines), 3)
        self.assertIsInstance(lines[-2], lib.Press)
        self.assertEqual(line_duration_sum, bar_duration)
        for line in lines:
            self.assertGreater(line.duration, 0)

        press_times = self.produce_press_absolute_timeline(lines)
        self.assertEqual(len(press_times), 1)
        self.assertEqual(press_times[0], 1500)

    def test_multinote_bar(self):
        bar = lib.produce_bar("0010\n0100\n0001\n1000\n")
        bar_duration = lib.get_bar_duration(self.bpm)

        lines, _ = lib.write_out_bar_code(bar, self.press_duration, self.bpm)
        line_duration_sum = sum(line.duration for line in lines)
        self.assertEqual(len(lines), 8)
        self.assertIsInstance(lines[0], lib.Press)
        self.assertEqual(line_duration_sum, bar_duration)
        for line in lines:
            self.assertGreater(line.duration, 0)

        press_times = self.produce_press_absolute_timeline(lines)
        self.assertEqual(len(press_times), 4)
        for idx, time in enumerate(press_times):
            self.assertEqual(time, 500 * idx)

    def test_firstnoteonly_bar(self):
        bar = lib.produce_bar("0010\n0000\n0000\n0000\n")
        bar_duration = lib.get_bar_duration(self.bpm)

        lines, _ = lib.write_out_bar_code(bar, self.press_duration, self.bpm)
        line_duration_sum = sum(line.duration for line in lines)
        self.assertEqual(len(lines), 2)
        self.assertIsInstance(lines[0], lib.Press)
        self.assertEqual(line_duration_sum, bar_duration)
        for line in lines:
            self.assertGreater(line.duration, 0)

        press_times = self.produce_press_absolute_timeline(lines)
        self.assertEqual(len(press_times), 1)
        self.assertEqual(press_times[0], 0)

    def test_firstnotealternatingnotes_bar(self):
        bar = lib.produce_bar("0010\n0000\n0100\n0000\n")
        bar_duration = lib.get_bar_duration(self.bpm)

        lines, _ = lib.write_out_bar_code(bar, self.press_duration, self.bpm)
        line_duration_sum = sum(line.duration for line in lines)
        self.assertEqual(len(lines), 4)
        self.assertIsInstance(lines[0], lib.Press)
        self.assertEqual(line_duration_sum, bar_duration)
        for line in lines:
            self.assertGreater(line.duration, 0)

        press_times = self.produce_press_absolute_timeline(lines)
        self.assertEqual(len(press_times), 2)
        self.assertEqual(press_times[0], 0)
        self.assertEqual(press_times[1], 1000)

    def test_secondnotealternatingnotes_bar(self):
        bar = lib.produce_bar("0000\n0100\n0000\n0001\n")
        bar_duration = lib.get_bar_duration(self.bpm)

        lines, _ = lib.write_out_bar_code(bar, self.press_duration, self.bpm)
        line_duration_sum = sum(line.duration for line in lines)
        self.assertEqual(len(lines), 5)
        self.assertIsInstance(lines[1], lib.Press)
        self.assertEqual(line_duration_sum, bar_duration)
        for line in lines:
            self.assertGreater(line.duration, 0)

        press_times = self.produce_press_absolute_timeline(lines)
        self.assertEqual(len(press_times), 2)
        self.assertEqual(press_times[0], 500)
        self.assertEqual(press_times[1], 1500)

    def test_problem_negative_postbardelay_8countbar(self):
        string = "\n1000\n0000\n0010\n1000\n0100\n0000\n1000\n0000\n"
        bar = lib.produce_bar(string)
        bar_duration = lib.get_bar_duration(self.bpm)

        lines, _ = lib.write_out_bar_code(bar, self.press_duration, self.bpm)
        line_duration_sum = sum(line.duration for line in lines)
        self.assertEqual(len(lines), 10)
        self.assertIsInstance(lines[0], lib.Press)
        self.assertEqual(line_duration_sum, bar_duration)
        for line in lines:
            self.assertGreater(line.duration, 0)

        press_times = self.produce_press_absolute_timeline(lines)
        expected_press_times = [0, 500, 750, 1000, 1500]
        self.assertEqual(press_times, expected_press_times)

    def test_between_beat_durations_make_sense(self):
        lib.get_bar_duration(self.bpm)

        fourbar = lib.produce_bar("0010\n0000\n0100\n0000\n")
        fourbetween_beat_delay = lib.get_between_beat_delay(
            self.bpm, fourbar.num_rows
        )

        string = "\n1000\n0000\n0010\n1000\n0100\n0000\n1000\n0000\n"
        eightbar = lib.produce_bar(string)
        eightbetween_beat_delay = lib.get_between_beat_delay(
            self.bpm, eightbar.num_rows
        )
        self.assertEqual(fourbetween_beat_delay, 2 * eightbetween_beat_delay)


class TestMultiBarLogic(unittest.TestCase):
    def setUp(self):
        self.press_duration = 10
        self.bpm = 180.0
        self.bar_duration = lib.get_bar_duration(self.bpm)

    def test_two_bar_simple(self):
        string = (
            "0010\n0000\n0100\n0000\n,"
            "\n1000\n0000\n0010\n1000\n0100\n0000\n1000\n0000\n"
        )
        lines = lib.get_chart_lines(string, self.bpm, self.press_duration)
        timeline = lib.produce_press_absolute_timeline(lines)
        self.assertEqual(len(lines), 4 + 10)
        self.assertEqual(len(timeline), 2 + 5)
        self.assertEqual(
            round(sum([line.duration for line in lines]), 2),
            round(2 * self.bar_duration, 2),
        )


if __name__ == "__main__":
    unittest.main()
