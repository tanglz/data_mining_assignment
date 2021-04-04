# transfer the letters in the name, first letter uppercase, the other letters are lowercase
def first_letter_uppercase(name):
    new_name = ''
    index = 0
    for letter in name:
        if index > 0:
            letter = letter.lower()
        new_name = new_name + letter
        index = index + 1
    return new_name


def load_txt(filename):
    try:
        with open(filename, encoding="cp1252") as f:
            content = f.read()
        return content
    except Exception:
        print(filename)
        return ""


def exclusive_word_list():
    e_l = ['Hi', 'Yes', 'No', 'Yeah', 'Hello', 'Hey', 'Mr', 'Miss', 'Mis', 'Mr.', 'Oh', 'Okay', 'Ok', 'The']
    return e_l
