# Tapahtumakalenteri
### Tietokantasovellus harjoitustyö - syksy 2021

> ##### Sovellus Herokussa
>
> * Voit luoda sovelluksessa oman käyttäjätunnuksen
> * Voit myös testata admin-tunnusta:
>
>> käyttäjätunnus: **admin**
>>
>> salasana: **salakana**
>> 
>
> - linkki sovellukseen: <https://tapahtuu.herokuapp.com>


Harjoitustyön aiheena on tapahtumakalenteri-sovellus. Sovellukseen voi lisätä tapahtumia ja selata niitä.
Jokaisella tapahtumalla on kategoria (teatteriesitys, peli-ilta, siivoustalkoot jne.) ja tapahtuma-aika
sekä -paikka. Tapahtuman voi määrittää julkiseksi tai yksityiseksi, jolloin se näkyy vain määrätyille käyttäjille.

Sovelluksessa tulee olemaan
kolme erilaista käyttäjäroolia:

* vierailija
* rekisteröitynyt käyttäjä
* ylläpitäjä

**Vierailija** voi selata kalenterissa olevia tapahtumia.

**Rekisteröitynyt käyttäjä** voi myös lisätä kalenteriin tapahtumia ja kirjoittaa tapahtumiin kommentteja. Rekisteröitynyt
käyttäjä voi lisäksi ilmoittaa osallistuvansa tiettyyn tapahtumaan ja lähettää kutsuja muille rekisteröityneille käyttäjille.
Rekisteröitynyt käyttäjä voi poistaa kalenterista itse lisäämänsä tapahtuman.

**Ylläpitäjällä** on samat oikeudet kuin rekisteröityneellä käyttäjällä ja tämän lisäksi ylläpitäjä voi poistaa
kalenterista myös muiden lisäämiä tapahtumia ja kommentteja.

## Aikataulun puitteissa valmistunut versio

Joitain suunniteltuja ominaisuuksia jäi pois, kuten ryhmien luominen ja siihen liittyvä tapahtumien näkyvyyden rajoittaminen.
Tapahtumilla ei myöskään ole varsinaisesti eri kategorioita, joihin ne jaettaisiin vaan vain sanallinen kuvaus tapahtumasta.

Ominaisuus, jota alkuperäisessä suunnitelmassa ei ollut, mutta julkaistuun versioon tuli, on viestien lähettäminen toisille käyttäjille.

## Jatkokehitys

Kurssi on päättynyt ja jatkan sovelluksen kehittämistä omaksi ilokseni ja harjoittelumielessä.
Uusia ominaisuuksia saattaa ilmestyä silloin tällöin. Jos on kiinnostusta ja ideoita tai parannusehdotuksia, ole hyvä ja
hyppää kelkkaan! Esitä ideasi tai tee pull request.

### Parannettavaa ja jatkokehitysideoita

* Tekstikenttien muotoilussa tapahtuma- ja viestilomakkeissa on parannettavaa
* käyttöliittymän ulkoasu ja käytettävyys ovat jokseenkin kömpelöitä
* koodissa on paljon refaktoroinnin ja siistimisen varaa
* tapahtumakutsujen ja viestien poistomahdollisuus
* ryhmien muodostaminen
