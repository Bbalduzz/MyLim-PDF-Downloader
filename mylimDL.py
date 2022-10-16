import requests

with open('cookies.txt', 'r') as f: auth = f.readline()
headers = {
    'Authorization': auth
}

def get_book_info(isbn):
    response = requests.get(f'https://www.cloudschooling.it/mialim2/api/v1/book/sommari/{isbn}/', headers=headers).json()
    title = response['opera']['nome']
    autore = response['opera']['autore']
    return title, autore

def get_book_pdf(isbn):
    response = requests.get(f'https://www.cloudschooling.it/mialim2/api/v1/book/pdf/{isbn}/', headers=headers)
    pdf_url = response.json()['url']
    return pdf_url

def download_book(pdf_url, title):
    download_obj = requests.get(pdf_url).content
    with open(f'{title}.pdf', 'wb') as pdf:
        pdf.write(download_obj)

if __name__ == '__main__':
    isbn = input('Enter the book url: \n').split('/')[5]
    title, autore = get_book_info(isbn)
    print('Book Found:', title, '-', autore)
    pdf_url = get_book_pdf(isbn)
    download_book(pdf_url, title)