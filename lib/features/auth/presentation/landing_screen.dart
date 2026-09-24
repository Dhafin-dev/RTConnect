import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import '../../../core/router/route_names.dart';
import '../../../core/theme/app_colors.dart';
import '../../../core/theme/app_spacing.dart';
import '../../../core/theme/app_typography.dart';
import '../../../shared/widgets/rt_bottom_nav_bar.dart';
import '../../../shared/widgets/rt_primary_button.dart';
import '../../../shared/widgets/rt_secondary_button.dart';

/// SCREEN-001: Landing Page (Welcome Screen)
class LandingScreen extends StatelessWidget {
  const LandingScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.background,
      body: SafeArea(
        child: Padding(
          padding: const EdgeInsets.symmetric(horizontal: AppSpacing.spaceLG),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              const Spacer(),
              // Hero Brand Title
              Text(
                'Selamat Datang',
                style: AppTypography.displayLarge.copyWith(
                  color: AppColors.textSecondary,
                  fontSize: 20,
                  fontWeight: FontWeight.w500,
                ),
              ),
              const SizedBox(height: AppSpacing.spaceXS),
              Text(
                'RTConnect',
                style: AppTypography.displayLarge.copyWith(
                  color: AppColors.textPrimary,
                  fontSize: 32,
                  fontWeight: FontWeight.w800,
                  letterSpacing: -0.5,
                ),
              ),
              const SizedBox(height: AppSpacing.space2XL),

              // Action Buttons
              RTSecondaryButton(
                text: 'Masuk',
                onPressed: () => context.push(RouteNames.login),
              ),
              const SizedBox(height: AppSpacing.spaceSM),
              RTSecondaryButton(
                text: 'Registrasi',
                onPressed: () => context.push(RouteNames.register),
              ),
              const Spacer(),
            ],
          ),
        ),
      ),
      bottomNavigationBar: RTBottomNavBar(
        currentIndex: 1, // Beranda
        onTap: (index) {
          if (index == 0) context.push(RouteNames.login);
          if (index == 2) context.push(RouteNames.login);
        },
      ),
    );
  }
}
