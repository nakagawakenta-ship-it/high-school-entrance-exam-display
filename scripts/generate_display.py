import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

W, H = 800, 480
MARGIN = 18


def font(size):
    candidates = [
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/opentype/noto/NotoSansCJKjp-Regular.otf",
        "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
    ]
    for p in candidates:
        if Path(p).exists():
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def text_width(draw, text, fnt):
    box = draw.textbbox((0, 0), text, font=fnt)
    return box[2] - box[0]


def wrap_text(draw, text, fnt, max_width):
    lines = []
    current = ""
    for ch in text:
        test = current + ch
        if text_width(draw, test, fnt) <= max_width:
            current = test
        else:
            if current:
                lines.append(current)
            current = ch
    if current:
        lines.append(current)
    return lines


def fit_font(draw, text, max_width, start_size, min_size):
    for size in range(start_size, min_size - 1, -1):
        fnt = font(size)
        if text_width(draw, text, fnt) <= max_width:
            return fnt
    return font(min_size)


def fit_head(draw, text, max_width):
    for size in (15, 14, 13, 12):
        fnt = font(size)
        lines = wrap_text(draw, text, fnt, max_width)
        if len(lines) <= 3:
            return fnt, lines
    fnt = font(11)
    return fnt, wrap_text(draw, text, fnt, max_width)[:3]


def main():
    data = json.loads(Path("daily.json").read_text(encoding="utf-8"))
    img = Image.new("1", (W, H), 1)
    draw = ImageDraw.Draw(img)

    title_font = font(22)
    answer_font = font(10)

    draw.text((MARGIN, 6), data.get("title", "高校入試 日替わり問題"), font=title_font, fill=0)

    questions = data["questions"][:10]
    columns = [questions[:5], questions[5:10]]

    col_gap = 18
    col_width = (W - 2 * MARGIN - col_gap) // 2
    choice_gap = 8
    choice_width = (col_width - choice_gap) // 2

    top_y = 38
    question_area_bottom = 438
    slot_h = (question_area_bottom - top_y) // 5

    # Each question gets a fixed-height slot so Q5/Q10 can never run off the page.
    for col, qs in enumerate(columns):
        x = MARGIN + col * (col_width + col_gap)

        for row, q in enumerate(qs):
            qnum = row + 1 + col * 5
            slot_y = top_y + row * slot_h
            subject = "英語" if q["subject"] == "english" else "社会"
            head = f"{qnum}. [{subject}] {q['question']}"

            head_font, head_lines = fit_head(draw, head, col_width)
            y = slot_y
            line_h = max(12, head_font.size + 1) if hasattr(head_font, "size") else 13

            for line in head_lines[:3]:
                draw.text((x, y), line, font=head_font, fill=0)
                y += line_h

            # Keep choices inside two fixed rows. Long choices shrink instead of wrapping.
            choices = q["choices"][:4]
            choice_row_h = 13
            max_choice_y = slot_y + slot_h - 4
            choices_start = min(y + 1, max_choice_y - 2 * choice_row_h)

            for i, choice in enumerate(choices):
                r = i // 2
                c = i % 2
                cx = x + c * (choice_width + choice_gap)
                cy = choices_start + r * choice_row_h
                text = f"{chr(65 + i)}. {choice}"
                cf = fit_font(draw, text, choice_width, 11, 8)
                draw.text((cx, cy), text, font=cf, fill=0)

            # subtle separator between questions, except after the last one
            if row < 4:
                sep_y = slot_y + slot_h - 2
                draw.line((x, sep_y, x + col_width, sep_y), fill=0, width=1)

    # Compact answer footer; question area now uses almost the full height.
    draw.line((MARGIN, 442, W - MARGIN, 442), fill=0, width=1)
    answers = "  ".join(f"{i+1}:{q['answer']}" for i, q in enumerate(questions))
    answer_lines = wrap_text(draw, "解答：" + answers, answer_font, W - 2 * MARGIN)
    y = 446
    for line in answer_lines[:2]:
        draw.text((MARGIN, y), line, font=answer_font, fill=0)
        y += 12

    pixels = img.load()
    raw = bytearray()
    for yy in range(H):
        for bx in range(0, W, 8):
            b = 0
            for bit in range(8):
                if pixels[bx + bit, yy] == 0:
                    b |= (0x80 >> bit)
            raw.append(b)

    Path("display.bin").write_bytes(raw)
    img.save("display_preview.png")


if __name__ == "__main__":
    main()
