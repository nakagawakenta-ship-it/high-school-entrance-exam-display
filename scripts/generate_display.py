import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

W, H = 800, 480
MARGIN = 20


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
    for size in (18, 17, 16, 15, 14):
        fnt = font(size)
        lines = wrap_text(draw, text, fnt, max_width)
        if len(lines) <= 2:
            return fnt, lines
    fnt = font(13)
    return fnt, wrap_text(draw, text, fnt, max_width)[:2]


def main():
    data = json.loads(Path("daily.json").read_text(encoding="utf-8"))
    img = Image.new("1", (W, H), 1)
    draw = ImageDraw.Draw(img)

    title_font = font(23)
    answer_font = font(11)
    draw.text((MARGIN, 7), data.get("title", "高校入試 日替わり問題"), font=title_font, fill=0)

    questions = data["questions"][:10]
    columns = [questions[:5], questions[5:10]]
    col_gap = 22
    col_width = (W - 2 * MARGIN - col_gap) // 2

    top_y = 43
    question_area_bottom = 405
    slot_h = (question_area_bottom - top_y) // 5

    for col, qs in enumerate(columns):
        x = MARGIN + col * (col_width + col_gap)
        for row, q in enumerate(qs):
            qnum = row + 1 + col * 5
            slot_y = top_y + row * slot_h
            subject = "英語" if q["subject"] == "english" else "社会"
            text = f"{qnum}. [{subject}] {q['question']}"
            qfont, lines = fit_question(draw, text, col_width)
            line_h = qfont.size + 3 if hasattr(qfont, "size") else 18
            y = slot_y + 5
            for line in lines:
                draw.text((x, y), line, font=qfont, fill=0)
                y += line_h
            if row < 4:
                sep_y = slot_y + slot_h - 3
                draw.line((x, sep_y, x + col_width, sep_y), fill=0, width=1)

    draw.line((MARGIN, 410, W - MARGIN, 410), fill=0, width=1)
    answers = "  ".join(f"{i+1}:{q['answer']}" for i, q in enumerate(questions))
    answer_lines = wrap_text(draw, "解答：" + answers, answer_font, W - 2 * MARGIN)
    y = 417
    for line in answer_lines[:4]:
        draw.text((MARGIN, y), line, font=answer_font, fill=0)
        y += 14

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
