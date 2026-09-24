import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../core/network/api_client.dart';
import '../../../core/theme/app_colors.dart';
import '../../../core/theme/app_spacing.dart';
import '../../../core/theme/app_typography.dart';

final notificationsProvider = FutureProvider<Map<String, dynamic>>((ref) async {
  final client = ApiClient();
  final res = await client.dio.get<Map<String, dynamic>>('/notifications');
  return Map<String, dynamic>.from(res.data?['data'] as Map);
});

class NotificationFeedScreen extends ConsumerWidget {
  const NotificationFeedScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final notifAsync = ref.watch(notificationsProvider);

    return Scaffold(
      backgroundColor: AppColors.surface,
      appBar: AppBar(
        title: const Text('Notifikasi', style: AppTypography.heading3),
        centerTitle: true,
        backgroundColor: AppColors.surface,
        elevation: 0,
        actions: [
          IconButton(
            icon: const Icon(Icons.done_all, color: AppColors.primary),
            tooltip: 'Tandai Semua Dibaca',
            onPressed: () async {
              final client = ApiClient();
              await client.dio.put<Map<String, dynamic>>('/notifications/read-all');
              ref.invalidate(notificationsProvider);
            },
          ),
        ],
      ),
      body: SafeArea(
        child: notifAsync.when(
          loading: () => const Center(child: CircularProgressIndicator()),
          error: (err, _) => Center(child: Text('Gagal memuat notifikasi: $err')),
          data: (data) {
            final items = (data['items'] as List?) ?? [];
            if (items.isEmpty) {
              return Center(
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    Icon(Icons.notifications_none, size: 64, color: AppColors.textSecondary.withValues(alpha: 0.5)),
                    const SizedBox(height: AppSpacing.sm),
                    const Text('Tidak ada notifikasi', style: AppTypography.heading3),
                    const Text('Pemberitahuan surat dan sistem akan muncul di sini.', style: AppTypography.caption),
                  ],
                ),
              );
            }

            return RefreshIndicator(
              onRefresh: () async {
                ref.invalidate(notificationsProvider);
              },
              child: ListView.separated(
                padding: const EdgeInsets.all(AppSpacing.md),
                itemCount: items.length,
                separatorBuilder: (_, __) => const SizedBox(height: AppSpacing.xs),
                itemBuilder: (context, index) {
                  final item = items[index] as Map;
                  final notifId = item['notifikasi_id'] as int;
                  final judul = item['judul']?.toString() ?? 'Pemberitahuan';
                  final pesan = item['pesan_notifikasi']?.toString() ?? '';
                  final isRead = item['is_dibaca'] == 1 || item['is_dibaca'] == true;

                  return Card(
                    elevation: 0,
                    color: isRead ? AppColors.surface : AppColors.primary.withValues(alpha: 0.06),
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(12),
                      side: BorderSide(color: isRead ? AppColors.border : AppColors.primary.withValues(alpha: 0.2)),
                    ),
                    child: ListTile(
                      leading: CircleAvatar(
                        backgroundColor: isRead ? Colors.grey.shade200 : AppColors.primary.withValues(alpha: 0.15),
                        child: Icon(
                          Icons.notifications_active_outlined,
                          color: isRead ? Colors.grey.shade600 : AppColors.primary,
                          size: 20,
                        ),
                      ),
                      title: Text(judul, style: AppTypography.labelBold),
                      subtitle: Text(pesan, style: AppTypography.bodySmall),
                      onTap: () async {
                        if (!isRead) {
                          final client = ApiClient();
                          await client.dio.put<Map<String, dynamic>>('/notifications/$notifId/read');
                          ref.invalidate(notificationsProvider);
                        }
                      },
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
