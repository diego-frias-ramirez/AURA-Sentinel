// emergency_chat_screen.dart
import 'package:flutter/material.dart';
import 'emergency_footer.dart';
import 'emergency_header.dart';
import 'emergency_warning_banner.dart';
import 'message_input.dart';
import 'quick_replies.dart';
import 'sos_button.dart';

class EmergencyChatScreen extends StatelessWidget {
  const EmergencyChatScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.white,
      body: SafeArea(
        child: Center(
          child: Container(
            width: double.infinity,
            constraints: const BoxConstraints(maxWidth: 400),
            child: SingleChildScrollView(
              padding: const EdgeInsets.symmetric(
                horizontal: 16.0,
                vertical: 8.0,
              ),
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                crossAxisAlignment: CrossAxisAlignment.center,
                children: [
                  // 1. Header
                  const EmergencyHeader(),
                  // 2. Warning Banner
                  const SizedBox(height: 16),
                  const EmergencyWarningBanner(),
                  // 3. Title
                  const SizedBox(height: 24),
                  const Padding(
                    padding: EdgeInsets.symmetric(horizontal: 24.0),
                    child: Text(
                      '¿Qué emergencia tienes?',
                      style: TextStyle(
                        fontSize: 20,
                        fontWeight: FontWeight.bold,
                      ),
                      textAlign: TextAlign.center,
                    ),
                  ),
                  // 4. SOS Button
                  const SizedBox(height: 32),
                  const Center(child: SOSButton()),
                  // 5. Quick Replies
                  const SizedBox(height: 24),
                  const QuickReplies(),
                  // 6. Message Input
                  const SizedBox(height: 24),
                  const MessageInput(),
                  // 7. Footer
                  const SizedBox(height: 24),
                  const EmergencyFooter(),
                ],
              ),
            ),
          ),
        ),
      ),
    );
  }
}
