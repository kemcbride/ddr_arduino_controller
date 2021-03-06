import dataclasses
from enum import Enum


PRESS_DURATION = 50


@dataclasses.dataclass
class Direction:
    name: str
    idx: int


class Directions(Enum):
    LEFT = Direction("Left", 0)
    DOWN = Direction("Down", 1)
    UP = Direction("Up", 2)
    RIGHT = Direction("Right", 3)


TAB = " " * 2
DIRS = {
    0: Directions.LEFT,
    1: Directions.DOWN,
    2: Directions.UP,
    3: Directions.RIGHT
}


@dataclasses.dataclass
class Bar:
    notes: str
    num_rows: int


class Delay:
    def __init__(self, duration):
        self._duration = duration
        self._string = f"delay({duration:.2f});"

    def __str__(self):
        return self._string

    @property
    def duration(self):
        return self._duration


class Press:
    def __init__(self, source_line, duration):
        self._source_line = source_line
        self._num_keys = len([k for k in source_line if k == "1"])
        self._keys = [
            DIRS[idx] for idx, val in enumerate(source_line) if val == "1"
        ]
        self._duration = duration
        self._function_name = (
            f"press{self.num_keys}_button" if self.num_keys > 1
            else "press_button"
        )
        self._button_dirs_str = ", ".join([d.name.title() for d in self.keys])
        self._string = (
            f"{self._function_name}({self._button_dirs_str}, "
            "press_duration);"
        )

    def __str__(self):
        return self._string

    @property
    def duration(self):
        return self._duration

    @property
    def num_keys(self):
        return self._num_keys

    @property
    def keys(self):
        return self._keys

    @property
    def source_line(self):
        return self._source_line


def get_bpm(sm):
    # Assumes there's only bpm in the song (takes the first one)
    bpm = float(sm.bpms.split("=")[-1])
    return bpm


def get_between_beat_delay(bpm, num_rows):
    bar_duration = get_bar_duration(bpm)
    return bar_duration / num_rows


def get_bar_duration(bpm):
    bps = bpm / 60.0
    spb = 1 / bps
    mspb = spb * 1000
    bar_duration = mspb * 4
    return bar_duration


def write_header(sm, press_duration):
    bpm = get_bpm(sm)
    return [
        "#ifndef SONG_H",
        "#define SONG_H",
        '#include "helpers.h"',
        f"float press_duration = {press_duration};",
        f"float bpm = {bpm};",
        "",
        "void play_song() {",
    ]


def write_footer():
    return [
        "}",
        "",
        "#endif",
    ]


def write_out_delay(next_delay):
    delay = Delay(next_delay)
    return delay


def write_out_one_beat(line, press_duration):
    press = Press(line, press_duration)
    return press


def write_line(
    line,
    first_note_written,
    last_delay,
    next_delay,
    press_delay,
    press_duration
):
    line_lines = []
    if not first_note_written:
        first_note_written = True
        if last_delay > 0:
            line_lines.append(write_out_delay(last_delay))
    else:
        if next_delay > 0:
            line_lines.append(write_out_delay(next_delay))
    line = write_out_one_beat(line, press_duration)
    line_lines.append(line)
    return line_lines, first_note_written, press_delay


def update_delays(
    first_note_written,
    last_delay,
    next_delay,
    between_beat_delay
):
    if not first_note_written:
        last_delay += between_beat_delay
    else:
        next_delay += between_beat_delay
    return last_delay, next_delay


def write_out_bar_code(bar, press_duration, bpm, last_delay=0.0):
    first_note_written = False
    between_beat_delay = get_between_beat_delay(bpm, bar.num_rows)
    press_delay = between_beat_delay - press_duration
    full_bar_duration = get_bar_duration(bpm)
    consumed_duration = 0

    next_delay = between_beat_delay - press_duration

    bar_lines = []
    line_lines = []
    if "1" not in bar.notes:
        # Is thsi right??? IDK lol, its not like there are any empty bars...?
        return [Delay(full_bar_duration)], 0.0

    for line in bar.notes.split():
        if "1" in line:
            line_lines, first_note_written, next_delay = write_line(
                line,
                first_note_written,
                last_delay,
                next_delay,
                press_delay,
                press_duration,
            )
            bar_lines += line_lines
        else:
            last_delay, next_delay = update_delays(
                first_note_written, last_delay, next_delay, between_beat_delay
            )

    consumed_duration += sum(line.duration for line in bar_lines)
    remainder_delay = full_bar_duration - consumed_duration
    bar_end_remainder_delay = write_out_delay(remainder_delay)
    bar_lines.append(bar_end_remainder_delay)
    return bar_lines, 0.0


def produce_press_absolute_timeline(bar_lines):
    time = 0
    press_times = []
    for line in bar_lines:
        if isinstance(line, Press):
            press_times.append(time)
        time += line.duration
    return press_times


def produce_bar(bar):
    num_rows = len(bar.split())
    return Bar(notes=bar, num_rows=num_rows)


def read_notes(notes: str):
    bar_list = [produce_bar(bar) for bar in notes.split(",")]
    return bar_list


def get_chart_lines(notes, bpm, press_duration):
    bars = read_notes(notes)
    leftover_delay = 0.0
    output_lines = []
    for bar in bars:
        bar_lines, leftover_delay = write_out_bar_code(
            bar, press_duration, bpm, leftover_delay
        )
        output_lines += bar_lines
    return output_lines


def remove_initial_delays(chart_lines):
    first_press_idx = len(chart_lines)
    for idx, line in enumerate(chart_lines):
        if isinstance(line, Press):
            first_press_idx = idx
            break
    return chart_lines[first_press_idx:]


def get_output_lines(sm, chart_index, press_duration, bpm_offset):
    header_lines = write_header(sm, press_duration)
    notes = sm.charts[chart_index].notes
    bpm = get_bpm(sm) + bpm_offset
    note_lines = [
        TAB + str(line) for line in
        remove_initial_delays(get_chart_lines(notes, bpm, press_duration))
    ]
    footer_lines = write_footer()
    return header_lines + note_lines + footer_lines
