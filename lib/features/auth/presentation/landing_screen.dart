import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import '../../../core/router/route_names.dart';
import '../../../core/theme/app_colors.dart';
import '../../../core/theme/app_spacing.dart';
import '../../../core/theme/app_typography.dart';
import '../../../shared/widgets/rt_primary_button.dart';
import '../../../shared/widgets/rt_secondary_button.dart';

/// SCREEN-001: Landing Page (Welcome Screen)
class LandingScreen extends StatelessWidget {
  const LandingScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.surface,
      body: SafeArea(
        child: Padding(
          padding: const EdgeInsets.symmetric(horizontal: AppSpacing.lg),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              const Spacer(),
              // Hero Icon & Brand
              Container(
                width: 88,
                height: 88,
                decoration: BoxDecoration(
                  color: AppColors.primary.withOpacity(0.1),
                  shape: BoxShape.circle,
                ),
                child: const Icon(
                  Icons.mark_email_read_outlined,
                  size: 48,
                  color: AppColors.primary,
                ),
              ),
              const SizedBox(height: AppSpacing.md),
              Text(
                'RTConnect',
                style: AppTypography.heading1.copyWith(
                  color: AppColors.primary,
                  fontSize: 32,
                  fontWeight: FontWeight.w800,
                ),
              ),
              const SizedBox(height: AppSpacing.xs),
              Text(
                'Sistem Administrasi RT 032 RW 08\nPerumahan Griya Taman Asri, Sidoarjo',
                textAlign: TextAlign.center,
                style: AppTypography.bodyMedium.copyWith(color: AppColors.textSecondary),
              ),
              const SizedBox(height: AppSpacing.xl),

              // Feature Badges
              Wrap(
                spacing: 8,
                runSpacing: 8,
                alignment: WrapWrapAlignment.center,
                children: [
                  _buildFeatureBadge(Icons.auto_awesome, 'AI Draft Narasi'),
                  _buildFeatureBadge(Icons.draw, 'TTD Digital Sah'),
                  _buildFeatureBadge(Icons.smart_toy, 'Tanya RT 24/7'),
                ],
              ),
              const Spacer(),

              // Action Buttons
              RTPrimaryButton(
                text: 'Masuk ke Akun',
                onPressed: () => context.push(RouteNames.login),
              ),
              const SizedBox(height: AppSpacing.sm),
              RTSecondaryButton(
                text: 'Registrasi Warga Baru',
                onPressed: () => context.push(RouteNames.register),
              ),
              const SizedBox(height: AppSpacing.xl),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildFeatureBadge(IconData icon, String text) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 6),
      decoration: BoxDecoration(
        color: AppColors.cardBackground,
        borderRadius: BorderRadius.circular(20),
        border: Border.all(color: AppColors.border),
      ),
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          Icon(icon, size: 14, color: AppColors.primary),
          const SizedBox(width: 4),
          Text(text, style: AppTypography.caption.copyWith(fontWeight: FontWeight.w600)),
        ],
      ),
    );
  }
}
