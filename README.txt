Aplikacija se pokrece iz main.py.

Login podaci:
    - Korisnicko ime: admin
    - Lozinka: admin
Admin je jedini korisnik. moze mijenjati svoje pristupne podatke klikom na gumb "Moj profil" koji se nalazi u gornjoj traci.

Klikom na gumb "Biljke" mogu se uredivati podaci o biljkama.

Pri pokretanju programa, generira se admin korisnik, podaci za biljke (11 komada) i jedna prazna posuda, sve u pripradnim bazama podataka.

Pri kreiraju posude s biljkom (neovisno da li se radi o novoj posudi ili se popunjava postojeca prazna) automatski se pokrece inicijalno mjerenje senzora.
Pretpostavka je da su sve biljke unutar kuce, tako da se mjere vrijednosti temperature na Algebri, ali se ne uzimaju u obzir.

Klikom na gumb "Sync" na glavnoj stranici (gdje se vise sve posude) pokrece se generiranje mjerenja za sve posude koje u sebi imaju biljku.
Klikom na gumb "Sync" na stranici posude, pokrece se generiranje mjerenja samo za tu posudu (naravno samo ako u sebi ima biljku).
Klikom na bilo koji od gumba, podaci se NE osvjezavaju automatski, nego je potrebno otvoriti neku drugu stranicu i ponovo se vratiti na zeljenu.

Odabirom grafa na stranici posude, na grafu se prikazuju podaci od svih senzora, svaki na posebnom. Potrebno je nekoliko puta stisnuti neki od "Sync" gumba da bi se senzor
baza popunila i da bi grafovi poceli izgledat smislenije.
Grafovi su redom, odozgo prema dolje: vlaznost tla, ph, salinitet, razina svjetlosti i sobna temperatura.
Pri otvaranju stranice posude, graf je prazan dok se ne odabere tip grafa.

Posude se brisu tako da se prvo ukloni biljka (gumb "Isprazni" na stranici posude), a onda se odabere prazna posuda i klikne na gumb "Ukloni posudu".

Pri provjeri stanja posude postoji sansa od 2% da ce posuda biti pokvarena. Ovo se dogadja nasumicno.

Kod unosa biljaka se za svaku vrijednost unosi samo jedan podatak. Za sve vrijednosti postoje hardkodirane tolerancije (funkcija check_pot_status u plant_and_pot_database.py)
koje se u toj funkciji usporeduju sa posljednjim mjerenjima senzora.

Nadam se da sam u ovoj datoteci naveo sve bitne informacije za uspjesno koristenje PyFloraPosude aplikacije.
