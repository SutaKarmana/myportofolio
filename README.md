## Identitas Mahasiswa : 
Name : I Nyoman Yadnya Suta Karmana

NPM : 2506615993

Class : PBP F

#### Pertanyaan Reflektif

1. Jawaban no 1:
    Ya, saya menggunakan beberapa elemen semantik HTML5 seperti `<header>`, `<nav>`, `<main>`, `<section>`, `<article>`, dan `<footer>`.Elemen `<section>` saya gunakan untuk memisahkan bagian-bagian utama halaman, yaitu profile, experience, dan awards. Sementara itu, elemen `<article>` saya terapkan pada setiap entri pengalaman dan penghargaan karena masing-masing memuat informasi yang berdiri sendiri secara utuh. Elemen-elemen ini membuat struktur kode HTML jauh lebih rapi dan mudah dibaca. Hal tersebut membantu saya memahami fungsi setiap bagian halaman dengan cepat, sehingga mempermudah saya ketika melanjutkan proyek ini ke depannya. Selain itu, struktur semantik juga meningkatkan aksesibilitas karena membantu browser maupun teknologi asistif  memahami hierarki konten dengan tepat. Untuk website statis, elemen semantik sangat berguna dalam mengorganisasi konten secara terstruktur meski belum melibatkan data dinamis dari database.

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

Dari prompt-prompt tersebut, AI membantu memberikan referensi sintaks transisi CSS, menunjukkan letak kesalahan pada tata letak responsif, serta menyarankan penggantian tag    `<div>` yang berlebihan dengan tag semantik seperti `<section>`, `<article>`, dan `<time>`. Hal ini membuat struktur kode menjadi lebih bersih dan mudah dipahami tanpa mengubah konsep desain awal yang sudah saya tentukan.

Meski begitu, saya tidak langsung menerima saran yang diberikan begitu saja. Saya memilah dan menyesuaikan kodenya secara manual agar elemen yang dipakai tetap cocok dengan konten portofolio dan tidak merusak desain yang sudah saya buat. Seluruh informasi pada profil, pengalaman, dan penghargaan murni saya tulis sendiri dari data pribadi saya. Saya juga selalu menjalankan perintah python manage.py check secara mandiri untuk memastikan proyek saya tetap berjalan tanpa kendala.

Mengenai keterbatasan, yang saya temukan adalah AI sering kali tidak memahami konteks visual maupun struktur proyek secara utuh. Terkadang saran yang diberikan justru berpotensi merusak tampilan atau menyarankan berkas baru yang sebenarnya tidak dibutuhkan di website saya. Proses ini menyadarkan saya bahwa AI sangat berguna sebagai referensi awal dan pemberi saran, tetapi keputusan logika, penyesuaian desain, dan pengecekan akhir tetap sepenuhnya menjadi tanggung jawab saya.

## Harap dibaca 
Disini saya menggunakan tambahan framework JS, yaitu AOS
Konfirmasi  : Saya sudah menanyakan hal ini terhadap asdos di lab dan diperbolehkan untuk menggunakan AOS sebagai efek animasi


### TUGAS 2

#### Pertanyaan Reflektif

1. **Jelaskan alur yang terjadi ketika pengguna membuka halaman portofolio baru.**

    Pada tugas ini, seluruh bagian portofolio yang ada di navbar, yaitu Education, Experience, dan Awards, sudah menggunakan model masing-masing. Namun, untuk menjelaskan alurnya, saya menggunakan halaman Education sebagai contoh. Ketika pengguna mengklik menu Education pada navbar, browser mengirimkan request ke URL `/education/`. Django kemudian menerima request tersebut melalui `portofolio/urls.py`, yang meneruskannya ke URL aplikasi `main` menggunakan `include("main.urls")`. Setelah itu, `main/urls.py` mencocokkan URL `/education/` dan mengarahkannya ke view `show_education`.

    Pada view `show_education`, seluruh data dari model `Education` diambil menggunakan `Education.objects.all()`. Data tersebut kemudian dimasukkan ke dalam context dengan nama `education_list` dan dikirim ke template `education.html` menggunakan fungsi `render`. Model `Education` pada `main/models.py` sendiri berfungsi sebagai penghubung antara aplikasi dengan tabel Education di database. Model ini menyimpan data seperti nama institusi, program studi, deskripsi, tahun mulai, tahun selesai, dan thumbnail. Dengan begitu, data pendidikan dapat disimpan di database dan tidak perlu ditulis langsung di dalam HTML.

    Setelah menerima context, template `education.html` menampilkan setiap data menggunakan perulangan `{% for education in education_list %}`. Setiap objek kemudian ditampilkan sebagai kartu pendidikan. Jika belum ada data Education di database, bagian `{% empty %}` akan menampilkan pesan bahwa belum ada riwayat pendidikan. Setelah template selesai diproses, Django mengirimkan hasil render berupa HTML ke browser sehingga halaman Education dapat ditampilkan kepada pengguna.

    Bagian lain seperti Profile, Experience, dan Awards juga dapat dibuka melalui navbar dan memiliki URL, view, model, serta template masing-masing. Alurnya pada dasarnya sama, tetapi Education saya gunakan sebagai contoh karena alurnya cukup jelas untuk menunjukkan bagaimana data portofolio diambil dari database dan ditampilkan secara dinamis.

2. **Mengapa data sebaiknya disimpan pada model dan tidak ditulis langsung di template?**

    Data sebaiknya disimpan pada model karena model terhubung dengan database dan membuat data lebih mudah dikelola. Dengan cara ini, Kalo saya ingin menambahkan penghargaan baru misalnya, saya cukup menambahkan datanya melalui database Django shell, atau halaman admin. Saya tidak perlu membuka dan mengubah kode HTML secara langsung. Jika data ditulis langsung di dalam template, setiap perubahan data akan membutuhkan perubahan pada kode HTML. Hal tersebut akan menyulitkan pemeliharaan, terutama jika jumlah penghargaan semakin banyak (AMINN), karena template juga akan menjadi lebih panjang dan sulit dibaca.

    Dengan menggunakan model, view, dan template, setiap bagian memiliki tugas masing-masing. Model digunakan untuk menyimpan data, view mengambil dan mengirimkan data, sedangkan template menampilkan data kepada pengguna. Pembagian ini membuat struktur aplikasi menjadi lebih rapi dan data dapat dikelola tanpa harus mengubah bagian tampilan secara langsung.

    Selain itu, penggunaan model juga memudahkan pengembangan aplikasi di kemudian hari. Misalnya, ketika ingin menambahkan fitur seperti edit, hapus, pencarian, atau filter penghargaan, data yang sudah tersimpan di database dapat digunakan kembali tanpa perlu mengubah struktur HTML secara keseluruhan.


3. **Apa perbedaan `makemigrations` dan `migrate` pada Django?**

    `makemigrations` digunakan untuk membuat file migration berdasarkan perubahan pada model. File migration berisi catatan tentang perubahan struktur database yang perlu dilakukan Django.

    Sementara itu, `migrate` digunakan untuk menjalankan file migration tersebut pada database. Jadi, `makemigrations` menyiapkan perintah perubahannya, sedangkan `migrate` menerapkan perubahan tersebut ke database.

    Contohnya, ketika saya menambahkan model `Education` dengan field `institusi`, `program`, `description`, `started_year`, `ended_year`, dan `thumbnail`, saya menjalankan:

    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

    Perintah pertama, `makemigrations`, akan membaca perubahan pada model `Education` dan membuat file migration yang berisi instruksi perubahan struktur database. Setelah itu, perintah `migrate` menjalankan file migration tersebut sehingga Django menerapkan perubahan ke database dan membuat tabel `main_education` beserta field yang sudah didefinisikan pada model `Education`.



## DOKUMENTASI AI Tugas 2

### AI Disclosure

Model yang digunakan : Github Copilot & Google Gemini (Flash & Advance level)

Dalam mengerjakan Tugas 2, saya menggunakan GitHub Copilot di VS Code dan Gemini model Flash 3.8. Pada awal pengerjaan, saya lebih sering menggunakan GitHub Copilot sambil menulis kode dan melakukan debugging. Copilot membantu saya membaca error di terminal, memahami command yang perlu dijalankan, serta mengecek hasil dari perintah seperti `makemigrations`, `migrate`, `check`, dan `test`. Biasanya saya langsung mencoba arahan tersebut di terminal. Kalau muncul error atau hasilnya belum sesuai, saya melihat outputnya dan melakukan perbaikan pada kode.

Setelah bagian awal mulai berjalan, saya menggunakan Gemini untuk memahami prosesnya dengan lebih terarah. Saya bertanya secara bertahap tentang perubahan dari data hard-code ke database, cara membuat model, menghubungkan URL, view, dan template, serta cara menjalankan migration. Saya juga meminta penjelasan yang lebih detail sambil mempelajari materi untuk mempersiapkan quiz.

Pada tahap berikutnya, Gemini saya gunakan untuk cross-check model, migration, URL, view, context, template, perulangan, kondisi kosong, dan unit test. Gemini juga membantu memberikan contoh command Django shell untuk menambahkan data ke database, termasuk cara mengisi path thumbnail gambar dan PDF. Saya mencocokkan saran tersebut dengan isi file proyek, hasil browser, dan output terminal sebelum melanjutkan ke langkah berikutnya.

### Alur Pengerjaan Tugas 2

Alur pengerjaan saya pada Tugas 2 adalah sebagai berikut:

1. Dengan bantuan AI agent sebagai pendamping, saya mempelajari kembali pola pada halaman Experience dan membaca checklist tugas untuk memahami bagian yang harus dibuat dinamis.
2. Saya menentukan field yang dibutuhkan, membuat atau menyesuaikan model, lalu menjalankan migration agar perubahan model masuk ke database.
3. Saya menghubungkan model dengan view, URL, dan template. Pada template, data ditampilkan menggunakan perulangan dan disiapkan juga tampilan ketika database masih kosong.
4. Saya mencoba mengisi data melalui Django shell atau terminal, termasuk data teks dan path thumbnail gambar atau PDF yang digunakan halaman portofolio.
5. Saya menambahkan unit test untuk URL/template, data yang tampil, dan kondisi kosong. Setelah itu, saya menjalankan pengecekan Django dan melihat hasilnya di browser.
6. Setelah alur dasarnya berjalan, saya menggunakan Gemini dan AI agent untuk membahas bagian yang masih membingungkan dan melakukan cross-check terhadap hasil implementasi.

### Contoh Prompt yang Saya Gunakan

Berikut beberapa contoh prompt yang saya gunakan selama percakapan tersebut. Percakapan lengkapnya dapat dilihat melalui link Gemini di bagian bawah:

1.

    > Aku sedang melanjutkan tugas 2. Sebelumnya aku sudah belajar model di tutorial 2, yaitu konsep mengganti hard-code pada website menjadi data yang disimpan di database Django. Sekarang ada arahan baru untuk tugas 2. Bantu aku menentukan langkah-langkah untuk melanjutkannya berdasarkan kode proyek dan instruksi tugas yang aku kirim.

2.

    > Berarti konsepnya sama seperti contoh pada Experience, kan? Bedanya, aku menambahkan field baru. Misalnya aku ingin membuat Education dengan thumbnail, deskripsi, dan field lainnya.

3.

    > Coba cek kodeku, apakah sudah aman? Berikan informasi kalau ada yang ngebug.

4.

    > Setelah ini aku harus melakukan apa? Dari tutorial 2 diminta mengganti URL dan bagian lain, tetapi masih bingung caranya. Tolong jelaskan langkah-langkahnya secara detail supaya aku memahami prosesnya dan bisa mempersiapkan quiz nanti.

Prompt tersebut saya gunakan sebagai percakapan lanjutan setelah mencoba langkah sebelumnya. Biasanya saya mencoba saran yang diberikan, lalu menyesuaikannya kalau belum cocok dengan struktur proyek saya. Setelah itu, saya mengecek kembali hasilnya dengan membaca kode, melihat halaman di browser, dan menjalankan:

```bash
python manage.py check
python manage.py showmigrations
python manage.py test
```

Perintah `check` digunakan untuk memeriksa konfigurasi Django, `showmigrations` untuk melihat status migration, dan `test` untuk menjalankan unit test aplikasi. Pada saat dokumentasi ini dibuat, seluruh test aplikasi menghasilkan `OK`.

### Link Percakapan Gemini

Berikut adalah link Share Chat Gemini yang saya gunakan sebagai dokumentasi proses belajar dan prompting:
(https://share.gemini.google/8qVCan7BICyR)

## Harap dibaca (Tugas 2)
Saya ga hanya membuat 1 model saja, tapi merekrontruksi section lain dengan konsep yang serupa, guna memperbagus tampilan web & membuat pengembangan di tahap selanjutnya jadi lebih mudah. 