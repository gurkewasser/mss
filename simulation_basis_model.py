import mesa
import random
import matplotlib.pyplot as plt
import pandas as pd

# --- 1. Definition der Agenten ---

class PassengerAgent(mesa.Agent):
    """Ein Fahrgast, der warten muss und dessen Zufriedenheit sinkt."""
    def __init__(self, unique_id, model, transport_type_preference):
        super().__init__(model) 
        self.unique_id = unique_id
        self.transport_type = transport_type_preference # "Bus" oder "Tram"
        self.waiting_time = 0
        self.satisfaction = 100  # Startzufriedenheit (Skala 0-100)
        self.arrived = False

    def step(self):
        if not self.arrived:
            self.waiting_time += 1
            
            # LE1 Feedback Loop: Zufriedenheit sinkt
            decay = 0.5 if self.transport_type == "Tram" else 0.8
            self.satisfaction -= decay
            if self.satisfaction < 0: self.satisfaction = 0

class VehicleAgent(mesa.Agent):
    """Bus oder Tram. Bewegt sich durch die Stadt."""
    def __init__(self, unique_id, model, v_type):
        super().__init__(model)
        self.unique_id = unique_id
        self.v_type = v_type # "Bus" oder "Tram"
        self.speed = 1       

    def step(self):
        x, y = self.pos
        
        # --- LE1 Einflussfaktor: Baustelle ---
        if self.v_type == "Bus" and self.model.construction_active:
            if 10 <= x <= 20: # Baustelle
                # Stochastischer Stau (70% Wahrscheinlichkeit zu warten)
                if random.random() < 0.7: 
                    return 

        # Bewegung
        new_x = (x + 1) % self.model.grid.width 
        self.model.grid.move_agent(self, (new_x, y))
        
        # Passagiere einsammeln
        cell_mates = self.model.grid.get_cell_list_contents([(new_x, y)])
        for mate in cell_mates:
            if isinstance(mate, PassengerAgent) and not mate.arrived:
                if mate.transport_type == self.v_type:
                    mate.arrived = True 

# --- 2. Das Modell ---

class CityTransportModel(mesa.Model):
    """Das Modell der Stadt."""
    def __init__(self, num_passengers, construction_active=True):
        super().__init__()
        self.construction_active = construction_active
        self.grid = mesa.space.MultiGrid(50, 2, torus=True)
        
        # FIX: In Mesa 3.0 nutzen wir self.agents statt Scheduler
        # Wir müssen keinen expliziten Scheduler mehr erstellen.

        # Datensammler
        self.datacollector = mesa.DataCollector(
            model_reporters={
                "Avg_Satisfaction": compute_avg_satisfaction,
                "Bus_Passengers_Waiting": lambda m: count_waiting(m, "Bus"),
                "Tram_Passengers_Waiting": lambda m: count_waiting(m, "Tram")
            }
        )

        # 1. Agenten erstellen: Fahrzeuge
        bus = VehicleAgent(0, self, "Bus")
        self.grid.place_agent(bus, (0, 0))
        # Hinweis: In Mesa 3.0 werden Agenten oft automatisch dem Model hinzugefügt,
        # wenn man super().__init__(model) aufruft.

        tram = VehicleAgent(1, self, "Tram")
        self.grid.place_agent(tram, (0, 1))

        # 2. Agenten erstellen: Passagiere
        for i in range(num_passengers):
            p_type = "Bus" if random.random() < 0.7 else "Tram"
            # IDs müssen eindeutig sein (deshalb +100)
            a = PassengerAgent(i + 100, self, p_type)
            
            x = random.randrange(self.grid.width)
            y = 0 if p_type == "Bus" else 1
            self.grid.place_agent(a, (x, y))

    def step(self):
        self.datacollector.collect(self)
        # FIX: Die moderne Art, Agenten zufällig zu aktivieren:
        self.agents.shuffle_do("step")

# --- Hilfsfunktionen für Daten ---

def compute_avg_satisfaction(model):
    # FIX: Zugriff über model.agents statt model.schedule.agents
    passengers = [a for a in model.agents if isinstance(a, PassengerAgent)]
    if not passengers: return 0
    return sum([a.satisfaction for a in passengers]) / len(passengers)

def count_waiting(model, v_type):
    return sum([1 for a in model.agents 
                if isinstance(a, PassengerAgent) 
                and a.transport_type == v_type 
                and not a.arrived])

# --- 3. Ausführen ---

if __name__ == "__main__":
    # Szenario: Baustelle ist AKTIV
    model = CityTransportModel(num_passengers=100, construction_active=True)

    for i in range(100): 
        model.step()

    # Daten abrufen
    results = model.datacollector.get_model_vars_dataframe()

    # Plotten
    plt.figure(figsize=(10, 6))
    plt.plot(results["Avg_Satisfaction"], label="Fahrgastzufriedenheit (Durchschnitt)")
    plt.plot(results["Bus_Passengers_Waiting"], label="Wartende Bus-Gäste", linestyle="--")
    plt.plot(results["Tram_Passengers_Waiting"], label="Wartende Tram-Gäste", linestyle="--")
    plt.title("Mesa 3.0: Auswirkung der Baustelle")
    plt.xlabel("Zeit (Ticks)")
    plt.ylabel("Wert")
    plt.legend()
    plt.grid(True)
    
    # Dies verhindert, dass das Fenster sofort schließt, falls du nicht in Jupyter bist:
    plt.show()