import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

W, H = 800, 480
MARGIN = 24


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


def draw_question(draw, q, y, qnum, title_font, body_font, small_font):
    subject = "英語" if q["subject"] == "english" else "社会"
    head = f"{qnum}. [{subject}] {q['question']}"
    lines = wrap_text(draw, head, body_font, W - 2 * MARGIN)
    for line in lines:
        draw.text((MARGIN, y), line, font=body_font, fill=0)
        y += 25

    for i, choice in enumerate(q["choices"]):
        label = chr(ord('A') + i)
        draw.text((MARGIN + 18, y), f"{label}. {choice}", font=small_font, fill=0)
        y += 20
    return y + 7


def main():
    data = json.loads(Path("daily.json").read_text(encoding="utf-8"))
    img = Image.new("1", (W, H), 1)
    draw = ImageDraw.Draw(img)

    title_font = font(28)
    body_font = font(20)
    small_font = font(16)
    answer_font = font(13)

    draw.text((MARGIN, 10), data.get("title", "高校入試 日替わり問題"), font=title_font, fill=0)
    y = 48

    questions = data["questions"][:10]
    # 10問を2列に配置して800x480に収める
    columns = [questions[:5], questions[5:10]]
    col_width = (W - 3 * MARGIN) // 2
    for col, qs in enumerate(columns):
        x = MARGIN + col * (col_width + MARGIN)
        y0 = 55
        for idx, q in enumerate(qs, start=1 + col * 5):
            subject = "英語" if q["subject"] == "english" else "社会"
            head = f"{idx}. [{subject}] {q['question']}"
            lines = wrap_text(draw, head, body_font, col_width)
            for line in lines:
                draw.text((x, y0), line, font=body_font, fill=0)
                y0 += 21
            for i, choice in enumerate(q["choices"]):
                draw.text((x + 8, y0), f"{chr(65+i)}. {choice}", font=small_font, fill=0)
                y0 += 17
            y0 += 5

    # 下部に解答一覧
    draw.line((MARGIN, 405, W - MARGIN, 405), fill=0, width=1)
    answers = "  ".join(f"{i+1}:{q['answer']}" for i, q in enumerate(questions))
    answer_lines = wrap_text(draw, "解答：" + answers, answer_font, W - 2 * MARGIN)
    y = 414
    for line in answer_lines[:3]:
        draw.text((MARGIN, y), line, font=answer_font, fill=0)
        y += 16

    # Waveshare/GxEPD2向け 1bit packed bitmap: 1=white, 0=black
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
