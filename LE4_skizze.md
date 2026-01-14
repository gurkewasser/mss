# Lösungsskizze LE4: Szenario-Analyse & Klimaresilienz des Zürcher ÖV-Netzes


## 1. Kontext & Verbindung zu LE 1-3
Während wir in LE3 das kurzfristige operative Verhalten bei einer bestehenden Baustelle simuliert haben, adressiert LE4 die **Ursache** solcher Störungen im langfristigen Kontext.
**Die These:** Durch den Klimawandel (Hitze/Starkregen) häufen sich ungeplante "Notfall-Baustellen" (z.B. Gleisverwerfungen), was die Systemstabilität massiv gefährdet. Wir nutzen einen **Impact-Assessment-Ansatz** (ähnlich CLIMADA).


---


## 2. Fragestellung & Szenarien
**Leitfrage:** *Wie verändert sich das Risikoprofil (Sachschaden & Betriebsunterbruch) des Zürcher Tramnetzes bis 2050 unter extremen Klimaszenarien?*


**Gewählte Klimaszenarien (IPCC / CH2018):**
* **Szenario A (Konsequenter Klimaschutz / RCP 2.6):** Einhaltung der Pariser Ziele, Stabilisierung des Klimas.
* **Szenario B (Hochemissions-Szenario / RCP 8.5):** Ungebremster Ausstoss (Worst-Case). Massive Zunahme von Tropennächten und Hitzetagen (>30°C) in Zürich.
*(Anmerkung: RCP 8.5 gilt heute nicht mehr als "Business as Usual", sondern als Risiko-Obergrenze.)*

> **Quellen Klimaszenarien:**
> - NCCS (2018): *Schweizer Klimaszenarien CH2018*. National Centre for Climate Services. URL: https://www.nccs.admin.ch/nccs/de/home/klimawandel-und-auswirkungen/schweizer-klimaszenarien.html
> - MeteoSchweiz, ETH Zürich, Universität Bern et al. (2018): *CH2018 – Klimaszenarien für die Schweiz*. Technischer Bericht. URL: https://www.sz.ch/public/upload/assets/74988/Klimaszenarien_fuer_die_Schweiz.pdf


---


## 3. Schrittweise Lösungsstrategie
Wir modellieren die Risiko-Kette: **Hazard (Gefahr) → Exposure (Werte) → Vulnerability (Verletzlichkeit) → Impact (Schaden).**


### Schritt A: Hazard (Gefährdung)
Wir fokussieren uns auf zwei klimabedingte Stressfaktoren für die Infrastruktur:
1.  **Extreme Hitze (Hitzetage > 30°C):**
    * *Mechanismus:* Thermische Ausdehnung der Schienen führt zu Gleisverwerfungen ("Gleis-Buckel").
    * *Folge:* Sofortige Sperrung und Notfall-Baustelle (siehe LE1).
2.  **Starkniederschlag (100-jährliches Ereignis):**
    * *Mechanismus:* Überflutung von tiefliegenden Haltestellen (z.B. Bahnhofquai, Unterführungen).

> **Quellen Hazard-Daten:**
> - NCCS (2018): *Heftige Niederschläge – Kernaussagen CH2018*. URL: https://www.nccs.admin.ch/nccs/de/home/klimawandel-und-auswirkungen/schweizer-klimaszenarien/kernaussagen/heftige-niederschlaege.html
> - NCCS (2018): *CH2018 Datensätze und Datenprodukte*. URL: https://www.nccs.admin.ch/nccs/de/home/klimawandel-und-auswirkungen/schweizer-klimaszenarien/ch2018---klimaszenarien-fuer-die-schweiz/ch2018---datensaetze.html


### Schritt B: Exposure (Exposition)
Wir unterscheiden zwei Wert-Kategorien (Assets), um die Konsistenz zwischen Sachschaden und Betriebsausfall zu gewährleisten:
1.  **Physische Assets (Sachwert):** Tramgleise (CHF pro km), Weichen, Fahrleitungen.
2.  **Operative Assets (Ertragswert):** Ticket-Einnahmen und volkswirtschaftlicher Nutzen pro Betriebsstunde.

> **Quellen Infrastruktur/Exposition:**
> - ZVV (2024): *Geschäftsbericht 2023*. Zürcher Verkehrsverbund. URL: https://geschaeftsbericht.zvv.ch
> - ZVV (2025): *ZVV-Geschäftsjahr 2024: Mehr Fahrgäste und höheres Defizit* (Medienmitteilung). URL: https://www.zvv.ch/de/ueber-uns/zuercher-verkehrsverbund/medien/medienmitteilungen/2025/2025-06-20_zvv-geschaeftsbericht-2024.html
> - Stadt Zürich / VBZ (2024): *VBZ Fakten 2024*. URL: https://www.stadt-zuerich.ch/content/dam/vbz/de/microsite/geschaeftsbericht/VBZ-Fakten-2024.pdf
> - Kanton Zürich (2023): *ZVV-Strategiebericht 2024–2027*. URL: https://www.zh.ch/content/dam/zhweb/bilder-dokumente/organisation/volkswirtschaftsdirektion/zvv/2024-2027-zvv-strategiebericht.pdf


### Schritt C: Vulnerability (Verletzlichkeit)
Wir definieren getrennte Schadensfunktionen für Sachschaden und Betriebsausfall:


| Gefahren-Level | Impact 1: Physischer Schaden (Reparaturkosten) | Impact 2: Betrieblicher Ausfall (Service-Level) |
| :--- | :--- | :--- |
| **Hitze 30°C** | 0% (Wartung im Rahmen) | Langsamfahrstellen (Verspätung ↑) |
| **Hitze 35°C** | 5% Wahrsch. für Gleisbruch (Kosten: 50k CHF) | **Totalsperrung** für 2 Tage (Notfall-Baustelle) |
| **Hochwasser 50cm** | Reinigungskosten & Elektronik-Ersatz (Hoch) | **Totalsperrung** bis Wasserabfluss + 1 Tag |

> **Quellen Verletzlichkeit / Ingenieurtechnische Grundlagen:**
> - SBB (2020): *Ob brütende Hitze oder Regenguss: Sicherheit geht vor*. SBB News. URL: https://news.sbb.ch/artikel/99013/ob-bruetende-hitze-oder-regenguss-sicherheit-geht-vor
> - SBB (2025): *Hitze im Griff: So meistert die SBB die Herausforderungen des Sommers*. SBB Media Dossier. URL: https://news.sbb.ch/medien/dossiers/dossier/122743/hitze-im-griff-so-meistert-die-sbb-die-herausforderungen-des-sommers
> - Plattform J (2025): *So kämpfen die SBB gegen Hitze-Verformungen der Schienen*. URL: https://www.plattformj.ch/artikel/234200/


### Schritt D: Risiko-Metriken (Die Simulation)
Wir simulieren 10'000 probabilistische Jahre (Monte Carlo), um nicht nur den Durchschnitt, sondern die Extreme zu erfassen.


**Ergebniskennzahlen (KPIs):**
1.  **Expected Annual Damage (EAD):** Der durchschnittliche jährliche Schaden (Budget-Relevanz).
2.  **Probable Maximum Loss (Tail Risk):** Der Schaden, der mit 1% Wahrscheinlichkeit eintritt (z.B. ein "Jahrhundertsommer" im Jahr 2050).
    * *Relevanz:* Dies ist das eigentliche **Risiko**, das Versicherungen oder Rücklagen abdecken müssen.
3.  **Value at Risk (VaR):** Maximale Ausfalltage bei einem Extremereignis.


---


## 4. Auswertungsstrategie & Adaption
Die Analyse dient der Bewertung von Investitionen (Cost-Benefit-Analysis):


1.  **Delta-Analyse:** Vergleich des *Tail Risk* von Szenario A vs. B. (Wie viel teurer wird der "Super-GAU" 2050 ohne Klimaschutz?)
2.  **Adaptionsmassnahme:** Einbau temperaturbeständigerer Spezialstähle oder Gleisbett-Begrünung (Kühlung).
3.  **Entscheidung:** Sind die Investitionskosten ("Cost of Adaptation") geringer als die vermiedenen Schäden im Szenario RCP 8.5 ("Avoided Risk")?


---


## 5. Datenquellen (Zusammenfassung)

### Klimadaten (Hazard)
| Quelle | Beschreibung | URL |
| :--- | :--- | :--- |
| NCCS CH2018 | Offizielle Schweizer Klimaszenarien (Hitzetage, Starkniederschlag, RCP-Szenarien) | https://www.nccs.admin.ch/nccs/de/home/klimawandel-und-auswirkungen/schweizer-klimaszenarien.html |
| CH2018 Technischer Bericht | Vollständiger Bericht mit Methodik und regionalen Auswertungen | https://www.sz.ch/public/upload/assets/74988/Klimaszenarien_fuer_die_Schweiz.pdf |
| NCCS Datensätze | Downloadbare Zeitreihen und Rasterdaten | https://www.nccs.admin.ch/nccs/de/home/klimawandel-und-auswirkungen/schweizer-klimaszenarien/ch2018---klimaszenarien-fuer-die-schweiz/ch2018---datensaetze.html |

### Infrastruktur (Exposure)
| Quelle | Beschreibung | URL |
| :--- | :--- | :--- |
| ZVV Geschäftsbericht | Finanzkennzahlen, Fahrgastzahlen, Anlagevermögen | https://geschaeftsbericht.zvv.ch |
| VBZ Fakten 2024 | Netzlängen, Fahrzeuge, Betriebskennzahlen Tram/Bus Stadt Zürich | https://www.stadt-zuerich.ch/content/dam/vbz/de/microsite/geschaeftsbericht/VBZ-Fakten-2024.pdf |
| ZVV-Strategiebericht 2024–2027 | Strategische Ziele, Investitionsplanung | https://www.zh.ch/content/dam/zhweb/bilder-dokumente/organisation/volkswirtschaftsdirektion/zvv/2024-2027-zvv-strategiebericht.pdf |
| OpenStreetMap | Netztopologie (Gleisverläufe, Haltestellen) | https://www.openstreetmap.org |

### Verletzlichkeit (Vulnerability)
| Quelle | Beschreibung | URL |
| :--- | :--- | :--- |
| SBB News: Hitze & Sicherheit | Betriebliche Massnahmen bei Extremtemperaturen | https://news.sbb.ch/artikel/99013/ob-bruetende-hitze-oder-regenguss-sicherheit-geht-vor |
| SBB Dossier: Hitze im Griff | Technische Massnahmen gegen Gleisverwerfungen | https://news.sbb.ch/medien/dossiers/dossier/122743/hitze-im-griff-so-meistert-die-sbb-die-herausforderungen-des-sommers |
| Plattform J: Hitze-Verformungen | Mechanismen thermischer Ausdehnung bei Schienen | https://www.plattformj.ch/artikel/234200/ |
