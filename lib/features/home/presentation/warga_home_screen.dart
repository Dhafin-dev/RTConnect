import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import '../../../core/router/route_names.dart';
import '../../../core/theme/app_colors.dart';
import '../../../core/theme/app_spacing.dart';
import '../../../core/theme/app_typography.dart';
import '../../../shared/widgets/rt_status_badge.dart';
import '../../auth/presentation/auth_controller.dart';
import '../../letters/presentation/letter_controller.dart';

class WargaHomeScreen extends ConsumerWidget {
  const WargaHomeScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final authState = ref.watch(authControllerProvider);
    final user = authState.user;
    final myAppsAsync = ref.watch(myApplicationsProvider);

    final namaWarga = user?.namaLengkap ?? 'Warga RT 032';

    return Scaffold(
      backgroundColor: AppColors.surface,
      appBar: AppBar(
        title: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text('RTConnect', style: AppTypography.heading2.copyWith(color: AppColors.primary)),
            const Text('RT 032 RW 08 Griya Taman Asri', style: AppTypography.caption),
          ],
        ),
        backgroundColor: AppColors.surface,
        elevation: 0,
        actions: [
          IconButton(
            icon: const Icon(Icons.notifications_none, color: AppColors.textPrimary),
            onPressed: () => context.push(RouteNames.notifications),
          ),
          IconButton(
            icon: const Icon(Icons.logout, color: AppColors.textSecondary),
            onPressed: () async {
              await ref.read(authControllerProvider.notifier).logout();
              if (context.mounted) context.go(RouteNames.login);
            },
          ),
        ],
      ),
      body: SafeArea(
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(AppSpacing.lg),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              // Greeting Banner Card
              Container(
                width: double.infinity,
                padding: const EdgeInsets.all(AppSpacing.lg),
                decoration: BoxDecoration(
                  gradient: const LinearGradient(
                    colors: [Color(0xFF0F172A), Color(0xFF1E293B)],
                    begin: Alignment.topLeft,
                    end: Alignment.bottomRight,
                  ),
                  borderRadius: BorderRadius.circular(16),
                ),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text('Halo, $namaWarga 👋', style: AppTypography.heading2.copyWith(color: Colors.white)),
                    const SizedBox(height: 4),
                    Text(
                      'Layanan administrasi rukun tetangga berbasis digital & AI.',
                      style: AppTypography.bodySmall.copyWith(color: Colors.white70),
                    ),
                  ],
                ),
              ),
              const SizedBox(height: AppSpacing.lg),

              // Menu Layanan Utama
              const Text('Menu Layanan', style: AppTypography.heading3),
              const SizedBox(height: AppSpacing.md),
              Row(
                children: [
                  Expanded(
                    child: _buildServiceCard(
                      context,
                      icon: Icons.note_add_outlined,
                       title: 'Ajukan Surat',
                      desc: 'Buat surat pengantar baru',
                      color: AppColors.primary,
                      onTap: () => context.push(RouteNames.wargaPengajuanBaru),
                    ),
                  ),
                  const SizedBox(width: AppSpacing.md),
                  Expanded(
                    child: _buildServiceCard(
                      context,
                      icon: Icons.smart_toy_outlined,
                      title: 'Tanya RT',
                      desc: 'AI Assistant warga 24/7',
                      color: Colors.indigo,
                      onTap: () => context.push(RouteNames.chatbot),
                    ),
                  ),
                ],
              ),
              const SizedBox(height: AppSpacing.md),
              Row(
                children: [
                  Expanded(
                    child: _buildServiceCard(
                      context,
                      icon: Icons.history,
                      title: 'Riwayat Surat',
                      desc: 'Pantau status permohonan',
                      color: Colors.teal,
                      onTap: () => context.push(RouteNames.wargaPengajuan),
                    ),
                  ),
                  const SizedBox(width: AppSpacing.md),
                  Expanded(
                    child: _buildServiceCard(
                      context,
                      icon: Icons.account_balance_wallet_outlined,
                      title: 'Iuran Kas',
                      desc: 'Informasi kas lingkungan',
                      color: Colors.deepOrange,
                      onTap: () {
                        showDialog<void>(
                          context: context,
                          builder: (c) => AlertDialog(
                            title: const Text('Iuran Lingkungan RT 032'),
                            content: const Text(
                              'Iuran kas kebersihan dan keamanan RT 032 sebesar Rp50.000/bulan dibayarkan paling lambat tanggal 10 setiap bulannya ke bendahara RT.',
                            ),
                            actions: [
                              TextButton(onPressed: () => Navigator.pop(c), child: const Text('Tutup')),
                            ],
                          ),
                        );
                      },
                    ),
                  ),
                ],
              ),
              const SizedBox(height: AppSpacing.xl),

              // Pengajuan Terkini
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  const Text('Pengajuan Surat Terkini', style: AppTypography.heading3),
                  TextButton(
                    onPressed: () => context.push(RouteNames.wargaPengajuan),
                    child: const Text('Lihat Semua'),
                  ),
                ],
              ),
              const SizedBox(height: AppSpacing.xs),
              myAppsAsync.when(
                loading: () => const Center(child: CircularProgressIndicator()),
                error: (err, _) => Text('Gagal memuat status: $err'),
                data: (apps) {
                  if (apps.isEmpty) {
                    return Container(
                      padding: const EdgeInsets.all(AppSpacing.lg),
                      decoration: BoxDecoration(
                        color: AppColors.cardBackground,
                        borderRadius: BorderRadius.circular(12),
                        border: Border.all(color: AppColors.border),
                      ),
                      child: const Center(
                        child: Text('Belum ada permohonan surat aktif.', style: AppTypography.bodySmall),
                      ),
                    );
                  }

                  final latest = apps.first;
                  final id = latest['pengajuan_id'] as int;
                  final namaSurat = latest['nama_surat']?.toString() ?? 'Surat Pengantar';
                  final nomorPengajuan = latest['nomor_pengajuan']?.toString() ?? '-';
                  final status = latest['status']?.toString() ?? 'diajukan';

                  return Card(
                    elevation: 1,
                    shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                    child: ListTile(
                      contentPadding: const EdgeInsets.all(AppSpacing.md),
                      title: Text(namaSurat, style: AppTypography.heading3),
                      subtitle: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          const SizedBox(height: 4),
                          Text('Nomor: $nomorPengajuan', style: AppTypography.caption),
                          const SizedBox(height: AppSpacing.xs),
                          RTStatusBadge(status: status),
                        ],
                      ),
                      trailing: const Icon(Icons.arrow_forward_ios, size: 16),
                      onTap: () => context.push('/letters/$id'),
                    ),
                  );
                },
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildServiceCard(
    BuildContext context, {
    required IconData icon,
    required String title,
    required String desc,
    required Color color,
    required VoidCallback onTap,
  }) {
    return Card(
      elevation: 1,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
      child: InkWell(
        borderRadius: BorderRadius.circular(12),
        onTap: onTap,
        child: Padding(
          padding: const EdgeInsets.all(AppSpacing.md),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              CircleAvatar(
                radius: 20,
                backgroundColor: color.withValues(alpha: 0.12),
                child: Icon(icon, color: color, size: 22),
              ),
              const SizedBox(height: AppSpacing.sm),
              Text(title, style: AppTypography.labelBold),
              const SizedBox(height: 2),
              Text(desc, style: AppTypography.caption, maxLines: 1, overflow: TextOverflow.ellipsis),
            ],
          ),
        ),
      ),
    );
  }
}
