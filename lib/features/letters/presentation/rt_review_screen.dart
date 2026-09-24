import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import '../../../core/router/route_names.dart';
import '../../../core/theme/app_colors.dart';
import '../../../core/theme/app_spacing.dart';
import '../../../core/theme/app_typography.dart';
import '../../../shared/widgets/rt_primary_button.dart';
import '../../../shared/widgets/rt_status_badge.dart';
import 'letter_controller.dart';

class RTReviewScreen extends ConsumerStatefulWidget {
  final int? selectedApplicationId;

  const RTReviewScreen({super.key, this.selectedApplicationId});

  @override
  ConsumerState<RTReviewScreen> createState() => _RTReviewScreenState();
}

class _RTReviewScreenState extends ConsumerState<RTReviewScreen> {
  final _pinController = TextEditingController();
  final _noteController = TextEditingController();

  @override
  void dispose() {
    _pinController.dispose();
    _noteController.dispose();
    super.dispose();
  }

  void _showDigitalSignDialog(int id, String namaWarga, String namaSurat) {
    _pinController.clear();
    showDialog(
      context: context,
      builder: (context) {
        return AlertDialog(
          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
          title: Row(
            children: [
              const Icon(Icons.draw, color: AppColors.primary),
              const SizedBox(width: AppSpacing.xs),
              Text('Otorisasi TTD Digital', style: AppTypography.heading3),
            ],
          ),
          content: Column(
            mainAxisSize: MainAxisSize.min,
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                'Anda akan mengesahkan $namaSurat untuk warga $namaWarga.',
                style: AppTypography.bodySmall,
              ),
              const SizedBox(height: AppSpacing.sm),
              Text(
                'Sistem akan menyematkan pindaian tanda tangan digital resmi Ketua RT ke dokumen PDF (UC-09).',
                style: AppTypography.caption,
              ),
              const SizedBox(height: AppSpacing.md),
              TextField(
                controller: _pinController,
                keyboardType: TextInputType.number,
                obscureText: true,
                maxLength: 6,
                decoration: InputDecoration(
                  labelText: 'PIN Otorisasi RT (Default: 123456)',
                  border: OutlineInputBorder(borderRadius: BorderRadius.circular(8)),
                  prefixIcon: const Icon(Icons.lock_outline),
                ),
              ),
            ],
          ),
          actions: [
            TextButton(
              onPressed: () => Navigator.pop(context),
              child: const Text('Batal'),
            ),
            ElevatedButton(
              style: ElevatedButton.styleFrom(backgroundColor: AppColors.primary),
              onPressed: () async {
                final pin = _pinController.text.trim();
                Navigator.pop(context);
                final success = await ref.read(letterSubmitControllerProvider.notifier).signDigital(id, pin);
                if (mounted) {
                  if (success) {
                    ScaffoldMessenger.of(context).showSnackBar(
                      const SnackBar(
                        backgroundColor: AppColors.success,
                        content: Text('Tanda tangan digital berhasil disematkan! Dokumen PDF resmi telah terbit.'),
                      ),
                    );
                    context.push('/surat/preview/$id');
                  } else {
                    final err = ref.read(letterSubmitControllerProvider).errorMessage ?? 'Gagal menandatangani';
                    ScaffoldMessenger.of(context).showSnackBar(
                      SnackBar(backgroundColor: AppColors.error, content: Text(err)),
                    );
                  }
                }
              },
              child: const Text('Sahkan Dokumen', style: TextStyle(color: Colors.white)),
            ),
          ],
        );
      },
    );
  }

  void _showRevisionDialog(int id) {
    _noteController.clear();
    showDialog(
      context: context,
      builder: (context) {
        return AlertDialog(
          title: Text('Minta Perbaikan (Revisi)', style: AppTypography.heading3),
          content: TextField(
            controller: _noteController,
            maxLines: 4,
            decoration: InputDecoration(
              hintText: 'Tuliskan catatan perbaikan untuk warga...',
              border: OutlineInputBorder(borderRadius: BorderRadius.circular(8)),
            ),
          ),
          actions: [
            TextButton(onPressed: () => Navigator.pop(context), child: const Text('Batal')),
            ElevatedButton(
              style: ElevatedButton.styleFrom(backgroundColor: Colors.amber.shade800),
              onPressed: () async {
                final note = _noteController.text.trim();
                if (note.isEmpty) return;
                Navigator.pop(context);
                final success = await ref.read(letterSubmitControllerProvider.notifier).submitDecision(id, 'revise', note);
                if (mounted && success) {
                  ScaffoldMessenger.of(context).showSnackBar(
                    const SnackBar(backgroundColor: Colors.amber, content: Text('Permintaan revisi telah dikirim ke warga')),
                  );
                }
              },
              child: const Text('Kirim Revisi', style: TextStyle(color: Colors.white)),
            ),
          ],
        );
      },
    );
  }

  void _showRejectDialog(int id) {
    _noteController.clear();
    showDialog(
      context: context,
      builder: (context) {
        return AlertDialog(
          title: Text('Tolak Permohonan Surat', style: AppTypography.heading3),
          content: TextField(
            controller: _noteController,
            maxLines: 4,
            decoration: InputDecoration(
              hintText: 'Tuliskan alasan penolakan surat...',
              border: OutlineInputBorder(borderRadius: BorderRadius.circular(8)),
            ),
          ),
          actions: [
            TextButton(onPressed: () => Navigator.pop(context), child: const Text('Batal')),
            ElevatedButton(
              style: ElevatedButton.styleFrom(backgroundColor: Colors.red.shade700),
              onPressed: () async {
                final reason = _noteController.text.trim();
                if (reason.isEmpty) return;
                Navigator.pop(context);
                final success = await ref.read(letterSubmitControllerProvider.notifier).submitDecision(id, 'reject', reason);
                if (mounted && success) {
                  ScaffoldMessenger.of(context).showSnackBar(
                    const SnackBar(backgroundColor: Colors.red, content: Text('Permohonan surat telah ditolak')),
                  );
                }
              },
              child: const Text('Tolak Surat', style: TextStyle(color: Colors.white)),
            ),
          ],
        );
      },
    );
  }

  @override
  Widget build(BuildContext context) {
    final queueAsync = ref.watch(incomingQueueProvider);

    return Scaffold(
      backgroundColor: AppColors.surface,
      appBar: AppBar(
        title: Text('Antrean Surat Masuk RT', style: AppTypography.heading3),
        centerTitle: true,
        backgroundColor: AppColors.surface,
        elevation: 0,
        actions: [
          IconButton(
            icon: const Icon(Icons.refresh, color: AppColors.primary),
            onPressed: () => ref.refresh(incomingQueueProvider),
          ),
        ],
      ),
      body: SafeArea(
        child: queueAsync.when(
          loading: () => const Center(child: CircularProgressIndicator()),
          error: (err, _) => Center(
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                const Icon(Icons.error_outline, size: 48, color: AppColors.error),
                const SizedBox(height: AppSpacing.sm),
                Text('Gagal memuat antrean: $err', style: AppTypography.bodySmall),
                TextButton(
                  onPressed: () => ref.refresh(incomingQueueProvider),
                  child: const Text('Muat Ulang'),
                ),
              ],
            ),
          ),
          data: (queue) {
            if (queue.isEmpty) {
              return Center(
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    Icon(Icons.mark_email_read_outlined, size: 64, color: AppColors.textSecondary.withOpacity(0.5)),
                    const SizedBox(height: AppSpacing.sm),
                    Text('Antrean Masuk Kosong', style: AppTypography.heading3),
                    Text('Saat ini tidak ada permohonan surat yang menunggu tindakan.', style: AppTypography.caption),
                  ],
                ),
              );
            }

            return RefreshIndicator(
              onRefresh: () async => ref.refresh(incomingQueueProvider),
              child: ListView.separated(
                padding: const EdgeInsets.all(AppSpacing.md),
                itemCount: queue.length,
                separatorBuilder: (_, __) => const SizedBox(height: AppSpacing.sm),
                itemBuilder: (context, index) {
                  final item = queue[index];
                  final id = item['pengajuan_id'] as int;
                  final nomorPengajuan = item['nomor_pengajuan']?.toString() ?? '-';
                  final namaSurat = item['nama_surat']?.toString() ?? 'Surat Pengantar';
                  final namaWarga = item['nama_lengkap']?.toString() ?? '-';
                  final alamat = item['alamat']?.toString() ?? '-';
                  final keperluan = item['keperluan']?.toString() ?? '-';
                  final status = item['status']?.toString() ?? 'diajukan';
                  final metode = item['metode_tanda_tangan']?.toString() ?? 'digital';

                  return Card(
                    elevation: 1,
                    shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                    child: Padding(
                      padding: const EdgeInsets.all(AppSpacing.md),
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Row(
                            mainAxisAlignment: MainAxisAlignment.spaceBetween,
                            children: [
                              Text(nomorPengajuan, style: AppTypography.caption.copyWith(fontWeight: FontWeight.bold)),
                              RTStatusBadge(status: status),
                            ],
                          ),
                          const SizedBox(height: AppSpacing.xs),
                          Text(namaSurat, style: AppTypography.heading3),
                          Text('Pemohon: $namaWarga ($alamat)', style: AppTypography.bodySmall.copyWith(fontWeight: FontWeight.w600)),
                          const SizedBox(height: 4),
                          Text('Keperluan: $keperluan', style: AppTypography.bodySmall),
                          const SizedBox(height: AppSpacing.sm),
                          Row(
                            children: [
                              Icon(
                                metode == 'digital' ? Icons.draw : Icons.edit_note,
                                size: 16,
                                color: AppColors.primary,
                              ),
                              const SizedBox(width: 4),
                              Text(
                                metode == 'digital' ? 'Metode: TTD Digital' : 'Metode: TTD Basah',
                                style: AppTypography.caption.copyWith(color: AppColors.primary, fontWeight: FontWeight.bold),
                              ),
                            ],
                          ),
                          const SizedBox(height: AppSpacing.md),

                          // Tombol Aksi Evaluasi RT
                          Row(
                            children: [
                              Expanded(
                                child: ElevatedButton.icon(
                                  style: ElevatedButton.styleFrom(
                                    backgroundColor: AppColors.primary,
                                    shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(8)),
                                  ),
                                  onPressed: () {
                                    if (metode == 'digital') {
                                      _showDigitalSignDialog(id, namaWarga, namaSurat);
                                    } else {
                                      ref.read(letterSubmitControllerProvider.notifier).confirmPhysical(id);
                                    }
                                  },
                                  icon: Icon(metode == 'digital' ? Icons.check_circle_outline : Icons.store, color: Colors.white, size: 18),
                                  label: Text(metode == 'digital' ? 'Sahkan TTD' : 'Siap Diambil', style: const TextStyle(color: Colors.white)),
                                ),
                              ),
                              const SizedBox(width: AppSpacing.xs),
                              IconButton(
                                icon: const Icon(Icons.edit_note, color: Colors.amber),
                                tooltip: 'Minta Revisi',
                                onPressed: () => _showRevisionDialog(id),
                              ),
                              IconButton(
                                icon: const Icon(Icons.cancel_outlined, color: Colors.red),
                                tooltip: 'Tolak',
                                onPressed: () => _showRejectDialog(id),
                              ),
                            ],
                          ),
                        ],
                      ),
                    ),
                  );
                },
              ),
            );
          },
        ),
      ),
    );
  }
}
