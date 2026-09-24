/// Base exception class for RTConnect application
class AppException implements Exception {
  final String message;
  final String? code;

  const AppException(this.message, {this.code});

  @override
  String toString() => message;
}

class NetworkException extends AppException {
  const NetworkException([String message = 'Koneksi jaringan terputus. Silakan coba lagi.'])
      : super(message, code: 'NETWORK_ERROR');
}

class AuthException extends AppException {
  const AuthException([String message = 'Email/NIK atau password salah.'])
      : super(message, code: 'AUTH_ERROR');
}

class ValidationException extends AppException {
  const ValidationException(String message) : super(message, code: 'VALIDATION_ERROR');
}

class ServerException extends AppException {
  const ServerException([String message = 'Terjadi kesalahan pada server.'])
      : super(message, code: 'SERVER_ERROR');
}
