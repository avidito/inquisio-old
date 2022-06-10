# Inquisio
Web-Crawler untuk mencari dan mengekstraksi informasi dari berita online dan abstrak artikel ilmiah. Bagian dari proyek idea-generator.

## Deskripsi
Modul untuk melakukan otomasi pencarian informasi secara sistematis di internet sekaligus mengekstrak berdasarkan masukan yang diberikan (contoh kata kunci atau jumlah data yang diinginkan). Inquisio ditujukan untuk mengambil informasi berupa teks dari berita, artikel ilmiah, forum, dan media sosial Twitter. Informasi diambil dari isi artikel, diskusi, atau abstrak (untuk artikel ilmiah hanya mengambil abstrak). Hasil ekstraksi berupa .csv atau json.

## Alur Kerja
Alur kerja dari sistem dijabarkan sebagai berikut:
- **Pengguna** memberikan argumen masukan ke dalam **Sistem**.
- **Sistem** memproses argumen masukan dan menjalankan *web-crawler*.
- **Sistem** memproses hasil scraping oleh web-crawler dan mengirimnya ke **Pengguna**.

## Media Sumber Data
**Daftar Media Informasi untuk *Web-Crawling***

| No |   Kategori   |      Nama      |  API? |          URL         |
|:--:|:------------:|:--------------:|:-----:|:--------------------:|
|  1 |    Berita    | Okezone        | Tidak | okezone.com          |
|  2 |    Berita    | Kompas         | Tidak | kompas.com           |
|  3 |    Berita    | Detik          | Tidak | detik.com            |
|  4 |    Berita    | Sindonews      | Tidak | sindonews.com        |
|  5 |    Berita    | Liputan6       | Tidak | liputan6.com         |
|  6 |  Repositori  | Repository IPB | Tidak | repository.ipb.ac.id |
|  7 |  Repositori  | Repository UI  | Tidak | repository.ui.ac.id  |
|  8 |  Repositori  | Repository ITB | Tidak | digilib.itb.ac.id    |
|  9 |  Repositori  | Repository UGM | Tidak | lib.ugm.ac.id        |
| 10 | Media Sosial | Twitter        |   Ya  | twitter.com          |

## Arsitektur Sistem
### Alur Data
![diagram-alir-data](https://github.com/leniangraeni/inquisio-old/blob/master/media/draft-skema-web-crawler.png)

**Diagram Alir Data Inquisio**

Aliran data untuk sistem Inquisio mengikuti skema di atas, dengan alur sebagai berikut:
1. **Front Desk** menerima masukan berupa argumen untuk menjalankan sistem. Argumen diproses dan diteruskan ke **Main Engine**.
2. **Main Engine** memproses kebutuhan sesuai masukan dari **Front Desk**. **Main Engine** kemudian membagi tugas ke berbagai **Interpreter** sesuai dengan argumen masukan dan kemampuan **Interpreter**.
3. **Interpreter** akan memecah komando dari **Main Engine** untuk membagi tugas ke **Web-Crawler** sesuai dengan domain pencarian dari masing-masing **Web-Crawler**. Jika domain/website tujuan memiliki API, **Interpreter** bertugas untuk men-*trigger* **API** tersebut.
4. **Web-Crawler** melakukan crawling ke **Internet** sesuai dengan spesifikasi dan jadwal yang diberikan.
5. **Internet** memberikan balasan informasi sesuai hasil pencarian **Web-Crawler** atau *request* **API**.
6. **Web-Crawler** / **API** meneruskan hasil pembacaan ke **Interpreter**.
7. **Interpreter** memastikan format dan pembersihan data dari **Web-Crawler** / **API**. Data yang sudah diproses kemudian diteruskan ke **Main Engine**.
8. **Main Engine** menyortir dan memvalidasi data yang diterima dari banyak **Interpreter**. Format data disesuaikan dengan kebutuhan **Front Desk**, kemudian data dikirimkan ke **Front Desk**.

## Komponen Sistem
### Front Desk
Front Desk bertugas untuk menerima permintaan pencarian data oleh pengguna sekaligus penyajian hasil pencarian. Komponen ini adalah komponen yang berhubungan langsung dengan pengguna. Komponen ini bertujuan untuk menerima masukan dari pengguna. Argumen yang diberikan oleh pengguna akan di-parsing dan dikonversi untuk menjadi parameter untuk pengajuan penjadwalan pencarian. Front Desk akan mengirimkan data request untuk mengajukan penjadwalan untuk pencarian dengan Main Engine. Front Desk juga akan mencatat perkembangan dari pencarian, sehingga pengguna bisa mengecek kondisi perkembangan pencarian. Informasi hasil pencarian akan disajikan oleh komponen ini.

### Main Engine
Main Engine bertugas untuk menerima pengajuan pencarian dari Front Desk dan menentukan bagaimana pencarian akan dilakukan. Komponen ini adalah komponen utama yang mengkoordinir seluruh penjadwalan, konfigurasi sistem, pengawasan, dan pengolahan pencarian data. Jika Main Engine mendapat banyak permintaan dari Front Desk, maka Main Engine akan melakukan penjadwalan pencarian yang sesuai dengan konfigurasi dan protokol yang diberlakukan. Komponen ini berhubungan langsung dengan Interpreter. Main Engine akan memberikan paket-paket informasi berisi tugas, konfigurasi, dan protokol yang perlu digunakan ke Interpreter sesuai jadwal yang sudah ditentukan. Main Engine juga memiliki pengawasan. Komponen ini akan terus mencatat log perkembangan tiap tugas yang diberikan. Ketika pengguna meng-request status pencarian ke Front Desk, Front Desk akan menanyakan hal ini ke Main Engine, Selain memberikan tugas dan pengawasan, Main Engine juga bertugas untuk melakukan validasi akhir data hasil pencarian. Main Engine akan melakukan pengolahan, penyesuaian, dan validasi data untuk kemudian dikirimkan ke Front Desk.

### Interpreter
Interpreter bertugas untuk mengkoordinir Web-Crawler / API untuk melakukan tugas sesuai penugasan dari Main Engine. Komponen ini adalah komponen yang menghubungkan antara Main Engine dengan agen-agen Web-Crawler / API. Interpreter bertugas untuk menerima tugas dari Main Engine dan meneruskan nya ke Web-Crawler / API. Interpreter akan menerima paket tugas dari Main Engine dan mengatur Web-Crawler / API untuk mengerjakan tugas tersebut. Tugas Web-Crawler / API akan terus diawasi oleh Interpreter untuk kemudian dilaporkan ke Main Engine. Interpreter juga memastikan bahwa Web-Crawler telah mendapatkan konfigurasi dan protokol yang tepat saat melakukan crawling. Kumpulan informasi yang diambil oleh Web-Crawler / API akan disimpan oleh Interpreter untuk diolah menjadi format yang lebih readable untuk Main Engine.

### Web-Crawler / API
Web-Crawler / API bertugas untuk mengekstrak informasi dari internet sesuai arahan dari Interpreter. Komponen ini adalah komponen yang berhubungan langsung dengan Internet. Web-Crawler akan menelusuri website sesuai dengan penugasannya masing-masing untuk mencari informasi yang dibutuhkan. Web-Crawler akan menaati protokol yang diberikan oleh Interpreter. Informasi yang telah diekstrak akan dikumpulkan menjadi paket item dan dikirimkan ke Interpreter. Komponen API adalah komponen yang digunakan untuk mengutilisasi API pengumpulan data yang disediakan oleh website. Komponen API akan memastikan penggunaan API sesuai dengan protokol.
