import requests, json
import fitz

with open('cookies.txt', 'r') as f: auth = f.readline()
headers = {
    'Authorization': auth
}

class metadata:
    def __init__(self, isbn):
        self.response = requests.get(f'https://www.cloudschooling.it/mialim2/api/v1/book/sommari/{isbn}/', headers=headers).json()
        self.toc = []

    def get_book_info(self):
        title = self.response['opera']['nome']
        autore = self.response['opera']['autore']
        return title, autore

    def get_toc(self, sezione, level):
        sub_toc = []
        sub_toc.append([level,sezione['titolo'],int(sezione['pagina'])])
        for sez in sezione['children']:
            sub_toc.extend(self.get_toc(sez, level+1))
        return sub_toc

def get_book_pdf(self):
    response = requests.get(f'https://www.cloudschooling.it/mialim2/api/v1/book/pdf/{self}/', headers=headers)
    pdf_url = response.json()['url']
    return pdf_url

def download_book(pdf_url, title, toc):
    import fitz
    download_obj = requests.get(pdf_url).content
    with open(f'{title}.pdf', 'wb') as pdf:
        pdf.write(download_obj)
    pdffile = fitz.Document(f'{title}.pdf')
    pdffile.set_toc(toc)
    pdffile.save(f'{title}_.pdf')


if __name__ == '__main__':
    isbn = input('Enter the book url: \n').split('/')[5]
    meta = metadata(isbn)
    for i in meta.response['sezioni']:
        meta.toc.extend(meta.get_toc(i,1))
    title, autore = meta.get_book_info()

    print('[+] Book Found:\n', title, '-', autore)
    pdf_url = get_book_pdf(isbn)
    download_book(pdf_url, title, meta.toc)
