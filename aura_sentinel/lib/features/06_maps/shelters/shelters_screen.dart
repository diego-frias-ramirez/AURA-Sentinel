// lib/features/06_maps/shelters_screen.dart
import 'package:flutter/material.dart';
import 'package:get/get.dart';

class SheltersScreen extends StatelessWidget {
  const SheltersScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.white,
      body: SafeArea(
        child: Center(
          child: SizedBox(
            width: 392, // Ancho fijo de 392px
            height: 850, // Alto fijo de 850px
            child: Container(
              decoration: BoxDecoration(
                border: Border.all(
                  color: Colors.blue,
                  width: 2,
                ), // 🟦 Borde azul para referencia (opcional)
              ),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  // Encabezado verde turquesa sólido
                  Container(
                    padding: const EdgeInsets.only(top: 30, bottom: 14),
                    decoration: const BoxDecoration(
                      color: Color.fromRGBO(
                        0,
                        200,
                        180,
                        1,
                      ), // Verde turquesa sólido
                    ),
                    child: Padding(
                      padding: const EdgeInsets.symmetric(horizontal: 16.0),
                      child: Column(
                        children: [
                          Row(
                            children: [
                              IconButton(
                                onPressed: () => Navigator.pop(context),
                                icon: const Icon(
                                  Icons.arrow_back,
                                  color: Colors.white,
                                ),
                              ),
                              const SizedBox(width: 8),
                              Text(
                                'Refugios Seguros',
                                style: TextStyle(
                                  color: Colors.white,
                                  fontWeight: FontWeight.bold,
                                  fontSize: 18,
                                ),
                              ),
                              const Spacer(),
                              IconButton(
                                onPressed: () {},
                                icon: const Icon(
                                  Icons.map,
                                  color: Colors.white,
                                ),
                              ),
                            ],
                          ),
                          const SizedBox(height: 14),
                          Container(
                            padding: const EdgeInsets.symmetric(
                              vertical: 7,
                              horizontal: 16,
                            ),
                            decoration: BoxDecoration(
                              color: Colors.white.withOpacity(0.3),
                              borderRadius: BorderRadius.circular(18),
                            ),
                            child: Row(
                              children: [
                                Icon(
                                  Icons.location_on,
                                  color: Colors.white,
                                  size: 18,
                                ),
                                const SizedBox(width: 6),
                                Text(
                                  'Tu ubicación: Av. Central 123, Ciudad',
                                  style: TextStyle(
                                    color: Colors.white,
                                    fontSize: 13,
                                  ),
                                ),
                              ],
                            ),
                          ),
                        ],
                      ),
                    ),
                  ),
                  const SizedBox(height: 14),
                  // Campo de búsqueda
                  Padding(
                    padding: const EdgeInsets.symmetric(horizontal: 16.0),
                    child: TextField(
                      decoration: InputDecoration(
                        hintText: 'Buscar refugios...',
                        prefixIcon: const Icon(Icons.search, size: 18),
                        border: OutlineInputBorder(
                          borderRadius: BorderRadius.circular(18),
                        ),
                        contentPadding: const EdgeInsets.symmetric(
                          vertical: 8,
                          horizontal: 12,
                        ),
                      ),
                    ),
                  ),
                  const SizedBox(height: 14),
                  // Botones de filtro
                  Padding(
                    padding: const EdgeInsets.symmetric(horizontal: 16.0),
                    child: Row(
                      children: [
                        ElevatedButton(
                          onPressed: () {},
                          style: ElevatedButton.styleFrom(
                            backgroundColor: Color.fromRGBO(
                              0,
                              200,
                              180,
                              1,
                            ), // Verde turquesa
                            foregroundColor: Colors.white,
                            padding: const EdgeInsets.symmetric(
                              horizontal: 8,
                              vertical: 4,
                            ),
                            shape: RoundedRectangleBorder(
                              borderRadius: BorderRadius.circular(18),
                            ),
                          ),
                          child: Row(
                            mainAxisSize: MainAxisSize.min,
                            children: [
                              Icon(Icons.filter_alt, size: 16),
                              const SizedBox(width: 4),
                              Text('Todos', style: TextStyle(fontSize: 13)),
                              const SizedBox(width: 4),
                              Container(
                                padding: const EdgeInsets.symmetric(
                                  horizontal: 4,
                                  vertical: 2,
                                ),
                                decoration: BoxDecoration(
                                  color: Colors.white,
                                  borderRadius: BorderRadius.circular(8),
                                ),
                                child: Text(
                                  '4',
                                  style: TextStyle(
                                    fontSize: 11,
                                    fontWeight: FontWeight.bold,
                                    color: Color.fromRGBO(
                                      0,
                                      200,
                                      180,
                                      1,
                                    ), // Verde turquesa
                                  ),
                                ),
                              ),
                            ],
                          ),
                        ),
                        const SizedBox(width: 6),
                        ElevatedButton(
                          onPressed: () {},
                          style: ElevatedButton.styleFrom(
                            backgroundColor: Colors.grey[300],
                            foregroundColor: Colors.black,
                            padding: const EdgeInsets.symmetric(
                              horizontal: 8,
                              vertical: 4,
                            ),
                            shape: RoundedRectangleBorder(
                              borderRadius: BorderRadius.circular(18),
                            ),
                          ),
                          child: Row(
                            mainAxisSize: MainAxisSize.min,
                            children: [
                              Icon(Icons.location_on, size: 16),
                              const SizedBox(width: 4),
                              Text('Cercanos', style: TextStyle(fontSize: 13)),
                              const SizedBox(width: 4),
                              Container(
                                padding: const EdgeInsets.symmetric(
                                  horizontal: 4,
                                  vertical: 2,
                                ),
                                decoration: BoxDecoration(
                                  color: Colors.white,
                                  borderRadius: BorderRadius.circular(8),
                                ),
                                child: Text(
                                  '2',
                                  style: TextStyle(
                                    fontSize: 11,
                                    fontWeight: FontWeight.bold,
                                    color: Colors.grey.shade600,
                                  ),
                                ),
                              ),
                            ],
                          ),
                        ),
                        const SizedBox(width: 6),
                        ElevatedButton(
                          onPressed: () {},
                          style: ElevatedButton.styleFrom(
                            backgroundColor: Colors.grey[300],
                            foregroundColor: Colors.black,
                            padding: const EdgeInsets.symmetric(
                              horizontal: 8,
                              vertical: 4,
                            ),
                            shape: RoundedRectangleBorder(
                              borderRadius: BorderRadius.circular(18),
                            ),
                          ),
                          child: Row(
                            mainAxisSize: MainAxisSize.min,
                            children: [
                              Icon(Icons.check_circle_outline, size: 16),
                              const SizedBox(width: 4),
                              Text(
                                'Disponibles',
                                style: TextStyle(fontSize: 13),
                              ),
                            ],
                          ),
                        ),
                      ],
                    ),
                  ),
                  const SizedBox(height: 14),
                  // Tarjeta "Refugios verificados"
                  Padding(
                    padding: const EdgeInsets.symmetric(horizontal: 16.0),
                    child: Container(
                      padding: const EdgeInsets.all(14.0),
                      decoration: BoxDecoration(
                        color: Color.fromRGBO(220, 255, 240, 1), // Fondo claro
                        borderRadius: BorderRadius.circular(12),
                      ),
                      child: Row(
                        children: [
                          Container(
                            padding: const EdgeInsets.all(7),
                            decoration: BoxDecoration(
                              color: Color.fromRGBO(
                                200,
                                255,
                                230,
                                1,
                              ), // Fondo más claro
                              shape: BoxShape.circle,
                            ),
                            child: Icon(
                              Icons.shield_outlined,
                              color: Color.fromRGBO(
                                0,
                                200,
                                180,
                                1,
                              ), // Verde turquesa
                              size: 18,
                            ),
                          ),
                          const SizedBox(width: 6),
                          Expanded(
                            child: Column(
                              crossAxisAlignment: CrossAxisAlignment.start,
                              children: [
                                Text(
                                  'Refugios verificados',
                                  style: TextStyle(
                                    color: Color.fromRGBO(
                                      0,
                                      200,
                                      180,
                                      1,
                                    ), // Verde turquesa
                                    fontWeight: FontWeight.bold,
                                    fontSize: 13,
                                  ),
                                ),
                                const SizedBox(height: 4),
                                Text(
                                  'Todos los refugios están verificados y ofrecen asistencia profesional.',
                                  style: TextStyle(
                                    fontSize: 12,
                                    color: Colors.grey.shade600,
                                  ),
                                ),
                              ],
                            ),
                          ),
                        ],
                      ),
                    ),
                  ),
                  const SizedBox(height: 14),
                  // Lista de tarjetas de refugios
                  Expanded(
                    child: ListView(
                      children: [
                        // Tarjeta 1
                        Card(
                          margin: const EdgeInsets.only(bottom: 14.0),
                          child: Padding(
                            padding: const EdgeInsets.all(14.0),
                            child: Column(
                              crossAxisAlignment: CrossAxisAlignment.start,
                              children: [
                                // Título
                                Text(
                                  'Centro de Apoyo Esperanza',
                                  style: Theme.of(context)
                                      .textTheme
                                      .headlineSmall
                                      ?.copyWith(
                                        fontWeight: FontWeight.bold,
                                        fontSize: 16,
                                      ),
                                ),
                                const SizedBox(height: 6),
                                Row(
                                  children: [
                                    Icon(
                                      Icons.location_on,
                                      color: Colors.grey.shade600,
                                      size: 16,
                                    ),
                                    const SizedBox(width: 4),
                                    Text(
                                      'Av. Principal 456, Centro',
                                      style: TextStyle(
                                        fontSize: 13,
                                        color: Colors.grey.shade600,
                                      ),
                                    ),
                                  ],
                                ),
                                const SizedBox(height: 14),
                                // Distancia y horario
                                Row(
                                  children: [
                                    Icon(
                                      Icons.directions_walk,
                                      color: Colors.grey.shade600,
                                      size: 16,
                                    ),
                                    const SizedBox(width: 4),
                                    Text(
                                      '0.8 km',
                                      style: TextStyle(
                                        fontSize: 13,
                                        color: Colors.grey.shade600,
                                      ),
                                    ),
                                    const Spacer(),
                                    Icon(
                                      Icons.access_time,
                                      color: Colors.grey.shade600,
                                      size: 16,
                                    ),
                                    const SizedBox(width: 4),
                                    Text(
                                      'Horario 24/7',
                                      style: TextStyle(
                                        fontSize: 13,
                                        color: Colors.grey.shade600,
                                      ),
                                    ),
                                  ],
                                ),
                                const SizedBox(height: 6),
                                // Espacios disponibles
                                Row(
                                  children: [
                                    Icon(
                                      Icons.person,
                                      color: Colors.grey.shade600,
                                      size: 16,
                                    ),
                                    const SizedBox(width: 4),
                                    Text(
                                      '12 espacios disponibles',
                                      style: TextStyle(
                                        fontSize: 13,
                                        color: Colors.grey.shade600,
                                      ),
                                    ),
                                  ],
                                ),
                                const SizedBox(height: 14),
                                // Servicios disponibles
                                Text(
                                  'Servicios disponibles:',
                                  style: TextStyle(
                                    fontSize: 13,
                                    fontWeight: FontWeight.bold,
                                  ),
                                ),
                                const SizedBox(height: 6),
                                Row(
                                  children: [
                                    Icon(
                                      Icons.bed,
                                      color: Colors.grey.shade600,
                                      size: 16,
                                    ),
                                    const SizedBox(width: 4),
                                    Text(
                                      'Alojamiento',
                                      style: TextStyle(
                                        fontSize: 13,
                                        color: Colors.grey.shade600,
                                      ),
                                    ),
                                    const SizedBox(width: 6),
                                    Icon(
                                      Icons.fastfood,
                                      color: Colors.grey.shade600,
                                      size: 16,
                                    ),
                                    const SizedBox(width: 4),
                                    Text(
                                      'Comida',
                                      style: TextStyle(
                                        fontSize: 13,
                                        color: Colors.grey.shade600,
                                      ),
                                    ),
                                    const SizedBox(width: 6),
                                    Icon(
                                      Icons.shield,
                                      color: Colors.grey.shade600,
                                      size: 16,
                                    ),
                                    const SizedBox(width: 4),
                                    Text(
                                      'Apoyo Legal',
                                      style: TextStyle(
                                        fontSize: 13,
                                        color: Colors.grey.shade600,
                                      ),
                                    ),
                                  ],
                                ),
                                const SizedBox(height: 14),
                                // Botones "Llamar" y "Ir ahora"
                                Row(
                                  children: [
                                    ElevatedButton(
                                      onPressed: () {},
                                      style: ElevatedButton.styleFrom(
                                        backgroundColor: Colors.grey[300],
                                        foregroundColor: Colors.black,
                                        padding: const EdgeInsets.symmetric(
                                          horizontal: 14,
                                          vertical: 6,
                                        ),
                                        shape: RoundedRectangleBorder(
                                          borderRadius: BorderRadius.circular(
                                            18,
                                          ),
                                        ),
                                      ),
                                      child: Row(
                                        mainAxisSize: MainAxisSize.min,
                                        children: [
                                          Icon(Icons.phone, size: 16),
                                          const SizedBox(width: 4),
                                          Text(
                                            'Llamar',
                                            style: TextStyle(fontSize: 13),
                                          ),
                                        ],
                                      ),
                                    ),
                                    const SizedBox(width: 6),
                                    ElevatedButton(
                                      onPressed: () {},
                                      style: ElevatedButton.styleFrom(
                                        backgroundColor: Color.fromRGBO(
                                          0,
                                          123,
                                          255,
                                          1,
                                        ), // Azul principal (como en el boceto)
                                        foregroundColor: Colors.white,
                                        padding: const EdgeInsets.symmetric(
                                          horizontal: 14,
                                          vertical: 6,
                                        ),
                                        shape: RoundedRectangleBorder(
                                          borderRadius: BorderRadius.circular(
                                            18,
                                          ),
                                        ),
                                      ),
                                      child: Row(
                                        mainAxisSize: MainAxisSize.min,
                                        children: [
                                          Icon(Icons.near_me, size: 16),
                                          const SizedBox(width: 4),
                                          Text(
                                            'Ir ahora',
                                            style: TextStyle(fontSize: 13),
                                          ),
                                        ],
                                      ),
                                    ),
                                  ],
                                ),
                                const SizedBox(height: 6),
                                // Enlace "Ver detalles completos"
                                TextButton(
                                  onPressed: () {},
                                  child: Text(
                                    'Ver detalles completos >',
                                    style: TextStyle(
                                      color: Colors.grey.shade600,
                                      fontSize: 13,
                                    ),
                                  ),
                                ),
                              ],
                            ),
                          ),
                        ),
                        // Tarjeta 2
                        Card(
                          margin: const EdgeInsets.only(bottom: 14.0),
                          child: Padding(
                            padding: const EdgeInsets.all(14.0),
                            child: Column(
                              crossAxisAlignment: CrossAxisAlignment.start,
                              children: [
                                // Título
                                Text(
                                  'Refugio Seguro San José',
                                  style: Theme.of(context)
                                      .textTheme
                                      .headlineSmall
                                      ?.copyWith(
                                        fontWeight: FontWeight.bold,
                                        fontSize: 16,
                                      ),
                                ),
                                const SizedBox(height: 6),
                                Row(
                                  children: [
                                    Icon(
                                      Icons.location_on,
                                      color: Colors.grey.shade600,
                                      size: 16,
                                    ),
                                    const SizedBox(width: 4),
                                    Text(
                                      'Calle Libertad 789, Norte',
                                      style: TextStyle(
                                        fontSize: 13,
                                        color: Colors.grey.shade600,
                                      ),
                                    ),
                                  ],
                                ),
                                const SizedBox(height: 14),
                                // Distancia y horario
                                Row(
                                  children: [
                                    Icon(
                                      Icons.directions_walk,
                                      color: Colors.grey.shade600,
                                      size: 16,
                                    ),
                                    const SizedBox(width: 4),
                                    Text(
                                      '1.2 km',
                                      style: TextStyle(
                                        fontSize: 13,
                                        color: Colors.grey.shade600,
                                      ),
                                    ),
                                    const Spacer(),
                                    Icon(
                                      Icons.access_time,
                                      color: Colors.grey.shade600,
                                      size: 16,
                                    ),
                                    const SizedBox(width: 4),
                                    Text(
                                      'Horario 24/7',
                                      style: TextStyle(
                                        fontSize: 13,
                                        color: Colors.grey.shade600,
                                      ),
                                    ),
                                  ],
                                ),
                                const SizedBox(height: 6),
                                // Espacios disponibles
                                Row(
                                  children: [
                                    Icon(
                                      Icons.person,
                                      color: Colors.grey.shade600,
                                      size: 16,
                                    ),
                                    const SizedBox(width: 4),
                                    Text(
                                      '8 espacios disponibles',
                                      style: TextStyle(
                                        fontSize: 13,
                                        color: Colors.grey.shade600,
                                      ),
                                    ),
                                  ],
                                ),
                                const SizedBox(height: 14),
                                // Servicios disponibles
                                Text(
                                  'Servicios disponibles:',
                                  style: TextStyle(
                                    fontSize: 13,
                                    fontWeight: FontWeight.bold,
                                  ),
                                ),
                                const SizedBox(height: 6),
                                Row(
                                  children: [
                                    Icon(
                                      Icons.bed,
                                      color: Colors.grey.shade600,
                                      size: 16,
                                    ),
                                    const SizedBox(width: 4),
                                    Text(
                                      'Alojamiento',
                                      style: TextStyle(
                                        fontSize: 13,
                                        color: Colors.grey.shade600,
                                      ),
                                    ),
                                    const SizedBox(width: 6),
                                    Icon(
                                      Icons.fastfood,
                                      color: Colors.grey.shade600,
                                      size: 16,
                                    ),
                                    const SizedBox(width: 4),
                                    Text(
                                      'Comida',
                                      style: TextStyle(
                                        fontSize: 13,
                                        color: Colors.grey.shade600,
                                      ),
                                    ),
                                    const SizedBox(width: 6),
                                    Icon(
                                      Icons.shield,
                                      color: Colors.grey.shade600,
                                      size: 16,
                                    ),
                                    const SizedBox(width: 4),
                                    Text(
                                      'Apoyo Legal',
                                      style: TextStyle(
                                        fontSize: 13,
                                        color: Colors.grey.shade600,
                                      ),
                                    ),
                                  ],
                                ),
                                const SizedBox(height: 14),
                                // Botones "Llamar" y "Ir ahora"
                                Row(
                                  children: [
                                    ElevatedButton(
                                      onPressed: () {},
                                      style: ElevatedButton.styleFrom(
                                        backgroundColor: Colors.grey[300],
                                        foregroundColor: Colors.black,
                                        padding: const EdgeInsets.symmetric(
                                          horizontal: 14,
                                          vertical: 6,
                                        ),
                                        shape: RoundedRectangleBorder(
                                          borderRadius: BorderRadius.circular(
                                            18,
                                          ),
                                        ),
                                      ),
                                      child: Row(
                                        mainAxisSize: MainAxisSize.min,
                                        children: [
                                          Icon(Icons.phone, size: 16),
                                          const SizedBox(width: 4),
                                          Text(
                                            'Llamar',
                                            style: TextStyle(fontSize: 13),
                                          ),
                                        ],
                                      ),
                                    ),
                                    const SizedBox(width: 6),
                                    ElevatedButton(
                                      onPressed: () {},
                                      style: ElevatedButton.styleFrom(
                                        backgroundColor: Color.fromRGBO(
                                          0,
                                          123,
                                          255,
                                          1,
                                        ), // Azul principal
                                        foregroundColor: Colors.white,
                                        padding: const EdgeInsets.symmetric(
                                          horizontal: 14,
                                          vertical: 6,
                                        ),
                                        shape: RoundedRectangleBorder(
                                          borderRadius: BorderRadius.circular(
                                            18,
                                          ),
                                        ),
                                      ),
                                      child: Row(
                                        mainAxisSize: MainAxisSize.min,
                                        children: [
                                          Icon(Icons.near_me, size: 16),
                                          const SizedBox(width: 4),
                                          Text(
                                            'Ir ahora',
                                            style: TextStyle(fontSize: 13),
                                          ),
                                        ],
                                      ),
                                    ),
                                  ],
                                ),
                                const SizedBox(height: 6),
                                // Enlace "Ver detalles completos"
                                TextButton(
                                  onPressed: () {},
                                  child: Text(
                                    'Ver detalles completos >',
                                    style: TextStyle(
                                      color: Colors.grey.shade600,
                                      fontSize: 13,
                                    ),
                                  ),
                                ),
                              ],
                            ),
                          ),
                        ),
                        // Tarjeta 3
                        Card(
                          margin: const EdgeInsets.only(bottom: 14.0),
                          child: Padding(
                            padding: const EdgeInsets.all(14.0),
                            child: Column(
                              crossAxisAlignment: CrossAxisAlignment.start,
                              children: [
                                // Título
                                Text(
                                  'Casa Refugio María',
                                  style: Theme.of(context)
                                      .textTheme
                                      .headlineSmall
                                      ?.copyWith(
                                        fontWeight: FontWeight.bold,
                                        fontSize: 16,
                                      ),
                                ),
                                const SizedBox(height: 6),
                                Row(
                                  children: [
                                    Icon(
                                      Icons.location_on,
                                      color: Colors.grey.shade600,
                                      size: 16,
                                    ),
                                    const SizedBox(width: 4),
                                    Text(
                                      'Av. Paz 321, Sur',
                                      style: TextStyle(
                                        fontSize: 13,
                                        color: Colors.grey.shade600,
                                      ),
                                    ),
                                  ],
                                ),
                                const SizedBox(height: 14),
                                // Distancia y horario
                                Row(
                                  children: [
                                    Icon(
                                      Icons.directions_walk,
                                      color: Colors.grey.shade600,
                                      size: 16,
                                    ),
                                    const SizedBox(width: 4),
                                    Text(
                                      '2.5 km',
                                      style: TextStyle(
                                        fontSize: 13,
                                        color: Colors.grey.shade600,
                                      ),
                                    ),
                                    const Spacer(),
                                    Icon(
                                      Icons.access_time,
                                      color: Colors.grey.shade600,
                                      size: 16,
                                    ),
                                    const SizedBox(width: 4),
                                    Text(
                                      'Horario 8:00 AM - 10:00 PM',
                                      style: TextStyle(
                                        fontSize: 13,
                                        color: Colors.grey.shade600,
                                      ),
                                    ),
                                  ],
                                ),
                                const SizedBox(height: 6),
                                // Espacios disponibles
                                Row(
                                  children: [
                                    Icon(
                                      Icons.person,
                                      color: Colors.grey.shade600,
                                      size: 16,
                                    ),
                                    const SizedBox(width: 4),
                                    Text(
                                      '3 espacios disponibles',
                                      style: TextStyle(
                                        fontSize: 13,
                                        color: Colors.grey.shade600,
                                      ),
                                    ),
                                  ],
                                ),
                                const SizedBox(height: 14),
                                // Servicios disponibles
                                Text(
                                  'Servicios disponibles:',
                                  style: TextStyle(
                                    fontSize: 13,
                                    fontWeight: FontWeight.bold,
                                  ),
                                ),
                                const SizedBox(height: 6),
                                Row(
                                  children: [
                                    Icon(
                                      Icons.bed,
                                      color: Colors.grey.shade600,
                                      size: 16,
                                    ),
                                    const SizedBox(width: 4),
                                    Text(
                                      'Alojamiento',
                                      style: TextStyle(
                                        fontSize: 13,
                                        color: Colors.grey.shade600,
                                      ),
                                    ),
                                    const SizedBox(width: 6),
                                    Icon(
                                      Icons.fastfood,
                                      color: Colors.grey.shade600,
                                      size: 16,
                                    ),
                                    const SizedBox(width: 4),
                                    Text(
                                      'Comida',
                                      style: TextStyle(
                                        fontSize: 13,
                                        color: Colors.grey.shade600,
                                      ),
                                    ),
                                    const SizedBox(width: 6),
                                    Icon(
                                      Icons.shield,
                                      color: Colors.grey.shade600,
                                      size: 16,
                                    ),
                                    const SizedBox(width: 4),
                                    Text(
                                      'Apoyo Legal',
                                      style: TextStyle(
                                        fontSize: 13,
                                        color: Colors.grey.shade600,
                                      ),
                                    ),
                                  ],
                                ),
                                const SizedBox(height: 14),
                                // Botones "Llamar" y "Ir ahora"
                                Row(
                                  children: [
                                    ElevatedButton(
                                      onPressed: () {},
                                      style: ElevatedButton.styleFrom(
                                        backgroundColor: Colors.grey[300],
                                        foregroundColor: Colors.black,
                                        padding: const EdgeInsets.symmetric(
                                          horizontal: 14,
                                          vertical: 6,
                                        ),
                                        shape: RoundedRectangleBorder(
                                          borderRadius: BorderRadius.circular(
                                            18,
                                          ),
                                        ),
                                      ),
                                      child: Row(
                                        mainAxisSize: MainAxisSize.min,
                                        children: [
                                          Icon(Icons.phone, size: 16),
                                          const SizedBox(width: 4),
                                          Text(
                                            'Llamar',
                                            style: TextStyle(fontSize: 13),
                                          ),
                                        ],
                                      ),
                                    ),
                                    const SizedBox(width: 6),
                                    ElevatedButton(
                                      onPressed: () {},
                                      style: ElevatedButton.styleFrom(
                                        backgroundColor: Color.fromRGBO(
                                          0,
                                          123,
                                          255,
                                          1,
                                        ), // Azul principal
                                        foregroundColor: Colors.white,
                                        padding: const EdgeInsets.symmetric(
                                          horizontal: 14,
                                          vertical: 6,
                                        ),
                                        shape: RoundedRectangleBorder(
                                          borderRadius: BorderRadius.circular(
                                            18,
                                          ),
                                        ),
                                      ),
                                      child: Row(
                                        mainAxisSize: MainAxisSize.min,
                                        children: [
                                          Icon(Icons.near_me, size: 16),
                                          const SizedBox(width: 4),
                                          Text(
                                            'Ir ahora',
                                            style: TextStyle(fontSize: 13),
                                          ),
                                        ],
                                      ),
                                    ),
                                  ],
                                ),
                                const SizedBox(height: 6),
                                // Enlace "Ver detalles completos"
                                TextButton(
                                  onPressed: () {},
                                  child: Text(
                                    'Ver detalles completos >',
                                    style: TextStyle(
                                      color: Colors.grey.shade600,
                                      fontSize: 13,
                                    ),
                                  ),
                                ),
                              ],
                            ),
                          ),
                        ),
                      ],
                    ),
                  ),
                  const SizedBox(height: 14),
                  // Botón "Ver Todos en el Mapa" (centrado y con ancho reducido)
                  Padding(
                    padding: const EdgeInsets.symmetric(horizontal: 16.0),
                    child: Center(
                      child: SizedBox(
                        width: 320, // Ancho reducido para centrarlo
                        child: ElevatedButton(
                          onPressed: () {},
                          style: ElevatedButton.styleFrom(
                            backgroundColor: Color.fromRGBO(
                              0,
                              123,
                              255,
                              1,
                            ), // Azul principal
                            foregroundColor: Colors.white,
                            padding: const EdgeInsets.symmetric(
                              horizontal: 30,
                              vertical: 14,
                            ),
                            shape: RoundedRectangleBorder(
                              borderRadius: BorderRadius.circular(18),
                            ),
                          ),
                          child: Row(
                            mainAxisSize: MainAxisSize.min,
                            children: [
                              Icon(Icons.map, size: 18),
                              const SizedBox(width: 6),
                              Text(
                                'Ver Todos en el Mapa',
                                style: TextStyle(
                                  fontSize: 16,
                                  fontWeight: FontWeight.bold,
                                ),
                              ),
                            ],
                          ),
                        ),
                      ),
                    ),
                  ),
                ],
              ),
            ),
          ),
        ),
      ),
    );
  }
}
