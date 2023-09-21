import PyPDF2
from googletrans import Translator
import json

Pages = [
    61,
    62,
    63,
    64,
    73,
    74,
    75,
    76,
    85,
    86,
    87,
    88,
    97,
    98,
    99,
    100,
    109,
    110,
    111,
    112,
    121,
    122,
    123,
    124,
    133,
    134,
    135,
    136,
    145,
    146,
    147,
    148,
]

IDs = []
Names = []
CNs = []
Ranges = []
Targets = []
Durations = []
Descriptions = []
Types = []


def Scrapper(pdf_file, page):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    target_page = pdf_reader.pages[page]
    text = target_page.extract_text()
    lines = text.split("\n")

    for line_number, line in enumerate(lines, start=0):
        if line[0:2] == "CN":
            if page < 65:
                Types.append("Light")
            elif page < 77:
                Types.append("Metal")
            elif page < 89:
                Types.append("Life")
            elif page < 101:
                Types.append("Heaven")
            elif page < 113:
                Types.append("Shadow")
            elif page < 125:
                Types.append("Death")
            elif page < 137:
                Types.append("Fire")
            elif page < 149:
                Types.append("Beast")
            IDs.append("m" + str(len(IDs) + 1))
            Names.append(lines[line_number - 1])
            CNs.append(line)
            Ranges.append(lines[line_number + 1])
            Targets.append(lines[line_number + 2])
            Durations.append(lines[line_number + 3])
            Descriptions.append("")
            i = 4
            while True:
                try:
                    if lines[line_number + i + 1][0:2] == "CN":
                        break
                    elif i > 50:
                        break
                    Descriptions[len(Descriptions) - 1] += " " + lines[line_number + i]
                    i += 1
                except IndexError:
                    break


def Translate(text_to_translate, target_language):
    translator = Translator()
    translation = translator.translate(
        text_to_translate, src="en", dest=target_language
    )
    return translation.text


# Open PDF
pdf = open("WFRP.pdf", "rb")

# Loop through pages and perform scraping
for page in Pages:
    Scrapper(pdf, page)

# Close PDF
pdf.close()

# Translate descriptions to Polish
for i in range(len(Descriptions)):
    Descriptions[i] = Translate(Descriptions[i], "pl")

# Create a list of dictionaries
data = []
for i in range(len(IDs)):
    entry = {
        "id": IDs[i],
        "name": Names[i],
        "cn": CNs[i],
        "range": Ranges[i],
        "target": Targets[i],
        "duration": Durations[i],
        "description": Descriptions[i],
        "type": Types[i],
    }
    data.append(entry)

# Write data to JSON file
with open("data.json", "w", encoding="utf-8") as json_file:
    json.dump(data, json_file, indent=4, ensure_ascii=False)
