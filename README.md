# 📡 GPS Asset Tracker — Integratieproject 2025-2026

> **Low-cost & low-power locatietracking van assets op bouwwerven in heel België.**

---

## 📋 Projectbeschrijving

Als bouwbedrijf staan er talloze assets verspreid over werven: pompen, leidingrekken, dataloggers, … Veel van deze toestellen hebben geen eigen voedingsbron, waardoor hun locatie moeilijk te volgen is.

Dit project bouwt een **Proof of Concept (PoC)** voor een slimme, goedkope GPS-tracker die:

- 📍 De locatie van assets in real-time bijhoudt
- 📡 Data verstuurt via **MQTT**
- 🗺️ Alles visualiseert op een **Grafana-dashboard**
- 🔋 Energiezuinig werkt zonder vaste voedingsbron
- ☔ Bestand is tegen weersomstandigheden (waterdichte behuizing)

Een afwijking van ~50 meter is ruim voldoende om te bepalen op welke werf of in welke zone een toestel zich bevindt.

---

## 👥 Het Team

| Naam | GitHub Account | Rol / Focusgebied |
| :--- | :--- | :--- |
| Lotfi Lamzira | [@Lotfi-lamzira](https://github.com/Lotfi-lamzira) | Deelnemer |
| Quinten van Nunen | [@quintenvannunen](https://github.com/quintenvannunen) | Deelnemer |
| Edric Yi Ling | [@LingLing404](https://github.com/LingLing404) | Deelnemer |
| Hadeel Khalil | [@Upsting](https://github.com/Upsting) | Deelnemer |

---

## 🛠️ Technologieën

| Categorie | Tools & Technologieën |
| :--- | :--- |
| **Hardware** | GPS-module, microcontroller, sensoren, waterdichte behuizing |
| **Communicatie** | MQTT |
| **Dashboard** | Grafana |
| **Programmeertalen** | C++, Python, HTML/CSS |
| **Development tools** | VS Code, GitHub Desktop |

---

## 🏗️ Architectuur

```
[GPS Tracker] ──MQTT──► [Broker] ──► [Backend / Data verwerking] ──► [Grafana Dashboard]
```

---

## 🚀 Installatie & Gebruik

> ⚠️ *Dit onderdeel wordt aangevuld naarmate het project vordert.*

---

## 📁 Projectstructuur

```
Integratieproject-GPSTracker-Eind-2026/
├── Integratie-Project/     # Broncode en configuraties
├── README.md               # Dit bestand
└── .gitattributes
```

---

## 📅 Planning & Bijdragen

Individuele bijdragen zijn terug te vinden in de **[Commit History](../../commits/main)**. We werken volgens de Git-flow methodiek waarbij ieder teamlid verantwoordelijk is voor zijn eigen deelopdracht.

---

## 👨‍🏫 Begeleiding

| Naam |
| :--- |
| Thomas De Witte |
| Hans Van Gompel |
| Petia Minnebach |
| Vincent Peters |
| Liesje Tops |

📍 **Locatie:** KdG Hoboken — IoT Lab