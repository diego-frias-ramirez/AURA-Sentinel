// lib/features/07_chat/presentation/widgets/quick_replies.dart
import 'package:flutter/material.dart';
// ignore: unused_import
import 'package:aura_sentinel/core/theme/app_theme.dart';

class QuickReplies extends StatelessWidget {
  const QuickReplies({super.key});

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 24.0, vertical: 16.0),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            'Respuestas rápidas:',
            style: TextStyle(
              color: Colors.grey[700],
              fontSize: 14,
              fontWeight: FontWeight.w500,
            ),
          ),
          const SizedBox(height: 8),
          Wrap(
            spacing: 8,
            runSpacing: 8,
            children: [
              _buildQuickReplyButton(
                context,
                icon: Icons.chat_bubble_outline,
                label: 'Necesito hablar ahora',
              ),
              _buildQuickReplyButton(
                context,
                icon: Icons.favorite_border,
                label: 'Técnicas de respiración',
              ),
            ],
          ),
        ],
      ),
    );
  }

  Widget _buildQuickReplyButton(
    BuildContext context, {
    required IconData icon,
    required String label,
  }) {
    return GestureDetector(
      onTap: () {
        ScaffoldMessenger.of(
          context,
        ).showSnackBar(SnackBar(content: Text('Seleccionaste: $label')));
      },
      child: Chip(
        label: Row(
          children: [
            Icon(icon, size: 16, color: Colors.grey[600]),
            const SizedBox(width: 4),
            Text(
              label,
              style: TextStyle(fontSize: 14, color: Colors.grey[700]),
            ),
          ],
        ),
        backgroundColor: Colors.grey[100],
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(20)),
        padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
      ),
    );
  }
}
