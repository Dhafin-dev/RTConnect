import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:rtconnect/features/letters/data/letter_repository.dart';
import 'package:rtconnect/features/letters/presentation/letter_application_screen.dart';
import 'package:rtconnect/features/letters/presentation/letter_controller.dart';

class _FakeLetterRepository extends LetterRepository {
  @override
  Future<Map<String, dynamic>?> getMyLastApplicantData() async => null;

  @override
  Future<List<Map<String, dynamic>>> getLetterTypes() async => [
        {
          'jenis_surat_id': 1,
          'kode_surat': 'DOM',
          'nama_surat': 'Surat Keterangan Domisili',
          'persyaratan_dokumen': 'KTP dan Bukti Tempat Tinggal',
        },
        {
          'jenis_surat_id': 2,
          'kode_surat': 'SKCK',
          'nama_surat': 'Surat Pengantar SKCK',
          'persyaratan_dokumen': 'KTP Asli dan Kartu Keluarga',
        },
      ];
}

void main() {
  group('TEST-WGT-LETTER-APP: LetterApplicationScreen (Issue #20)', () {
    testWidgets('renders form fields, letter type dropdown, and validates required fields on submit',
        (tester) async {
      final fakeRepo = _FakeLetterRepository();

      await tester.pumpWidget(
        ProviderScope(
          overrides: [
            letterRepositoryProvider.overrideWithValue(fakeRepo),
            letterTypesProvider.overrideWith((ref) => fakeRepo.getLetterTypes()),
          ],
          child: const MaterialApp(
            home: LetterApplicationScreen(),
          ),
        ),
      );
      await tester.pumpAndSettle();

      expect(find.text('Pengajuan Surat'), findsOneWidget);
      expect(find.text('Jenis Surat Pengantar'), findsOneWidget);
      expect(find.text('Kirim Pengajuan Surat'), findsOneWidget);
      expect(find.text('Format PDF, PNG, atau JPG (Maks. 8 MB)'), findsOneWidget);

      // Buka dropdown jenis surat dan pilih Surat Pengantar SKCK
      final dropdown = find.byType(DropdownButtonFormField<int>);
      await tester.ensureVisible(dropdown);
      await tester.tap(dropdown);
      await tester.pumpAndSettle();
      await tester.tap(find.text('Surat Pengantar SKCK').last);
      await tester.pumpAndSettle();

      expect(find.text('KTP Asli dan Kartu Keluarga'), findsOneWidget);

      // Scroll ke tombol submit dan tekan saat field wajib masih kosong
      await tester.scrollUntilVisible(
        find.text('Kirim Pengajuan Surat'),
        300,
        scrollable: find.byType(Scrollable).first,
      );
      await tester.tap(find.text('Kirim Pengajuan Surat'));
      await tester.pumpAndSettle();

      expect(find.text('Pekerjaan wajib diisi'), findsOneWidget);
      expect(find.text('Nomor KK harus 16 digit angka'), findsOneWidget);
    });
  });
}
