import PyPDF2
import re
import json


class Weapon:
    def __init__(
        self,
        category,
        subcategory,
        weapon_name,
        price,
        weight,
        accessibility,
        weapon_range,
        damage,
        pros_and_cons,
    ):
        self.category: str = category
        self.subcategory: str = subcategory
        self.weapon_name: str = weapon_name
        self.price: str = price
        self.weight: str = weight
        self.accessibility: str = accessibility
        self.weapon_range: str = " ".join(weapon_range)
        self.damage: str = damage
        self.pros_and_cons: list[str] = self.preprocess(pros_and_cons)

    def preprocess(self, perks):
        result = []
        current_item = ""

        for item in perks:
            if item in {"1", "2", "3", "4", "5", "1,", "2,", "3,", "4,", "5,"}:
                current_item += " " + item
                current_item = current_item.replace(",", "")
                result.append(current_item.strip())
            else:
                if current_item:
                    current_item = current_item.replace(",", "")
                    result.append(current_item.strip())
                current_item = item

            if current_item:
                current_item = current_item.replace(",", "")
                result.append(current_item.strip())
        return list(set(result))

    def to_json(self):
        weapon_json = {
            "category": self.category,
            "subcategory": self.subcategory,
            "weapon_name": self.weapon_name,
            "price": self.price,
            "weight": self.weight,
            "accessibility": self.accessibility,
            "weapon_range": self.weapon_range,
            "damage": self.damage,
            "pros_and_cons": self.pros_and_cons,
        }
        return weapon_json


def extract_data_from_pdf(pdf_file_path, start_page=0, end_page=None):
    pdf_data = []

    with open(pdf_file_path, "rb") as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)

        if end_page is None:
            end_page = pdf_reader.numPages

        for page_number in range(start_page, end_page):
            page = pdf_reader.pages[page_number]
            page_text = page.extract_text()

            lines = page_text.split("\n")

            # Initialize variables for each row
            category = "Manually Assigned Category"
            subcategory = None
            weapon_name = None
            price = None
            weight = None
            accessibility = None
            weapon_range = None
            damage = None
            pros_and_cons = []
            for line in lines[4:]:
                words = line.split()
                if len(words) == 1:
                    subcategory = words[0]
                elif (
                    len(words) >= 6
                    and words[0] != "*"
                    and words[0] != "**"
                    and words[0] != "***"
                ):
                    weapon_name = " ".join(
                        words[
                            : next(
                                (
                                    i
                                    for i, x in enumerate(words)
                                    if x[0].isdigit() or x.lower() == "darmo"
                                ),
                                len(words),
                            )
                        ]
                    )

                    price_index = next(
                        (
                            i
                            for i, x in enumerate(words)
                            if (
                                len(x) == 1
                                and (x in {"0", "1", "2", "3", "4"})
                                and words[i + 1] not in {"ZK", "s" "p"}
                                or x.lower() == "różne"
                            )
                        ),
                        len(words),
                    )
                    price = " ".join(
                        words[words.index(weapon_name.split()[-1]) + 1 : price_index]
                    )
                    weight = words[price_index]
                    accessibility = words[price_index + 1]
                    damage_index = next(
                        (
                            i
                            for i, x in enumerate(words)
                            if x[0] == "+" or x[0] == "–" or x == "Specjalny***"
                        ),
                        len(words),
                    )
                    weapon_range = words[words.index(accessibility) + 1 : damage_index]
                    damage = words[words.index(weapon_range[-1]) + 1]
                    pros_and_cons = words[words.index(damage) + 1 :]
                    weapon = Weapon(
                        category,
                        subcategory,
                        weapon_name,
                        price,
                        weight,
                        accessibility,
                        weapon_range,
                        damage,
                        pros_and_cons,
                    )
                    pdf_data.append(weapon)

    return pdf_data


pdf_file_path = "./WFRPbase.pdf"

start_page = 294
end_page = 296

result = extract_data_from_pdf(pdf_file_path, start_page, end_page)


def save_to_json_file(data, filename):
    with open(filename, "w", encoding="utf-8") as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)


all_weapons = []

for res in result:
    weapon_json = res.to_json()
    all_weapons.append(weapon_json)

# Save the entire list to weapons.json
save_to_json_file(all_weapons, "weapons.json")
