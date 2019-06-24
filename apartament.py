import requests
from bs4 import BeautifulSoup


articole = []
linkHolder = []
descriptionHolder = []

base = "https://www.olx.ro/imobiliare/apartamente-garsoniere-de-inchiriat/2-camere/bucuresti/?search%5Bfilter_float_price%3Ato%5D=310&search%5Bprivate_business%5D=private&page="
filename = "apartamentProprietar310.csv"
filename2 = "apartamentProprietarAnimal310.csv"
headers = "titlu, pret, link\n"
# I used utf-8 since my language gave some errors and was forced to convert it
f = open(filename, "w", encoding='utf-8')
f2 = open(filename2, "w", encoding='utf-8')
f.write(headers)
f2.write(headers)

for pagina in range(1, 10):
    # We have to reset i to 0 for every changed page
    i = 0
    print(pagina)
    result = requests.get(base+str(pagina))
    src = result.content
    soup = BeautifulSoup(src, 'html.parser')
    container = soup.find_all("tr", {"class": "wrap"})
    for anunt in container:
        # Titlu
        titlu = anunt.strong.text
        # Pret
        pret_container = anunt.find_all("p", {"class": "price"})
        pret = pret_container[0].text
        # Link
        link_container = anunt.find_all("a", {"class": "link"})
        link = link_container[0].attrs["href"]

        storia_container = anunt.find_all("span", {"class": "storia_label"})
        if(storia_container):
            continue
        else:
            # articole.extend([titlu, pret, link])
            linkHolder.extend([link])
            f.write(titlu.replace(",", "|") + "," +
                    str(pret.replace("\n", " ")) + "," + link + "\n")
            result2 = requests.get(link)
            soup2 = BeautifulSoup(result2.content, "html.parser")
            container2 = soup2.find_all("div", {"id": "textContent"})
            # This for will enter in every article and search for keywords in my case "Animal"
            for animal in container2:
                descriptionHolder.append(animal.text)
                for cuvant in descriptionHolder[i].split():
                    if(cuvant == "animale" or cuvant == "animal" or cuvant == "Animal" or cuvant == "Animale" or cuvant == "catel" or cuvant == "catei"):
                        print(descriptionHolder[i])
                        print("---------------------------------------------")
                        f2.write(titlu.replace(",", "|") + "," +
                                 str(pret.replace("\n", " ")) + "," + linkHolder[i] + "\n")
                        # articole.append(animal.text)
        i += 1
