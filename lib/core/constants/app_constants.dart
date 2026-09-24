import 'dart:io' show Platform;
import 'package:flutter/foundation.dart';

/// Application-wide constants for RTConnect
class AppConstants {
  static const String appName = 'RTConnect';
  static const String appTagline = 'Aplikasi Administrasi Warga RT 032 RW 08';

  // Environment & Base URL with automatic emulator/desktop detection
  static String get defaultBaseUrl {
    if (kIsWeb) return 'http://127.0.0.1:5000/api/v1';
    try {
      if (Platform.isAndroid) return 'http://10.0.2.2:5000/api/v1';
    } catch (_) {}
    return 'http://127.0.0.1:5000/api/v1';
  }

  // Secure Storage Keys
  static const String keyAuthToken = 'auth_token';
  static const String keyUserRole = 'user_role';
  static const String keyUserId = 'user_id';
  static const String keyUserNik = 'user_nik';
  static const String keyUserName = 'user_name';

  // Support Contacts
  static const String defaultRTWhatsApp = '6281234567890';
}
