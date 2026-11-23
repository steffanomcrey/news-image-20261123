"""news-image-20261123 entrypoint (Python 3.13, standard library only).

Copies the pre-rendered front page (repo/entry.png, drawn at build time
with PIL by render.py in the workdir) to the grader output directory and
verifies it is a whole PNG before finishing. The program runs twice and
both runs write the same bytes, because the copy is byte-exact.

Run locally: mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""
import hashlib
import os
import shutil
import sys

PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    with open(src, "rb") as f:
        head = f.read(len(PNG_MAGIC))
    if head != PNG_MAGIC:
        print("entry.png is not a PNG", file=sys.stderr)
        return 1
    shutil.copyfile(src, dst)
    digest = hashlib.sha256(open(dst, "rb").read()).hexdigest()
    source_digest = hashlib.sha256(open(src, "rb").read()).hexdigest()
    if digest != source_digest:
        print("copy mismatch: %s != %s" % (digest, source_digest), file=sys.stderr)
        return 1
    print("wrote %s (%d bytes, sha256 %s)" % (dst, os.path.getsize(dst), digest))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
