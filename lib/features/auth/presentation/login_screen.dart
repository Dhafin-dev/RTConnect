import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:go_router/go_router.dart';
import '../../../core/constants/app_constants.dart';
import '../../../core/router/route_names.dart';
import '../../../core/theme/app_colors.dart';
import '../../../core/theme/app_spacing.dart';
import '../../../core/theme/app_typography.dart';
import '../../../shared/widgets/rt_primary_button.dart';
import '../../../shared/widgets/rt_text_field.dart';
import '../domain/auth_validators.dart';
import 'auth_controller.dart';

/// SCREEN-003: Login Page
class LoginScreen extends ConsumerStatefulWidget {
  const LoginScreen({super.key});

  @override
  ConsumerState<LoginScreen> createState() => _LoginScreenState();
}

class _LoginScreenState extends ConsumerState<LoginScreen> {
  final _formKey = GlobalKey<FormState>();
  final _identifierController = TextEditingController(text: 'dafin@gmail.com');
  final _passwordController = TextEditingController(text: '123456');

  @override
  void initState() {
    super.initState();
    _loadSavedServerUrl();
  }

  Future<void> _loadSavedServerUrl() async {
    const storage = FlutterSecureStorage();
    final savedUrl = await storage.read(key: AppConstants.keyCustomBaseUrl);
    if (savedUrl != null && savedUrl.isNotEmpty && mounted) {
      setState(() {
        AppConstants.customBaseUrl = savedUrl;
      });
    }
  }

  @override
  void dispose() {
    _identifierController.dispose();
    _passwordController.dispose();
    super.dispose();
  }

  Future<void> _handleLogin() async {
    if (!_formKey.currentState!.validate()) return;

    final identity = _identifierController.text.trim();
    final password = _passwordController.text.trim();

    final success = await ref.read(authControllerProvider.notifier).login(identity, password);

    if (mounted) {
      if (success) {
        final user = ref.read(authControllerProvider).user;
        if (user?.role == 'rt') {
          context.go(RouteNames.rtHome);
        } else {
          context.go(RouteNames.wargaHome);
        }
      } else {
        final error = ref.read(authControllerProvider).errorMessage ?? 'Login gagal';
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            backgroundColor: AppColors.error,
            content: Text(error),
          ),
        );
      }
    }
  }

  Future<void> _showServerConfigDialog() async {
    const storage = FlutterSecureStorage();
    final savedUrl = await storage.read(key: AppConstants.keyCustomBaseUrl) ?? AppConstants.defaultBaseUrl;
    final controller = TextEditingController(text: savedUrl);

    if (!mounted) return;
    await showDialog<void>(
      context: context,
      builder: (ctx) => AlertDialog(
        title: const Row(
          children: [
            Icon(Icons.dns, color: AppColors.primary),
            SizedBox(width: 8),
            Text('Alamat Server API'),
          ],
        ),
        content: Column(
          mainAxisSize: MainAxisSize.min,
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text(
              'Masukkan IP laptop backend (Wi-Fi / Hotspot yang sama):',
              style: AppTypography.bodySmall,
            ),
            const SizedBox(height: AppSpacing.sm),
            TextField(
              controller: controller,
              decoration: const InputDecoration(
                hintText: 'http://10.11.13.24:5000/api/v1',
                border: OutlineInputBorder(),
              ),
            ),
          ],
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(ctx),
            child: const Text('Batal'),
          ),
          ElevatedButton(
            onPressed: () async {
              final newUrl = controller.text.trim();
              if (newUrl.isNotEmpty) {
                await storage.write(key: AppConstants.keyCustomBaseUrl, value: newUrl);
                AppConstants.customBaseUrl = newUrl;
                if (ctx.mounted) {
                  Navigator.pop(ctx);
                }
                if (mounted) {
                  setState(() {});
                  ScaffoldMessenger.of(context).showSnackBar(
                    SnackBar(
                      backgroundColor: AppColors.success,
                      content: Text('Server disetel ke: $newUrl'),
                    ),
                  );
                }
              }
            },
            child: const Text('Simpan'),
          ),
        ],
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    final authState = ref.watch(authControllerProvider);

    return Scaffold(
      backgroundColor: AppColors.surface,
      body: SafeArea(
        child: Center(
          child: SingleChildScrollView(
            padding: const EdgeInsets.symmetric(horizontal: AppSpacing.lg),
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                const Icon(
                  Icons.mark_email_read_outlined,
                  size: 64,
                  color: AppColors.primary,
                ),
                const SizedBox(height: AppSpacing.sm),
                Text(
                  'RTConnect',
                  style: AppTypography.heading1.copyWith(color: AppColors.primary),
                ),
                const Text(
                  'Pelayanan Administrasi RT 032 RW 08',
                  style: AppTypography.bodySmall,
                ),
                const SizedBox(height: AppSpacing.xl),

                // Login Form Card
                Card(
                  elevation: 2,
                  shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
                  child: Padding(
                    padding: const EdgeInsets.all(AppSpacing.lg),
                    child: Form(
                      key: _formKey,
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.stretch,
                        children: [
                          const Text('Masuk ke Akun', style: AppTypography.heading3),
                          const SizedBox(height: AppSpacing.md),
                          RTTextField(
                            label: 'Email / NIK',
                            hint: 'Masukkan email atau NIK',
                            controller: _identifierController,
                            validator: (val) =>
                                AuthValidators.validateRequired(val, 'Email / NIK'),
                            prefixIcon: const Icon(Icons.person_outline, color: AppColors.textSecondary),
                          ),
                          const SizedBox(height: AppSpacing.md),
                          RTTextField(
                            label: 'Password',
                            hint: 'Masukkan password',
                            controller: _passwordController,
                            isPassword: true,
                            validator: AuthValidators.validatePassword,
                            prefixIcon: const Icon(Icons.lock_outline, color: AppColors.textSecondary),
                          ),
                          const SizedBox(height: AppSpacing.lg),
                          RTPrimaryButton(
                            text: 'Masuk Sekarang',
                            isLoading: authState.isLoading,
                            onPressed: _handleLogin,
                          ),
                        ],
                      ),
                    ),
                  ),
                ),

                const SizedBox(height: AppSpacing.lg),
                TextButton(
                  onPressed: () => context.push(RouteNames.register),
                  child: RichText(
                    text: TextSpan(
                      text: 'Belum punya akun warga? ',
                      style: AppTypography.bodyMedium.copyWith(color: AppColors.textSecondary),
                      children: [
                        TextSpan(
                          text: 'Daftar di sini',
                          style: AppTypography.bodyMedium.copyWith(
                            color: AppColors.primary,
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                      ],
                    ),
                  ),
                ),
                const SizedBox(height: AppSpacing.sm),
                TextButton.icon(
                  onPressed: _showServerConfigDialog,
                  icon: const Icon(Icons.settings_ethernet, size: 16, color: AppColors.textSecondary),
                  label: Text(
                    'Server: ${AppConstants.customBaseUrl ?? AppConstants.defaultBaseUrl}',
                    style: AppTypography.caption.copyWith(color: AppColors.textSecondary),
                  ),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
