// medical_form_screen.dart
import 'package:flutter/material.dart';
import 'package:get/get.dart';
import '../../../../app/routes.dart';

class MedicalFormScreen extends StatefulWidget {
  const MedicalFormScreen({super.key});

  @override
  State<MedicalFormScreen> createState() => _MedicalFormScreenState();
}

class _MedicalFormScreenState extends State<MedicalFormScreen> {
  final TextEditingController _nameController = TextEditingController();
  final TextEditingController _ageController = TextEditingController();
  final TextEditingController _weightController = TextEditingController();
  final TextEditingController _genderController = TextEditingController();
  String _bloodType = '';

  bool _hasAllergies = false;
  bool _hasChronicConditions = false;
  bool _takesMedication = false;
  bool _hasInsurance = false;

  @override
  void dispose() {
    _nameController.dispose();
    _ageController.dispose();
    _weightController.dispose();
    _genderController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Ficha Médica'),
        actions: [
          IconButton(
            icon: const Icon(Icons.help_outline),
            onPressed: () {
              // Mostrar ayuda o info adicional
            },
          ),
        ],
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Subtítulo
            Text(
              'Información vital accesible en emergencias',
              style: TextStyle(
                color: Colors.blue[700],
                fontWeight: FontWeight.bold,
              ),
            ),
            const SizedBox(height: 24),

            // Paso 1 de 3
            Row(
              children: [
                Container(
                  width: 32,
                  height: 32,
                  decoration: BoxDecoration(
                    shape: BoxShape.circle,
                    color: Colors.blue[100],
                  ),
                  child: Icon(Icons.add, color: Colors.blue, size: 20),
                ),
                const SizedBox(width: 8),
                Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      'Datos Personales',
                      style: TextStyle(fontWeight: FontWeight.bold),
                    ),
                    Text(
                      'Información básica',
                      style: TextStyle(color: Colors.grey[600]),
                    ),
                  ],
                ),
              ],
            ),
            const SizedBox(height: 24),

            // Nombre completo
            Text(
              'Nombre completo',
              style: TextStyle(fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 8),
            TextField(
              controller: _nameController,
              decoration: const InputDecoration(
                border: OutlineInputBorder(),
                hintText: 'Ej. Juan Pérez',
              ),
            ),
            const SizedBox(height: 16),

            // Edad y Peso
            Row(
              children: [
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        'Edad (0-120 años)',
                        style: TextStyle(fontWeight: FontWeight.bold),
                      ),
                      const SizedBox(height: 8),
                      TextField(
                        controller: _ageController,
                        decoration: const InputDecoration(
                          border: OutlineInputBorder(),
                          hintText: 'Ej. 35',
                        ),
                      ),
                    ],
                  ),
                ),
                const SizedBox(width: 16),
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        'Peso (20-300 kg)',
                        style: TextStyle(fontWeight: FontWeight.bold),
                      ),
                      const SizedBox(height: 8),
                      TextField(
                        controller: _weightController,
                        decoration: const InputDecoration(
                          border: OutlineInputBorder(),
                          hintText: 'Ej. 70',
                        ),
                      ),
                    ],
                  ),
                ),
              ],
            ),
            const SizedBox(height: 16),

            // Género
            Text('Género', style: TextStyle(fontWeight: FontWeight.bold)),
            const SizedBox(height: 8),
            TextField(
              controller: _genderController,
              decoration: const InputDecoration(
                border: OutlineInputBorder(),
                hintText: 'Ej. Masculino / Femenino / Otro',
              ),
            ),
            const SizedBox(height: 16),

            // Tipo de Sangre
            Row(
              children: [
                Icon(Icons.water_drop, color: Colors.blue),
                const SizedBox(width: 8),
                Text(
                  'Tipo de Sangre',
                  style: TextStyle(fontWeight: FontWeight.bold),
                ),
                const Spacer(),
                Text(
                  'CRÍTICO',
                  style: TextStyle(
                    color: Colors.red,
                    fontWeight: FontWeight.bold,
                  ),
                ),
              ],
            ),
            const SizedBox(height: 8),
            Wrap(
              spacing: 8,
              runSpacing: 8,
              children: [
                ...['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-'].map((
                  type,
                ) {
                  return OutlinedButton(
                    onPressed: () {
                      setState(() {
                        _bloodType = type;
                      });
                    },
                    style: OutlinedButton.styleFrom(
                      foregroundColor: _bloodType == type
                          ? Colors.white
                          : Colors.blue,
                      backgroundColor: _bloodType == type
                          ? Colors.blue
                          : Colors.white,
                      side: const BorderSide(color: Colors.blue),
                      shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(20),
                      ),
                    ),
                    child: Text(type),
                  );
                }).toList(),
              ],
            ),
            const SizedBox(height: 32),

            // Sección Alergias
            Row(
              children: [
                Container(
                  width: 32,
                  height: 32,
                  decoration: BoxDecoration(
                    shape: BoxShape.circle,
                    color: Colors.amber[100],
                  ),
                  child: Icon(
                    Icons.warning,
                    color: Colors.amber[800],
                    size: 20,
                  ),
                ),
                const SizedBox(width: 8),
                Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      'Alergias',
                      style: TextStyle(fontWeight: FontWeight.bold),
                    ),
                    Text(
                      'Importante',
                      style: TextStyle(color: Colors.grey[600]),
                    ),
                  ],
                ),
              ],
            ),
            const SizedBox(height: 16),

            // ¿Tienes alergias?
            Row(
              children: [
                const Text('¿Tienes alergias?'),
                const Spacer(),
                Switch(
                  value: _hasAllergies,
                  onChanged: (value) {
                    setState(() {
                      _hasAllergies = value;
                    });
                  },
                ),
              ],
            ),
            const SizedBox(height: 8),
            if (_hasAllergies)
              Wrap(
                spacing: 8,
                runSpacing: 8,
                children:
                    [
                      'Penicilina',
                      'Maní',
                      'Lácteos',
                      'Gluten',
                      'Mariscos',
                      'Otros',
                    ].map((allergy) {
                      return Chip(
                        label: Text(allergy),
                        onDeleted: () {
                          // Lógica para eliminar alergia
                        },
                      );
                    }).toList(),
              ),
            const SizedBox(height: 8),
            if (_hasAllergies)
              const TextField(
                decoration: InputDecoration(
                  border: OutlineInputBorder(),
                  hintText: 'Describe tus alergias...',
                ),
              ),
            const SizedBox(height: 16),

            // ¿Padeces condiciones médicas crónicas?
            Row(
              children: [
                const Text('¿Padeces condiciones médicas crónicas?'),
                const Spacer(),
                Switch(
                  value: _hasChronicConditions,
                  onChanged: (value) {
                    setState(() {
                      _hasChronicConditions = value;
                    });
                  },
                ),
              ],
            ),
            const SizedBox(height: 8),
            if (_hasChronicConditions)
              Wrap(
                spacing: 8,
                runSpacing: 8,
                children:
                    [
                      'Diabetes',
                      'Hipertensión',
                      'Asma',
                      'Enfermedad Cardíaca',
                      'Epilepsia',
                      'Otras',
                    ].map((condition) {
                      return OutlinedButton(
                        onPressed: () {},
                        style: OutlinedButton.styleFrom(
                          foregroundColor: Colors.grey[700],
                          side: BorderSide(color: Colors.grey[300]!),
                          shape: RoundedRectangleBorder(
                            borderRadius: BorderRadius.circular(20),
                          ),
                        ),
                        child: Row(
                          mainAxisSize: MainAxisSize.min,
                          children: [
                            Icon(
                              Icons.favorite_border,
                              color: Colors.grey[700],
                              size: 18,
                            ),
                            const SizedBox(width: 4),
                            Text(condition),
                          ],
                        ),
                      );
                    }).toList(),
              ),
            const SizedBox(height: 8),
            if (_hasChronicConditions)
              const TextField(
                decoration: InputDecoration(
                  border: OutlineInputBorder(),
                  hintText: 'Otra condición...',
                ),
              ),
            const SizedBox(height: 32),

            // Sección Medicamentos
            Row(
              children: [
                Container(
                  width: 32,
                  height: 32,
                  decoration: BoxDecoration(
                    shape: BoxShape.circle,
                    color: Colors.green[100],
                  ),
                  child: Icon(
                    Icons.medical_services,
                    color: Colors.green[800],
                    size: 20,
                  ),
                ),
                const SizedBox(width: 8),
                Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      'Medicamentos',
                      style: TextStyle(fontWeight: FontWeight.bold),
                    ),
                    Text(
                      'Registra tus medicamentos',
                      style: TextStyle(color: Colors.grey[600]),
                    ),
                  ],
                ),
              ],
            ),
            const SizedBox(height: 16),

            // ¿Tomas medicamentos regularmente?
            Row(
              children: [
                const Text('¿Tomas medicamentos regularmente?'),
                const Spacer(),
                Switch(
                  value: _takesMedication,
                  onChanged: (value) {
                    setState(() {
                      _takesMedication = value;
                    });
                  },
                ),
              ],
            ),
            const SizedBox(height: 8),
            if (_takesMedication)
              Column(
                children: [
                  Row(
                    children: [
                      Expanded(
                        child: TextField(
                          decoration: const InputDecoration(
                            border: OutlineInputBorder(),
                            labelText: 'Nombre del medicamento',
                          ),
                        ),
                      ),
                      const SizedBox(width: 8),
                      Expanded(
                        child: TextField(
                          decoration: const InputDecoration(
                            border: OutlineInputBorder(),
                            labelText: 'Dosis',
                          ),
                        ),
                      ),
                    ],
                  ),
                  const SizedBox(height: 8),
                  Row(
                    children: [
                      Expanded(
                        child: DropdownButtonFormField<String>(
                          items:
                              [
                                    'Diario',
                                    'Cada 12 horas',
                                    'Cada 8 horas',
                                    'Otro',
                                  ]
                                  .map(
                                    (freq) => DropdownMenuItem<String>(
                                      value: freq,
                                      child: Text(freq),
                                    ),
                                  )
                                  .toList(),
                          onChanged: (value) {},
                          decoration: const InputDecoration(
                            border: OutlineInputBorder(),
                            labelText: 'Frecuencia',
                          ),
                        ),
                      ),
                      const SizedBox(width: 8),
                      IconButton(
                        icon: const Icon(Icons.delete_outline),
                        onPressed: () {
                          // Eliminar medicamento
                        },
                      ),
                    ],
                  ),
                  const SizedBox(height: 8),
                  ElevatedButton(
                    onPressed: () {},
                    style: ElevatedButton.styleFrom(
                      backgroundColor: Colors.grey[200],
                      foregroundColor: Colors.black,
                      padding: const EdgeInsets.symmetric(horizontal: 16),
                      shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(20),
                      ),
                    ),
                    child: const Row(
                      mainAxisSize: MainAxisSize.min,
                      children: [
                        Icon(Icons.add, size: 18),
                        SizedBox(width: 4),
                        Text('+ Agregar medicamento'),
                      ],
                    ),
                  ),
                ],
              ),
            const SizedBox(height: 16),

            // ¿Cuentas con seguro médico?
            Row(
              children: [
                const Text('¿Cuentas con seguro médico?'),
                const Spacer(),
                Switch(
                  value: _hasInsurance,
                  onChanged: (value) {
                    setState(() {
                      _hasInsurance = value;
                    });
                  },
                ),
              ],
            ),
            const SizedBox(height: 8),
            if (_hasInsurance)
              Column(
                children: [
                  TextField(
                    decoration: const InputDecoration(
                      border: OutlineInputBorder(),
                      labelText: 'Proveedor (e.g., IMSS)',
                    ),
                  ),
                  const SizedBox(height: 8),
                  TextField(
                    decoration: const InputDecoration(
                      border: OutlineInputBorder(),
                      labelText: 'Número de póliza',
                    ),
                  ),
                  const SizedBox(height: 8),
                  TextField(
                    decoration: const InputDecoration(
                      border: OutlineInputBorder(),
                      labelText: 'Válido hasta (DD/MM/AAAA)',
                    ),
                  ),
                ],
              ),
            const SizedBox(height: 16),

            // Mensaje de seguridad
            Text(
              'Tus datos están encriptados y solo se comparten en emergencias reales',
              style: TextStyle(
                color: Colors.grey[600],
                fontStyle: FontStyle.italic,
              ),
            ),
            const SizedBox(height: 24),

            // Botones Guardar y continuar / Omitir
            ElevatedButton(
              onPressed: () {
                Get.offNamed(AppRoutes.home);
              },
              style: ElevatedButton.styleFrom(
                backgroundColor: Colors.blue,
                foregroundColor: Colors.white,
                padding: const EdgeInsets.symmetric(vertical: 16),
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(30),
                ),
              ),
              child: const Text(
                'Guardar y continuar',
                style: TextStyle(fontSize: 18),
              ),
            ),
            const SizedBox(height: 16),
            OutlinedButton(
              onPressed: () {
                Get.offNamed(AppRoutes.home);
              },
              style: OutlinedButton.styleFrom(
                foregroundColor: Colors.grey[700],
                side: BorderSide(color: Colors.grey[300]!),
                padding: const EdgeInsets.symmetric(vertical: 16),
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(30),
                ),
              ),
              child: const Text(
                'Omitir por ahora',
                style: TextStyle(fontSize: 18),
              ),
            ),
            const SizedBox(height: 8),
            Align(
              alignment: Alignment.center,
              child: TextButton(
                onPressed: () {},
                child: const Text(
                  'Podrás editar esto después en Configuración',
                  style: TextStyle(color: Colors.blue),
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
