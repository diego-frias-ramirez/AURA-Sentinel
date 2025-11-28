import 'package:flutter/material.dart';

class MedicalProfileScreen extends StatelessWidget {
  const MedicalProfileScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.grey[50],
      body: SingleChildScrollView(
        child: Column(
          children: [
            _buildHeader(context),
            _buildVitalInfoCard(),
            _buildPersonalDataSection(),
            _buildBloodTypeSection(),
            _buildAllergiesSection(),
            _buildMedicalConditionsSection(),
            _buildCurrentMedicationsSection(),
            _buildEmergencyContactsSection(),
            _buildInsuranceSection(),
            const SizedBox(height: 20),
          ],
        ),
      ),
    );
  }

  // -------------------------------------------------------------
  // HEADER
  // -------------------------------------------------------------
  Widget _buildHeader(BuildContext context) {
    return Container(
      decoration: BoxDecoration(
        gradient: LinearGradient(
          colors: [Colors.red[400]!, Colors.red[600]!],
          begin: Alignment.topLeft,
          end: Alignment.bottomRight,
        ),
        borderRadius: const BorderRadius.only(
          bottomLeft: Radius.circular(30),
          bottomRight: Radius.circular(30),
        ),
      ),
      child: SafeArea(
        child: Padding(
          padding: const EdgeInsets.all(20.0),
          child: Column(
            children: [
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  IconButton(
                    icon: const Icon(Icons.arrow_back, color: Colors.white),
                    onPressed: () => Navigator.pop(context),
                  ),
                  IconButton(
                    icon: const Icon(
                      Icons.favorite_border,
                      color: Colors.white,
                    ),
                    onPressed: () {},
                  ),
                  IconButton(
                    icon: const Icon(Icons.edit, color: Colors.white),
                    onPressed: () {},
                  ),
                ],
              ),
              const SizedBox(height: 10),
              const Text(
                'Ficha Médica',
                style: TextStyle(
                  color: Colors.white,
                  fontSize: 28,
                  fontWeight: FontWeight.bold,
                ),
              ),
              const SizedBox(height: 5),
              const Text(
                'Información de Emergencia',
                style: TextStyle(color: Colors.white, fontSize: 16),
              ),
              const SizedBox(height: 15),
              Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: const [
                  Icon(Icons.access_time, color: Colors.white, size: 16),
                  SizedBox(width: 5),
                  Text(
                    'Última actualización: 10 Nov 2024',
                    style: TextStyle(color: Colors.white, fontSize: 12),
                  ),
                ],
              ),
              const SizedBox(height: 20),
            ],
          ),
        ),
      ),
    );
  }

  // -------------------------------------------------------------
  // VITAL INFO CARD
  // -------------------------------------------------------------
  Widget _buildVitalInfoCard() {
    return Padding(
      padding: const EdgeInsets.all(16.0),
      child: Container(
        decoration: BoxDecoration(
          color: Colors.white,
          borderRadius: BorderRadius.circular(15),
          border: Border.all(color: Colors.red[200]!, width: 2),
        ),
        padding: const EdgeInsets.all(16),
        child: Row(
          children: [
            Container(
              padding: const EdgeInsets.all(10),
              decoration: const BoxDecoration(
                color: Color(0xffffebee),
                shape: BoxShape.circle,
              ),
              child: Icon(Icons.info_outline, color: Colors.red[400], size: 24),
            ),
            const SizedBox(width: 15),
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    'Información Vital',
                    style: TextStyle(
                      fontSize: 16,
                      fontWeight: FontWeight.bold,
                      color: Colors.grey[800],
                    ),
                  ),
                  const SizedBox(height: 4),
                  Text(
                    'Esta información es accesible en caso de emergencia médica',
                    style: TextStyle(fontSize: 12, color: Colors.grey[600]),
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }

  // -------------------------------------------------------------
  // PERSONAL DATA
  // -------------------------------------------------------------
  Widget _buildPersonalDataSection() {
    return _buildSection(
      title: 'Datos Personales',
      icon: Icons.person_outline,
      child: Column(
        children: [
          _buildInfoRow('Nombre Completo', 'Juan Pérez', 'Edad', '28 años'),
          const Divider(height: 20),
          _buildInfoRow('Género', 'Masculino', 'Peso', '75 kg'),
        ],
      ),
    );
  }

  // -------------------------------------------------------------
  // BLOOD TYPE
  // -------------------------------------------------------------
  Widget _buildBloodTypeSection() {
    return _buildSection(
      title: 'Tipo de Sangre',
      icon: Icons.bloodtype_outlined,
      child: Container(
        padding: const EdgeInsets.all(12),
        decoration: BoxDecoration(
          color: Colors.red[50],
          borderRadius: BorderRadius.circular(10),
        ),
        child: Row(
          children: [
            Container(
              padding: const EdgeInsets.all(12),
              decoration: BoxDecoration(
                color: Colors.white,
                borderRadius: BorderRadius.circular(10),
              ),
              child: const Icon(Icons.bloodtype, color: Colors.red, size: 28),
            ),
            const SizedBox(width: 15),
            const Text(
              'Grupo Sanguíneo',
              style: TextStyle(fontSize: 12, color: Colors.grey),
            ),
            const Spacer(),
            const Text(
              'O+',
              style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
            ),
            const SizedBox(width: 10),
            Container(
              padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
              decoration: BoxDecoration(
                color: Colors.red,
                borderRadius: BorderRadius.circular(12),
              ),
              child: const Text(
                'Crítico',
                style: TextStyle(
                  color: Colors.white,
                  fontSize: 10,
                  fontWeight: FontWeight.bold,
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }

  // -------------------------------------------------------------
  // ALLERGIES
  // -------------------------------------------------------------
  Widget _buildAllergiesSection() {
    return _buildSection(
      title: 'Alergias',
      icon: Icons.warning_amber_outlined,
      child: Column(
        children: [
          _buildAllergyItem('Penicilina', 'Alta', Colors.red),
          const SizedBox(height: 10),
          _buildAllergyItem('Maní', 'Media', Colors.orange),
        ],
      ),
    );
  }

  // -------------------------------------------------------------
  // MEDICAL CONDITIONS
  // -------------------------------------------------------------
  Widget _buildMedicalConditionsSection() {
    return _buildSection(
      title: 'Condiciones Médicas',
      icon: Icons.favorite_outline,
      child: Column(
        children: [
          _buildConditionItem('Asma', 'Controlado', Colors.teal),
          const SizedBox(height: 10),
          _buildConditionItem('Hipertensión', 'En tratamiento', Colors.cyan),
        ],
      ),
    );
  }

  // -------------------------------------------------------------
  // CURRENT MEDICATIONS
  // -------------------------------------------------------------
  Widget _buildCurrentMedicationsSection() {
    return _buildSection(
      title: 'Medicamentos Actuales',
      icon: Icons.medication_outlined,
      child: Column(
        children: [
          _buildMedicationItem('Salbutamol', '100 mcg • Según necesidad'),
          const SizedBox(height: 10),
          _buildMedicationItem('Losartán', '50 mg • 1 vez al día'),
        ],
      ),
    );
  }

  // -------------------------------------------------------------
  // EMERGENCY CONTACTS
  // -------------------------------------------------------------
  Widget _buildEmergencyContactsSection() {
    return _buildSection(
      title: 'Contactos de Emergencia',
      icon: Icons.contact_phone_outlined,
      child: Column(
        children: [
          _buildContactItem(
            'María Pérez (Madre)',
            '+1 555-0123',
            'Familiar',
            Colors.blue,
          ),
          const SizedBox(height: 10),
          _buildContactItem(
            'Dr. García',
            '+1 555-0456',
            'Médico de cabecera',
            Colors.blue,
          ),
        ],
      ),
    );
  }

  // -------------------------------------------------------------
  // INSURANCE
  // -------------------------------------------------------------
  Widget _buildInsuranceSection() {
    return _buildSection(
      title: 'Seguro Médico',
      icon: Icons.shield_outlined,
      child: Container(
        padding: const EdgeInsets.all(12),
        decoration: BoxDecoration(
          color: Colors.grey[100],
          borderRadius: BorderRadius.circular(10),
        ),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              'Proveedor',
              style: TextStyle(fontSize: 11, color: Colors.grey[600]),
            ),
            const Text(
              'Seguro Nacional de Salud',
              style: TextStyle(fontSize: 15, fontWeight: FontWeight.w500),
            ),
            const SizedBox(height: 10),
            Text(
              'Número de Póliza',
              style: TextStyle(fontSize: 11, color: Colors.grey[600]),
            ),
            const Text(
              'SNS-2024-789456',
              style: TextStyle(fontSize: 15, fontWeight: FontWeight.w500),
            ),
            const SizedBox(height: 10),
            Row(
              children: [
                Text(
                  'Válido hasta',
                  style: TextStyle(fontSize: 11, color: Colors.grey[600]),
                ),
                const Spacer(),
                Container(
                  padding: const EdgeInsets.symmetric(
                    horizontal: 10,
                    vertical: 4,
                  ),
                  decoration: BoxDecoration(
                    color: Colors.teal,
                    borderRadius: BorderRadius.circular(12),
                  ),
                  child: const Text(
                    'Dic 2025',
                    style: TextStyle(
                      color: Colors.white,
                      fontSize: 10,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }

  // -------------------------------------------------------------
  // GENERIC SECTION CONTAINER
  // -------------------------------------------------------------
  Widget _buildSection({
    required String title,
    required IconData icon,
    required Widget child,
  }) {
    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
      child: Container(
        decoration: BoxDecoration(
          color: Colors.white,
          borderRadius: BorderRadius.circular(15),
          boxShadow: [
            BoxShadow(
              color: Colors.grey.withOpacity(0.1),
              spreadRadius: 1,
              blurRadius: 5,
            ),
          ],
        ),
        child: Padding(
          padding: const EdgeInsets.all(16),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Row(
                children: [
                  Icon(icon, color: Colors.red[400], size: 20),
                  const SizedBox(width: 8),
                  Text(
                    title,
                    style: TextStyle(
                      fontSize: 16,
                      fontWeight: FontWeight.bold,
                      color: Colors.grey[800],
                    ),
                  ),
                ],
              ),
              const SizedBox(height: 15),
              child,
            ],
          ),
        ),
      ),
    );
  }

  // -------------------------------------------------------------
  // INFO ROW
  // -------------------------------------------------------------
  Widget _buildInfoRow(
    String label1,
    String value1,
    String label2,
    String value2,
  ) {
    return Row(
      children: [
        Expanded(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                label1,
                style: TextStyle(fontSize: 12, color: Colors.grey[600]),
              ),
              const SizedBox(height: 4),
              Text(
                value1,
                style: const TextStyle(
                  fontSize: 15,
                  fontWeight: FontWeight.w500,
                ),
              ),
            ],
          ),
        ),
        Expanded(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                label2,
                style: TextStyle(fontSize: 12, color: Colors.grey[600]),
              ),
              const SizedBox(height: 4),
              Text(
                value2,
                style: const TextStyle(
                  fontSize: 15,
                  fontWeight: FontWeight.w500,
                ),
              ),
            ],
          ),
        ),
      ],
    );
  }

  // -------------------------------------------------------------
  // ALLERGY ITEM
  // -------------------------------------------------------------
  Widget _buildAllergyItem(String name, String severity, Color color) {
    return Row(
      children: [
        Container(
          width: 8,
          height: 8,
          decoration: BoxDecoration(color: color, shape: BoxShape.circle),
        ),
        const SizedBox(width: 12),
        Text(name, style: const TextStyle(fontSize: 15)),
        const Spacer(),
        Container(
          padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
          decoration: BoxDecoration(
            color: color,
            borderRadius: BorderRadius.circular(12),
          ),
          child: Text(
            severity,
            style: const TextStyle(
              color: Colors.white,
              fontSize: 10,
              fontWeight: FontWeight.bold,
            ),
          ),
        ),
      ],
    );
  }

  // -------------------------------------------------------------
  // MEDICAL CONDITION ITEM
  // -------------------------------------------------------------
  Widget _buildConditionItem(String name, String status, Color color) {
    return Row(
      children: [
        Text(name, style: const TextStyle(fontSize: 15)),
        const Spacer(),
        Container(
          padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
          decoration: BoxDecoration(
            color: color,
            borderRadius: BorderRadius.circular(12),
          ),
          child: Text(
            status,
            style: const TextStyle(
              color: Colors.white,
              fontSize: 10,
              fontWeight: FontWeight.bold,
            ),
          ),
        ),
      ],
    );
  }

  // -------------------------------------------------------------
  // MEDICATION ITEM
  // -------------------------------------------------------------
  Widget _buildMedicationItem(String name, String dosage) {
    return Container(
      padding: const EdgeInsets.all(12),
      decoration: BoxDecoration(
        color: Colors.teal[50],
        borderRadius: BorderRadius.circular(10),
      ),
      child: Row(
        children: [
          Container(
            padding: const EdgeInsets.all(8),
            decoration: BoxDecoration(
              color: Colors.teal[100],
              borderRadius: BorderRadius.circular(8),
            ),
            child: Icon(Icons.medication, color: Colors.teal[700], size: 20),
          ),
          const SizedBox(width: 12),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  name,
                  style: const TextStyle(
                    fontSize: 15,
                    fontWeight: FontWeight.w500,
                  ),
                ),
                const SizedBox(height: 2),
                Text(
                  dosage,
                  style: TextStyle(fontSize: 12, color: Colors.grey[600]),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  // -------------------------------------------------------------
  // CONTACT ITEM
  // -------------------------------------------------------------
  Widget _buildContactItem(
    String name,
    String phone,
    String relation,
    Color color,
  ) {
    return Container(
      padding: const EdgeInsets.all(12),
      decoration: BoxDecoration(
        color: Colors.grey[100],
        borderRadius: BorderRadius.circular(10),
      ),
      child: Row(
        children: [
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  name,
                  style: const TextStyle(
                    fontSize: 15,
                    fontWeight: FontWeight.w500,
                  ),
                ),
                const SizedBox(height: 4),
                Row(
                  children: [
                    Icon(Icons.phone, size: 12, color: Colors.grey[600]),
                    const SizedBox(width: 4),
                    Text(
                      phone,
                      style: TextStyle(fontSize: 12, color: Colors.grey[600]),
                    ),
                  ],
                ),
              ],
            ),
          ),
          Container(
            padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
            decoration: BoxDecoration(
              color: color,
              borderRadius: BorderRadius.circular(12),
            ),
            child: Text(
              relation,
              style: const TextStyle(
                color: Colors.white,
                fontSize: 10,
                fontWeight: FontWeight.bold,
              ),
            ),
          ),
        ],
      ),
    );
  }
}
