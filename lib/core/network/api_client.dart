import 'package:dio/dio.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import '../constants/app_constants.dart';
import '../errors/app_exception.dart';

/// Centralized Dio REST API Client
class ApiClient {
  late final Dio _dio;
  final FlutterSecureStorage _storage = const FlutterSecureStorage();

  ApiClient({String? baseUrl}) {
    final effectiveBaseUrl = baseUrl ?? AppConstants.defaultBaseUrl;
    _dio = Dio(
      BaseOptions(
        baseUrl: effectiveBaseUrl,
        connectTimeout: const Duration(seconds: 10),
        receiveTimeout: const Duration(seconds: 15),
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
        },
      ),
    );

    _dio.interceptors.add(
      InterceptorsWrapper(
        onRequest: (options, handler) async {
          final customUrl = await _storage.read(key: AppConstants.keyCustomBaseUrl);
          if (customUrl != null && customUrl.isNotEmpty) {
            options.baseUrl = customUrl;
          } else {
            options.baseUrl = AppConstants.defaultBaseUrl;
          }

          final token = await _storage.read(key: AppConstants.keyAuthToken);
          if (token != null) {
            options.headers['Authorization'] = 'Bearer $token';
          }
          return handler.next(options);
        },
        onError: (DioException error, handler) {
          final exception = _handleDioError(error);
          return handler.reject(
            DioException(
              requestOptions: error.requestOptions,
              error: exception,
              message: exception.message,
            ),
          );
        },
      ),
    );
  }

  Dio get dio => _dio;

  AppException _handleDioError(DioException error) {
    switch (error.type) {
      case DioExceptionType.connectionTimeout:
      case DioExceptionType.receiveTimeout:
      case DioExceptionType.connectionError:
        return const NetworkException();
      case DioExceptionType.badResponse:
        final statusCode = error.response?.statusCode;
        final data = error.response?.data;
        final message = (data is Map && data['message'] != null)
            ? data['message'].toString()
            : 'Terjadi kesalahan sistem (${statusCode ?? 500})';

        if (statusCode == 401) {
          return AuthException(message);
        } else if (statusCode == 400) {
          return ValidationException(message);
        }
        return ServerException(message);
      default:
        return AppException(error.message ?? 'Kesalahan tidak terduga');
    }
  }
}
