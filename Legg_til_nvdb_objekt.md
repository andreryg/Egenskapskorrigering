For å legge til NVDB-objekter i applikasjonen krever det at følgende gjøres i følgende filer:
- app.py
  - Legg til NVDB ID til objektet i nvdbObjekter-listen.
- index.html
  - Legg til ny div i form rett over \<div class="filters"\>. Div skal inneholde input og label for hver egenskap. Id og value til input skal brukes som egenskapID i view.html. Class til div skal fortsette mønsteret.
  - Legg til input og label for objektet i \<div class="dank"\>. Value skal være samme tall som class til div for egenskapene til objektet.
- view.html
  - Legg til egenskapene som skal implementeres i egenskaperForm-objektet på form: egenskapID: 'addLabel(" label ");add____Input(___, "egenskapID")'
  - Legg til egenskapsID fra Datakatalogen i egenskaperIdForm-objekter på form: egenskapID: 'ID'
  - Legg til hva som skal vises i vegkart i nvdbObjekter-arrayet. Referer til eksisterende elementer i arrayet. 
