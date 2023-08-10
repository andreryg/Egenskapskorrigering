import datetime


def createEgenskapJSON(egenskaper, egenskaperIds):
    startdato = egenskaper[2]
    nvdbId = int(egenskaper[0])
    versjon = egenskaper[1]
    egenskaperListe = []
    for i,v in enumerate(egenskaper[3:]):
        egenskaperListe.append(
            {
            "typeId": int(egenskaperIds[i]), 
            "verdi": [
                v
                ],
            "operasjon": "oppdater"
            }
        )

    return {
        "gyldighetsperiode": {
            "startdato": startdato
            },
        "validering": {
            "lestFraNvdb": str(datetime.datetime.now()).replace(" ", "T").split(".")[0]
            },
        "typeId": 37,
        "nvdbId":nvdbId,
        "versjon": int(versjon),
        "egenskaper":egenskaperListe
        }