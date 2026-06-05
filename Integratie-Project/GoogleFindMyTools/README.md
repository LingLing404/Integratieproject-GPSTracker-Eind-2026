# GoogleFindMyTools (Met InfluxDB & Grafana Integratie)

Dit project is een uitbreiding op de tools die delen van het Google Find My Device-netwerk (Find Hub) implementeren. Hiermee kun je locatiegegevens van alle gekoppelde trackers en Android-apparaten volautomatisch ophalen, decoderen en live visualiseren op een Grafana-kaart via InfluxDB.

> [!CAUTION]
> Zorg ervoor dat je Google Chrome en Python up-to-date zijn. Als Chrome niet up-to-date is, zal het authenticatiescript **gegarandeerd niet werken**.

> [!IMPORTANT]
> Dit project draait op een **Raspberry Pi**. Voor de authenticatiestap (Google inloggen via Chrome) **moet je een monitor aansluiten op de Raspberry Pi**. Chromium op de Pi kan niet headless authenticeren — een scherm is verplicht.

---

## Vereisten & Voorbereiding

Het script vereist een moderne versie van Python 3 en een up-to-date versie van Chromium.

### Google Chromium installeren op de Raspberry Pi

1. Open een terminal op de Raspberry Pi.
2. Installeer Chromium met het volgende commando:
   ```bash
   sudo apt update && sudo apt install chromium-browser -y
   ```

3. **Mocht er een foutmelding optreden**, herstel dan de afgebroken installatie met:
   ```bash
   sudo apt --fix-broken install
   ```

4. Wacht tot dit proces klaar is en voer daarna stap 2 opnieuw uit.

---

## Installatie en Setup

### 1. Repository downloaden en map openen

Kloon de repository en navigeer naar de juiste map:

```bash
git clone https://github.com/LingLing404/Integratieproject-GPSTracker-Eind-2026
cd Integratieproject-GPSTracker-Eind-2026/Integratie-Project/GoogleFindMyTools
```

Je werkmap ziet er dan als volgt uit:

```
pi@raspberrypi:~/Integratieproject-GPSTracker-Eind-2026/Integratie-Project/GoogleFindMyTools $
```

### 2. Virtual Environment opzetten & Modules installeren

Maak een virtual environment aan om conflicten met andere Python-pakketten te voorkomen, activeer deze en installeer de vereiste bibliotheken:

```bash
# Virtual environment aanmaken
python -m venv venv

# Activeren (Raspberry Pi)
source venv/bin/activate

# Requirements installeren
pip install -r requirements.txt
pip install python-dotenv
```

---

## Database & Omgevingsvariabelen (.env)

Voordat je het script start, moet de verbinding met InfluxDB worden opgezet.

### 1. InfluxDB & Grafana Installeren

Zorg ervoor dat je InfluxDB (v2.x) en Grafana op je Raspberry Pi hebt geïnstalleerd.

* Volg de officiële documentatie voor [InfluxDB installatie](https://docs.influxdata.com/).
* Volg de officiële documentatie voor [Grafana installatie](https://grafana.com/).

### 2. `.env` bestand aanmaken

Kopieer het voorbeeld-configuratiebestand:

```bash
cp .env.example .env
```

Open het zojuist aangemaakte `.env`-bestand (bijvoorbeeld met `nano .env`) en vul je eigen InfluxDB-gegevens en tokens in:

```ini
INFLUX_URL=http://pi.local:8086
INFLUX_TOKEN=JOUW_INFLUX_API_TOKEN_HIER
INFLUX_ORG=jouw_organisatie_naam
INFLUX_BUCKET=jouw_bucket_naam
```

*Opmerking: Het `.env`-bestand staat automatisch in de `.gitignore` en zal nooit naar GitHub worden gepusht.*

---

## Gebruik & Automatische Tracking

1. Start het hoofdprogramma:
   ```bash
   python main.py
   ```

2. **Eerste keer opstarten (Authenticatie):** Er opent een Chromium-venster op de Raspberry Pi. **Zorg dat je een monitor aangesloten hebt** — zonder scherm kan dit venster niet worden weergegeven. Log hier eenmalig in met het Google-account waar de trackers aan gekoppeld zijn. *Let op: Als je Two-Factor Authentication (2FA) aan hebt staan, hou dan je telefoon bij de hand.* Zodra de authenticatie is voltooid, sluit het Chromium-venster automatisch. De inlogsessie wordt veilig lokaal opgeslagen in `Auth/secrets.json`.

3. Na de initialisatie (of bij opeenvolgende keren opstarten) hoef je alleen nog maar op **Enter** te drukken in de terminal om de tracking te starten.

### Wat gebeurt er achter de schermen?

Het script haalt de volledige lijst met gekoppelde apparaten op en start een automatische loop. Het script loopt sequentieel langs elk apparaat (bijv. *Device 1/3, Device 2/3, Device 3/3*), vraagt de meest recente locatie op bij het Google FMD-netwerk, ontcijfert de end-to-end versleutelde GPS-coördinaten en schrijft deze direct weg naar InfluxDB.

Elk uniek apparaat krijgt automatisch een eigen `device_index` toegewezen (opgeslagen in `device_index.json`), zodat ze in Grafana makkelijk uit elkaar te houden zijn.

---

## Visualisatie in Grafana (Kaart instellen)

Om de live locaties van al je trackers op een kaart te zien, koppel je InfluxDB aan Grafana.

### 1. Data Source Toevoegen

1. Open Grafana op `http://pi.local:3000`.
2. Ga naar **Connections** -> **Data sources** -> **Add data source**.
3. Kies **InfluxDB**.
4. Stel de Query Language in op **Flux**.
5. Vul de URL in (`http://pi.local:8086`), je Organisatie, Token en het standaard Bucket (bijv. `coordinaten`).

### 2. Dashboard & Geomap aanmaken

1. Maak een nieuw Dashboard aan en voeg een **Visualization panel** toe.
2. Kies in de rechterkolom onder visualisaties voor de **Geomap** weergave.
3. Gebruik onderstaande Flux-query in de editor. Deze query zorgt ervoor dat de losse meetwaarden (`latitude`, `longitude` en `device_index`) per apparaat en per exacte tijdstempel netjes worden samengevoegd (`pivot`) tot één logisch coördinaat dat Grafana kan tekenen:

```flux
from(bucket: "coordinaten")
  |> range(start: v.timeRangeStart, stop: v.timeRangeStop)
  |> filter(fn: (r) => r._measurement == "location")
  |> filter(fn: (r) => r._field == "latitude" or r._field == "longitude" or r._field == "device_index")
  |> pivot(rowKey: ["_time", "device_id"], columnKey: ["_field"], valueColumn: "_value")
  |> keep(columns: ["_time", "device_id", "device_name", "latitude", "longitude", "device_index"])
  |> group()
```

Voor meer geavanceerde instellingen en dashboards, raadpleeg de officiële gidsen:

* [Grafana Fundamentals: Get started with InfluxDB](https://grafana.com/docs/grafana/latest/fundamentals/getting-started/first-dashboards/get-started-grafana-influxdb/)
* [InfluxData: Query and visualize data in Grafana](https://docs.influxdata.com/influxdb/v2/tools/grafana/#query-and-visualize-data)

---

## Dashboard publiek toegankelijk maken via ngrok

Om het Grafana-dashboard van buitenaf te bekijken (bijvoorbeeld op je smartphone of op een andere locatie), gebruik je **ngrok** om een beveiligde publieke tunnel op te zetten.

### 1. ngrok installeren

Volg de officiële installatiegids op [https://ngrok.com/download](https://ngrok.com/download) en koppel je account met het opgegeven `ngrok authtoken`-commando.

### 2. Tunnel starten

Start een tunnel naar Grafana met het volgende commando:

```bash
ngrok http 3000
```

> [!NOTE]
> Poort `3000` is de standaardpoort van Grafana. Als je Grafana op een andere poort hebt geconfigureerd, vervang dan `3000` door de juiste poort.

ngrok geeft een publieke URL terug, bijvoorbeeld:

```
Forwarding  https://abc123.ngrok-free.app -> http://localhost:3000
```

Via die URL is je Grafana-dashboard bereikbaar vanuit de hele wereld.