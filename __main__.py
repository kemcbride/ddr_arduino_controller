import argparse
import simfile
import lib


def main(args):
    print(args.source_sm)
    print(args.press_duration)
    if args.output_fname is not None:
        print(args.output_fname)

    with open(args.source_sm, "r") as f:
        sm = simfile.load(f)

    bpm = lib.get_bpm(sm)
    hard_single = sm.charts[3]
    lines = lib.write_out_chart(hard_single.notes, bpm, args.press_duration)
    print("\n".join([str(line) for line in lines]))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("source_sm", type=str)
    ap.add_argument("--output-fname", type=str)
    ap.add_argument(
        "--press-duration",
        type=int,
        default=lib.PRESS_DURATION,
        help="Duration for press in ms",
    )
    args = ap.parse_args()
    main(args)
