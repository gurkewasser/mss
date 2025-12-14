# Mini Challenge: Systemanalyse einer innerstädtischen Baustelle (mss – LE 1)

## 1. Projektkontext
**Von der vagen Sorge zur Systemkarte**

Der öffentliche Verkehr (ÖV) ist ein komplexes, dynamisches System. Eine Baustelle stellt darin eine Störung dar, die weit über den unmittelbaren Ort des Geschehens hinauswirkt. Sie verändert Verkehrsflüsse, Fahrzeiten, das Fahrgastverhalten und die operative Effizienz des ÖV.

### Forschungsleitende Fragen
> **Hauptfrage:** Wie beeinflusst eine temporäre Baustelle auf einer Hauptverkehrsachse die Pünktlichkeit und Auslastung von Bus- und Tramlinien im Stadtverkehr?

> **Erweiterte Frage:** Welchen Einfluss hat eine 10-minütige Taktverdichtung während der Stosszeiten auf die CO2-Emissionen und die Passagierzufriedenheit?

---

## 2. Definition der Systemgrenzen
Das Modell konzentriert sich auf den innerstädtischen Personenverkehr. Regionale Linien oder der Gesamtverkehr werden ausgeblendet, um die Komplexität auf die relevanten Wechselwirkungen zu reduzieren.

| Dimension | Abgrenzung / Definition |
| :--- | :--- |
| **Räumlich** | Ein städtisches Quartier (z. B. Innenstadt) mit **1 Buslinie** (von Baustelle betroffen) und **1 Tramlinie** (Ausweichoption). |
| **Zeitlich** | Fokus auf den täglichen **Berufsverkehr (7–9 Uhr)**. Der Simulationszeitraum erstreckt sich über mehrere Tage, um Lerneffekte/Anpassungen zu erfassen. |
| **Akteure** | Busse, Trams, Fahrgäste (Pendler), Stadtverwaltung/Bauamt. |

---

## 3. Artefakt: Cluster-Systemkarte & Gedankenprozess
*Visualisierung von Schlüsselfaktoren und deren Wechselwirkungen.*

In einem ersten Schritt wurden die Einflussfaktoren gesammelt und thematisch gruppiert, um die Struktur des Systems zu erfassen.

<img width="633" height="677" alt="image" src="https://github.com/user-attachments/assets/796d06f3-6ce0-4ccd-b751-7a900d464334" />


### Identifizierte Cluster
* **Cluster 1: Infrastruktur & Verkehr** (Baustelle, Strassenkapazität, Verkehrsaufkommen, Stauintensität)
* **Cluster 2: Betrieb & Angebot** (Busfrequenz, Fahrzeiten, Anschlusszeiten, Verspätungen)
* **Cluster 3: Nutzerverhalten** (Fahrgastzufriedenheit, Modal-Split, Anpassungsverhalten)
* **Cluster 4: Stadtplanung & Feedback** (Baustellenmanagement, Kommunikation, Taktung)

### Wesentliche Wirkungsketten (Hypothesen)
1.  **Kaskadeneffekt:** Baustelle ↓ → Strassenkapazität ↓ → Stau ↑ → Busfahrzeit ↑ → Pünktlichkeit ↓ → Zufriedenheit ↓
2.  **Verlagerung:** Zufriedenheit ↓ → Busnachfrage ↓ → Tramnachfrage ↑
3.  **Rebound:** Tramnachfrage ↑ → Tram-Auslastung ↑ → Wartezeit ↑

---

## 4. Artefakt: Stakeholder Map
Basierend auf der Cluster-Analyse agieren folgende Hauptakteure im System:

* **Fahrgäste:** Nutzenmaximierer, die Verkehrsmittel basierend auf Wartezeit, Pünktlichkeit und Komfort wählen.
* **Bus-Betrieb:** Direkt abhängig von der Strasseninfrastruktur; reagiert sensibel auf Stau.
* **Tram-Betrieb:** Verfügt über eigenes Trassee (fahrzeitstabil), ist aber kapazitätsbeschränkt (Auslastung).
* **Stadt / Verkehrsbetriebe:** Regulatoren, die durch Baustellenmanagement, Umleitungen und Taktverdichtungen steuernd eingreifen.

---

## 5. Artefakt: Causal Loop Map (Kausalschleifen-Diagramm)
*Identifikation der dynamischen Rückkopplungen.*

Das Kausalschleifen-Diagramm formalisiert die Beziehungen und zeigt, warum das System zu Instabilität neigt.

<img width="1224" height="816" alt="image" src="https://github.com/user-attachments/assets/8b341bf1-84d7-4abd-b61f-2281092d351b" />


### Hauptvariablen
`Baustellenaktivität` | `Strassenkapazität` | `Stauintensität` | `Busfahrzeit` | `Pünktlichkeit Bus` | `Fahrgastzufriedenheit` | `Modal-Split (Tramanteil)` | `Tram-Auslastung`

### Systemdynamik: Die Schleifen

#### Verstärkende Schleifen (R – Reinforcing)
*Destabilisierende Faktoren, die Probleme eskalieren lassen.*

* **R1: Nachfrageverschiebung (Teufelskreis der Unzufriedenheit)**
    Baustelle ↑ → Busfahrzeit ↑ → Pünktlichkeit ↓ → Zufriedenheit ↓ → Busnachfrage ↓ → Tramnachfrage ↑ → Tram-Auslastung ↑ → *(Implizit: Tram-Komfort ↓)* → Zufriedenheit (gesamt) ↓
    *Wirkung:* Die Unzufriedenheit im Bus verlagert sich auf das Tram, überlastet dieses und senkt die Gesamtzufriedenheit im System weiter.

* **R2: Verkehrsüberlastung**
    Baustelle ↑ → Stau ↑ → Durchschnittsgeschwindigkeit ↓ → Rückstau ↑ → zusätzliche Verzögerungen ↑
    *Wirkung:* Klassische Stau-Spirale. Je dichter der Verkehr, desto geringer der Durchfluss.

#### Abschwächende Schleifen (B – Balancing)
*Stabilisierende Faktoren oder Management-Eingriffe.*

* **B1: Betriebsanpassung**
    Verspätung ↑ → Betrieb passt Fahrplan / Takt an → Busfrequenz ↑ → Wartezeit ↓ → Zufriedenheit ↑
    *Wirkung:* Versucht, die Servicequalität durch Ressourceneinsatz wiederherzustellen.

* **B2: Kommunikation & Ausweichen**
    Baustelle ↑ → Kommunikationsmassnahmen ↑ → Fahrgäste planen Umstieg früher / anders → Systemlast verteilt sich → Stauentlastung ↓
    *Wirkung:* Information führt zu einer besseren Verteilung der Last und entlastet den Engpass.
