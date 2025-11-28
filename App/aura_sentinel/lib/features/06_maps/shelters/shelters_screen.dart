// shelters_screen.dart
import 'package:flutter/material.dart';

class SheltersScreen extends StatelessWidget {
  const SheltersScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Refugios Seguros'),
        backgroundColor: Colors.white,
        foregroundColor: Colors.black,
        elevation: 0,
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Barra de búsqueda
            Container(
              padding: const EdgeInsets.symmetric(horizontal: 16),
              decoration: BoxDecoration(
                color: Colors.grey[100],
                borderRadius: BorderRadius.circular(12),
              ),
              child: const TextField(
                decoration: InputDecoration(
                  hintText: 'Buscar refugios...',
                  border: InputBorder.none,
                  icon: Icon(Icons.search),
                ),
              ),
            ),
            const SizedBox(height: 16),

            // Filtros
            Row(
              children: [
                _buildFilterChip('Todos', true),
                const SizedBox(width: 8),
                _buildFilterChip('Cercanos', false),
                const SizedBox(width: 8),
                _buildFilterChip('Disponible', false),
              ],
            ),
            const SizedBox(height: 24),

            // Título de sección
            const Text(
              'Refugios verificados',
              style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 8),
            Text(
              'Todos los refugios están verificados y ofrecen asistencia profesional',
              style: TextStyle(color: Colors.grey[600], fontSize: 14),
            ),
            const SizedBox(height: 20),

            // Lista de refugios
            _buildShelterCard(
              name: 'Centro de Apoyo Esperanza',
              address: 'Av. Principal 456, Centro',
              distance: '0.8 km',
              availableSpaces: 12,
              rating: 4.8,
              services: [
                'Alojamiento',
                'Comida',
                'Apoyo Legal',
                'Asistencia Psicológica',
              ],
              isOpen: true,
            ),
            const SizedBox(height: 16),

            _buildShelterCard(
              name: 'Refugio Seguro San José',
              address: 'Calle Libertad 789, Norte',
              distance: '1.2 km',
              availableSpaces: 8,
              rating: 4.6,
              services: [
                'Alojamiento',
                'Comida',
                'Atención Médica',
                'Guardería',
              ],
              isOpen: true,
            ),
            const SizedBox(height: 20),

            // Botón ver en mapa
            Center(
              child: OutlinedButton(
                onPressed: () {
                  // TODO: Navegar al mapa
                },
                style: OutlinedButton.styleFrom(
                  foregroundColor: Colors.blue,
                  side: const BorderSide(color: Colors.blue),
                  padding: const EdgeInsets.symmetric(
                    horizontal: 32,
                    vertical: 12,
                  ),
                ),
                child: const Text('Ver Todos en el Mapa'),
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildFilterChip(String label, bool selected) {
    return FilterChip(
      label: Text(label),
      selected: selected,
      onSelected: (bool value) {
        // TODO: Implementar filtro
      },
      backgroundColor: Colors.grey[100],
      selectedColor: Colors.blue[100],
      labelStyle: TextStyle(color: selected ? Colors.blue : Colors.grey[700]),
    );
  }

  Widget _buildShelterCard({
    required String name,
    required String address,
    required String distance,
    required int availableSpaces,
    required double rating,
    required List<String> services,
    required bool isOpen,
  }) {
    return Card(
      elevation: 2,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Nombre y estado
            Row(
              children: [
                Expanded(
                  child: Text(
                    name,
                    style: const TextStyle(
                      fontSize: 18,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                ),
                Container(
                  padding: const EdgeInsets.symmetric(
                    horizontal: 8,
                    vertical: 4,
                  ),
                  decoration: BoxDecoration(
                    color: isOpen ? Colors.green[100] : Colors.red[100],
                    borderRadius: BorderRadius.circular(8),
                  ),
                  child: Text(
                    isOpen ? 'Disponible' : 'Cerrado',
                    style: TextStyle(
                      color: isOpen ? Colors.green[800] : Colors.red[800],
                      fontSize: 12,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                ),
              ],
            ),
            const SizedBox(height: 8),

            // Dirección
            Text(
              address,
              style: TextStyle(color: Colors.grey[600], fontSize: 14),
            ),
            const SizedBox(height: 12),

            // Información de distancia y espacios
            Row(
              children: [
                Icon(Icons.location_on, color: Colors.grey[600], size: 16),
                const SizedBox(width: 4),
                Text(
                  'Distancia $distance',
                  style: TextStyle(color: Colors.grey[600]),
                ),
                const SizedBox(width: 16),
                Icon(Icons.people, color: Colors.grey[600], size: 16),
                const SizedBox(width: 4),
                Text(
                  '$availableSpaces espacios disponibles',
                  style: TextStyle(color: Colors.grey[600]),
                ),
                const Spacer(),
                Icon(Icons.star, color: Colors.amber, size: 16),
                const SizedBox(width: 4),
                Text(
                  rating.toString(),
                  style: const TextStyle(fontWeight: FontWeight.bold),
                ),
              ],
            ),
            const SizedBox(height: 16),

            // Servicios disponibles
            const Text(
              'Servicios disponibles:',
              style: TextStyle(fontWeight: FontWeight.bold, fontSize: 14),
            ),
            const SizedBox(height: 8),
            Wrap(
              spacing: 8,
              runSpacing: 4,
              children: services.map((service) {
                return Chip(
                  label: Text(service),
                  backgroundColor: Colors.blue[50],
                  labelStyle: const TextStyle(fontSize: 12),
                  materialTapTargetSize: MaterialTapTargetSize.shrinkWrap,
                );
              }).toList(),
            ),
            const SizedBox(height: 16),

            // Botones de acción
            Row(
              children: [
                Expanded(
                  child: OutlinedButton(
                    onPressed: () {
                      // TODO: Llamar al refugio
                    },
                    child: const Text('Llamar'),
                  ),
                ),
                const SizedBox(width: 12),
                Expanded(
                  child: ElevatedButton(
                    onPressed: () {
                      // TODO: Navegar al refugio
                    },
                    child: const Text('Ir ahora'),
                  ),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }
}
