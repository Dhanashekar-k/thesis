"""
figure_catalog.py — Match figure captions to their cropped image files.

PaddleOCR layout for a figure page (from iso20_spec_25_res.json):

    { "block_label": "image",
      "block_bbox":  [255, 236, 867, 1327],
      "block_order": null }

    { "block_label": "figure_title",
      "block_content": "Figure 4 — Example for call flows",
      "block_order": null }

The cropped image is saved as:
    imgs/img_in_image_box_255_236_867_1327.jpg

Note: coordinates in the filename may differ from block_bbox by a few pixels
due to PaddleOCR rounding. We match by finding the file whose embedded bbox
is closest to the block bbox, within a configurable tolerance.

Caption formats supported:
    "Figure 4 — Example for call flows"
    "Figure 215 — AC message sequence diagram"
    "Figure A.3 — Certificate hierarchy"
    "Table 7 — AC_ChargeLoopReq fields"
"""

from __future__ import annotations

import re
from pathlib import Path
from models import RawBlock, Figure

# Extracts x1, y1, x2, y2 from filenames like:
#   img_in_image_box_255_236_867_1327.jpg
_IMG_FNAME_RE = re.compile(r"img_in_image_box_(\d+)_(\d+)_(\d+)_(\d+)")

# Figure/Table caption: "Figure 4 — ..." or "Figure A.3 — ..."
# Supports em-dash (—), en-dash (–), and plain hyphen (-)
_CAPTION_RE = re.compile(
    r"^(Figure|Table)\s+([\dA-Z][\dA-Z.]*)\s*[—–\-]\s*(.+)$",
    re.IGNORECASE,
)

# Sum of absolute coordinate differences across 4 values for a match
_BBOX_TOLERANCE = 30


def _bbox_from_filename(name: str) -> tuple[int, int, int, int] | None:
    m = _IMG_FNAME_RE.search(name)
    if not m:
        return None
    return (int(m.group(1)), int(m.group(2)), int(m.group(3)), int(m.group(4)))


def _bbox_distance(a: tuple, b: tuple) -> int:
    """Sum of absolute differences across all four coordinates."""
    return sum(abs(x - y) for x, y in zip(a, b))


def find_image_file(
    bbox: tuple[int, int, int, int],
    img_dir: str,
    tolerance: int = _BBOX_TOLERANCE,
) -> str:
    """
    Return the path of the image file whose embedded bbox is closest to
    `bbox` and within `tolerance` pixel-sum distance.
    Returns "" if no matching file is found or img_dir does not exist.
    """
    img_path = Path(img_dir)
    if not img_path.exists():
        return ""

    best_path = ""
    best_dist = tolerance + 1

    for f in img_path.iterdir():
        if f.suffix.lower() not in (".jpg", ".jpeg", ".png"):
            continue
        file_bbox = _bbox_from_filename(f.name)
        if file_bbox is None:
            continue
        dist = _bbox_distance(bbox, file_bbox)
        if dist < best_dist:
            best_dist = dist
            best_path = str(f)

    return best_path


def parse_caption(text: str) -> tuple[str, str]:
    """
    Parse a figure/table caption into (figure_id, description).

    Examples:
        "Figure 215 — AC message sequence diagram"
            → ("Figure 215", "AC message sequence diagram")
        "Figure A.3 — Certificate hierarchy"
            → ("Figure A.3", "Certificate hierarchy")
        "Some plain text"
            → ("", "Some plain text")
    """
    m = _CAPTION_RE.match(text.strip())
    if m:
        kind   = m.group(1).capitalize()
        number = m.group(2)
        desc   = m.group(3).strip()
        return (f"{kind} {number}", desc)
    return ("", text.strip())


class FigureCatalog:
    """
    Stateful collector.  Feed blocks in reading order (unordered blocks
    sorted by y-position, as loader.py guarantees).

    An image block sets a pending image.  The next figure_title block
    closes it and creates a Figure entry.  If figure_title appears
    without a preceding image block, image_path is set to "" — this
    happens when PaddleOCR fails to detect the image region.
    """

    def __init__(self) -> None:
        self.figures:       list[Figure]    = []
        self._pending_img:  RawBlock | None = None

    def feed(self, block: RawBlock, img_dir: str) -> None:
        """Process a single block."""
        if block.label == "image":
            self._pending_img = block
            return

        if block.label == "figure_title":
            fig_id, caption = parse_caption(block.content)

            if self._pending_img is not None:
                image_path = find_image_file(self._pending_img.bbox, img_dir)
                img_bbox   = self._pending_img.bbox
                img_page   = self._pending_img.page
            else:
                image_path = ""
                img_bbox   = block.bbox
                img_page   = block.page

            self.figures.append(Figure(
                figure_id=fig_id if fig_id else block.content[:40],
                caption=caption,
                image_path=image_path,
                page=img_page,
                bbox=img_bbox,
            ))
            self._pending_img = None
            return

        # Text/table blocks between image and its caption are rare but possible
        # (footnotes, notes). Reset pending only for definitive content blocks.
        if block.label in ("table", "paragraph_title"):
            self._pending_img = None

    def get_by_id(self, figure_id: str) -> Figure | None:
        """Look up a figure by normalised ID, e.g. 'Figure 215'."""
        for f in self.figures:
            if f.figure_id.lower() == figure_id.lower():
                return f
        return None