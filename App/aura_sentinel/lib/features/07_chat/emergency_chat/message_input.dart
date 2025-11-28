import 'package:flutter/material.dart';

class MessageInput extends StatelessWidget {
  const MessageInput({super.key});

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 24.0, vertical: 16.0),
      child: Container(
        padding: const EdgeInsets.symmetric(horizontal: 12),
        decoration: BoxDecoration(
          color: Colors.grey.shade100,
          borderRadius: BorderRadius.circular(24),
        ),
        child: Row(
          children: [
            IconButton(
              onPressed: () {},
              icon: Icon(Icons.attach_file, color: Colors.grey.shade600),
            ),
            Expanded(
              child: TextField(
                decoration: InputDecoration(
                  hintText: 'Escribe tu mensaje...',
                  border: InputBorder.none,
                  hintStyle: TextStyle(color: Colors.grey.shade500),
                ),
              ),
            ),
            IconButton(
              onPressed: () {},
              icon: Icon(
                Icons.emoji_emotions_outlined,
                color: Colors.grey.shade600,
              ),
            ),
            IconButton(
              onPressed: () {},
              icon: Icon(Icons.send, color: Colors.blue.shade600),
            ),
          ],
        ),
      ),
    );
  }
}
