import textract

# This file reads the contents of the donwloaded pdf and checks if the given string (grade) is part it, then returns the according boolean.

def pdftotext():                        # Returns the content of the pdf donwloaded last
    text = textract.process(
        'v/v.pdf',
        method='pdftotext'
    )
    text = str(text)
    text = text.replace(r"\n","\n")     # Turns incorrectly converted line breaks into working ones again
    return text
def grade_check(grade):                 # Checks if given string (grade) is part of the pdfs content
    if not grade in text:
        return False
    else:
        print("String is in file!")
        return True

text = pdftotext()
