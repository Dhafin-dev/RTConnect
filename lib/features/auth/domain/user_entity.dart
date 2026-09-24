/// Domain Entity for User
class UserEntity {
  final int userId;
  final String nik;
  final String name;
  final String email;
  final String role;
  final String? phoneNumber;
  final String? address;
  final String? signatureUrl;

  const UserEntity({
    required this.userId,
    required this.nik,
    required this.name,
    required this.email,
    required this.role,
    this.phoneNumber,
    this.address,
    this.signatureUrl,
  });

  bool get isRT => role.toLowerCase() == 'rt';
  bool get isWarga => role.toLowerCase() == 'warga';
}
