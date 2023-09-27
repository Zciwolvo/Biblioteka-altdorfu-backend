import PyPDF2
import json


class Talent:
    def __init__(self, name, maksimum, tests, description):
        self.name = name
        self.maksimum = maksimum
        self.tests = tests
        self.description = description.replace("-", "")


def extract_data_from_pdf(pdf_file_path, start_page=0, end_page=None):
    pdf_data = []

    with open(pdf_file_path, "rb") as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        description = ""
        name = ""
        maksimum = ""
        tests = ""
        if end_page is None:
            end_page = len(pdf_reader.pages)

        for page_number in range(start_page, end_page):
            page = pdf_reader.pages[page_number]
            page_text = page.extract_text()

            lines = page_text.split("\n")

            for i, line in enumerate(lines):
                if line[0:8] == "Maksimum":
                    if name != "" and maksimum != "" and description != "":
                        talent = Talent(name, maksimum, tests, description)
                        pdf_data.append(talent)
                    name = lines[i - 1]
                    maksimum = line[10:]
                    if lines[i + 1][0:5] == "Testy":
                        tests = lines[i + 1][7:]
                    else:
                        tests = ""
                    description = ""
                else:
                    try:
                        if lines[i + 1][0:8] != "Maksimum" and not line.startswith(
                            "Testy:"
                        ):
                            description += line
                    except:
                        description += line

    return pdf_data


pdf_file_path = "./pdfScrapper/WFRPbase.pdf"
start_page = 132
end_page = 148

result = extract_data_from_pdf(pdf_file_path, start_page, end_page)

# Save the extracted data to talents.json
with open("./pdfScrapper/talents.json", "w", encoding="utf-8") as json_file:
    json.dump(
        [talent.__dict__ for talent in result], json_file, ensure_ascii=False, indent=4
    )

print("Data saved to talents.json")
