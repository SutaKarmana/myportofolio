## Identitas Mahasiswa : 
Name : I Nyoman Yadnya Suta Karmana

NPM : 2506615993

Class : PBP F

#### Pertanyaan Reflektif

1. Jawaban no 1:
    Ya, saya menggunakan beberapa elemen semantik HTML5 seperti `<header>`, `<nav>`, `<main>`, `<section>`, `<article>`, dan `<footer>`.Elemen <section> saya gunakan untuk memisahkan bagian-bagian utama halaman, yaitu profile, experience, dan awards. Sementara itu, elemen <article> saya terapkan pada setiap entri pengalaman dan penghargaan karena masing-masing memuat informasi yang berdiri sendiri secara utuh. Elemen-elemen ini membuat struktur kode HTML jauh lebih rapi dan mudah dibaca. Hal tersebut membantu saya memahami fungsi setiap bagian halaman dengan cepat, sehingga mempermudah saya ketika melanjutkan proyek ini ke depannya. Selain itu, struktur semantik juga meningkatkan aksesibilitas karena membantu browser maupun teknologi asistif  memahami hierarki konten dengan tepat. Untuk website statis, elemen semantik sangat berguna dalam mengorganisasi konten secara terstruktur meski belum melibatkan data dinamis dari database.

2. Jawaban no 2:
    Tantangan tata letak utama yang saya hadapi adalah menyesuaikan tampilan multi-kolom pada desktop ke layar mobile yang jauh lebih sempit. Elemen-elemen dengan konten padat seperti foto profil, linimasa pengalaman, dan kartu penghargaan rentan saling berhimpitan atau meluap keluar dari batas layar sehingga memicu horizontal scroll yang mengganggu kenyamanan visual. Dalam mengevaluasi elemen mana yang harus diubah atau diprioritaskan, saya menitikberatkan pada hierarki informasi dan keterbacaan. Informasi utama seperti nama, ringkasan profil, dan rincian pengalaman saya prioritaskan agar tetap menjadi fokus utama dengan ukuran teks yang jelas. Sebaliknya, elemen pendukung seperti dimensi foto profil serta jarak antarelemen saya perkecil agar ruang layar vertikal tidak terbuang sia-sia.
    Untuk implementasinya, saya menggunakan CSS media query untuk mengubah tata letak multi-kolom menjadi satu kolom vertikal. Proses evaluasi ini saya lakukan secara iteratif menggunakan fitur inspect pada developer tools dengan menguji berbagai ukuran layar, memastikan seluruh teks mengalir dengan rapi, proporsi visual seimbang, serta tautan navigasi tetap nyaman diakses.

3. Jawaban no 3: 
    Batasan utama yang saya rasakan adalah tampilan website masih terasa kaku karena minimnya interaktivitas, serta seluruh kontennya masih tertulis manual di dalam berkas HTML. Hal ini membuat proses pembaruan data portofolio menjadi tidak praktis karena saya harus terus-menerus mengedit kode HTML setiap kali ada pengalaman baru yang ingin ditambahkan.Pada iterasi berikutnya, fungsionalitas dinamis yang paling ingin saya tambahkan adalah menghubungkan halaman web dengan database agar pengisian dan pembaruan data dapat dilakukan secara terpusat tanpa perlu menyunting berkas HTML lagi. Selain itu, saya ingin menerapkan JavaScript untuk menambahkan interaktivitas serta animasi halus, seperti efek transisi antarhalaman, tampilan kartu yang interaktif, atau filter kategori, sehingga website terasa lebih hidup, responsif, dan menarik bagi pengunjung.

#### Dokumentasi Penggunaan AI

Dalam mengerjakan Tugas 1, saya menggunakan GitHub Copilot yang terpasang langsung di VS Code serta Gemini model Pro dan Flash sebagai alat bantu belajar dan menulis kode. Keduanya saya manfaatkan untuk kebutuhan yang berbeda, mulai dari pelengkapan otomatis hingga diskusi penataan kode. Untuk menggali solusi, saya mengajukan beberapa prompt spesifik, seperti:

1. “Dari designku ini, terdapat error saat aku ingin coba buat agar websitenya responsive. Coba cek dan berikan tanda pada bagian mana aku salah dan berikan saran.”

2. “Aku ingin menambahkan transisi saat dihover, namun kurang tau syntax dan penulisan dalam css. berikan aku code dan tuntun aku untuk memahaminya.”

3. “Coba cek hasil coding htmlku, terutama pada syntax yang aku gunakan. Apakah ada saran perbaikan seperti penggunaan syntax lain, terutama pada bagian Div.”

Dari prompt-prompt tersebut, AI membantu memberikan referensi sintaks transisi CSS, menunjukkan letak kesalahan pada tata letak responsif, serta menyarankan penggantian tag <div> yang berlebihan dengan tag semantik seperti <section>, <article>, dan <time>. Hal ini membuat struktur kode menjadi lebih bersih dan mudah dipahami tanpa mengubah konsep desain awal yang sudah saya tentukan.

Meski begitu, saya tidak langsung menerima saran yang diberikan begitu saja. Saya memilah dan menyesuaikan kodenya secara manual agar elemen yang dipakai tetap cocok dengan konten portofolio dan tidak merusak desain yang sudah saya buat. Seluruh informasi pada profil, pengalaman, dan penghargaan murni saya tulis sendiri dari data pribadi saya. Saya juga selalu menjalankan perintah python manage.py check secara mandiri untuk memastikan proyek saya tetap berjalan tanpa kendala.

Mengenai keterbatasan, yang saya temukan adalah AI sering kali tidak memahami konteks visual maupun struktur proyek secara utuh. Terkadang saran yang diberikan justru berpotensi merusak tampilan atau menyarankan berkas baru yang sebenarnya tidak dibutuhkan di website saya. Proses ini menyadarkan saya bahwa AI sangat berguna sebagai referensi awal dan pemberi saran, tetapi keputusan logika, penyesuaian desain, dan pengecekan akhir tetap sepenuhnya menjadi tanggung jawab saya.

## Harap dibaca 
Disini saya menggunakan tambahan framework JS, yaitu AOS
Konfirmasi  : Saya sudah menanyakan hal ini terhadap asdos di lab dan diperbolehkan untuk menggunakan AOS sebagai efek animasi