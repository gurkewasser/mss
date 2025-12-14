# Lösungsskizze LE4: Szenario-Analyse & Klimaresilienz des Zürcher ÖV-Netzes

**Kontext:**
Während wir in LE3 das kurzfristige Verhalten bei Baustellen simuliert haben, adressiert diese Skizze für LE4 die langfristigen Risiken durch den Klimawandel. Wir nutzen den **Integrated Assessment Approach** (z.B. mit dem Framework CLIMADA), um zu untersuchen, wie sich extreme Wetterereignisse auf die Infrastruktur auswirken.

### 1. Fragestellung & Szenarien
**Leitfrage:** *Wie entwickeln sich die wirtschaftlichen Schäden und Betriebsausfälle des Zürcher Tram- und Busnetzes bis zum Jahr 2050 unter verschiedenen Klimaszenarien (Hitze & Starkregen)?*

**Gewählte Szenarien (IPCC):**
* **Szenario A (Status Quo / RCP 2.6):** Einhaltung der Klimaziele, moderate Erwärmung.
* **Szenario B (Business as Usual / RCP 8.5):** Starke Erwärmung, Zunahme von Hitzetagen (>30°C) und 100-jährlichen Hochwassern.

### 2. Schrittweise Lösungsstrategie
Wir folgen dem Standard-Vorgehen für Naturgefahren-Modellierung (Hazard, Exposure, Vulnerability).

**Schritt A: Hazard (Gefährdung) definieren**
* Wir laden probabilistische Gefahrenkarten für Zürich.
* *Gefahr 1:* **Hitze**. Fokus auf Tage >30°C (Gleisverwerfungen bei Trams).
* *Gefahr 2:* **Überschwemmung**. Fokus auf Überflutung von Verkehrsknotenpunkten (z.B. Bahnhofplatz, Bürkliplatz) durch Starkregen.

**Schritt B: Exposure (Exposition) kartieren**
* Wir repräsentieren das ÖV-Netz nicht als Agenten, sondern als **Assets** (Vermögenswerte).
* *Assets:* Tramgleise (km), Fahrleitungen, Haltestellen-Infrastruktur.
* Wir weisen jedem Asset einen monetären Wert zu (z.B. 1 km Tramgleis = 5 Mio. CHF).

**Schritt C: Vulnerability (Verletzlichkeit) modellieren**
* Wir definieren **Schadensfunktionen (Impact Functions)**, die den Grad der Zerstörung oder des Betriebsausfalls beschreiben.
* *Beispiel Funktion:* Wenn Temperatur > 35°C → Wahrscheinlichkeit für Gleisschaden = 20% → Betriebsstopp für 2 Tage.
* *Beispiel Funktion:* Wenn Wasserstand > 20cm → Busse können nicht passieren → Ausfall.

**Schritt D: Risiko-Berechnung (Simulation)**
* Wir nutzen das Python-Framework **CLIMADA** (oder eine vereinfachte Monte-Carlo-Simulation), um tausende "Jahre" zu simulieren.
* Ergebnis: "Jahresdurchschnittlicher Schaden" (Annual Expected Damage) in CHF und "Ausfalltage pro Jahr".

### 3. Auswertungsstrategie
Die Ergebnisse werden nicht als Zeitreihe, sondern als Verteilung und Risikokennzahl ausgewertet:

1.  **Vergleich der Szenarien:** Wie viel höher sind die kumulierten Schäden im Szenario RCP 8.5 im Vergleich zu RCP 2.6 bis 2050?
2.  **Kosten-Nutzen-Analyse von Massnahmen:**
    * *Massnahme:* Einbau hitzeresistenterer Gleise oder Erhöhung von Haltestellen (Investitionskosten).
    * *Bewertung:* Lohnt sich die Investition im Vergleich zu den vermiedenen Schäden (Adaptierungsmassnahmen).
3.  **Backtest / Validierung:**
    * Wir vergleichen die simulierten Schäden mit historischen Daten der VBZ (z.B. Schäden durch das Unwetter im Juli 2021 in Zürich) um die Parameter der Schadensfunktionen zu kalibrieren.

### 4. Identifikation der Datenquellen
Für die Umsetzung würden folgende Quellen genutzt:

* **Hazard (Klima):**
    * MeteoSchweiz (Klimaszenarien CH2018).
    * BAFU (Gefahrenkarte Oberflächenabfluss Schweiz).
* **Exposure (Assets):**
    * OpenStreetMap (Export der Liniennetze und Infrastruktur).
    * Geschäftsberichte ZVV/VBZ (für Kostenschätzungen der Infrastruktur).
* **Vulnerability:**
    * Ingenieur-Studien zur Hitzebeständigkeit von Schienenstahl.
    * Historische Ausfallstatistiken der VBZ (Open Data Stadt Zürich).