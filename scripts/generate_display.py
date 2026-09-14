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


def wrap_text(draw, text, fnt, max_width):
    lines = []
    current = ""
    for ch in text:
        test = current + ch
        if draw.textbbox((0, 0), test, font=fnt)[2] <= max_width:
            current = test
        else:
            if current:
                lines.append(current)
            current = ch
    if current:
        lines.append(current)
    return lines


def main():
    data = json.loads(Path("daily.json").read_text(encoding="utf-8"))
    img = Image.new("1", (W, H), 1)
    draw = ImageDraw.Draw(img)

    title_font = font(24)
    body_font = font(17)
    small_font = font(13)
    answer_font = font(12)

    draw.text((MARGIN, 8), data.get("title", "高校入試 日替わり問題"), font=title_font, fill=0)

    questions = data["questions"][:10]
    columns = [questions[:5], questions[5:10]]
    col_gap = 18
    col_width = (W - 2 * MARGIN - col_gap) // 2
    choice_gap = 8
    choice_width = (col_width - choice_gap) // 2

    for col, qs in enumerate(columns):
        x = MARGIN + col * (col_width + col_gap)
        y = 45

        for idx, q in enumerate(qs, start=1 + col * 5):
            subject = "英語" if q["subject"] == "english" else "社会"
            head = f"{idx}. [{subject}] {q['question']}"
            lines = wrap_text(draw, head, body_font, col_width)

            for line in lines:
                draw.text((x, y), line, font=body_font, fill=0)
                y += 18

            choices = q["choices"]
            for row in range(2):
                for c in range(2):
                    i = row * 2 + c
                    if i >= len(choices):
                        continue
                    cx = x + c * (choice_width + choice_gap)
                    text = f"{chr(65 + i)}. {choices[i]}"
                    wrapped = wrap_text(draw, text, small_font, choice_width)
                    for li, line in enumerate(wrapped[:2]):
                        draw.text((cx, y + li * 14), line, font=small_font, fill=0)
                y += 28 if any(len(wrap_text(draw, f"{chr(65 + row*2 + c)}. {choices[row*2 + c]}", small_font, choice_width)) > 1 for c in range(2) if row*2 + c < len(choices)) else 15

            y += 4

    draw.line((MARGIN, 405, W - MARGIN, 405), fill=0, width=1)
    answers = "  ".join(f"{i+1}:{q['answer']}" for i, q in enumerate(questions))
    answer_lines = wrap_text(draw, "解答：" + answers, answer_font, W - 2 * MARGIN)
    y = 412
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
