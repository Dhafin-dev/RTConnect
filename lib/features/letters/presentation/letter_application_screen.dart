import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:file_picker/file_picker.dart';
import 'package:go_router/go_router.dart';
import '../../../core/router/route_names.dart';
import '../../../core/theme/app_colors.dart';
import '../../../core/theme/app_spacing.dart';
import '../../../core/theme/app_typography.dart';
import '../../../shared/widgets/rt_primary_button.dart';
import '../../../shared/widgets/rt_text_field.dart';
import 'letter_controller.dart';

class LetterApplicationScreen extends ConsumerStatefulWidget {
  const LetterApplicationScreen({super.key});

  @override
  ConsumerState<LetterApplicationScreen> createState() => _LetterApplicationScreenState();
}

class _LetterApplicationScreenState extends ConsumerState<LetterApplicationScreen> {
  final _formKey = GlobalKey<FormState>();
  final _keperluanController = TextEditingController();

  int? _selectedJenisSuratId;
  String? _selectedSyarat;
  String _metodeTtd = 'digital'; // 'digital' or 'basah'
  String? _lampiranPath;
  String? _lampiranFileName;

  @override
  void dispose() {
    _keperluanController.dispose();
    super.dispose();
  }

  Future<void> _pickAttachment() async {
    final result = await FilePicker.platform.pickFiles(
      type: FileType.custom,
      allowedExtensions: ['pdf', 'png', 'jpg', 'jpeg'],
    );
    if (result != null && result.files.single.path != null) {
      setState(() {
        _lampiranPath = result.files.single.path;
        _lampiranFileName = result.files.single.name;
      });
    }
  }

  Future<void> _submitApplication() async {
    if (!_formKey.currentState!.validate()) return;
    if (_selectedJenisSuratId == null) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          backgroundColor: AppColors.error,
          content: Text('Silakan pilih jenis surat terlebih dahulu'),
        ),
      );
      return;
    }

    final success = await ref.read(letterSubmitControllerProvider.notifier).submitApplication(
      jenisSuratId: _selectedJenisSuratId!,
      keperluan: _keperluanController.text.trim(),
      metodeTandaTangan: _metodeTtd,
      lampiranPath: _lampiranPath,
    );

    if (mounted) {
      if (success) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(
            backgroundColor: AppColors.success,
            content: Text('Permohonan surat berhasil dikirim! Draf AI sedang disiapkan.'),
          ),
        );
        context.go(RouteNames.wargaPengajuan);
      } else {
        final error = ref.read(letterSubmitControllerProvider).errorMessage ?? 'Gagal mengirim permohonan';
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            backgroundColor: AppColors.error,
            content: Text(error),
          ),
        );
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    final letterTypesAsync = ref.watch(letterTypesProvider);
    final submitState = ref.watch(letterSubmitControllerProvider);

    return Scaffold(
      backgroundColor: AppColors.surface,
      appBar: AppBar(
        title: const Text('Pengajuan Surat Pengantar', style: AppTypography.heading3),
        centerTitle: true,
        backgroundColor: AppColors.surface,
        elevation: 0,
        leading: IconButton(
          icon: const Icon(Icons.arrow_back, color: AppColors.textPrimary),
          onPressed: () => context.pop(),
        ),
      ),
      body: SafeArea(
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(AppSpacing.lg),
          child: Form(
            key: _formKey,
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: [
                // Header Banner Info
                Container(
                  padding: const EdgeInsets.all(AppSpacing.md),
                  decoration: BoxDecoration(
                    color: AppColors.primary.withValues(alpha: 0.08),
                    borderRadius: BorderRadius.circular(12),
                    border: Border.all(color: AppColors.primary.withValues(alpha: 0.2)),
                  ),
                  child: Row(
                    children: [
                      const Icon(Icons.auto_awesome, color: AppColors.primary, size: 28),
                      const SizedBox(width: AppSpacing.sm),
                      Expanded(
                        child: Text(
                          'Sistem didukung Generative AI untuk menyusun draf narasi surat secara otomatis.',
                          style: AppTypography.bodySmall.copyWith(color: AppColors.primary),
                        ),
                      ),
                    ],
                  ),
                ),
                const SizedBox(height: AppSpacing.lg),

                // Pilih Jenis Surat
                const Text('Pilih Jenis Surat', style: AppTypography.labelBold),
                const SizedBox(height: AppSpacing.xs),
                letterTypesAsync.when(
                  loading: () => const Center(child: CircularProgressIndicator()),
                  error: (err, _) => Text('Gagal memuat jenis surat: $err', style: const TextStyle(color: AppColors.error)),
                  data: (types) {
                    return DropdownButtonFormField<int>(
                      initialValue: _selectedJenisSuratId,
                      decoration: InputDecoration(
                        hintText: 'Pilih jenis surat yang diajukan',
                        border: OutlineInputBorder(borderRadius: BorderRadius.circular(12)),
                        filled: true,
                        fillColor: AppColors.cardBackground,
                      ),
                      items: types.map((t) {
                        return DropdownMenuItem<int>(
                          value: t['jenis_surat_id'] as int,
                          child: Text(t['nama_surat'].toString(), style: AppTypography.bodyMedium),
                        );
                      }).toList(),
                      onChanged: (val) {
                        setState(() {
                          _selectedJenisSuratId = val;
                          final match = types.firstWhere((e) => e['jenis_surat_id'] == val);
                          _selectedSyarat = match['persyaratan_dokumen']?.toString();
                        });
                      },
                      validator: (val) => val == null ? 'Wajib memilih jenis surat' : null,
                    );
                  },
                ),
                const SizedBox(height: AppSpacing.md),

                // Kotak Persyaratan Dokumen
                if (_selectedSyarat != null) ...[
                  Container(
                    padding: const EdgeInsets.all(AppSpacing.md),
                    decoration: BoxDecoration(
                      color: AppColors.cardBackground,
                      borderRadius: BorderRadius.circular(8),
                      border: Border.all(color: AppColors.border),
                    ),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        const Text('Persyaratan Berkas:', style: AppTypography.labelBold),
                        const SizedBox(height: 4),
                        Text(_selectedSyarat!, style: AppTypography.bodySmall),
                      ],
                    ),
                  ),
                  const SizedBox(height: AppSpacing.md),
                ],

                // Rincian Keperluan
                RTTextField(
                  label: 'Keperluan / Tujuan Surat',
                  hint: 'Contoh: Persyaratan pembukaan rekening bank syariah cabang Sidoarjo',
                  controller: _keperluanController,
                  maxLines: 3,
                  validator: (v) => (v == null || v.trim().length < 5) ? 'Mohon jelaskan keperluan minimal 5 karakter' : null,
                ),
                const SizedBox(height: AppSpacing.lg),

                // Pilihan Metode Tanda Tangan
                const Text('Metode Pengesahan Tanda Tangan', style: AppTypography.labelBold),
                const SizedBox(height: AppSpacing.xs),
                Container(
                  decoration: BoxDecoration(
                    color: AppColors.cardBackground,
                    borderRadius: BorderRadius.circular(12),
                    border: Border.all(color: AppColors.border),
                  ),
                  child: RadioGroup<String>(
                    groupValue: _metodeTtd,
                    onChanged: (val) {
                      if (val != null) {
                        setState(() => _metodeTtd = val);
                      }
                    },
                    child: const Column(
                      children: [
                        RadioListTile<String>(
                          value: 'digital',
                          activeColor: AppColors.primary,
                          title: Text('Tanda Tangan Digital (Rekomendasi)', style: AppTypography.labelBold),
                          subtitle: Text(
                            'Surat disahkan langsung dengan tempelan gambar tanda tangan resmi Ketua RT dan dapat langsung diunduh (PDF).',
                            style: AppTypography.caption,
                          ),
                        ),
                        Divider(height: 1),
                        RadioListTile<String>(
                          value: 'basah',
                          activeColor: AppColors.primary,
                          title: Text('Tanda Tangan Basah', style: AppTypography.labelBold),
                          subtitle: Text(
                            'Surat fisik dicetak dan ditandatangani manual oleh Ketua RT. Pengambilan langsung di kediaman RT.',
                            style: AppTypography.caption,
                          ),
                        ),
                      ],
                    ),
                  ),
                ),
                const SizedBox(height: AppSpacing.lg),

                // Upload Lampiran Pendukung (Opsional)
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
                      const Text('Berkas Lampiran Pendukung (Opsional)', style: AppTypography.labelBold),
                      const SizedBox(height: 4),
                      const Text('Unggah foto KTP/KK/Surat Terkait (PDF/PNG/JPG maks 5MB)', style: AppTypography.caption),
                      const SizedBox(height: AppSpacing.sm),
                      OutlinedButton.icon(
                        onPressed: _pickAttachment,
                        icon: const Icon(Icons.attach_file),
                        label: Text(_lampiranFileName ?? 'Pilih Berkas Lampiran'),
                      ),
                    ],
                  ),
                ),
                const SizedBox(height: AppSpacing.xl),

                // Tombol Kirim Pengajuan
                RTPrimaryButton(
                  text: 'Kirim Pengajuan Surat',
                  isLoading: submitState.isLoading,
                  onPressed: _submitApplication,
                ),
                const SizedBox(height: AppSpacing.lg),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
