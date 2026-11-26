"""Proteksi brute-force & rate limiting untuk autentikasi (/auth/login & /auth/register).

Melacak percobaan login gagal berdasarkan pasangan (identitas, IP) dan membekukan
akses selama ``LOCK_MINUTES`` menit setelah ``MAX_ATTEMPTS`` kegagalan beruntun,
serta membatasi laju pendaftaran akun per IP.
"""

import threading
import time
from typing import Optional

MAX_ATTEMPTS = 5
LOCK_MINUTES = 15
LOCK_SECONDS = LOCK_MINUTES * 60

REGISTER_MAX_REQUESTS = 10
REGISTER_WINDOW_SECONDS = 15 * 60

_lock = threading.Lock()
_login_attempts: dict[tuple[str, str], dict] = {}
_register_windows: dict[str, list[float]] = {}


class AuthGuardResult:
    def __init__(
        self,
        ok: bool,
        http_status: int = 200,
        error: Optional[str] = None,
        message: str = '',
        remaining_attempts: Optional[int] = None,
        locked_minutes: Optional[int] = None,
    ):
        self.ok = ok
        self.http_status = http_status
        self.error = error
        self.message = message
        self.remaining_attempts = remaining_attempts
        self.locked_minutes = locked_minutes

    def data(self):
        payload = {}
        if self.remaining_attempts is not None:
            payload['sisa_percobaan'] = self.remaining_attempts
        if self.locked_minutes is not None:
            payload['sisa_menit'] = self.locked_minutes
            payload['sisa_percobaan'] = 0
        return payload or None


def _normalize_key(identity: str, client_ip: str) -> tuple[str, str]:
    return ((identity or '').strip().lower(), (client_ip or 'unknown').strip())


def check_login_allowed(identity: str, client_ip: str) -> AuthGuardResult:
    """Periksa apakah pasangan (identitas, IP) sedang terkunci akibat gagal beruntun."""
    key = _normalize_key(identity, client_ip)
    now = time.monotonic()
    with _lock:
        entry = _login_attempts.get(key)
        if not entry:
            return AuthGuardResult(True)
        locked_until = entry.get('locked_until')
        if locked_until and locked_until > now:
            remaining_secs = locked_until - now
            minutes = max(1, int((remaining_secs + 59) // 60))
            return AuthGuardResult(
                ok=False,
                http_status=429,
                error='TOO_MANY_REQUESTS',
                message=(
                    f'Terlalu banyak percobaan login gagal ({MAX_ATTEMPTS} kali). '
                    f'Coba lagi dalam {minutes} menit.'
                ),
                locked_minutes=minutes,
            )
        if locked_until and locked_until <= now:
            _login_attempts.pop(key, None)
    return AuthGuardResult(True)


def record_login_failure(identity: str, client_ip: str) -> AuthGuardResult:
    """Catat satu percobaan login gagal dan kunci jika mencapai batas MAX_ATTEMPTS."""
    key = _normalize_key(identity, client_ip)
    now = time.monotonic()
    with _lock:
        entry = _login_attempts.get(key)
        if not entry or (entry.get('locked_until') and entry['locked_until'] <= now):
            entry = {'count': 0, 'locked_until': None}

        entry['count'] += 1
        if entry['count'] >= MAX_ATTEMPTS:
            entry['count'] = 0
            entry['locked_until'] = now + LOCK_SECONDS
            _login_attempts[key] = entry
            return AuthGuardResult(
                ok=False,
                http_status=429,
                error='TOO_MANY_REQUESTS',
                message=(
                    f'Terlalu banyak percobaan login gagal ({MAX_ATTEMPTS} kali). '
                    f'Akun dikunci sementara selama {LOCK_MINUTES} menit.'
                ),
                locked_minutes=LOCK_MINUTES,
            )

        _login_attempts[key] = entry
        remaining = MAX_ATTEMPTS - entry['count']
        return AuthGuardResult(
            ok=False,
            http_status=401,
            error='UNAUTHORIZED',
            message=f'Email/NIK atau password salah. Sisa percobaan: {remaining}',
            remaining_attempts=remaining,
        )


def reset_login_attempts(identity: Optional[str] = None, client_ip: Optional[str] = None) -> None:
    """Reset penghitung kegagalan login (setelah login sukses atau pada setup pengujian)."""
    with _lock:
        if identity is None and client_ip is None:
            _login_attempts.clear()
            _register_windows.clear()
            return
        if identity is not None and client_ip is not None:
            _login_attempts.pop(_normalize_key(identity, client_ip), None)
            return
        target_id = (identity or '').strip().lower()
        target_ip = (client_ip or '').strip()
        for k in list(_login_attempts.keys()):
            if (identity is not None and k[0] == target_id) or (client_ip is not None and k[1] == target_ip):
                _login_attempts.pop(k, None)


def check_register_rate_limit(client_ip: str) -> AuthGuardResult:
    """Batasi frekuensi pendaftaran akun baru per IP."""
    ip = (client_ip or 'unknown').strip()
    now = time.monotonic()
    cutoff = now - REGISTER_WINDOW_SECONDS
    with _lock:
        timestamps = [ts for ts in _register_windows.get(ip, []) if ts > cutoff]
        if len(timestamps) >= REGISTER_MAX_REQUESTS:
            _register_windows[ip] = timestamps
            return AuthGuardResult(
                ok=False,
                http_status=429,
                error='TOO_MANY_REQUESTS',
                message='Terlalu banyak permintaan pendaftaran dari perangkat ini. Coba lagi beberapa saat.',
                locked_minutes=LOCK_MINUTES,
            )
        timestamps.append(now)
        _register_windows[ip] = timestamps
    return AuthGuardResult(True)
