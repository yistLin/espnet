import argparse
from typing import Type

from espnet2.main_funcs.pack_funcs import pack


class PackedContents:
    files = []
    yaml_files = []


class ASRPackedContents(PackedContents):
    files = ["asr/pretrain.pth", "lm/pretrain.pth"]
    yaml_files = ["asr/config.yaml", "lm/config.yaml"]


class TTSPackedContents(PackedContents):
    files = ["pretrain.pth"]
    yaml_files = ["config.yaml"]


class EnhPackedContents(PackedContents):
    files = ["model_file.pth"]
    yaml_files = ["train_config.yaml"]


def add_arguments(parser: argparse.ArgumentParser, contents: Type[PackedContents]):
    parser.add_argument("--outpath", type=str, required=True)
    for key in contents.yaml_files:
        parser.add_argument(f"--{key}", type=str, default=None)
    for key in contents.files:
        parser.add_argument(f"--{key}", type=str, default=None)
    parser.add_argument("--option", type=str, action="append", default=[])
    parser.add_argument("--dirname", type=str, default="Base dirname in archived file")


def get_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Pack input files to archive format. If the external file path "
        "are written in the input yaml files, then the paths are "
        "rewritten to the archived name",
    )
    subparsers = parser.add_subparsers()

    # Create subparser for ASR
    for name, contents in [
        ("asr", ASRPackedContents),
        ("tts", TTSPackedContents),
        ("enh", EnhPackedContents),
    ]:
        parser_asr = subparsers.add_parser(
            name, formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        )
        add_arguments(parser_asr, contents)
        parser_asr.set_defaults(contents=contents)
    return parser


def main(cmd=None):
    parser = get_parser()
    args = parser.parse_args(cmd)
    if not hasattr(args, "contents"):
        parser.print_help()
        parser.exit(2)

    yaml_files = {
        y: getattr(args, y)
        for y in args.contents.yaml_files
        if getattr(args, y) is not None
    }
    files = {
        y: getattr(args, y) for y in args.contents.files if getattr(args, y) is not None
    }
    pack(
        yaml_files=yaml_files,
        files=files,
        option=args.option,
        dirname=args.dirname,
        outpath=args.outpath,
    )


if __name__ == "__main__":
    main()
