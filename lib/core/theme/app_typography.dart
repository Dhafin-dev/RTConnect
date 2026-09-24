import 'package:flutter/material.dart';
import 'app_colors.dart';

/// Design Tokens: Typography for RTConnect
class AppTypography {
  static const TextStyle displayLarge = TextStyle(
    fontSize: 24.0,
    fontWeight: FontWeight.w700,
    height: 32.0 / 24.0,
    color: AppColors.textPrimary,
  );

  static const TextStyle titleLarge = TextStyle(
    fontSize: 18.0,
    fontWeight: FontWeight.w600,
    height: 24.0 / 18.0,
    color: AppColors.textPrimary,
  );

  static const TextStyle titleMedium = TextStyle(
    fontSize: 16.0,
    fontWeight: FontWeight.w600,
    height: 22.0 / 16.0,
    color: AppColors.textPrimary,
  );

  static const TextStyle bodyLarge = TextStyle(
    fontSize: 14.0,
    fontWeight: FontWeight.w400,
    height: 20.0 / 14.0,
    color: AppColors.textPrimary,
  );

  static const TextStyle bodyMedium = TextStyle(
    fontSize: 13.0,
    fontWeight: FontWeight.w400,
    height: 18.0 / 13.0,
    color: AppColors.textSecondary,
  );

  static const TextStyle labelSmall = TextStyle(
    fontSize: 11.0,
    fontWeight: FontWeight.w500,
    height: 14.0 / 11.0,
    color: AppColors.textSecondary,
  );

  static const TextStyle buttonLabel = TextStyle(
    fontSize: 14.0,
    fontWeight: FontWeight.w600,
    height: 20.0 / 14.0,
    color: Colors.white,
  );

  // Convenient Aliases
  static const TextStyle heading1 = displayLarge;
  static const TextStyle heading2 = titleLarge;
  static const TextStyle heading3 = titleMedium;
  static const TextStyle bodySmall = labelSmall;
  static const TextStyle caption = labelSmall;
  static const TextStyle labelBold = TextStyle(
    fontSize: 13.0,
    fontWeight: FontWeight.w600,
    height: 18.0 / 13.0,
    color: AppColors.textPrimary,
  );
}
