import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:rtconnect/features/letters/presentation/letter_controller.dart';
import 'package:rtconnect/features/letters/presentation/rt_review_screen.dart';

void main() {
  group('TEST-WGT-RT-REVIEW: RTReviewScreen (Issue #20)', () {
    final mockQueue = <Map<String, dynamic>>[
      {
        'pengajuan_id': 10,
        'nomor_pengajuan': 'SRT-2026-00010',
        'nama_surat': 'Surat Keterangan Domisili',
        'nama_lengkap': 'Budi Santoso',
        'alamat': 'Blok A-1',
        'keperluan': 'Pembukaan rekening bank',
        'status': 'diajukan',
        'metode_tanda_tangan': 'digital',
      },
      {
        'pengajuan_id': 11,
        'nomor_pengajuan': 'SRT-2026-00011',
        'nama_surat': 'Surat Pengantar SKCK',
        'nama_lengkap': 'Siti Aminah',
        'alamat': 'Blok B-2',
        'keperluan': 'Melamar kerja',
        'status': 'perlu_revisi',
        'metode_tanda_tangan': 'digital',
        'catatan_revisi': 'Lampirkan scan KTP terbaru',
      },
      {
        'pengajuan_id': 12,
        'nomor_pengajuan': 'SRT-2026-00012',
        'nama_surat': 'Surat Keterangan Usaha',
        'nama_lengkap': 'Andi Wijaya',
        'alamat': 'Blok C-3',
        'keperluan': 'Pengajuan KUR UMKM',
        'status': 'selesai',
        'metode_tanda_tangan': 'basah',
      },
    ];

    testWidgets('displays queue items, filters by status chips, and filters by search query',
        (tester) async {
      await tester.pumpWidget(
        ProviderScope(
          overrides: [
            incomingQueueProvider.overrideWith((ref) async => mockQueue),
          ],
          child: const MaterialApp(
            home: RTReviewScreen(),
          ),
        ),
      );
      await tester.pumpAndSettle();

      expect(find.text('Antrean Pengajuan Warga'), findsOneWidget);
      expect(find.text('Budi Santoso'), findsOneWidget);
      expect(find.text('Siti Aminah'), findsOneWidget);

      // Filter chip: Perlu Revisi (chip berada paling atas sebelum kartu antrean)
      await tester.tap(find.text('Perlu Revisi').first);
      await tester.pumpAndSettle();
      expect(find.text('Siti Aminah'), findsOneWidget);
      expect(find.text('Budi Santoso'), findsNothing);
      expect(find.text('Melamar kerja'), findsOneWidget);

      // Filter chip: Semua + Search query
      await tester.tap(find.text('Semua'));
      await tester.pumpAndSettle();
      await tester.enterText(find.byType(TextField), 'Andi');
      await tester.pumpAndSettle();

      expect(find.text('Andi Wijaya'), findsOneWidget);
      expect(find.text('Budi Santoso'), findsNothing);
    });
  });
}
