import 'package:dio/dio.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:rtconnect/core/errors/app_exception.dart';

void main() {
  group('TEST-UNIT-ERR: formatErrorMessage', () {
    test('unwraps AppException and FormatException cleanly', () {
      expect(
        formatErrorMessage(const AuthException('Email/NIK atau password salah')),
        'Email/NIK atau password salah',
      );
      expect(
        formatErrorMessage(
          const FormatException('Aplikasi release hanya menerima API melalui HTTPS.'),
        ),
        'Aplikasi release hanya menerima API melalui HTTPS.',
      );
    });

    test('unwraps DioException inner AppException without leaking DioException text', () {
      final dioErr = DioException(
        requestOptions: RequestOptions(path: '/auth/login'),
        error: const AuthException('Email/NIK atau password salah'),
      );
      final msg = formatErrorMessage(dioErr);
      expect(msg, 'Email/NIK atau password salah');
      expect(msg.contains('DioException'), isFalse);
    });
  });
}
