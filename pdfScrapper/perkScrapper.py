import json
import re


text = """
Celna
Strzelając z tej broni, łatwo trafić w cel. W takiej sytuacji zyskujesz premię +10 do Testu trafienia.

Dekoncentrująca
Ze względu na swoją niebezpieczną naturę broń Dekoncentrująca może zmuszać wroga do cofania się. Zwykle działa podobnie 
jak bicz. Zamiast zadawać Obrażenia, udany atak bronią Dekoncentrującą może zmusić przeciwnika do cofnięcia się o 1 metr na 
każdy PS, o który wygrywasz Test Przeciwstawny.

Druzgocząca
Pewne bronie są po prostu ogromne albo zadają straszliwe obrażenia ze względu na swoją masę lub formę. Po udanym trafieniu 
dodaj do wszelkich Obrażeń zadanych przez broń Druzgoczącą 
wynik na kostce jedności w rzucie na atak. Broń Tępa nigdy nie 
może być także Druzgoczącą (cecha Tępa jest nadrzędna).

Łamacz mieczy
Pewne rodzaje broni przeznaczone są do unieruchamiania innych, 
a czasem nawet są w stanie je złamać. Jeśli uzyskasz Trafienie Krytyczne, broniąc się przed atakiem broni siecznej, możesz ją unieruchomić, zamiast korzystać z efektów Trafienia Krytycznego.
Jeśli się na to zdecydujesz, wykonaj Test Przeciwstawny Siły, dodając swój PS z poprzedniego Testu Walki Wręcz. Jeśli Test się 
uda, twój przeciwnik upuszcza ostrze, które zostaje wyrwane mu 
z dłoni. Jeśli uzyskasz Zdumiewający Sukces, nie tylko rozbrajasz 
przeciwnika, ale siła twojego manewru powoduje także złamanie 
ostrza jego broni, o ile nie ma ona Zalety Niełamliwa. Jeśli Test się 
nie uda, twój przeciwnik uwalnia ostrze i może walczyć normalnie.

Nadziewająca
Broń Nadziewająca może zabić jednym czystym ciosem. Zadaje 
ona Trafienie Krytyczne przy dowolnej wartości rzutu podzielnej 
przez 10 (np. 10, 20, 30 itd.), a także przy dubletach (tj. 11, 22, 
33), jeśli wynik rzutu był równy lub niższy od poziomu odpowiedniego Testu w walce.
Jeśli cecha Nadziewająca charakteryzuje użytą broń dystansową, 
oznacza to, że amunicja głęboko utkwiła w ciele trafionej ofiary. 
Usunięcie takich strzał lub bełtów wymaga udanego Wymagającego (+0) Testu Leczenia. Wyjęcie pocisków z broni prochowej wymaga już zabiegu chirurgicznego (patrz Talent Chirurgia
w Rozdziale 4: Umiejętności i Zdolności). Postać nie może 
wyleczyć jednej ze swoich Ran za każdy pocisk (prochowy lub 
tradycyjny) pozostający w jej ciele.

Niełamliwa
Broń jest wyjątkowo dobrze wykonana lub do jej konstrukcji użyto szczególnie mocnego materiału. W większości okoliczności ta 
broń nie złamie się, nie ulegnie korozji ani nie stępi się.

Ogłuszająca
Broń Ogłuszająca szczególnie dobrze nadaje się do sprowadzania 
wrogów do parteru. Jeśli trafisz w głowę bronią Ogłuszającą, wykonaj Test Przeciwstawny Siły przeciw Odporności trafionego 
przeciwnika. Jeśli wygrasz Test, cel dostaje Stan Oszołomienie.

Parująca
Broń Parująca przeznaczona jest do parowania ataków. Jeśli 
posługujesz się taką bronią, dostajesz premię +1 PS do każdego 
Testu Broni Białej, gdy parujesz atak.

Pistolety
Można używać tej broni do atakowania w walce w zwarciu.

Plącząca
Broń Plącząca ma zazwyczaj długie łańcuchy z obciążnikami na 
końcach, przez co bardzo trudno skutecznie bronić się przed nią 
parowaniem. Testy Broni Białej przeciwko atakowi broni Plączącej obciążone są karą -1 PS, ponieważ parowane ciosy owijają się 
wokół ostrzy lub górnych krawędzi tarcz.

Precyzyjna
Tą bronią łatwo trafić w cel. Zyskujesz premię +1 PS do każdego 
udanego Testu podczas ataku tą bronią.

Prochowa
Huk wystrzałów, po którym następują kłęby dymu i zamieszanie, 
może być przerażający. Jeśli jesteś celem broni prochowej, musisz wykonać udany Przeciętny (+20) Test Opanowania, inaczej 
otrzymujesz Stan Panika, nawet jeśli strzał spudłuje.

Przebijająca
Aby ustalić Obrażenia zadane na skutek trafienia bronią Przebijającą, można wykorzystać wynik rzutu kostką jedności albo PS, 
cokolwiek jest wyższe. Na przykład, jeśli wyrzucisz 34 w Teście 
ataku, a wynik celu wynosił 52, możesz użyć PS, który w tym 
przypadku jest równy 2, albo wyniku rzutu jedności, czyli 4. Broń 
Tępa nigdy nie może być także Przebijającą (cecha Tępa jest nadrzędna).

Przekłuwająca
Ta broń niezwykle skutecznie przebija się przez pancerz. Punkty 
Pancerza z warstw niemetalowych są ignorowane. W przypadku 
wszystkich pozostałych pancerzy pomijany jest ich pierwszy PP.

Rąbiąca
Broń rąbiąca ma ciężkie ostrze, które z przerażającą łatwością 
przecina pancerze. Jeśli trafisz przeciwnika, uszkadzasz trafiony 
fragment pancerza lub tarczy za 1 punkt. Jednocześnie normalnie 
ranisz cel.

Szybka
Szybka broń uderza z taką prędkością, że parowanie ciosu w zasadzie nie wchodzi w grę. Przeciwnik zostaje przebity, zanim 
zdoła zareagować. Bohater posługujący się Szybką bronią może 
zdecydować się na atak poza normalną sekwencją Inicjatywy, 
atakując pierwszy, ostatni lub w innej, wybranej przez siebie 
kolejności.
Co więcej, wszystkie Testy obrony Bronią Białą przeciwko Szybkiej broni obciążone są karą -10, jeśli przeciwnik korzysta z broni 
nieposiadającej Zalety Szybka. Inne Umiejętności wykorzystane 
w obronie działają normalnie. Para przeciwników z Szybką bronią 
walczy w kolejności Inicjatywy (względem siebie nawzajem), jak 
normalnie. Szybka broń nigdy nie może być także Powolną (cecha Powolna jest nadrzędna).

Tarcza (wartość)
Jeśli używasz tej broni do sparowania ataku, odpowiada to 
posiadaniu tylu Punktów Pancerza, ile wynosi (wartość) na 
wszystkich Miejscach Trafień na twoim ciele. Jeśli twoja broń 
ma Zaletę Tarcza o wartości 2 lub wyższej (czyli Tarcza 2 lub 
Tarcza 3), możesz także wykonać Test Przeciwstawny przeciwko 
nadlatującym pociskom w twoim polu widzenia.

Unieruchamiająca
Twoja broń okręca się wokół przeciwników, unieruchamiając ich. 
Każdy przeciwnik trafiony taką bronią dostaje Stan Pochwycony
z Siłą o wartości równej twojej Cesze Siła. Unieruchamiając 
przeciwnika, nie możesz używać tej broni, by próbować trafić 
go w inny sposób. Możesz zakończyć Unieruchomienie w dowolnym momencie

Wielostrzał (wartość)
Broń może oddać tyle strzałów, ile wynosi (wartość), i automatycznie przeładowuje się po każdym z nich. Gdy zostaną 
one wszystkie wykorzystane lub skończą się pociski, musisz 
całkowicie przeładować broń, stosując zwykłe zasady.

Wybuchowa (wartość)
Wszystkie postacie w promieniu tylu metrów, ile wynosi 
(wartość), od trafionego celu odnoszą obrażenia równe PS + 
Obrażenia danej broni Wybuchowej i otrzymują wszelkie Stany 
przez nią wywołane.

Ciężka
Używanie tej broni jest męczące lub trudno ją opanować. Możesz 
korzystać z Zalet broni Druzgocząca i Przebijająca tylko w Turze, 
w której wykonujesz Szarżę.

Niebezpieczna
Zdarza się broń, która niemal równie często może wyrządzić 
krzywdę posługującej się nią osobie, jak jej przeciwnikowi. Dowolny nieudany Test, w którym wypadła 9 na kości dziesiątek 
lub jedności, uznawany jest za Rzut Pechowy (więcej o Rzutach 
Pechowych w Rozdziale 5: Zasady).

Nieprecyzyjna
Opanowanie broni Nieprecyzyjnej nastręcza trudności z powodu 
jej nieporęczności lub trudnego celowania. Wykonując atak taką 
bronią, otrzymujesz karę -1 PS. Broń Nieprecyzyjna nigdy nie 
może być także Precyzyjną (cecha Nieprecyzyjna jest nadrzędna).

Powolna
Powolna broń jest nieporęczna i ciężka, przez co trudno używać 
jej prawidłowo. Bohaterowie używający Powolnej broni zawsze 
atakują ostatni w Rundzie, niezależnie od kolejności Inicjatywy. 
Co więcej, przeciwnicy zyskują premię +1 PS do każdego Testu 
obrony przed takim atakiem.

Przeładowanie (wartość)
Przeładowanie tej broni jest powolne. Przeładowanie broni obarczonej tą Wadą wymaga wykonania Wydłużonego Testu Broni 
Zasięgowej w odpowiedniej Kategorii broni i uzyskania tylu 
PS, ile wynosi (wartość). Jeśli coś zakłóci 
przeładowanie, trzeba je podjąć od początku.

Tępa
Pewne rodzaje broni nie nadają się zbytnio 
do przebijania pancerzy. W przypadku obrony przed bronią 
Tępą wszystkie PP są podwajane. Co więcej, nie obowiązuje 
w jej przypadku zasada zadawania minimum 1 Rany po udanym 
trafieniu (obrażenia mogą być 
zredukowane do 0).

"""


# Split text into blocks based on empty lines
text_blocks = re.split(r"\n\s*\n", text)

# Initialize a list to store JSON objects
json_objects = []

# Process each text block and format it as a JSON object
for i in range(0, len(text_blocks), 2):
    perk_name = text_blocks[i].strip()

    # Check if there is a corresponding description for this perk_name
    if i + 1 < len(text_blocks):
        description = text_blocks[i + 1].strip()
    else:
        description = ""  # Handle the case where description is missing

    # Replace Polish characters with their Unicode escape sequences

    # Create a JSON object
    json_obj = {"perk_name": perk_name, "description": description}

    json_objects.append(json_obj)

# Convert the list of JSON objects to a JSON array
json_data = json.dumps(json_objects, indent=4, ensure_ascii=False)

# Print or save the JSON data as needed
print(json_data)
