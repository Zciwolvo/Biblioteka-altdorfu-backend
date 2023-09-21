import PyPDF2
import re
import json


class Subclass:
    def __init__(self, subclassname, status, skills, talents, equipment):
        if subclassname[0] == "h":
            subclassname = subclassname[2:]
        self.subclassname: str = subclassname
        self.status: str = status
        self.skills: list[str] = self.preprocess(skills)
        self.talents: list[str] = self.preprocess(talents)
        self.equipment: list[str] = self.preprocess(equipment)

    def to_dict(self):
        return {
            "subclassname": self.subclassname,
            "status": self.status,
            "skills": self.skills,
            "talents": self.talents,
            "equipment": self.equipment,
        }

    def preprocess(self, li):
        correct_li = []
        prev = ""
        for i, item in enumerate(li):
            parted = item.split()
            for part in parted:
                if count_capital_letters(part) > 1 and not any(
                    char in ["/", "(", ")"] for char in part
                ):
                    fixed = parted[0 : parted.index(part)]
                    fixed = " ".join(fixed)
                    fixed += " " + split_on_capital_letters(part)[0]
                    correct_li.append(fixed)
                    return correct_li
            else:
                if item != "":
                    if item[-1] == "-":
                        prev += item[0:-1]
                    else:
                        if (i < len(li) - 1) and li[i + 1] != "":
                            if li[i + 1][0] == "(":
                                item += " " + li[i + 1]
                                li.pop(i + 1)
                        item = prev + item
                        item = item.replace("-", "")
                        correct_li.append(item)
                        prev = ""
        return correct_li


class Class:
    def __init__(self, category, path, subclasses):
        self.category: str = category
        self.path: str = remove_last_letter(path)
        self.subclasses: list[Subclass] = subclasses

    def to_dict(self):
        return {
            "path": self.path,
            "subclasses": [subclass.to_dict() for subclass in self.subclasses],
        }

    def to_json(self, file_path):
        data = self.to_dict()
        with open(file_path, "w") as json_file:
            json.dump(data, json_file, indent=4)


def remove_last_letter(input_string):
    # Check if the input string is not empty
    if input_string:
        # Use slicing to remove the last letter
        result_string = input_string[:-1]
        return result_string
    else:
        # Handle the case of an empty string
        return input_string


def has_two_capital_letters(word):
    return bool(re.search(r"[A-Z][A-Z]", word))


def split_on_capital_letters(word):
    parts = re.findall(
        r"[a-ząćęłńóśźżĄĆĘŁŃÓŚŹŻ]+|[A-ZĄĆĘŁŃÓŚŹŻ][a-ząćęłńóśźżĄĆĘŁŃÓŚŹŻ]*", word
    )
    return parts


def count_capital_letters(s):
    count = 0
    for char in s:
        if char.isupper():
            count += 1
    return count


def extract_data_from_pdf(pdf_file_path, start_page=0, end_page=None):
    pdf_data = []
    current_class = None
    current_subclass = None

    with open(pdf_file_path, "rb") as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)

        if end_page is None:
            end_page = pdf_reader.numPages

        for page_number in range(start_page, end_page):
            page = pdf_reader.pages[page_number]
            page_text = page.extract_text()

            lines = page_text.split("\n")

            found = False

            for i, line in enumerate(lines):
                line = line.strip()

                if re.match(r"^SCHEMAT ROZWOJU", line):
                    if current_class is not None:
                        if current_class is not None:
                            if page_number < 61:
                                pdf_data.append(
                                    Class(
                                        "Uczeni",
                                        current_class["path"],
                                        current_class["subclasses"],
                                    )
                                )
                            elif page_number < 69:
                                pdf_data.append(
                                    Class(
                                        "Mieszczanie",
                                        current_class["path"],
                                        current_class["subclasses"],
                                    )
                                )
                            elif page_number < 77:
                                pdf_data.append(
                                    Class(
                                        "Dworzanie",
                                        current_class["path"],
                                        current_class["subclasses"],
                                    )
                                )
                            elif page_number < 85:
                                pdf_data.append(
                                    Class(
                                        "Pospólstwo",
                                        current_class["path"],
                                        current_class["subclasses"],
                                    )
                                )
                            elif page_number < 93:
                                pdf_data.append(
                                    Class(
                                        "Wędrowcy",
                                        current_class["path"],
                                        current_class["subclasses"],
                                    )
                                )
                            elif page_number < 101:
                                pdf_data.append(
                                    Class(
                                        "Wodniacy",
                                        current_class["path"],
                                        current_class["subclasses"],
                                    )
                                )
                            elif page_number < 109:
                                pdf_data.append(
                                    Class(
                                        "Łotrzykowie",
                                        current_class["path"],
                                        current_class["subclasses"],
                                    )
                                )
                            elif page_number < 117:
                                pdf_data.append(
                                    Class(
                                        "Wojownicy",
                                        current_class["path"],
                                        current_class["subclasses"],
                                    )
                                )
                    class_match = re.match(r"^SCHEMAT ROZWOJU (.+)", line)
                    current_class = {"path": class_match.group(1), "subclasses": []}
                    current_subclass = None

                elif current_class is not None:
                    subclass_match = re.match(r"^([^\–]+) – (.+)", line)
                    if (
                        subclass_match
                        and subclass_match.group(1).strip()
                        and len(current_class["subclasses"]) < 3
                    ):
                        if current_subclass is not None:
                            current_class["subclasses"].append(current_subclass)
                        subclassname = subclass_match.group(1).strip()
                        status = subclass_match.group(2).strip()
                        skills = []
                        talents = []
                        equipment = []
                        found = True

                    while found:
                        if line.startswith(("SCHEMAT ROZWOJU")):
                            if current_subclass is not None:
                                current_class["subclasses"].append(current_subclass)
                                found = False
                            break
                        elif lines[i].startswith("Umiejętności:"):
                            line = line.lstrip("Umiejętności:")
                            lines[i] = lines[i].lstrip("Umiejętności:")
                            while True:
                                if line.startswith(("Talenty:")):
                                    break
                                else:
                                    if lines[i + 1] != "" and line != "":
                                        if line[-1] != "," and not lines[
                                            i + 1
                                        ].startswith("Talenty:"):
                                            splited = lines[i + 1].split()
                                            line += splited[0]
                                            lines[i + 1] = " ".join(splited[1:])
                                    skills.extend(
                                        [skill.strip() for skill in line.split(",")]
                                    )
                                    line = lines[i + 1]
                                    i += 1
                        elif line.startswith("Talenty:"):
                            line = line.lstrip("Talenty:")
                            lines[i] = lines[i].lstrip("Talenty:")
                            while True:
                                if line.startswith(("Wyposażenie:")):
                                    break
                                else:
                                    if lines[i + 1] != "" and line != "":
                                        if line[-1] != "," and not lines[
                                            i + 1
                                        ].startswith("Wyposażenie:"):
                                            splited = lines[i + 1].split()
                                            line += splited[0]
                                            lines[i + 1] = " ".join(splited[1:])
                                    talents.extend(
                                        [talent.strip() for talent in line.split(",")]
                                    )
                                    line = lines[i + 1]
                                    i += 1
                        elif line.startswith("Wyposażenie:"):
                            line = line.lstrip("Wyposażenie:")
                            lines[i] = lines[i].lstrip("Wyposażenie:")
                            while True:
                                if line.startswith(("SCHEMAT ROZWOJU")) or any(
                                    phrase in line
                                    for phrase in ["Brąz", "Srebro", "Złoto"]
                                ):
                                    break
                                else:
                                    check = line.split()
                                    if any(
                                        count_capital_letters(word) > 1
                                        for word in check
                                    ):
                                        equipment.extend(
                                            [equip.strip() for equip in line.split(",")]
                                        )
                                        current_subclass = Subclass(
                                            subclassname,
                                            status,
                                            skills,
                                            talents,
                                            equipment,
                                        )
                                        current_class["subclasses"].append(
                                            current_subclass
                                        )
                                        break
                                    else:
                                        equipment.extend(
                                            [equip.strip() for equip in line.split(",")]
                                        )
                                        line = lines[i + 1]
                                        i += 1
                        else:
                            if len(current_class["subclasses"]) != 3:
                                current_subclass = Subclass(
                                    subclassname, status, skills, talents, equipment
                                )
                            break

    if current_class is not None:
        if page_number < 61:
            pdf_data.append(
                Class("Uczeni", current_class["path"], current_class["subclasses"])
            )
        elif page_number < 69:
            pdf_data.append(
                Class("Mieszczanie", current_class["path"], current_class["subclasses"])
            )
        elif page_number < 77:
            pdf_data.append(
                Class("Dworzanie", current_class["path"], current_class["subclasses"])
            )
        elif page_number < 85:
            pdf_data.append(
                Class("Pospólstwo", current_class["path"], current_class["subclasses"])
            )
        elif page_number < 93:
            pdf_data.append(
                Class("Wędrowcy", current_class["path"], current_class["subclasses"])
            )
        elif page_number < 101:
            pdf_data.append(
                Class("Wodniacy", current_class["path"], current_class["subclasses"])
            )
        elif page_number < 109:
            pdf_data.append(
                Class("Łotrzykowie", current_class["path"], current_class["subclasses"])
            )
        elif page_number < 117:
            pdf_data.append(
                Class("Wojownicy", current_class["path"], current_class["subclasses"])
            )
    return pdf_data


# Replace 'your_pdf_file.pdf' with the path to your PDF file.
pdf_file_path = "./pdfScrapper/WFRPbase.pdf"

# Specify the range of pages you want to iterate through (start_page and end_page).
start_page = 53
end_page = 117  # 117

result = extract_data_from_pdf(pdf_file_path, start_page, end_page)

# Save the extracted data to a JSON file named "classes.json"
output_json_file = "./pdfScrapper/classes.json"

# Create a list to store the extracted data in the desired format
data = []

# Iterate through the result list, which contains Class objects
for class_obj in result:
    # Extract data from the Class object
    category = class_obj.category
    path = class_obj.path
    subclasses_data = []

    # Iterate through the Subclass objects within the Class object
    for subclass_obj in class_obj.subclasses:
        subclassname = subclass_obj.subclassname
        status = subclass_obj.status
        skills = subclass_obj.skills
        talents = subclass_obj.talents
        equipment = subclass_obj.equipment

        # Create a dictionary for the Subclass data
        subclass_data = {
            "subclassname": subclassname,
            "status": status,
            "skills": skills,
            "talents": talents,
            "equipment": equipment,
        }

        # Append the Subclass data to the list
        subclasses_data.append(subclass_data)

    # Create a dictionary for the Class data
    class_data = {"category": category, "path": path, "subclasses": subclasses_data}

    # Append the Class data to the main list
    data.append(class_data)

# Write data to JSON file
with open(output_json_file, "w", encoding="utf-8") as json_file:
    json.dump(data, json_file, indent=4, ensure_ascii=False)
