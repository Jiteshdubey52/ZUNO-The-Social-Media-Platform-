import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

void main() {
  runApp(const ProviderScope(child: ZunoApp()));
}

class ZunoApp extends StatelessWidget {
  const ZunoApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'ZUNO',
      themeMode: ThemeMode.system,
      theme: ThemeData.light(useMaterial3: true),
      darkTheme: ThemeData.dark(useMaterial3: true),
      home: const ZunoHome(),
    );
  }
}

class ZunoHome extends StatelessWidget {
  const ZunoHome({super.key});

  @override
  Widget build(BuildContext context) {
    final screens = <String>[
      'Auth',
      'Feed',
      'Create Post',
      'Profile',
      'Follow List',
      'Chat',
      'Notifications',
      'Verification / Monetization',
      'Report / Safety',
    ];
    return Scaffold(
      appBar: AppBar(title: const Text('ZUNO')),
      body: ListView.builder(
        itemCount: screens.length,
        itemBuilder: (context, index) => ListTile(
          title: Text(screens[index]),
          subtitle: const Text('Clean architecture feature module ready for implementation'),
        ),
      ),
    );
  }
}
