import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import '../../../core/router/route_names.dart';
import '../../../core/theme/app_colors.dart';
import '../../../core/theme/app_spacing.dart';
import '../../../core/theme/app_typography.dart';
import '../../../shared/widgets/rt_bottom_nav_bar.dart';
import '../../../shared/widgets/rt_primary_button.dart';
import '../../../shared/widgets/rt_text_field.dart';
import '../domain/auth_validators.dart';

/// SCREEN-003: Login Page
class LoginScreen extends StatefulWidget {
  const LoginScreen({super.key});

  @override
  State<LoginScreen> createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> {
  final _formKey = GlobalKey<FormState>();
  final _identifierController = TextEditingController(text: 'dafin@gmail.com');
  final _passwordController = TextEditingController(text: '123456');
  bool _isLoading = false;
  String? _errorMessage;

  @override
  void dispose() {
    _identifierController.dispose();
    _passwordController.dispose();
    super.dispose();
  }

  void _handleLogin() async {
    if (!_formKey.currentState!.validate()) return;

    setState(() {
      _isLoading = true;
      _errorMessage = null;
    });

    // Simulated Auth matching sequence diagram
    await Future.delayed(const Duration(milliseconds: 600));

    final identity = _identifierController.text.trim().toLowerCase();
    setState(() => _isLoading = false);

    if (identity.contains('rt')) {
      // Role: Ketua RT
      if (mounted) context.go(RouteNames.rtQueue);
    } else {
      // Role: Warga
      if (mounted) context.go(RouteNames.wargaHome);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.background,
      body: SafeArea(
        child: Center(
          child: SingleChildScrollView(
            padding: const EdgeInsets.symmetric(horizontal: AppSpacing.spaceLG),
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Text(
                  'Masuk Akun',
                  style: AppTypography.displayLarge.copyWith(
                    fontWeight: FontWeight.w700,
                  ),
                ),
                const SizedBox(height: AppSpacing.spaceXL),

                // Login Form Card
                Card(
                  child: Padding(
                    padding: const EdgeInsets.all(AppSpacing.spaceLG),
                    child: Form(
                      key: _formKey,
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          if (_errorMessage != null) ...[
                            Container(
                              padding: const EdgeInsets.all(AppSpacing.spaceSM),
                              decoration: BoxDecoration(
                                color: AppColors.statusRevisi.withOpacity(0.1),
                                borderRadius: BorderRadius.circular(AppSpacing.radiusSM),
                              ),
                              child: Text(
                                _errorMessage!,
                                style: AppTypography.bodyMedium.copyWith(
                                  color: AppColors.statusRevisi,
                                ),
                              ),
                            ),
                            const SizedBox(height: AppSpacing.spaceMD),
                          ],
                          RTTextField(
                            label: 'Email / NIK',
                            hint: 'Masukkan email atau NIK',
                            controller: _identifierController,
                            validator: (val) =>
                                AuthValidators.validateRequired(val, 'Email / NIK'),
                          ),
                          const SizedBox(height: AppSpacing.spaceMD),
                          RTTextField(
                            label: 'Password',
                            hint: 'Masukkan password',
                            controller: _passwordController,
                            isPassword: true,
                            validator: AuthValidators.validatePassword,
                          ),
                          const SizedBox(height: AppSpacing.spaceLG),
                          RTPrimaryButton(
                            text: 'Masuk',
                            isLoading: _isLoading,
                            onPressed: _handleLogin,
                          ),
                        ],
                      ),
                    ),
                  ),
                ),

                const SizedBox(height: AppSpacing.spaceMD),
                TextButton(
                  onPressed: () => context.push(RouteNames.register),
                  child: Text(
                    'Belum punya akun? Registrasi di sini',
                    style: AppTypography.bodyMedium.copyWith(
                      color: AppColors.primaryBrand,
                      fontWeight: FontWeight.w600,
                    ),
                  ),
                ),
              ],
            ),
          ),
        ),
      ),
      bottomNavigationBar: RTBottomNavBar(
        currentIndex: 1,
        onTap: (index) {
          if (index == 0) context.go(RouteNames.landing);
          if (index == 1) context.go(RouteNames.landing);
        },
      ),
    );
  }
}
