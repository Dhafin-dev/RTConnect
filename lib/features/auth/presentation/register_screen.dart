import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:file_picker/file_picker.dart';
import 'package:go_router/go_router.dart';
import '../../../core/router/route_names.dart';
import '../../../core/theme/app_colors.dart';
import '../../../core/theme/app_spacing.dart';
import '../../../core/theme/app_typography.dart';
import '../../../shared/widgets/rt_primary_button.dart';
import '../../../shared/widgets/rt_text_field.dart';
import '../domain/auth_validators.dart';
import 'auth_controller.dart';

class RegisterScreen extends ConsumerStatefulWidget {
  const RegisterScreen({super.key});

  @override
  ConsumerState<RegisterScreen> createState() => _RegisterScreenState();
}

class _RegisterScreenState extends ConsumerState<RegisterScreen> {
  final _formKey = GlobalKey<FormState>();

  final _nikController = TextEditingController();
  final _namaController = TextEditingController();
  final _emailController = TextEditingController();
  final _passwordController = TextEditingController();
  final _phoneController = TextEditingController();
  final _alamatController = TextEditingController();

  String? _selectedSignaturePath;
  String? _signatureFileName;

  @override
  void dispose() {
    _nikController.dispose();
    _namaController.dispose();
    _emailController.dispose();
    _passwordController.dispose();
    _phoneController.dispose();
    _alamatController.dispose();
    super.dispose();
  }

  Future<void> _pickSignatureFile() async {
    final result = await FilePicker.platform.pickFiles(
      type: FileType.custom,
      allowedExtensions: ['png', 'jpg', 'jpeg'],
    );

    if (result != null && result.files.single.path != null) {
      setState(() {
        _selectedSignaturePath = result.files.single.path;
        _signatureFileName = result.files.single.name;
      });
    }
  }

  Future<void> _submitRegister() async {
    if (!_formKey.currentState!.validate()) return;

    final success = await ref.read(authControllerProvider.notifier).register(
      nik: _nikController.text.trim(),
      namaLengkap: _namaController.text.trim(),
      email: _emailController.text.trim(),
      password: _passwordController.text.trim(),
      nomorTelepon: _phoneController.text.trim(),
      alamat: _alamatController.text.trim(),
      signaturePath: _selectedSignaturePath,
    );

    if (mounted) {
      if (success) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(
            backgroundColor: AppColors.success,
            content: Text('Registrasi berhasil! Silakan masuk dengan akun Anda.'),
          ),
        );
        context.go(RouteNames.login);
      } else {
        final error = ref.read(authControllerProvider).errorMessage ?? 'Gagal mendaftar';
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            backgroundColor: AppColors.error,
            content: Text(error),
          ),
        );
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    final authState = ref.watch(authControllerProvider);

    return Scaffold(
      backgroundColor: AppColors.surface,
      appBar: AppBar(
        title: const Text('Pendaftaran Warga', style: AppTypography.heading3),
        centerTitle: true,
        backgroundColor: AppColors.surface,
        elevation: 0,
        leading: IconButton(
          icon: const Icon(Icons.arrow_back, color: AppColors.textPrimary),
          onPressed: () => context.go(RouteNames.login),
        ),
      ),
      body: SafeArea(
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(AppSpacing.lg),
          child: Form(
            key: _formKey,
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: [
                const Text(
                  'Buat Akun RTConnect',
                  style: AppTypography.heading2,
                ),
                const SizedBox(height: AppSpacing.xs),
                const Text(
                  'Daftarkan diri Anda sebagai warga RT 032 RW 08 Griya Taman Asri.',
                  style: AppTypography.bodySmall,
                ),
                const SizedBox(height: AppSpacing.lg),

                // Form NIK
                RTTextField(
                  label: 'Nomor Induk Kependudukan (NIK)',
                  hint: '16 digit NIK sesuai KTP',
                  controller: _nikController,
                  keyboardType: TextInputType.number,
                  validator: AuthValidators.validateNik,
                  prefixIcon: const Icon(Icons.badge_outlined, color: AppColors.textSecondary),
                ),
                const SizedBox(height: AppSpacing.md),

                // Nama Lengkap
                RTTextField(
                  label: 'Nama Lengkap',
                  hint: 'Nama lengkap sesuai KTP',
                  controller: _namaController,
                  validator: (v) => (v == null || v.trim().isEmpty) ? 'Nama lengkap wajib diisi' : null,
                  prefixIcon: const Icon(Icons.person_outline, color: AppColors.textSecondary),
                ),
                const SizedBox(height: AppSpacing.md),

                // Email
                RTTextField(
                  label: 'Alamat Email',
                  hint: 'nama@email.com',
                  controller: _emailController,
                  keyboardType: TextInputType.emailAddress,
                  validator: AuthValidators.validateEmail,
                  prefixIcon: const Icon(Icons.email_outlined, color: AppColors.textSecondary),
                ),
                const SizedBox(height: AppSpacing.md),

                // Password
                RTTextField(
                  label: 'Password',
                  hint: 'Minimal 6 karakter',
                  controller: _passwordController,
                  isPassword: true,
                  validator: AuthValidators.validatePassword,
                  prefixIcon: const Icon(Icons.lock_outline, color: AppColors.textSecondary),
                ),
                const SizedBox(height: AppSpacing.md),

                // Nomor Telepon / WA
                RTTextField(
                  label: 'Nomor WhatsApp / HP',
                  hint: 'Contoh: 081234567890',
                  controller: _phoneController,
                  keyboardType: TextInputType.phone,
                  validator: AuthValidators.validatePhone,
                  prefixIcon: const Icon(Icons.phone_android_outlined, color: AppColors.textSecondary),
                ),
                const SizedBox(height: AppSpacing.md),

                // Alamat
                RTTextField(
                  label: 'Alamat Rumah',
                  hint: 'Contoh: Griya Taman Asri Blok B-12',
                  controller: _alamatController,
                  validator: (v) => (v == null || v.trim().isEmpty) ? 'Alamat wajib diisi' : null,
                  prefixIcon: const Icon(Icons.home_outlined, color: AppColors.textSecondary),
                ),
                const SizedBox(height: AppSpacing.lg),

                // Upload Tanda Tangan Digital
                Container(
                  padding: const EdgeInsets.all(AppSpacing.md),
                  decoration: BoxDecoration(
                    color: AppColors.cardBackground,
                    borderRadius: BorderRadius.circular(12),
                    border: Border.all(color: AppColors.border),
                  ),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      const Row(
                        children: [
                          Icon(Icons.draw_outlined, color: AppColors.primary),
                          SizedBox(width: AppSpacing.xs),
                          Text('Pindaian Tanda Tangan (Opsional)', style: AppTypography.labelBold),
                        ],
                      ),
                      const SizedBox(height: 4),
                      const Text(
                        'Unggah foto tanda tangan digital Anda di atas kertas putih bersih (PNG/JPG)',
                        style: AppTypography.caption,
                      ),
                      const SizedBox(height: AppSpacing.sm),
                      OutlinedButton.icon(
                        onPressed: _pickSignatureFile,
                        icon: const Icon(Icons.upload_file),
                        label: Text(_signatureFileName ?? 'Pilih Berkas Tanda Tangan'),
                        style: OutlinedButton.styleFrom(
                          foregroundColor: AppColors.primary,
                          side: const BorderSide(color: AppColors.primary),
                          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(8)),
                        ),
                      ),
                    ],
                  ),
                ),
                const SizedBox(height: AppSpacing.xl),

                // Tombol Submit
                RTPrimaryButton(
                  text: 'Daftar Akun Warga',
                  isLoading: authState.isLoading,
                  onPressed: _submitRegister,
                ),
                const SizedBox(height: AppSpacing.md),

                // Link ke Login
                Row(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    const Text('Sudah memiliki akun? ', style: AppTypography.bodySmall),
                    GestureDetector(
                      onTap: () => context.go(RouteNames.login),
                      child: Text(
                        'Masuk di sini',
                        style: AppTypography.bodySmall.copyWith(
                          color: AppColors.primary,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                    ),
                  ],
                ),
                const SizedBox(height: AppSpacing.lg),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
