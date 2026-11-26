"""Unit test backend terisolasi dengan mock (tanpa koneksi database eksternal).

Memenuhi Issue #20: validasi skema input, dekode token JWT, sanitasi path berkas
storage, proteksi brute-force login, dan perilaku fallback TanyaRT.
"""

import io
import os
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

import jwt
from PIL import Image
from werkzeug.datastructures import FileStorage

BACKEND_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)

from app import create_app
from config import Config
from middleware.auth_middleware import generate_token
from services.applicant_data import parse_applicant_data
from services.file_storage import _local_path, _validate_key, store_upload
from services.login_guard_service import (
    MAX_ATTEMPTS,
    check_login_allowed,
    record_login_failure,
    reset_login_attempts,
)
from services.rag_service import search_knowledge_base


def _png_bytes() -> bytes:
    buf = io.BytesIO()
    Image.new('RGB', (4, 4), color=(10, 20, 30)).save(buf, format='PNG')
    return buf.getvalue()


class ApplicantSchemaValidationTests(unittest.TestCase):
    VALID_DATA = {
        'pekerjaan': 'Karyawan Swasta',
        'jenis_kelamin': 'Laki-laki',
        'tempat_lahir': 'Surabaya',
        'tanggal_lahir': '1995-08-17',
        'agama': 'Islam',
        'status_kawin': 'Belum Kawin',
        'kewarganegaraan': 'WNI',
        'nomor_kk': '3578080101950001',
        'tujuan': 'Polsek Karang Pilang',
    }

    def test_valid_applicant_data_parses_cleanly(self):
        values, err = parse_applicant_data(self.VALID_DATA)
        self.assertIsNone(err)
        self.assertEqual(values['pekerjaan'], 'Karyawan Swasta')
        self.assertEqual(values['instansi_tujuan'], 'Polsek Karang Pilang')
        self.assertIsNone(values['keterangan_lain'])

    def test_invalid_kk_and_gender_rejected(self):
        bad_kk = {**self.VALID_DATA, 'nomor_kk': '12345'}
        _, err = parse_applicant_data(bad_kk)
        self.assertIn('16 digit', err)

        bad_gender = {**self.VALID_DATA, 'jenis_kelamin': 'Lainnya'}
        _, err = parse_applicant_data(bad_gender)
        self.assertIn('Jenis kelamin', err)

    def test_partial_update_only_validates_sent_fields(self):
        values, err = parse_applicant_data({'pekerjaan': 'Wiraswasta'}, partial=True)
        self.assertIsNone(err)
        self.assertEqual(values, {'pekerjaan': 'Wiraswasta'})


class JwtAndAuthMiddlewareTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = create_app()
        cls.client = cls.app.test_client()

    def test_generate_and_decode_token(self):
        token = generate_token(42, 'warga', 'warga@example.test')
        payload = jwt.decode(token, Config.JWT_SECRET, algorithms=['HS256'])
        self.assertEqual(payload['sub'], '42')
        self.assertEqual(payload['role'], 'warga')
        self.assertEqual(payload['email'], 'warga@example.test')

    @patch('middleware.auth_middleware.get_user')
    def test_bearer_header_accepted_and_query_token_rejected(self, mock_get_user):
        mock_get_user.return_value = {
            'user_id': 7,
            'nik': '3578000000000007',
            'nama_lengkap': 'Warga Mock',
            'email': 'mock@example.test',
            'nomor_telepon': '08123456789',
            'alamat': 'Blok A-1',
            'nomor_rt': '04',
            'nomor_rw': '09',
            'role': 'warga',
            'tanda_tangan_url': None,
            'foto_profil': None,
            'is_active': True,
        }
        token = generate_token(7, 'warga', 'mock@example.test')

        ok_res = self.client.get('/api/v1/auth/me', headers={'Authorization': f'Bearer {token}'})
        self.assertEqual(ok_res.status_code, 200)
        self.assertEqual(ok_res.get_json()['data']['nama_lengkap'], 'Warga Mock')

        # SEC-02: query string ?token= wajib ditolak
        q_res = self.client.get(f'/api/v1/auth/me?token={token}')
        self.assertEqual(q_res.status_code, 401)

    @patch('middleware.auth_middleware.get_user')
    def test_update_profile_null_and_duplicate_rejected(self, mock_get_user):
        mock_get_user.return_value = {
            'user_id': 7,
            'nik': '3578000000000007',
            'nama_lengkap': 'Warga Mock',
            'email': 'mock@example.test',
            'nomor_telepon': '08123456789',
            'alamat': 'Blok A-1',
            'nomor_rt': '04',
            'nomor_rw': '09',
            'role': 'warga',
            'tanda_tangan_url': None,
            'foto_profil': None,
            'is_active': True,
        }
        token = generate_token(7, 'warga', 'mock@example.test')
        headers = {'Authorization': f'Bearer {token}'}

        res_null = self.client.put('/api/v1/auth/me', headers=headers, json={'nama_lengkap': None})
        self.assertEqual(res_null.status_code, 400)

        with patch('routes.auth_routes.query_one', return_value={'email': 'other@example.test'}):
            res_dup = self.client.put('/api/v1/auth/me', headers=headers, json={'email': 'other@example.test'})
            self.assertEqual(res_dup.status_code, 409)

    @patch('middleware.auth_middleware.get_user')
    def test_signature_json_injection_rejected(self, mock_get_user):
        mock_get_user.return_value = {
            'user_id': 7,
            'role': 'warga',
            'is_active': True,
            'tanda_tangan_url': 'attachments/secret.png',
        }
        token = generate_token(7, 'warga', 'mock@example.test')
        headers = {'Authorization': f'Bearer {token}'}

        res_post = self.client.post('/api/v1/auth/signature', headers=headers, json={'signature_key': 'attachments/secret.png'})
        self.assertEqual(res_post.status_code, 400)

        res_get = self.client.get('/api/v1/auth/signature', headers=headers)
        self.assertEqual(res_get.status_code, 404)


class FileStorageSanitizationTests(unittest.TestCase):
    def test_path_traversal_and_invalid_category_blocked(self):
        for bad_key in (
            '../.env',
            'signatures/../../config.py',
            '/etc/passwd',
            'unknown_dir/file.png',
            '',
        ):
            with self.assertRaises(ValueError):
                _validate_key(bad_key)
            with self.assertRaises(ValueError):
                _local_path(bad_key)

    def test_local_path_stays_inside_upload_root(self):
        resolved = _local_path('signatures/sample.png')
        upload_root = os.path.abspath(Config.UPLOAD_FOLDER)
        self.assertEqual(os.path.commonpath([upload_root, resolved]), upload_root)

    def test_store_upload_rejects_mismatched_magic_bytes(self):
        fake_png = FileStorage(stream=io.BytesIO(b'not-an-image'), filename='fake.png')
        with self.assertRaises(ValueError):
            store_upload(fake_png, 'signatures')

    @patch('services.file_storage.store_bytes', side_effect=lambda key, data, ct: key)
    def test_store_upload_accepts_valid_png(self, mock_store):
        valid_png = FileStorage(stream=io.BytesIO(_png_bytes()), filename='sig.png')
        key = store_upload(valid_png, 'signatures')
        self.assertTrue(key.startswith('signatures/'))
        self.assertTrue(key.endswith('.png'))
        mock_store.assert_called_once()


class LoginBruteForceAndRagFallbackTests(unittest.TestCase):
    def setUp(self):
        reset_login_attempts()

    def test_login_guard_locks_after_five_failures_and_resets(self):
        for i in range(MAX_ATTEMPTS - 1):
            res = record_login_failure('warga@example.test', '127.0.0.1')
            self.assertEqual(res.http_status, 401)
            self.assertEqual(res.remaining_attempts, MAX_ATTEMPTS - 1 - i)

        locked = record_login_failure('warga@example.test', '127.0.0.1')
        self.assertEqual(locked.http_status, 429)
        self.assertEqual(locked.error, 'TOO_MANY_REQUESTS')
        self.assertFalse(check_login_allowed('warga@example.test', '127.0.0.1').ok)

        reset_login_attempts('warga@example.test', '127.0.0.1')
        self.assertTrue(check_login_allowed('warga@example.test', '127.0.0.1').ok)

    def test_tanyart_no_false_escalation_when_llm_unavailable(self):
        mock_chunks = [{
            'chunk_id': 1,
            'knowledge_id': 1,
            'urutan_chunk': 1,
            'isi_chunk': 'Untuk membuat SKCK online siapkan KTP, pasfoto merah, dan email aktif.',
            'kata_kunci': 'skck syarat online polri',
            'kode_sumber': 'RTC-025',
            'embedding_vector': None,
            'judul_dokumen': 'Persyaratan mengurus SKCK secara online melalui Polri',
            'kategori': 'skck',
            'document_text': '',
        }]
        with patch('services.rag_service.get_knowledge_chunks', return_value=mock_chunks), \
             patch('services.rag_service.is_embedding_configured', return_value=False), \
             patch('services.rag_service.synthesize_answer_with_gemini', side_effect=lambda q, c, h, time_budget=None: ('Jawaban fallback', 'Rujukan', False)):
            res = search_knowledge_base('Syarat Surat SKCK', time_budget=2.0)
            self.assertEqual(res['status'], 'SUMBER_DITEMUKAN')
            self.assertFalse(res['is_escalated'])
            self.assertIsNone(res['escalation_whatsapp_url'])


if __name__ == '__main__':
    unittest.main()
