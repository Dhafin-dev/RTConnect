import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import '../../../core/router/route_names.dart';
import '../../../core/theme/app_colors.dart';
import '../../../core/theme/app_spacing.dart';
import '../../../core/theme/app_typography.dart';
import '../../auth/presentation/auth_controller.dart';
import '../../letters/presentation/letter_controller.dart';

class RTHomeScreen extends ConsumerWidget {
  const RTHomeScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final authState = ref.watch(authControllerProvider);
    final user = authState.user;
    final queueAsync = ref.watch(incomingQueueProvider);

    final rtName = user?.namaLengkap ?? 'Pak RT Indra';

    return Scaffold(
      backgroundColor: AppColors.surface,
      appBar: AppBar(
        title: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text('RTConnect — Panel RT', style: AppTypography.heading3.copyWith(color: AppColors.primary)),
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
              // Hero Banner
              Container(
                width: double.infinity,
                padding: const EdgeInsets.all(AppSpacing.lg),
                decoration: BoxDecoration(
                  gradient: const LinearGradient(
                    colors: [Color(0xFF1E3A8A), Color(0xFF0F172A)],
                    begin: Alignment.topLeft,
                    end: Alignment.bottomRight,
                  ),
                  borderRadius: BorderRadius.circular(16),
                ),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text('Selamat Bertugas, $rtName', style: AppTypography.heading2.copyWith(color: Colors.white)),
                    const SizedBox(height: 4),
                    Text(
                      'Kelola pengesahan surat pengantar digital & verifikasi permohonan warga.',
                      style: AppTypography.bodySmall.copyWith(color: Colors.white70),
                    ),
                  ],
                ),
              ),
              const SizedBox(height: AppSpacing.lg),

              // Metrik Counter
              queueAsync.when(
                loading: () => const Center(child: CircularProgressIndicator()),
                error: (e, _) => Text('Error: $e'),
                data: (queue) {
                  final totalDiajukan = queue.where((q) => q['status'] == 'diajukan').length;
                  final totalRevisi = queue.where((q) => q['status'] == 'perlu_revisi').length;
                  final totalSelesai = queue.where((q) => q['status'] == 'selesai' || q['status'] == 'siap_diambil').length;

                  return Row(
                    children: [
                      Expanded(
                        child: _buildMetricCard(
                          title: 'Perlu Review',
                          count: totalDiajukan.toString(),
                          color: AppColors.primary,
                          icon: Icons.hourglass_top,
                        ),
                      ),
                      const SizedBox(width: AppSpacing.sm),
                      Expanded(
                        child: _buildMetricCard(
                          title: 'Perlu Revisi',
                          count: totalRevisi.toString(),
                          color: Colors.amber.shade800,
                          icon: Icons.edit_note,
                        ),
                      ),
                      const SizedBox(width: AppSpacing.sm),
                      Expanded(
                        child: _buildMetricCard(
                          title: 'Selesai',
                          count: totalSelesai.toString(),
                          color: AppColors.success,
                          icon: Icons.check_circle_outline,
                        ),
                      ),
                    ],
                  );
                },
              ),
              const SizedBox(height: AppSpacing.xl),

              // Menu Cepat Tindakan
              const Text('Tindakan Administrasi', style: AppTypography.heading3),
              const SizedBox(height: AppSpacing.md),
              Card(
                elevation: 1,
                shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                child: ListTile(
                  leading: const CircleAvatar(
                    backgroundColor: Color(0xFFEFF6FF),
                    child: Icon(Icons.rate_review_outlined, color: AppColors.primary),
                  ),
                  title: const Text('Buka Antrean Verifikasi Surat', style: AppTypography.labelBold),
                  subtitle: const Text('Tinjau draf AI, sahkan TTD digital, atau setujui TTD basah.', style: AppTypography.caption),
                  trailing: const Icon(Icons.arrow_forward_ios, size: 16),
                  onTap: () => context.push(RouteNames.rtQueue),
                ),
              ),
              const SizedBox(height: AppSpacing.sm),
              Card(
                elevation: 1,
                shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                child: ListTile(
                  leading: const CircleAvatar(
                    backgroundColor: Color(0xFFF0FDF4),
                    child: Icon(Icons.chat_bubble_outline, color: AppColors.success),
                  ),
                  title: const Text('Uji Coba Tanya RT (RAG)', style: AppTypography.labelBold),
                  subtitle: const Text('Pantau kecocokan data peraturan RT dan simulasi asisten AI.', style: AppTypography.caption),
                  trailing: const Icon(Icons.arrow_forward_ios, size: 16),
                  onTap: () => context.push(RouteNames.chatbot),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildMetricCard({
    required String title,
    required String count,
    required Color color,
    required IconData icon,
  }) {
    return Container(
      padding: const EdgeInsets.all(AppSpacing.md),
      decoration: BoxDecoration(
        color: color.withValues(alpha: 0.08),
        borderRadius: BorderRadius.circular(12),
        border: Border.all(color: color.withValues(alpha: 0.2)),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Icon(icon, color: color, size: 20),
          const SizedBox(height: AppSpacing.xs),
          Text(count, style: AppTypography.heading1.copyWith(color: color)),
          Text(title, style: AppTypography.caption.copyWith(fontWeight: FontWeight.bold)),
        ],
      ),
    );
  }
}
