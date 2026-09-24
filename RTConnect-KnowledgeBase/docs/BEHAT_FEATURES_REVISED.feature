# language: id
Fitur: Sistem Administrasi Warga RTConnect Terpadu
  Sebagai Warga dan Pengurus RT di Lingkungan RT 032 RW 08 Griya Taman Asri
  Kami membutuhkan platform administrasi surat digital terintegrasi AI dan chatbot
  Agar proses pelayanan surat pengantar cepat, akurat, dan transparan

  # ------------------------------------------------------------------
  # US-01 & US-02: AUTENTIKASI DAN AKSES PENGGUNA
  # ------------------------------------------------------------------
  Skenario: Warga baru berhasil melakukan registrasi akun mandiri
    Menimbang Warga berada pada halaman registrasi "/register"
    Ketika Warga mengisi "nik" dengan "3515082104990001"
    Dan Warga mengisi "nama_lengkap" dengan "Budi Santoso"
    Dan Warga mengisi "email" dengan "budi.santoso@gmail.com"
    Dan Warga mengisi "password" dengan "Rahasia123!"
    Dan Warga mengisi "konfirmasi_password" dengan "Rahasia123!"
    Dan Warga mengunggah berkas "ttd_budi.png" pada kolom "tanda_tangan"
    Dan Warga menekan tombol "Daftar Akun"
    Maka Warga akan melihat notifikasi "Registrasi akun berhasil, silakan masuk"
    Dan Warga dialihkan ke halaman "/login"

  Skenario: Pengguna berhasil login sesuai dengan perannya
    Menimbang Pengguna berada pada halaman "/login"
    Ketika Pengguna mengisi "identity" dengan "budi.santoso@gmail.com"
    Dan Pengguna mengisi "password" dengan "Rahasia123!"
    Dan Pengguna menekan tombol "Masuk"
    Maka Pengguna dialihkan ke halaman "/warga/beranda"
    Dan Pengguna melihat pesan sambutan "Selamat Datang, Budi Santoso"

  # ------------------------------------------------------------------
  # US-03: PENGAJUAN SURAT PENGANTAR (WARGA)
  # ------------------------------------------------------------------
  Skenario: Warga berhasil mengajukan surat pengantar domisili dengan TTD digital
    Menimbang Warga telah login dan berada di halaman "/warga/surat/baru"
    Ketika Warga memilih "Surat Keterangan Domisili" dari daftar "jenis_surat"
    Dan Warga mengisi "keperluan" dengan "Persyaratan perpanjangan KTP elektronik"
    Dan Warga memilih opsi "Tanda Tangan Digital (Tempelan Gambar Tanda Tangan)"
    Dan Warga menekan tombol "Kirim Pengajuan"
    Maka Warga melihat pesan sukses "Pengajuan surat pengantar berhasil dikirim"
    Dan Status pengajuan pada daftar riwayat berubah menjadi "Diajukan"

  # ------------------------------------------------------------------
  # US-04: PERBAIKAN FORMULIR / REVISI PENGAJUAN
  # ------------------------------------------------------------------
  Skenario: Warga mengirimkan revisi pengajuan yang sebelumnya diminta oleh RT
    Menimbang Warga memiliki pengajuan bernomor "SRT-032-001" dengan status "Perlu Revisi"
    Dan Warga membuka formulir perbaikan pada tautan "/warga/surat/revisi/SRT-032-001"
    Ketika Warga memperbarui "keperluan" dengan "Perpanjangan KTP elektronik dan pembukaan rekening bank"
    Dan Warga mengunggah dokumen "kk_terbaru.pdf" pada lampiran
    Dan Warga menekan tombol "Kirim Ulang Revisi"
    Maka Warga melihat notifikasi "Revisi pengajuan berhasil dikirim kembali"
    Dan Status pengajuan diperbarui menjadi "Diajukan"

  # ------------------------------------------------------------------
  # US-05: TINJAUAN DAN TINDAK LANJUT BERKAS (KETUA RT)
  # ------------------------------------------------------------------
  Skenario: Ketua RT menyetujui pengajuan surat pengantar setelah meninjau draf
    Menimbang Ketua RT login dan membuka daftar antrean pengajuan pada "/rt/pengajuan"
    Ketika Ketua RT memilih berkas dengan ID "SRT-032-001"
    Dan Ketua RT memeriksa draf surat hasil formulasi Generative AI
    Dan Ketua RT mengisi catatan persetujuan "Berkas pemohon lengkap dan sah"
    Dan Ketua RT menekan tombol "Setujui Pengajuan"
    Maka status berkas berubah menjadi "Disetujui"
    Dan Sistem menerbitkan nomor surat resmi secara otomatis

  # ------------------------------------------------------------------
  # US-06: PENGESAHAN DOKUMEN DENGAN TANDA TANGAN DIGITAL (QR CODE)
  # ------------------------------------------------------------------
  Skenario: Ketua RT membubuhkan stempel digital Tempelan Gambar Tanda Tangan pada berkas yang disetujui
    Menimbang Ketua RT berada pada halaman pengesahan surat "/rt/pengesahan/SRT-032-001"
    Ketika Ketua RT memasukkan PIN otorisasi "123456"
    Dan Ketua RT menekan tombol "Bubuhkan Tanda Tangan Digital"
    Maka sistem menyematkan tempelan gambar tanda tangan digital resmi pada lembar PDF surat
    Dan Status pengajuan berubah menjadi "Selesai"
    Dan Notifikasi penerbitan surat terkirim ke akun Warga

  # ------------------------------------------------------------------
  # US-07: PENGESAHAN TANDA TANGAN BASAH (ALUR HIBRIDA FISIK)
  # ------------------------------------------------------------------
  Skenario: Ketua RT mencetak dan mengonfirmasi kesiapan surat fisik bertanda tangan basah
    Menimbang Surat bernomor "SRT-032-002" berstatus "Disetujui" dengan metode "Basah"
    Ketika Ketua RT menekan tombol "Cetak Dokumen Fisik"
    Dan Ketua RT menandatangani berkas fisik dengan tinta basah
    Dan Ketua RT menekan tombol "Konfirmasi Siap Diambil"
    Maka sistem mengubah status menjadi "Siap Diambil"
    Dan Warga menerima pemberitahuan alamat dan waktu pengambilan surat fisik

  # ------------------------------------------------------------------
  # US-08: UNDUH SURAT OLEH WARGA
  # ------------------------------------------------------------------
  Skenario: Warga mengunduh surat pengantar resmi berstempel Tempelan Gambar Tanda Tangan
    Menimbang Warga membuka riwayat pengajuan pada "/warga/riwayat"
    Dan Pengajuan "SRT-032-001" memiliki status "Selesai"
    Ketika Warga menekan tombol "Unduh Berkas PDF"
    Maka browser mengunduh berkas surat resmi bertipe "application/pdf"
    Dan Dokumen dapat diverifikasi keasliannya melalui pemindaian Tempelan Gambar Tanda Tangan

  # ------------------------------------------------------------------
  # US-09: TANYA JAWAB DENGAN CHATBOT NLP RAG & ESKALASI WA
  # ------------------------------------------------------------------
  Skenario: Chatbot menjawab pertanyaan warga berdasarkan basis pengetahuan regulasi RT
    Menimbang Warga membuka menu Tanya RT pada "/warga/chatbot"
    Ketika Warga mengirim pertanyaan "Berapa lama masa berlaku surat pengantar RT?"
    Maka Chatbot menampilkan respons "Surat pengantar RT berlaku selama 30 hari sejak tanggal penerbitan"
    Dan Chatbot menyertakan label sumber "Ketentuan Umum Layanan RT 032"

  Skenario: Chatbot mengalihkan pertanyaan warga ke WhatsApp Ketua RT jika informasi belum tersedia
    Menimbang Warga membuka menu Tanya RT pada "/warga/chatbot"
    Ketika Warga mengirim pertanyaan "Apakah ada koordinasi gotong royong saluran air minggu depan?"
    Maka Chatbot menampilkan pesan "Mohon maaf, informasi terkait belum tercatat dalam basis data resmi"
    Dan Sistem menyediakan tombol "Eskalasi ke WhatsApp Ketua RT" yang berisi ringkasan pertanyaan
