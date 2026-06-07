import argparse
from pathlib import Path
import sys

from pydub import AudioSegment
from pydub.utils import which


def ensure_ffmpeg_installed() -> None:
    if which("ffmpeg") is None:
        raise EnvironmentError(
            "ffmpeg binary not found. Install ffmpeg and make sure it is on your PATH. "
            "See https://ffmpeg.org/download.html"
        )


def extract_audio(source_path: Path, output_format: str = "wav") -> Path:
    ensure_ffmpeg_installed()

    if not source_path.exists():
        raise FileNotFoundError(f"Source file not found: {source_path}")

    input_format = source_path.suffix.lstrip(".").lower()
    if input_format == "":
        raise ValueError("Source file must have an extension to infer the input format.")

    output_file = source_path.with_suffix(f".{output_format}")
    audio = AudioSegment.from_file(source_path, format=input_format)
    audio.export(output_file, format=output_format)
    return output_file


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Extract audio from a media file.")
    parser.add_argument(
        "source",
        type=Path,
        nargs="?",
        default=Path("downloades/Generative AI Full Course (Part 1 ) ｜ Beginner to Advanced ｜ LangChain, LLMs & Prompt Engineering.webm"),
        help="Path to the source media file."
    )
    parser.add_argument(
        "--format",
        choices=["wav", "mp3", "ogg"],
        default="wav",
        help="Output audio format."
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        output_path = extract_audio(args.source, args.format)
        print(f"Audio extracted to: {output_path}")
        return 0
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
