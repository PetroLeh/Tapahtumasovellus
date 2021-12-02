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
>> Tosin tässä vaiheessa ei vielä ole paljon testattavaa...
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
