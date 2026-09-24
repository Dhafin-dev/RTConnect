import 'package:flutter/material.dart';
import '../../core/theme/app_colors.dart';
import '../../core/theme/app_spacing.dart';
import '../../core/theme/app_typography.dart';

/// COMP-CORE-004: RTStatusBadge
class RTStatusBadge extends StatelessWidget {
  final String status;

  const RTStatusBadge({super.key, required this.status});

  @override
  Widget build(BuildContext context) {
    Color bg;
    Color fg;
    String label;

    switch (status.toLowerCase()) {
      case 'diajukan':
        bg = AppColors.statusDiajukan.withOpacity(0.15);
        fg = const Color(0xFFB45309); // Amber 700
        label = 'Diajukan';
        break;
      case 'perlu_revisi':
        bg = AppColors.statusRevisi.withOpacity(0.15);
        fg = AppColors.statusRevisi;
        label = 'Perlu Revisi';
        break;
      case 'disetujui':
        bg = AppColors.statusDisetujui.withOpacity(0.15);
        fg = AppColors.statusDisetujui;
        label = 'Disetujui';
        break;
      case 'siap_diambil':
        bg = AppColors.statusSiapDiambil.withOpacity(0.15);
        fg = AppColors.statusSiapDiambil;
        label = 'Siap Diambil';
        break;
      case 'selesai':
        bg = AppColors.statusSelesai.withOpacity(0.15);
        fg = AppColors.statusSelesai;
        label = 'Selesai';
        break;
      case 'ditolak':
      default:
        bg = AppColors.statusDitolak.withOpacity(0.15);
        fg = AppColors.statusDitolak;
        label = 'Ditolak';
        break;
    }

    return Container(
      padding: const EdgeInsets.symmetric(
        horizontal: AppSpacing.spaceXS,
        vertical: AppSpacing.space2XS,
      ),
      decoration: BoxDecoration(
        color: bg,
        borderRadius: BorderRadius.circular(AppSpacing.radiusXS),
      ),
      child: Text(
        label,
        style: AppTypography.labelSmall.copyWith(
          color: fg,
          fontWeight: FontWeight.w600,
        ),
      ),
    );
  }
}
