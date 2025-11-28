import numpy as np

class ARTNetwork:
    def __init__(self, n, m, rho=0.5, beta=1.0):
        """
        n: número de componentes de entrada (tamaño del grid)
        m: número máximo de categorías (neuronas de salida)
        rho: parámetro de vigilancia (0 a 1)
        """
        self.n = n
        self.m = m
        self.rho = rho
        self.beta = beta
        self.active_categories = 0
        
        # Inicialización de pesos
        # Bottom-up (b_ij): Inicialmente bajos
        self.W_bu = np.full((n, m), 1.0 / (1.0 + n))
        # Top-down (t_ji): Inicialmente 1 (todo conectado)
        self.W_td = np.ones((m, n))

    def predict(self, input_vector):
        """Intenta clasificar el vector de entrada o aprenderlo si es nuevo"""
        x = np.array(input_vector)
        
        # Si no hay categorías aprendidas, crea la primera
        if self.active_categories == 0:
            self._create_category(0, x)
            return 0, "Aprendido como nuevo Patrón 0"

        # Calcular activaciones para todas las categorías activas
        scores = np.dot(x, self.W_bu[:, :self.active_categories])
        indices = np.argsort(scores)[::-1] # Ordenar de mayor a menor coincidencia
        
        for j in indices:
            # 1. Hipótesis: Verificar si pasa la prueba de vigilancia
            # El vector 'v' es la intersección entre entrada y lo que la red sabe
            v = x * self.W_td[j, :] 
            mag_v = np.sum(v)
            mag_x = np.sum(x)
            
            match_score = mag_v / mag_x if mag_x > 0 else 0
            
            # Chequeo de Vigilancia (Rho)
            if match_score >= self.rho:
                # RESONANCIA: Es similar, actualizamos el conocimiento
                self._update_weights(j, x)
                return j, f"Reconocido como Patrón {j} (Similitud: {match_score:.2f})"
        
        # Si ninguno cumple la vigilancia, crear nueva categoría
        if self.active_categories < self.m:
            new_idx = self.active_categories
            self._create_category(new_idx, x)
            return new_idx, f"Diferente. Aprendido como nuevo Patrón {new_idx}"
        
        return -1, "Memoria llena"

    def _create_category(self, idx, x):
        self.W_td[idx, :] = x
        self.W_bu[:, idx] = x / (0.5 + np.sum(x)) 
        self.active_categories += 1

    def _update_weights(self, idx, x):
        # Actualizar Top-Down (Intersección)
        self.W_td[idx, :] = self.W_td[idx, :] * x
        # Actualizar Bottom-Up
        self.W_bu[:, idx] = self.W_td[idx, :] / (0.5 + np.sum(self.W_td[idx, :]))
    
    def get_prototype(self, idx):
        return self.W_td[idx, :]