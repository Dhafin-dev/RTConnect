import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import '../../../core/errors/app_exception.dart';
import '../../../core/router/route_names.dart';
import '../../../core/theme/app_colors.dart';
import '../../../core/theme/app_spacing.dart';
import '../../../core/theme/app_typography.dart';
import 'chatbot_controller.dart';

final rtKnowledgeListProvider =
    FutureProvider<List<Map<String, dynamic>>>((ref) async {
  return ref.watch(chatbotRepositoryProvider).getKnowledgeDocuments();
});

/// Halaman Kelola Basis Pengetahuan TanyaRT khusus Ketua RT (FIX-02)
class RTKnowledgeScreen extends ConsumerStatefulWidget {
  const RTKnowledgeScreen({super.key});

  @override
  ConsumerState<RTKnowledgeScreen> createState() => _RTKnowledgeScreenState();
}

class _RTKnowledgeScreenState extends ConsumerState<RTKnowledgeScreen> {
  String _searchQuery = '';
  bool _isSubmitting = false;

  Future<void> _showDocumentDialog({Map<String, dynamic>? existing}) async {
    final isEdit = existing != null;
    final judulCtrl = TextEditingController(text: existing?['judul']?.toString() ?? '');
    final kategoriCtrl = TextEditingController(
      text: existing?['kategori']?.toString() ?? 'administrasi',
    );
    final sumberCtrl = TextEditingController(
      text: existing?['sumber']?.toString() ?? 'SOP Resmi RT',
    );
    final isiCtrl = TextEditingController(
      text: existing?['isi_dokumen']?.toString() ?? '',
    );
    final formKey = GlobalKey<FormState>();

    final saved = await showDialog<bool>(
      context: context,
      builder: (ctx) => AlertDialog(
        title: Text(isEdit ? 'Ubah Dokumen Basis Pengetahuan' : 'Tambah Dokumen TanyaRT'),
        content: SingleChildScrollView(
          child: Form(
            key: formKey,
            child: Column(
              mainAxisSize: MainAxisSize.min,
              children: [
                TextFormField(
                  controller: judulCtrl,
                  decoration: const InputDecoration(
                    labelText: 'Judul Dokumen *',
                    border: OutlineInputBorder(),
                  ),
                  validator: (v) =>
                      (v == null || v.trim().isEmpty) ? 'Judul wajib diisi' : null,
                ),
                const SizedBox(height: AppSpacing.sm),
                TextFormField(
                  controller: kategoriCtrl,
                  decoration: const InputDecoration(
                    labelText: 'Kategori',
                    border: OutlineInputBorder(),
                  ),
                ),
                const SizedBox(height: AppSpacing.sm),
                TextFormField(
                  controller: sumberCtrl,
                  decoration: const InputDecoration(
                    labelText: 'Sumber Resmi',
                    border: OutlineInputBorder(),
                  ),
                ),
                const SizedBox(height: AppSpacing.sm),
                TextFormField(
                  controller: isiCtrl,
                  maxLines: 5,
                  decoration: const InputDecoration(
                    labelText: 'Isi Dokumen / SOP *',
                    border: OutlineInputBorder(),
                  ),
                  validator: (v) =>
                      (v == null || v.trim().isEmpty) ? 'Isi dokumen wajib diisi' : null,
                ),
              ],
            ),
          ),
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(ctx, false),
            child: const Text('Batal'),
          ),
          ElevatedButton(
            onPressed: () {
              if (formKey.currentState!.validate()) {
                Navigator.pop(ctx, true);
              }
            },
            child: Text(isEdit ? 'Simpan' : 'Tambah'),
          ),
        ],
      ),
    );

    if (saved != true || !mounted) return;
    setState(() => _isSubmitting = true);
    try {
      final repo = ref.read(chatbotRepositoryProvider);
      if (isEdit) {
        await repo.updateKnowledgeDocument(
          knowledgeId: existing['knowledge_id'] as int,
          judul: judulCtrl.text.trim(),
          kategori: kategoriCtrl.text.trim().isEmpty ? 'administrasi' : kategoriCtrl.text.trim(),
          isiDokumen: isiCtrl.text.trim(),
          sumber: sumberCtrl.text.trim().isEmpty ? 'SOP Resmi RT' : sumberCtrl.text.trim(),
        );
      } else {
        await repo.createKnowledgeDocument(
          judul: judulCtrl.text.trim(),
          kategori: kategoriCtrl.text.trim().isEmpty ? 'administrasi' : kategoriCtrl.text.trim(),
          isiDokumen: isiCtrl.text.trim(),
          sumber: sumberCtrl.text.trim().isEmpty ? 'SOP Resmi RT' : sumberCtrl.text.trim(),
        );
      }
      ref.invalidate(rtKnowledgeListProvider);
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            backgroundColor: AppColors.success,
            content: Text(
              isEdit
                  ? 'Dokumen basis pengetahuan diperbarui'
                  : 'Dokumen basis pengetahuan ditambahkan',
            ),
          ),
        );
      }
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            backgroundColor: AppColors.error,
            content: Text(formatErrorMessage(e, 'Gagal menyimpan dokumen')),
          ),
        );
      }
    } finally {
      if (mounted) setState(() => _isSubmitting = false);
    }
  }

  Future<void> _deleteDocument(Map<String, dynamic> doc) async {
    final confirmed = await showDialog<bool>(
      context: context,
      builder: (ctx) => AlertDialog(
        title: const Text('Hapus Dokumen?'),
        content: Text('Hapus "${doc['judul']}" dari basis pengetahuan TanyaRT?'),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(ctx, false),
            child: const Text('Batal'),
          ),
          ElevatedButton(
            style: ElevatedButton.styleFrom(backgroundColor: AppColors.error),
            onPressed: () => Navigator.pop(ctx, true),
            child: const Text('Hapus', style: TextStyle(color: Colors.white)),
          ),
        ],
      ),
    );
    if (confirmed != true || !mounted) return;
    setState(() => _isSubmitting = true);
    try {
      await ref.read(chatbotRepositoryProvider).deleteKnowledgeDocument(
            doc['knowledge_id'] as int,
          );
      ref.invalidate(rtKnowledgeListProvider);
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(
            backgroundColor: AppColors.success,
            content: Text('Dokumen berhasil dihapus'),
          ),
        );
      }
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            backgroundColor: AppColors.error,
            content: Text(formatErrorMessage(e, 'Gagal menghapus dokumen')),
          ),
        );
      }
    } finally {
      if (mounted) setState(() => _isSubmitting = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    final docsAsync = ref.watch(rtKnowledgeListProvider);

    return Scaffold(
      backgroundColor: AppColors.background,
      appBar: AppBar(
        backgroundColor: Colors.white,
        elevation: 0,
        leading: IconButton(
          tooltip: 'Kembali ke Beranda RT',
          icon: const Icon(Icons.arrow_back_ios_new, color: AppColors.textPrimary, size: 20),
          onPressed: () => context.go(RouteNames.rtHome),
        ),
        title: Text(
          'Basis Pengetahuan TanyaRT',
          style: AppTypography.heading3.copyWith(
            color: AppColors.textPrimary,
            fontWeight: FontWeight.w800,
          ),
        ),
        actions: [
          IconButton(
            tooltip: 'Segarkan Basis Pengetahuan',
            icon: const Icon(Icons.refresh_rounded, color: AppColors.primaryAccent),
            onPressed: () => ref.invalidate(rtKnowledgeListProvider),
          ),
        ],
        bottom: const PreferredSize(
          preferredSize: Size.fromHeight(1.0),
          child: Divider(height: 1.0, color: AppColors.border),
        ),
      ),
      floatingActionButton: FloatingActionButton.extended(
        onPressed: _isSubmitting ? null : () => _showDocumentDialog(),
        backgroundColor: AppColors.primaryAccent,
        icon: const Icon(Icons.add_rounded, color: Colors.white),
        label: const Text('Tambah SOP', style: TextStyle(color: Colors.white)),
      ),
      body: SafeArea(
        child: Column(
          children: [
            Container(
              color: Colors.white,
              padding: const EdgeInsets.all(AppSpacing.lg),
              child: TextField(
                onChanged: (v) => setState(() => _searchQuery = v.toLowerCase()),
                decoration: InputDecoration(
                  labelText: 'Cari dokumen SOP atau kebijakan RT',
                  hintText: 'Cari judul, kategori, atau sumber...',
                  prefixIcon: const Icon(Icons.search_rounded),
                  border: OutlineInputBorder(borderRadius: BorderRadius.circular(12)),
                  filled: true,
                  fillColor: const Color(0xFFF8FAFC),
                ),
              ),
            ),
            Expanded(
              child: docsAsync.when(
                loading: () => const Center(child: CircularProgressIndicator()),
                error: (err, _) => Center(
                  child: Padding(
                    padding: const EdgeInsets.all(AppSpacing.lg),
                    child: Column(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        const Icon(Icons.error_outline, size: 48, color: AppColors.error),
                        const SizedBox(height: AppSpacing.sm),
                        Text(
                          formatErrorMessage(err, 'Gagal memuat basis pengetahuan'),
                          textAlign: TextAlign.center,
                          style: AppTypography.bodySmall,
                        ),
                        const SizedBox(height: AppSpacing.sm),
                        TextButton(
                          onPressed: () => ref.invalidate(rtKnowledgeListProvider),
                          child: const Text('Muat Ulang'),
                        ),
                      ],
                    ),
                  ),
                ),
                data: (docs) {
                  final filtered = docs.where((d) {
                    if (_searchQuery.isEmpty) return true;
                    final title = d['judul']?.toString().toLowerCase() ?? '';
                    final cat = d['kategori']?.toString().toLowerCase() ?? '';
                    final src = d['sumber']?.toString().toLowerCase() ?? '';
                    return title.contains(_searchQuery) ||
                        cat.contains(_searchQuery) ||
                        src.contains(_searchQuery);
                  }).toList();

                  if (filtered.isEmpty) {
                    return const Center(
                      child: Text('Belum ada dokumen basis pengetahuan.'),
                    );
                  }

                  return ListView.separated(
                    padding: const EdgeInsets.fromLTRB(
                      AppSpacing.lg,
                      AppSpacing.md,
                      AppSpacing.lg,
                      96,
                    ),
                    itemCount: filtered.length,
                    separatorBuilder: (_, __) => const SizedBox(height: AppSpacing.sm),
                    itemBuilder: (context, index) {
                      final doc = filtered[index];
                      return Container(
                        padding: const EdgeInsets.all(AppSpacing.md),
                        decoration: BoxDecoration(
                          color: Colors.white,
                          borderRadius: BorderRadius.circular(16),
                          border: Border.all(color: AppColors.border),
                        ),
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Row(
                              children: [
                                Expanded(
                                  child: Text(
                                    doc['judul']?.toString() ?? '-',
                                    style: AppTypography.labelBold.copyWith(fontSize: 15),
                                  ),
                                ),
                                IconButton(
                                  tooltip: 'Ubah dokumen',
                                  icon: const Icon(Icons.edit_outlined, size: 20),
                                  onPressed: _isSubmitting
                                      ? null
                                      : () => _showDocumentDialog(existing: doc),
                                ),
                                IconButton(
                                  tooltip: 'Hapus dokumen',
                                  icon: const Icon(
                                    Icons.delete_outline_rounded,
                                    size: 20,
                                    color: AppColors.error,
                                  ),
                                  onPressed: _isSubmitting ? null : () => _deleteDocument(doc),
                                ),
                              ],
                            ),
                            const SizedBox(height: 4),
                            Text(
                              '${doc['kategori'] ?? 'administrasi'} • ${doc['sumber'] ?? 'SOP Resmi RT'} • ${doc['total_chunks'] ?? 0} bagian',
                              style: AppTypography.caption.copyWith(color: AppColors.textMuted),
                            ),
                          ],
                        ),
                      );
                    },
                  );
                },
              ),
            ),
          ],
        ),
      ),
    );
  }
}
