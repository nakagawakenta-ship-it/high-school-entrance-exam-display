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


def fit_question(draw, text, max_width):
    for size in (14, 13, 12, 11):
        fnt = font(size)
        lines = wrap_text(draw, text, fnt, max_width)
        if len(lines) <= 2:
            return fnt, lines
    fnt = font(10)
    return fnt, wrap_text(draw, text, fnt, max_width)[:2]


def fit_choice(draw, text, max_width):
    for size in (10, 9, 8, 7):
        fnt = font(size)
        if text_width(draw, text, fnt) <= max_width:
            return fnt, text

    fnt = font(7)
    trimmed = text
    while len(trimmed) > 1 and text_width(draw, trimmed + "…", fnt) > max_width:
        trimmed = trimmed[:-1]
    return fnt, trimmed + "…"


def main():
    data = json.loads(Path("daily.json").read_text(encoding="utf-8"))
    img = Image.new("1", (W, H), 1)
    draw = ImageDraw.Draw(img)

    title_font = font(22)
    section_font = font(13)
    answer_font = font(10)
    draw.text((MARGIN, 6), data.get("title", "高校入試 日替わり問題"), font=title_font, fill=0)

    questions = data["questions"][:10]
    columns = [questions[:5], questions[5:10]]

    col_gap = 18
    col_width = (W - 2 * MARGIN - col_gap) // 2
    choice_gap = 8
    choice_width = (col_width - choice_gap) // 2

    # Show the subject once per column, like the earlier layout.
    left_x = MARGIN
    right_x = MARGIN + col_width + col_gap
    draw.text((left_x, 31), "英語", font=section_font, fill=0)
    draw.text((right_x, 31), "社会", font=section_font, fill=0)

    top_y = 48
    question_area_bottom = 438
    slot_h = (question_area_bottom - top_y) // 5

    for col, qs in enumerate(columns):
        x = MARGIN + col * (col_width + col_gap)

        for row, q in enumerate(qs):
            qnum = row + 1 + col * 5
            slot_y = top_y + row * slot_h
            head = f"{qnum}. {q['question']}"

            qfont, qlines = fit_question(draw, head, col_width)
            line_h = qfont.size + 2 if hasattr(qfont, "size") else 13
            y = slot_y + 2

            for line in qlines[:2]:
                draw.text((x, y), line, font=qfont, fill=0)
                y += line_h

            choices = q.get("choices", [])[:4]
            choice_start_y = slot_y + 37
            choice_row_h = 14

            for i, choice in enumerate(choices):
                r = i // 2
                c = i % 2
                cx = x + c * (choice_width + choice_gap)
                cy = choice_start_y + r * choice_row_h
                label = f"{chr(65 + i)}. {choice}"
                cf, shown = fit_choice(draw, label, choice_width)
                draw.text((cx, cy), shown, font=cf, fill=0)

            if row < 4:
                sep_y = slot_y + slot_h - 2
                draw.line((x, sep_y, x + col_width, sep_y), fill=0, width=1)

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
