# ummm testing for script generator for ... ddr arduino project...
import unittest

import simfile
import lib


class Test1(unittest.TestCase):
    def setUp(self):
        pass

    def check_total_duration(self, lines, num_bars, bpm, addl_delay=0):
        line_duration_sum = sum(line.duration for line in lines)
        expected_duration_sum = num_bars * lib.get_bar_duration(bpm) + addl_delay
        self.assertEqual(line_duration_sum, expected_duration_sum)

    def test_empty_song(self):
        with open("testing/test1.sm", 'r') as f:
            sm = simfile.load(f);
        chart = sm.charts[0]
        press_duration = 10
        bpm = lib.get_bpm(sm)
        lines = lib.write_out_chart(chart.notes, bpm, press_duration)
        self.assertEqual(len(lines), 0)

    def test_single_note_song(self):
        with open("testing/test2.sm", 'r') as f:
            sm = simfile.load(f);
        chart = sm.charts[0]
        press_duration = 10
        bpm = lib.get_bpm(sm)

        bars = lib.read_notes(chart.notes)
        self.assertEqual(len(bars), 8)

        leftover_delay = 0.0
        output_lines = []
        for bar in bars:
            bar_lines, leftover_delay = lib.write_out_bar_code(bar, press_duration, bpm, leftover_delay)
            self.assertLess(len(bar_lines), 3)

        lines = lib.write_out_chart(chart.notes, bpm, press_duration)
        self.assertEqual(len(lines), 2)
        import ipdb; ipdb.set_trace()

        # I would just say let's check against the duration of the whole song, 8 bars
        # But, how i've implemented it, it only prints a delay for up to the first
        # note, and nothing after the last note
        # Since it has one note at start of bar 5 (0-indexed), it will wait for that time, then 
        # have a delay for the press duration
        self.check_total_duration(lines, 5, bpm, addl_delay=press_duration)

    def test_simple_multi_note_song(self):
        with open("testing/test3.sm", 'r') as f:
            sm = simfile.load(f);
        chart = sm.charts[0]
        press_duration = 10
        bpm = lib.get_bpm(sm)

        bars = lib.read_notes(chart.notes)
        self.assertEqual(len(bars), 8)

        leftover_delay = 0.0
        output_lines = []
        for bar in bars:
            bar_lines, leftover_delay = lib.write_out_bar_code(bar, press_duration, bpm, leftover_delay)
            self.assertLess(len(bar_lines), 9)

        lines = lib.write_out_chart(chart.notes, bpm, press_duration)
        self.assertEqual(len(lines), 30)

        # I would just say let's check against the duration of the whole song, 8 bars
        # But, how i've implemented it, it only prints a delay for up to the first
        # note, and nothing after the last note
        # For this one, it prints for every bar in the song, and then technically,
        # we expect to be missing a delay for the last "beat" - press_duration
        between_beat_delay = lib.get_between_beat_delay(bpm, 4)
        self.check_total_duration(lines, 8, bpm, addl_delay=-(between_beat_delay - press_duration))


if __name__ == '__main__':
    unittest.main()
