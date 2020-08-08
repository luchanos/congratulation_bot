from PIL import Image, ImageFont, ImageDraw
import random
import os

from io import BytesIO


def get_valid_files(path: str, formats: list) -> list:
    """Функция для получения случайной группы файлов из директории нужных форматов"""
    all_files = os.listdir(path)
    valid_files = [file for file in all_files if file.split(".")[1] in formats]
    return valid_files


PATH_TO_CORNER_ELEMENTS = "./images/corner_elements"
PATH_TO_BACKGROUNDS = "./images/backgrounds"
PATH_TO_FONTS = "./fonts"
PATH_TO_VIGNETTES = "./images/vignettes"

# переменные для хранения картинок и шрифтов
VALID_CORNER_PICTURES = get_valid_files(path=PATH_TO_CORNER_ELEMENTS, formats=["png", ])
VALID_BACKGROUNDS = get_valid_files(path=PATH_TO_BACKGROUNDS, formats=["jpeg", "jpg"])
VALID_FONTS = get_valid_files(path=PATH_TO_FONTS, formats=["ttf", "otf"])
VALID_VIGNETTES = get_valid_files(path=PATH_TO_VIGNETTES, formats=["png", ])


def get_elements_for_picture() -> dict:
    """Функция для получения случайных ингредиентов для изготовления поздравительной открытки"""
    return {"font": f"{PATH_TO_FONTS}/{random.sample(VALID_FONTS, k=1)[0]}",
            "corner_pictures": list(map(lambda x: f"{PATH_TO_CORNER_ELEMENTS}/{x}",
                                        random.sample(VALID_CORNER_PICTURES, k=4))),
            "background": f"{PATH_TO_BACKGROUNDS}/{random.sample(VALID_BACKGROUNDS, k=1)[0]}",
            "vignette": f"{PATH_TO_VIGNETTES}/{random.sample(VALID_VIGNETTES, k=1)[0]}"
            }


def paste_corner_elements(card_image, corner_elements):
    """Функция для отрисовки на базовом изображении угловых элементов"""
    coordinates = {
        # координаты картинок сверху
        0: (20, 20),
        1: (430, 20),
        # координаты картинок снизу
        2: (20, 280),
        3: (430, 280)
    }
    el_num = 0
    for element in corner_elements:
        element_to_paste = Image.open(element).convert("RGBA")
        card_image.paste(element_to_paste, coordinates[el_num], element_to_paste)
        el_num += 1
    return card_image


def draw_text_on_image(card_image, congratulation_phrase, fontpath, color):
    """Размещает поздравление на изображении"""
    font = ImageFont.truetype(font=fontpath, size=35)
    draw = ImageDraw.Draw(card_image)  # объект для рисования на нашем холсте
    x, y = card_image.size
    w, h = draw.textsize(congratulation_phrase, font=font)
    draw.text(((x - w) / 2, (y - h) / 2), congratulation_phrase.upper(), font=font, fill=color, align="center")


def draw_vignette(card_image, vignette_path):
    """Рисует виньетку"""
    element_to_paste = Image.open(vignette_path).convert("RGBA")
    card_image.paste(element_to_paste, (100, 30), element_to_paste)
    return card_image


def congratulation_func(congratulation_phrase: str):
    picture_ingredients = get_elements_for_picture()
    bg = Image.open(picture_ingredients["background"]).convert("RGBA")  # конверт в red, green, blue, alpha каналы
    corner_elements = picture_ingredients["corner_pictures"]
    vignette = picture_ingredients["vignette"]
    font = picture_ingredients["font"]
    output_content = BytesIO()
    output_content.name = 'output_content.jpeg'

    # создали сам "холст" на который всё будем накладывать
    card = Image.new(mode="RGB", size=bg.size)
    card.paste(bg, (0, 0, *bg.size), bg)  # кладём основу нашей картинки в "форму для готовки"
    card = draw_vignette(card, vignette)
    card = paste_corner_elements(card, corner_elements)

    draw_text_on_image(card_image=card, congratulation_phrase=congratulation_phrase, fontpath=font, color="yellow")

    card.save(output_content, 'JPEG')
    output_content.seek(0)
    return output_content
