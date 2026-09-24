import 'package:flutter/material.dart';

/// Design Tokens: Colors for RTConnect
class AppColors {
  // Brand & Accents
  static const Color primaryBrand = Color(0xFF1E3A8A); // Blue 900
  static const Color primary = primaryBrand;
  static const Color primaryLight = Color(0xFF3B82F6); // Blue 500
  static const Color primaryContainer = Color(0xFFEFF6FF); // Blue 50
  static const Color secondaryDark = Color(0xFF0F172A); // Slate 900
  static const Color brandWhatsApp = Color(0xFF25D366);
  static const Color success = Color(0xFF10B981);
  static const Color error = Color(0xFFEF4444);

  // Surfaces & Backgrounds
  static const Color background = Color(0xFFF8FAFC); // Slate 50
  static const Color surface = Color(0xFFFFFFFF);
  static const Color cardBackground = surface;
  static const Color surfaceAlt = Color(0xFFF1F5F9); // Slate 100
  static const Color border = Color(0xFFE2E8F0); // Slate 200

  // Text Colors
  static const Color textPrimary = Color(0xFF0F172A);
  static const Color textSecondary = Color(0xFF64748B);
  static const Color textMuted = Color(0xFF94A3B8);

  // Status Colors
  static const Color statusDiajukan = Color(0xFFF59E0B); // Amber 500
  static const Color statusRevisi = Color(0xFFEF4444); // Red 500
  static const Color statusDisetujui = Color(0xFF10B981); // Emerald 500
  static const Color statusSelesai = Color(0xFF059669); // Emerald 600
  static const Color statusDitolak = Color(0xFF6B7280); // Gray 500
  static const Color statusSiapDiambil = Color(0xFF0284C7); // Sky 600

  // Chat Bubbles
  static const Color chatBubbleBot = Color(0xFFF1F5F9);
  static const Color chatBubbleUser = Color(0xFF1E3A8A);
}
