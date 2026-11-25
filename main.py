"""One-sentence absurd invention pitch.

Writes a single-sentence pitch for a ridiculous invention to
``<output-dir>/entry.txt``. The output directory comes from the
``MAKEFUN_OUTPUT_DIR`` environment variable when set, and defaults to
``/output`` (the grader's writable output directory).

The pitch itself is a fixed, hand-written sentence: a smoke detector
that turns the tables on the kitchen by filing a formal noise
complaint against the toast and dragging the toaster to a hearing
before it may beep again.

Only the entry file is ever chmodded (to 0644, so the grader can read
it as another user). The output directory itself is never chmodded.
"""

import os
import stat
import sys

# The entry: exactly one sentence, 144 characters.
SENTENCE = (
    "A smoke detector that files a formal noise complaint against your "
    "toast and summons the toaster to a hearing before it is allowed "
    "to beep again."
)

MAX_CHARS = 220


def check_sentence(sentence):
    """Refuse to write anything that is not exactly one short sentence."""
    text = sentence.strip()
    if text != sentence:
        raise ValueError("sentence must not have leading/trailing space")
    if "\n" in text or "\r" in text:
        raise ValueError("sentence must be a single line")
    if len(text) > MAX_CHARS:
        raise ValueError(
            "sentence is %d characters, over the %d limit"
            % (len(text), MAX_CHARS)
        )
    # Exactly one sentence: one full stop, at the very end, and no
    # other sentence-ending punctuation anywhere.
    if not text.endswith("."):
        raise ValueError("sentence must end with a full stop")
    if text.count(".") != 1:
        raise ValueError("sentence must contain exactly one full stop")
    if "!" in text or "?" in text:
        raise ValueError("sentence must not contain '!' or '?'")
    return text


def main():
    # Files created below inherit world-readable permissions.
    os.umask(0o022)

    sentence = check_sentence(SENTENCE)

    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    # Never chmod the output directory itself: it may be owned by
    # another user and merely writable, so chmodding it can fail.
    os.makedirs(output_dir, exist_ok=True)

    entry_path = os.path.join(output_dir, "entry.txt")
    with open(entry_path, "w", encoding="utf-8", newline="") as handle:
        handle.write(sentence)

    # The grader collects outputs as a different user, so the file
    # itself must be world-readable.
    os.chmod(entry_path, 0o644)

    # Read the file back and prove what landed on disk is exact.
    with open(entry_path, "r", encoding="utf-8") as handle:
        written = handle.read()
    if written != sentence:
        raise ValueError("entry.txt does not match the sentence")
    if len(written.encode("utf-8")) > MAX_CHARS:
        raise ValueError("entry.txt is over the 220-character limit")
    mode = stat.S_IMODE(os.stat(entry_path).st_mode)
    if mode != 0o644:
        raise ValueError("entry.txt mode is %o, expected 644" % mode)

    print("Wrote %d characters to %s" % (len(sentence), entry_path))
    print(sentence)
    return 0


if __name__ == "__main__":
    sys.exit(main())
