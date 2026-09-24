import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import '../../../core/theme/app_colors.dart';
import '../../../core/theme/app_spacing.dart';
import '../../../core/theme/app_typography.dart';
import '../../../shared/widgets/rt_primary_button.dart';
import '../../../shared/widgets/rt_status_badge.dart';
import 'letter_controller.dart';

class LetterDetailScreen extends ConsumerStatefulWidget {
  final int applicationId;

  const LetterDetailScreen({super.key, required this.applicationId});

  @override
  ConsumerState<LetterDetailScreen> createState() => _LetterDetailScreenState();
}

class _LetterDetailScreenState extends ConsumerState<LetterDetailScreen> {
  final _resubmitController = TextEditingController();

  @override
  void dispose() {
    _resubmitController.dispose();
    super.dispose();
  }

  void _showRevisionDialog(String currentKeperluan) {
    _resubmitController.text = currentKeperluan;
    showDialog<void>(
      context: context,
      builder: (dialogContext) {
        return AlertDialog(
          title: const Text('Perbaiki Pengajuan', style: AppTypography.heading3),
          content: Column(
            mainAxisSize: MainAxisSize.min,
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              const Text('Perbarui rincian keperluan surat sesuai catatan dari Ketua RT:', style: AppTypography.caption),
              const SizedBox(height: AppSpacing.sm),
              TextField(
                controller: _resubmitController,
                maxLines: 4,
                decoration: InputDecoration(
                  hintText: 'Masukkan perbaikan keperluan...',
                  border: OutlineInputBorder(borderRadius: BorderRadius.circular(8)),
                ),
              ),
            ],
          ),
          actions: [
            TextButton(
              onPressed: () => Navigator.pop(dialogContext),
              child: const Text('Batal'),
            ),
            ElevatedButton(
              style: ElevatedButton.styleFrom(backgroundColor: AppColors.primary),
              onPressed: () async {
                Navigator.pop(dialogContext);
                try {
                  final repo = ref.read(letterRepositoryProvider);
                  await repo.resubmitLetter(widget.applicationId, _resubmitController.text.trim());
                  ref.invalidate(applicationDetailProvider(widget.applicationId));
                  if (!mounted) return;
                  ScaffoldMessenger.of(context).showSnackBar(
                    const SnackBar(
                      backgroundColor: AppColors.success,
                      content: Text('Pengajuan berhasil diperbarui dan dikirim ulang ke Ketua RT'),
                    ),
                  );
                } catch (e) {
                  if (!mounted) return;
                  ScaffoldMessenger.of(context).showSnackBar(
                    SnackBar(backgroundColor: AppColors.error, content: Text('Gagal memperbarui: $e')),
                  );
                }
              },
              child: const Text('Kirim Ulang', style: TextStyle(color: Colors.white)),
            ),
          ],
        );
      },
    );
  }

  @override
  Widget build(BuildContext context) {
    final detailAsync = ref.watch(applicationDetailProvider(widget.applicationId));

    return Scaffold(
      backgroundColor: AppColors.surface,
      appBar: AppBar(
        title: const Text('Rincian Surat', style: AppTypography.heading3),
        centerTitle: true,
        backgroundColor: AppColors.surface,
        elevation: 0,
        leading: IconButton(
          icon: const Icon(Icons.arrow_back, color: AppColors.textPrimary),
          onPressed: () => context.pop(),
        ),
      ),
      body: SafeArea(
        child: detailAsync.when(
          loading: () => const Center(child: CircularProgressIndicator()),
          error: (err, _) => Center(
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                const Icon(Icons.error_outline, size: 48, color: AppColors.error),
                const SizedBox(height: AppSpacing.sm),
                Text('Gagal memuat rincian: $err', style: AppTypography.bodySmall),
                TextButton(
                  onPressed: () => ref.refresh(applicationDetailProvider(widget.applicationId)),
                  child: const Text('Muat Ulang'),
                ),
              ],
            ),
          ),
          data: (data) {
            final nomorPengajuan = data['nomor_pengajuan']?.toString() ?? '-';
            final nomorResmi = data['nomor_surat_resmi']?.toString();
            final namaSurat = data['nama_surat']?.toString() ?? 'Surat Pengantar';
            final status = data['status']?.toString() ?? 'diajukan';
            final keperluan = data['keperluan']?.toString() ?? '-';
            final drafAi = data['draf_ai_konten']?.toString();
            final metode = data['metode_tanda_tangan']?.toString() ?? 'digital';
            final namaWarga = data['nama_lengkap']?.toString() ?? '-';
            final nik = data['nik']?.toString() ?? '-';
            final alamat = data['alamat']?.toString() ?? '-';
            final catatanRevisi = data['catatan_revisi']?.toString();
            final alasanTolak = data['alasan_penolakan']?.toString();

            return SingleChildScrollView(
              padding: const EdgeInsets.all(AppSpacing.lg),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.stretch,
                children: [
                  // Status Card
                  Container(
                    padding: const EdgeInsets.all(AppSpacing.md),
                    decoration: BoxDecoration(
                      color: AppColors.cardBackground,
                      borderRadius: BorderRadius.circular(12),
                      border: Border.all(color: AppColors.border),
                    ),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Row(
                          mainAxisAlignment: MainAxisAlignment.spaceBetween,
                          children: [
                            Text(nomorPengajuan, style: AppTypography.heading3),
                            RTStatusBadge(status: status),
                          ],
                        ),
                        if (nomorResmi != null) ...[
                          const SizedBox(height: 4),
                          Text('Nomor Resmi: $nomorResmi', style: AppTypography.caption.copyWith(fontWeight: FontWeight.bold)),
                        ],
                        const SizedBox(height: AppSpacing.xs),
                        Text(namaSurat, style: AppTypography.bodyMedium.copyWith(color: AppColors.primary, fontWeight: FontWeight.bold)),
                      ],
                    ),
                  ),
                  const SizedBox(height: AppSpacing.md),

                  // Catatan Revisi jika ada
                  if (status == 'perlu_revisi' && catatanRevisi != null) ...[
                    Container(
                      padding: const EdgeInsets.all(AppSpacing.md),
                      decoration: BoxDecoration(
                        color: Colors.amber.shade50,
                        borderRadius: BorderRadius.circular(12),
                        border: Border.all(color: Colors.amber.shade400),
                      ),
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Row(
                            children: [
                              Icon(Icons.warning_amber_rounded, color: Colors.amber.shade800),
                              const SizedBox(width: AppSpacing.xs),
                              Text('Catatan Revisi dari Pak RT:', style: AppTypography.labelBold.copyWith(color: Colors.amber.shade900)),
                            ],
                          ),
                          const SizedBox(height: 4),
                          Text(catatanRevisi, style: AppTypography.bodySmall),
                          const SizedBox(height: AppSpacing.sm),
                          ElevatedButton.icon(
                            style: ElevatedButton.styleFrom(backgroundColor: Colors.amber.shade800),
                            onPressed: () => _showRevisionDialog(keperluan),
                            icon: const Icon(Icons.edit, color: Colors.white, size: 16),
                            label: const Text('Perbaiki Isian Surat', style: TextStyle(color: Colors.white)),
                          ),
                        ],
                      ),
                    ),
                    const SizedBox(height: AppSpacing.md),
                  ],

                  // Alasan Penolakan jika ada
                  if (status == 'ditolak' && alasanTolak != null) ...[
                    Container(
                      padding: const EdgeInsets.all(AppSpacing.md),
                      decoration: BoxDecoration(
                        color: Colors.red.shade50,
                        borderRadius: BorderRadius.circular(12),
                        border: Border.all(color: Colors.red.shade300),
                      ),
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Row(
                            children: [
                              Icon(Icons.cancel_outlined, color: Colors.red.shade700),
                              const SizedBox(width: AppSpacing.xs),
                              Text('Alasan Penolakan:', style: AppTypography.labelBold.copyWith(color: Colors.red.shade800)),
                            ],
                          ),
                          const SizedBox(height: 4),
                          Text(alasanTolak, style: AppTypography.bodySmall),
                        ],
                      ),
                    ),
                    const SizedBox(height: AppSpacing.md),
                  ],

                  // Banner Siap Diambil untuk TTD Basah
                  if (status == 'siap_diambil') ...[
                    Container(
                      padding: const EdgeInsets.all(AppSpacing.md),
                      decoration: BoxDecoration(
                        color: Colors.blue.shade50,
                        borderRadius: BorderRadius.circular(12),
                        border: Border.all(color: Colors.blue.shade300),
                      ),
                      child: Row(
                        children: [
                          Icon(Icons.storefront_outlined, color: Colors.blue.shade700, size: 28),
                          const SizedBox(width: AppSpacing.sm),
                          Expanded(
                            child: Text(
                              'Surat fisik bertanda tangan basah sudah siap. Silakan ambil di kediaman Ketua RT (18.30 - 21.00 WIB).',
                              style: AppTypography.bodySmall.copyWith(color: Colors.blue.shade900),
                            ),
                          ),
                        ],
                      ),
                    ),
                    const SizedBox(height: AppSpacing.md),
                  ],

                  // Data Pemohon
                  const Text('Data Pemohon', style: AppTypography.labelBold),
                  const SizedBox(height: AppSpacing.xs),
                  Container(
                    padding: const EdgeInsets.all(AppSpacing.md),
                    decoration: BoxDecoration(
                      color: AppColors.cardBackground,
                      borderRadius: BorderRadius.circular(12),
                      border: Border.all(color: AppColors.border),
                    ),
                    child: Column(
                      children: [
                        _buildDetailRow('Nama Lengkap', namaWarga),
                        const Divider(),
                        _buildDetailRow('NIK', nik),
                        const Divider(),
                        _buildDetailRow('Alamat', alamat),
                        const Divider(),
                        _buildDetailRow('Metode TTD', metode == 'digital' ? 'Digital (Tempelan Gambar)' : 'Fisik (Tanda Tangan Basah)'),
                        const Divider(),
                        _buildDetailRow('Keperluan', keperluan),
                      ],
                    ),
                  ),
                  const SizedBox(height: AppSpacing.lg),

                  // Draf Narasi AI
                  if (drafAi != null && drafAi.isNotEmpty) ...[
                    const Row(
                      children: [
                        Icon(Icons.auto_awesome, color: AppColors.primary, size: 20),
                        SizedBox(width: AppSpacing.xs),
                        Text('Draf Narasi Surat (Hasil Formulasi AI)', style: AppTypography.labelBold),
                      ],
                    ),
                    const SizedBox(height: AppSpacing.xs),
                    Container(
                      padding: const EdgeInsets.all(AppSpacing.md),
                      decoration: BoxDecoration(
                        color: AppColors.primary.withValues(alpha: 0.04),
                        borderRadius: BorderRadius.circular(12),
                        border: Border.all(color: AppColors.primary.withValues(alpha: 0.15)),
                      ),
                      child: Text(
                        drafAi,
                        style: AppTypography.bodySmall.copyWith(height: 1.5),
                      ),
                    ),
                    const SizedBox(height: AppSpacing.xl),
                  ],

                  // Tombol Unduh PDF jika status selesai
                  if (status == 'selesai') ...[
                    RTPrimaryButton(
                      text: 'Lihat & Unduh Dokumen PDF Resmi',
                      onPressed: () => context.push('/surat/preview/${widget.applicationId}'),
                    ),
                    const SizedBox(height: AppSpacing.md),
                  ],
                ],
              ),
            );
          },
        ),
      ),
    );
  }

  Widget _buildDetailRow(String label, String value) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 4),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          SizedBox(width: 110, child: Text(label, style: AppTypography.caption)),
          const SizedBox(width: 8),
          Expanded(child: Text(value, style: AppTypography.bodySmall.copyWith(fontWeight: FontWeight.w600))),
        ],
      ),
    );
  }
}
