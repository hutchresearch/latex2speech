


# Check if there is a corresponding bib file
def check_bib(bib_name, bib_holder):
    if bib_name in bib_holder:
        print("There is!")
        bib_file = str(bib_holder.get(bib_name)[0], 'utf-8')
        print(bib_file)
        bib = "Yes"
        return bib
    else:
        print(" There is no corresponding bibliography found. ")
        return " There is no corresponding bibliography found. "