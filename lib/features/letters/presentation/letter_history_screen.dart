import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import '../../../core/router/route_names.dart';
import '../../../core/theme/app_colors.dart';
import '../../../core/theme/app_spacing.dart';
import '../../../core/theme/app_typography.dart';
import '../../../shared/widgets/rt_status_badge.dart';
import 'letter_controller.dart';

class LetterHistoryScreen extends ConsumerStatefulWidget {
  const LetterHistoryScreen({super.key});

  @override
  ConsumerState<LetterHistoryScreen> createState() => _LetterHistoryScreenState();
}

class _LetterHistoryScreenState extends ConsumerState<LetterHistoryScreen> {
  String _selectedFilter = 'semua';

  @override
  Widget build(BuildContext context) {
    final applicationsAsync = ref.watch(myApplicationsProvider);

    return Scaffold(
      backgroundColor: AppColors.surface,
      appBar: AppBar(
        title: const Text('Riwayat Pengajuan Surat', style: AppTypography.heading3),
        centerTitle: true,
        backgroundColor: AppColors.surface,
        elevation: 0,
        leading: IconButton(
          icon: const Icon(Icons.arrow_back, color: AppColors.textPrimary),
          onPressed: () => context.go(RouteNames.wargaHome),
        ),
      ),
      body: SafeArea(
        child: Column(
          children: [
            // Filter Bar
            SingleChildScrollView(
              scrollDirection: Axis.horizontal,
              padding: const EdgeInsets.symmetric(horizontal: AppSpacing.md, vertical: AppSpacing.sm),
              child: Row(
                children: [
                  _buildFilterChip('Semua', 'semua'),
                  _buildFilterChip('Diajukan', 'diajukan'),
                  _buildFilterChip('Perlu Revisi', 'perlu_revisi'),
                  _buildFilterChip('Disetujui', 'disetujui'),
                  _buildFilterChip('Selesai', 'selesai'),
                ],
              ),
            ),
            const Divider(height: 1),

            // Daftar Pengajuan
            Expanded(
              child: applicationsAsync.when(
                loading: () => const Center(child: CircularProgressIndicator()),
                error: (err, _) => Center(
                  child: Column(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      const Icon(Icons.error_outline, size: 48, color: AppColors.error),
                      const SizedBox(height: AppSpacing.sm),
                      Text('Gagal memuat data surat: $err', style: AppTypography.bodySmall),
                      TextButton(
                        onPressed: () => ref.refresh(myApplicationsProvider),
                        child: const Text('Coba Lagi'),
                      ),
                    ],
                  ),
                ),
                data: (apps) {
                  final filtered = _selectedFilter == 'semua'
                      ? apps
                      : apps.where((a) => a['status'] == _selectedFilter).toList();

                  if (filtered.isEmpty) {
                    return Center(
                      child: Column(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          Icon(Icons.inbox_outlined, size: 64, color: AppColors.textSecondary.withValues(alpha: 0.5)),
                          const SizedBox(height: AppSpacing.sm),
                          const Text('Belum ada riwayat pengajuan', style: AppTypography.heading3),
                          const Text('Pengajuan surat yang Anda buat akan muncul di sini.', style: AppTypography.caption),
                        ],
                      ),
                    );
                  }

                  return RefreshIndicator(
                    onRefresh: () async => ref.refresh(myApplicationsProvider),
                    child: ListView.separated(
                      padding: const EdgeInsets.all(AppSpacing.md),
                      itemCount: filtered.length,
                      separatorBuilder: (_, __) => const SizedBox(height: AppSpacing.sm),
                      itemBuilder: (context, index) {
                        final item = filtered[index];
                        final id = item['pengajuan_id'] as int;
                        final nomorPengajuan = item['nomor_pengajuan']?.toString() ?? '-';
                        final namaSurat = item['nama_surat']?.toString() ?? 'Surat Pengantar';
                        final keperluan = item['keperluan']?.toString() ?? '-';
                        final status = item['status']?.toString() ?? 'diajukan';
                        final metode = item['metode_tanda_tangan']?.toString() ?? 'digital';

                        return Card(
                          elevation: 1,
                          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                          child: InkWell(
                            borderRadius: BorderRadius.circular(12),
                            onTap: () => context.push('/letters/$id'),
                            child: Padding(
                              padding: const EdgeInsets.all(AppSpacing.md),
                              child: Column(
                                crossAxisAlignment: CrossAxisAlignment.start,
                                children: [
                                  Row(
                                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                                    children: [
                                      Text(
                                        nomorPengajuan,
                                        style: AppTypography.caption.copyWith(fontWeight: FontWeight.bold),
                                      ),
                                      RTStatusBadge(status: status),
                                    ],
                                  ),
                                  const SizedBox(height: AppSpacing.xs),
                                  Text(namaSurat, style: AppTypography.heading3),
                                  const SizedBox(height: 4),
                                  Text(
                                    keperluan,
                                    maxLines: 2,
                                    overflow: TextOverflow.ellipsis,
                                    style: AppTypography.bodySmall,
                                  ),
                                  const SizedBox(height: AppSpacing.sm),
                                  Row(
                                    children: [
                                      Icon(
                                        metode == 'digital' ? Icons.draw : Icons.edit_note,
                                        size: 16,
                                        color: AppColors.textSecondary,
                                      ),
                                      const SizedBox(width: 4),
                                      Text(
                                        metode == 'digital' ? 'TTD Digital' : 'TTD Basah',
                                        style: AppTypography.caption,
                                      ),
                                      const Spacer(),
                                      const Icon(Icons.arrow_forward_ios, size: 14, color: AppColors.textSecondary),
                                    ],
                                  ),
                                ],
                              ),
                            ),
                          ),
                        );
                      },
                    ),
                  );
                },
              ),
            ),
          ],
        ),
      ),
      floatingActionButton: FloatingActionButton.extended(
        backgroundColor: AppColors.primary,
        onPressed: () => context.push(RouteNames.wargaPengajuanBaru),
        icon: const Icon(Icons.add, color: Colors.white),
        label: const Text('Ajukan Surat', style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold)),
      ),
    );
  }

  Widget _buildFilterChip(String label, String value) {
    final isSelected = _selectedFilter == value;
    return Padding(
      padding: const EdgeInsets.only(right: AppSpacing.xs),
      child: FilterChip(
        label: Text(label),
        selected: isSelected,
        selectedColor: AppColors.primary.withValues(alpha: 0.2),
        checkmarkColor: AppColors.primary,
        onSelected: (_) => setState(() => _selectedFilter = value),
      ),
    );
  }
}
