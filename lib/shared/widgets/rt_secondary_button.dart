import 'package:flutter/material.dart';
import '../../core/theme/app_colors.dart';
import '../../core/theme/app_spacing.dart';
import '../../core/theme/app_typography.dart';

/// COMP-CORE-002: RTSecondaryButton
class RTSecondaryButton extends StatelessWidget {
  final String text;
  final VoidCallback? onPressed;
  final IconData? icon;

  const RTSecondaryButton({
    super.key,
    required this.text,
    this.onPressed,
    this.icon,
  });

  @override
  Widget build(BuildContext context) {
    return SizedBox(
      height: AppSpacing.buttonHeight,
      width: double.infinity,
      child: OutlinedButton(
        style: OutlinedButton.styleFrom(
          backgroundColor: AppColors.surfaceAlt,
          foregroundColor: AppColors.secondaryDark,
          elevation: 0,
          side: const BorderSide(color: AppColors.border, width: 1.0),
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(AppSpacing.radiusSM),
          ),
          padding: const EdgeInsets.symmetric(horizontal: AppSpacing.spaceMD),
        ),
        onPressed: onPressed,
        child: Row(
          mainAxisAlignment: MainAxisAlignment.center,
          mainAxisSize: MainAxisSize.min,
          children: [
            if (icon != null) ...[
              Icon(icon, size: 18, color: AppColors.secondaryDark),
              const SizedBox(width: AppSpacing.spaceXS),
            ],
            Text(
              text,
              style: AppTypography.buttonLabel.copyWith(color: AppColors.secondaryDark),
            ),
          ],
        ),
      ),
    );
  }
}
