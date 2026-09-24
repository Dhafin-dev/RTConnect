import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import '../../core/router/route_names.dart';
import '../../core/theme/app_colors.dart';
import '../../core/theme/app_spacing.dart';
import '../../core/theme/app_typography.dart';
import 'rt_primary_button.dart';

/// COMP-SHR-003: RTDrawerMenu
class RTDrawerMenu extends StatelessWidget {
  final String userName;
  final String userEmail;
  final String userRole;
  final VoidCallback onLogout;

  const RTDrawerMenu({
    super.key,
    required this.userName,
    required this.userEmail,
    required this.userRole,
    required this.onLogout,
  });

  @override
  Widget build(BuildContext context) {
    final isRT = userRole.toLowerCase() == 'rt';

    return Drawer(
      backgroundColor: AppColors.surface,
      child: SafeArea(
        child: Padding(
          padding: const EdgeInsets.symmetric(
            horizontal: AppSpacing.spaceLG,
            vertical: AppSpacing.spaceMD,
          ),
          child: Column(
            children: [
              // Avatar
              CircleAvatar(
                radius: AppSpacing.avatarDiameter / 2,
                backgroundColor: AppColors.secondaryDark,
                child: Text(
                  userName.isNotEmpty ? userName[0].toUpperCase() : 'U',
                  style: const TextStyle(
                    fontSize: 24,
                    color: Colors.white,
                    fontWeight: FontWeight.bold,
                  ),
                ),
              ),
              const SizedBox(height: AppSpacing.spaceSM),
              // User Meta
              Text(
                'Halo, $userName',
                style: AppTypography.titleMedium.copyWith(fontWeight: FontWeight.w700),
              ),
              Text(userEmail, style: AppTypography.bodyMedium),
              const SizedBox(height: AppSpacing.spaceXS),
              Container(
                padding: const EdgeInsets.symmetric(
                  horizontal: AppSpacing.spaceXS,
                  vertical: 2.0,
                ),
                decoration: BoxDecoration(
                  color: isRT ? AppColors.primaryContainer : AppColors.surfaceAlt,
                  borderRadius: BorderRadius.circular(AppSpacing.radiusXS),
                ),
                child: Text(
                  userRole,
                  style: AppTypography.labelSmall.copyWith(
                    color: isRT ? AppColors.primaryBrand : AppColors.textSecondary,
                    fontWeight: FontWeight.w600,
                  ),
                ),
              ),
              const SizedBox(height: AppSpacing.spaceLG),
              const Divider(color: AppColors.border),

              // Navigation tiles
              Expanded(
                child: ListView(
                  children: [
                    _buildDrawerTile(
                      icon: Icons.person_outline,
                      title: 'Profil Saya',
                      onTap: () => Navigator.pop(context),
                    ),
                    _buildDrawerTile(
                      icon: Icons.history,
                      title: isRT ? 'Daftar Pengajuan Masuk' : 'Riwayat Pengajuan',
                      onTap: () {
                        Navigator.pop(context);
                        context.go(isRT ? RouteNames.rtQueue : RouteNames.wargaPengajuan);
                      },
                    ),
                    _buildDrawerTile(
                      icon: Icons.settings_outlined,
                      title: 'Pengaturan',
                      onTap: () => Navigator.pop(context),
                    ),
                  ],
                ),
              ),

              // Log Out Button
              RTPrimaryButton(
                text: 'Log Out',
                backgroundColor: AppColors.secondaryDark,
                onPressed: () {
                  Navigator.pop(context);
                  onLogout();
                },
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildDrawerTile({
    required IconData icon,
    required String title,
    required VoidCallback onTap,
  }) {
    return ListTile(
      leading: Icon(icon, color: AppColors.secondaryDark, size: 22),
      title: Text(title, style: AppTypography.bodyLarge),
      contentPadding: EdgeInsets.zero,
      onTap: onTap,
    );
  }
}
