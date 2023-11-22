import re


def clean_mail(mail):
    string = mail
    new = re.sub(r'\s', '', string)
    new = re.sub(r'[.]p.{0,4}$', '.pl', new)
    new = re.sub(r'[.]c.{0,4}$', '.com', new)
    if re.match(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b", new):
        return new
    else:
        return "not_email"


if __name__ == '__main__':
    mail = 'man.compl@compl.p\l'
    mail1 = 'sk utk    a@compl.cor'
    print(mail)
    print(mail1)
    print(clean_mail(mail))
    print(clean_mail(mail1))
