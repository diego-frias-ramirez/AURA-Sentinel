import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

const String _apiKey = String.fromEnvironment('OPENAI_API_KEY');
const String _model = String.fromEnvironment('OPENAI_MODEL', defaultValue: 'gpt-4o-mini');

void main() {
  runApp(const ChatApp());
}

class ChatApp extends StatelessWidget {
  const ChatApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'AI Chatbot',
      theme: ThemeData(colorSchemeSeed: Colors.indigo, brightness: Brightness.light),
      darkTheme: ThemeData(colorSchemeSeed: Colors.indigo, brightness: Brightness.dark),
      home: const ChatPage(),
    );
  }
}

class Message {
  final String role;
  final String content;
  Message(this.role, this.content);
}

class AiClient {
  final String apiKey;
  final String model;
  AiClient({required this.apiKey, required this.model});

  Future<String> chat(List<Message> history, {String? system}) async {
    final uri = Uri.parse('https://api.openai.com/v1/chat/completions');
    final messages = <Map<String, String>>[];
    if (system != null && system.isNotEmpty) {
      messages.add({'role': 'system', 'content': system});
    }
    for (final m in history) {
      messages.add({'role': m.role, 'content': m.content});
    }
    final body = jsonEncode({
      'model': model,
      'messages': messages,
      'temperature': 0.7,
    });
    final res = await http.post(
      uri,
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer $apiKey',
      },
      body: body,
    );
    if (res.statusCode != 200) {
      throw Exception('Error ${res.statusCode}: ${res.body}');
    }
    final data = jsonDecode(res.body) as Map<String, dynamic>;
    final choices = data['choices'] as List<dynamic>;
    final msg = choices.first['message'] as Map<String, dynamic>;
    return msg['content'] as String;
  }
}

class ChatPage extends StatefulWidget {
  const ChatPage({super.key});

  @override
  State<ChatPage> createState() => _ChatPageState();
}

class _ChatPageState extends State<ChatPage> {
  final List<Message> _messages = [];
  final TextEditingController _controller = TextEditingController();
  bool _loading = false;
  late final AiClient _client;

  @override
  void initState() {
    super.initState();
    _client = AiClient(apiKey: _apiKey, model: _model);
  }

  Future<void> _send() async {
    final text = _controller.text.trim();
    if (text.isEmpty) return;
    if (_apiKey.isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('Define OPENAI_API_KEY')));
      return;
    }
    setState(() {
      _messages.add(Message('user', text));
      _controller.clear();
      _loading = true;
    });
    try {
      final reply = await _client.chat(_messages, system: 'Eres un asistente útil.');
      setState(() {
        _messages.add(Message('assistant', reply));
      });
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('$e')));
    } finally {
      setState(() {
        _loading = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('AI Chatbot')),
      body: Column(
        children: [
          Expanded(
            child: ListView.builder(
              padding: const EdgeInsets.all(12),
              itemCount: _messages.length,
              itemBuilder: (context, index) {
                final m = _messages[index];
                final isUser = m.role == 'user';
                return Align(
                  alignment: isUser ? Alignment.centerRight : Alignment.centerLeft,
                  child: Container(
                    margin: const EdgeInsets.symmetric(vertical: 6),
                    padding: const EdgeInsets.all(12),
                    decoration: BoxDecoration(
                      color: isUser ? Theme.of(context).colorScheme.primaryContainer : Theme.of(context).colorScheme.surfaceVariant,
                      borderRadius: BorderRadius.circular(12),
                    ),
                    child: Text(m.content),
                  ),
                );
              },
            ),
          ),
          SafeArea(
            child: Padding(
              padding: const EdgeInsets.fromLTRB(12, 6, 12, 12),
              child: Row(
                children: [
                  Expanded(
                    child: TextField(
                      controller: _controller,
                      minLines: 1,
                      maxLines: 5,
                      decoration: const InputDecoration(border: OutlineInputBorder(), hintText: 'Escribe tu mensaje'),
                      onSubmitted: (_) => _send(),
                    ),
                  ),
                  const SizedBox(width: 8),
                  _loading
                      ? const SizedBox(width: 48, height: 48, child: Padding(padding: EdgeInsets.all(8), child: CircularProgressIndicator()))
                      : IconButton(onPressed: _send, icon: const Icon(Icons.send)),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }
}
