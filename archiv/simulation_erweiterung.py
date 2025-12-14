import mesa
import random
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime, timedelta

# --- KONFIGURATION: REALITÄT ZÜRICH ---
# Ort: Zürich, Bahnhofstrasse (HB -> Bürkliplatz)
# Skala: 1 Zelle = ca. 10 Meter
# Länge: ca. 1.5 km = 150 Zellen
# Zeit: 1 Tick = 20 Sekunden
TICK_DURATION_SECONDS = 20 
GRID_LENGTH = 150 

# Haltestellen-Positionen (auf dem Gitter 0-150)
STOPS = {
    "Zürich HB": 5,
    "Rennweg": 50,
    "Paradeplatz": 100,
    "Bürkliplatz": 145
}

# --- 1. Agenten ---

class PassengerAgent(mesa.Agent):
    """Ein Fahrgast in Zürich."""
    def __init__(self, unique_id, model, transport_type_preference, origin_pos):
        super().__init__(model) 
        self.unique_id = unique_id
        self.transport_type = transport_type_preference 
        self.origin_pos = origin_pos
        
        # Tracking in Realzeit
        self.waiting_start_time = model.current_time
        self.waiting_minutes = 0.0
        
        self.satisfaction = 100 
        self.arrived = False
        self.has_switched = False 

    def step(self):
        if not self.arrived:
            # Wartezeit berechnen (Realzeit)
            current_wait = self.model.current_time - self.waiting_start_time
            self.waiting_minutes = current_wait.total_seconds() / 60.0
            
            # Zufriedenheit sinkt (Tram-Fahrer sind entspannter als Bus-Fahrer)
            decay_factor = 0.5 if self.transport_type == "Tram" else 0.8
            # Alle 20 Sekunden (1 Tick) sinkt die Zufriedenheit
            self.satisfaction -= (decay_factor * 0.5) 
            if self.satisfaction < 0: self.satisfaction = 0

            # --- SWITCHING LOGIC (R1 Loop) in REALZEIT ---
            # Wenn man länger als 5 Minuten wartet, wechselt man
            if self.transport_type == "Bus" and self.waiting_minutes > 5.0:
                self.switch_to_tram()

    def switch_to_tram(self):
        """Passagier läuft rüber zu den Tramgleisen."""
        self.transport_type = "Tram"
        self.has_switched = True
        self.satisfaction -= 15 # Ärger über das Wechseln (Einmalige Kosten)
        
        # Visueller Wechsel auf Spur 1 (Tramgleis)
        x, y = self.pos
        if y == 0: 
            self.model.grid.move_agent(self, (x, 1))

class VehicleAgent(mesa.Agent):
    """ZVV Bus oder Tram."""
    def __init__(self, unique_id, model, v_type):
        super().__init__(model)
        self.unique_id = unique_id
        self.v_type = v_type 
        
        # Geschwindigkeit in Zellen pro Tick (20 sek)
        # Tram = ca. 4 Zellen (40m) pro 20sek (langsamer Stadtverkehr)
        if v_type == "Tram":
            self.speed = 4 
        else:
            self.speed = 3 # Bus ist generell langsamer

    def step(self):
        x, y = self.pos
        
        # --- Baustelle am Rennweg (Zelle 50 bis 90) ---
        move_distance = self.speed
        
        if self.v_type == "Bus" and self.model.construction_active:
            # Baustelle zwischen Rennweg und Paradeplatz
            if 50 <= x <= 90: 
                # Massiver Stau: 80% Wahrscheinlichkeit, dass nichts geht
                if random.random() < 0.8: 
                    move_distance = 0 
                else:
                    move_distance = 1 # Kriechmodus

        # Bewegung (Looping Strecke für Simulation)
        new_x = (x + move_distance) % self.model.grid.width 
        self.model.grid.move_agent(self, (new_x, y))
        
        # Passagiere einsammeln (im Umkreis der neuen Position)
        # Da wir mehrere Zellen springen, müssen wir prüfen, ob wir eine Haltestelle überfahren haben
        pickup_range = range(x, x + move_distance + 1)
        
        for check_x in pickup_range:
            real_check_x = check_x % self.model.grid.width
            cell_mates = self.model.grid.get_cell_list_contents([(real_check_x, y)])
            
            for mate in cell_mates:
                if isinstance(mate, PassengerAgent) and not mate.arrived:
                    # Nimmt Passagiere mit, die den gleichen Typ haben
                    # (Auch "Wechsler", da sie ihren Typ auf Tram geändert haben)
                    if mate.transport_type == self.v_type:
                        mate.arrived = True 

# --- 2. Das Modell ---

class ZurichTransportModel(mesa.Model):
    """Simulation Bahnhofstrasse Zürich."""
    def __init__(self, num_passengers, construction_active=True):
        super().__init__()
        self.construction_active = construction_active
        
        # REALZEIT INITIALISIERUNG
        self.current_time = datetime(2025, 6, 1, 7, 30, 0) # 07:30 Uhr Morgens
        
        # Gitter: 150 Zellen lang (Bahnhofstrasse), 2 Spuren
        # Spur 0 = Strasse, Spur 1 = Tramgleis
        self.grid = mesa.space.MultiGrid(GRID_LENGTH, 2, torus=True)

        self.datacollector = mesa.DataCollector(
            model_reporters={
                "Time": lambda m: m.current_time,
                "Avg_Satisfaction": compute_avg_satisfaction,
                "Bus_Wait": lambda m: count_waiting(m, "Bus"),
                "Tram_Wait": lambda m: count_waiting(m, "Tram"),
                "Total_Switchers": count_switchers
            }
        )

        # 1. Fahrzeuge erstellen (3 Busse, 3 Trams für dichten Takt)
        for i in range(3):
            bus = VehicleAgent(f"Bus_{i}", self, "Bus")
            self.grid.place_agent(bus, (i * 40, 0)) # Verteilt auf der Strasse
            
            tram = VehicleAgent(f"Tram_{i}", self, "Tram")
            self.grid.place_agent(tram, (i * 40, 1)) # Verteilt auf Schienen

        # 2. Passagiere erstellen (nur an Haltestellen!)
        stop_locations = list(STOPS.values())
        
        for i in range(num_passengers):
            p_type = "Bus" if random.random() < 0.6 else "Tram"
            # Wähle eine zufällige Haltestelle
            start_pos = random.choice(stop_locations)
            
            a = PassengerAgent(i + 100, self, p_type, start_pos)
            
            # Busse auf y=0, Trams auf y=1
            y_pos = 0 if p_type == "Bus" else 1
            self.grid.place_agent(a, (start_pos, y_pos))

    def step(self):
        self.datacollector.collect(self)
        self.agents.shuffle_do("step")
        
        # Zeit voranschreiten lassen
        self.current_time += timedelta(seconds=TICK_DURATION_SECONDS)

# --- Hilfsfunktionen ---

def compute_avg_satisfaction(model):
    passengers = [a for a in model.agents if isinstance(a, PassengerAgent)]
    if not passengers: return 0
    return sum([a.satisfaction for a in passengers]) / len(passengers)

def count_waiting(model, v_type):
    return sum([1 for a in model.agents 
                if isinstance(a, PassengerAgent) 
                and a.transport_type == v_type 
                and not a.arrived])

def count_switchers(model):
    """Zählt, wie viele Leute bisher umgestiegen sind."""
    return sum([1 for a in model.agents 
                if isinstance(a, PassengerAgent) and a.has_switched])

# --- 3. Ausführung ---

if __name__ == "__main__":
    # Simulation: 30 Minuten Pendlerverkehr
    # 30 min * 60 sek / 20 sek/tick = 90 Ticks
    print("Starte Simulation: Zürich Bahnhofstrasse (07:30 - 08:00 Uhr)")
    model = ZurichTransportModel(num_passengers=200, construction_active=True)

    steps = 90
    for i in range(steps): 
        model.step()

    # Daten abrufen
    results = model.datacollector.get_model_vars_dataframe()

    # --- PLOTTING ---
    fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, figsize=(10, 8))

    # Zeitachse formatieren (nur Uhrzeit)
    time_labels = results["Time"].dt.strftime('%H:%M:%S')
    
    # Plot 1: Zufriedenheit & Wechsler
    ax1.plot(results["Time"], results["Avg_Satisfaction"], label="Zufriedenheit", color="green")
    ax1.set_ylabel("Zufriedenheit (0-100)")
    ax1.legend(loc="upper left")
    ax1.grid(True)
    
    # Zweite Achse für Umsteiger
    ax1b = ax1.twinx()
    ax1b.plot(results["Time"], results["Total_Switchers"], label="Umsteiger (zur Tram)", color="red", linestyle="--")
    ax1b.set_ylabel("Anzahl Personen")
    ax1b.legend(loc="upper right")
    ax1.set_title("Zürich HB -> Bürkliplatz: Impact der Baustelle (Rennweg)")

    # Plot 2: Warteschlangen
    ax2.plot(results["Time"], results["Bus_Wait"], label="Wartende Bus", color="blue")
    ax2.plot(results["Time"], results["Tram_Wait"], label="Wartende Tram", color="orange")
    ax2.set_ylabel("Wartende Passagiere")
    ax2.set_xlabel("Uhrzeit")
    ax2.legend()
    ax2.grid(True)

    # X-Achse lesbar machen (nur jeden 10. Label anzeigen)
    ax2.set_xticks(results["Time"][::10])
    ax2.set_xticklabels(time_labels[::10], rotation=45)

    plt.tight_layout()
    plt.show()