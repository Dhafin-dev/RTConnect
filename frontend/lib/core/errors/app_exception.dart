import 'package:dio/dio.dart';

/// Base exception class for RTConnect application
class AppException implements Exception {
  final String message;
  final String? code;

  const AppException(this.message, {this.code});

  @override
  String toString() => message;
}

class NetworkException extends AppException {
  const NetworkException([super.message = 'Koneksi jaringan terputus. Silakan coba lagi.'])
      : super(code: 'NETWORK_ERROR');
}

class AuthException extends AppException {
  const AuthException([super.message = 'Email/NIK atau password salah.'])
      : super(code: 'AUTH_ERROR');
}

class ValidationException extends AppException {
  const ValidationException(super.message) : super(code: 'VALIDATION_ERROR');
}

class ServerException extends AppException {
  const ServerException([super.message = 'Terjadi kesalahan pada server.'])
      : super(code: 'SERVER_ERROR');
}

/// Mengubah objek error (DioException, AppException, FormatException, dll.) menjadi pesan aman untuk UI.
String formatErrorMessage(
  Object error, [
  String fallback = 'Terjadi kesalahan. Silakan coba lagi.',
]) {
  if (error is AppException) {
    return error.message;
  }
  if (error is FormatException) {
    return error.message.isNotEmpty ? error.message : fallback;
  }
  if (error is DioException) {
    final inner = error.error;
    if (inner is AppException) return inner.message;
    if (inner is FormatException) {
      return inner.message.isNotEmpty ? inner.message : fallback;
    }
    final data = error.response?.data;
    if (data is Map && data['message'] != null) {
      return data['message'].toString();
    }
    if (error.type == DioExceptionType.connectionTimeout ||
        error.type == DioExceptionType.receiveTimeout ||
        error.type == DioExceptionType.sendTimeout ||
        error.type == DioExceptionType.connectionError) {
      return const NetworkException().message;
    }
    return fallback;
  }
  final raw = error.toString().trim();
  for (final prefix in const ['FormatException: ', 'Exception: ']) {
    if (raw.startsWith(prefix)) {
      final stripped = raw.substring(prefix.length).trim();
      return stripped.isNotEmpty ? stripped : fallback;
    }
  }
  return raw.isNotEmpty ? raw : fallback;
}
