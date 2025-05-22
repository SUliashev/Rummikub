from PIL import Image, ImageDraw, ImageFont
import os


# === Settings ===
chip_width, chip_height = 65, 90
chip_bg_color = (235, 220, 180)  # vintage cream
corner_radius = 12

circle_radius = 25
circle_size = circle_radius * 2

font_path = "/usr/share/fonts/truetype/ubuntu/Ubuntu-B.ttf"

font_size = 34
output_dir = "chips"
os.makedirs(output_dir, exist_ok=True)

# === Color Definitions ===
colors = {
    "red": (180, 0, 0),
    "blue": (0, 0, 200),
    "black": (20, 20, 20),
    "orange": (255, 140, 0),
    "purple": (128, 0, 128),  # Added purple for joker
}

light_cream = (245, 230, 190)
dark_cream = (210, 190, 150)

def create_chip_base():
    chip = Image.new("RGBA", (chip_width, chip_height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(chip)

    # Rounded background
    mask = Image.new("L", (chip_width, chip_height), 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.rounded_rectangle(
        [(0, 0), (chip_width, chip_height)],
        radius=corner_radius,
        fill=255
    )
    bg = Image.new("RGBA", (chip_width, chip_height), chip_bg_color + (255,))
    chip.paste(bg, (0, 0), mask)

    # Gradient circle
    circle_img = Image.new("RGBA", (circle_size, circle_size), (0, 0, 0, 0))
    circle_draw = ImageDraw.Draw(circle_img)
    for x in range(circle_size):
        blend = x / circle_size
        r = int(light_cream[0] * (1 - blend) + dark_cream[0] * blend)
        g = int(light_cream[1] * (1 - blend) + dark_cream[1] * blend)
        b = int(light_cream[2] * (1 - blend) + dark_cream[2] * blend)
        circle_draw.line([(x, 0), (x, circle_size)], fill=(r, g, b, 255))

    circle_mask = Image.new("L", (circle_size, circle_size), 0)
    circle_mask_draw = ImageDraw.Draw(circle_mask)
    circle_mask_draw.ellipse([0, 0, circle_size, circle_size], fill=255)

    circle_center_x = chip_width // 2
    circle_center_y = chip_height // 2 - 10
    circle_pos = (circle_center_x - circle_radius, circle_center_y - circle_radius)
    chip.paste(circle_img, circle_pos, circle_mask)

    return chip, circle_center_y, circle_pos

# === Generate Regular Chips ===
for color_name, color_value in colors.items():
    for number in range(1, 14):
        for copy in range(2):  # Two of each tile
            chip, circle_center_y, circle_pos = create_chip_base()
            draw = ImageDraw.Draw(chip)

            draw.ellipse(
                [circle_pos[0], circle_pos[1],
                 circle_pos[0] + circle_size, circle_pos[1] + circle_size],
                outline=color_value,
                width=2
            )

            font = ImageFont.truetype(font_path, font_size)
            text = str(number)
            bbox = font.getbbox(text)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]

            vertical_shift = int(chip_height * 0.08)  # Raise the number
            text_x = chip_width // 2 - text_width // 2
            text_y = circle_center_y - text_height // 2 - vertical_shift

            draw.text((text_x, text_y), text, fill=color_value, font=font)

            filename = f"{color_name}_{number}_{copy + 1}.png"
            chip.save(os.path.join(output_dir, filename))

for i in range(2):
    file_path = os.path.join(output_dir, f"joker_{i + 1}.png")
    chip, circle_center_y, _ = create_chip_base()
    draw = ImageDraw.Draw(chip)

    text = "J"
    font = ImageFont.truetype(font_path, 28)
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    text_x = (chip_width - text_width) // 2
    text_y = circle_center_y - text_height // 2 - 2

    draw.text((text_x, text_y), "J", font= ImageFont.truetype(font_path, 36), fill=(128, 0, 128))  # purple

    chip.save(file_path)
    chip.save(os.path.join(output_dir, f"joker_{i + 1}.png"))

print("Deck generated in /chips")
