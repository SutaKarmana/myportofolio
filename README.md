## Identitas Mahasiswa : 
Name : I Nyoman Yadnya Suta Karmana

NPM : 2506615993

Class : PBP F

## Deskripsi Proyek (New)

Proyek ini merupakan website portofolio pribadi yang dibuat menggunakan Django. Website menampilkan informasi profile, education, experience, awards, dan projects. Data pada beberapa bagian portofolio disimpan di database melalui model Django, kemudian diambil oleh view dan ditampilkan pada template. Pada bagian Education, Experience, dan Awards, pengguna dapat menambahkan, mengubah, dan menghapus data melalui form. Proyek ini juga menyediakan endpoint JSON untuk data Experience dan Project.

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

    Bagian lain seperti Profile, Experience, dan Awards juga dapat dibuka melalui navbar dan memiliki URL, view, model, serta template masing-masing. Alurnya pada dasarnya sama, tetapi Education saya gunakan sebagai contoh karena alurnya cukup jelas untuk menunjukkan bagaimana data portofolio diambil dari database dan ditampilkan secara dinamis. Pada perkembangan terbaru, Education dan Awards juga sudah memiliki tombol tambah, edit, dan hapus yang terhubung ke form masing-masing.

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

### TUGAS 3

#### Pertanyaan Reflektif

1. Jawaban no 1:

    `ModelForm` digunakan karena dapat menghubungkan form secara langsung dengan model Django. Pada proyek ini, saya menggunakan `ExperienceForm`, `EducationForm`, dan `AwardForm` berdasarkan model masing-masing. Field seperti judul, deskripsi, institusi, tahun, thumbnail, dan link sertifikat dapat dibuat dari struktur model yang sudah ada. Dengan cara ini, saya tidak perlu menulis ulang seluruh field HTML secara manual dan dapat mengurangi kemungkinan perbedaan antara form dengan model yang ada di database.

    Selain membuat field secara otomatis, `ModelForm` juga membantu proses validasi data. Contohnya, field `thumbnail` dan `certificate_url` yang berasal dari `URLField` akan diperiksa sebagai URL, sedangkan field tahun akan diperiksa sebagai angka. Setelah data valid, saya dapat menggunakan `form.save()` untuk menyimpan data ke database. Pada bagian upload thumbnail Experience, saya menggunakan `form.save(commit=False)` terlebih dahulu agar file dapat diproses sebelum objek Experience disimpan.

    Sementara itu, `{% csrf_token %}` digunakan untuk melindungi form dari serangan Cross-Site Request Forgery atau CSRF. Serangan ini dapat terjadi ketika pengguna yang sedang login secara tidak sadar mengirimkan request dari situs lain ke aplikasi. Token CSRF memastikan bahwa request POST benar-benar berasal dari form yang dibuat oleh aplikasi Django. Jika token tersebut tidak ditambahkan, Django biasanya akan menolak request POST karena dianggap tidak aman.

2. Jawaban no 2:

    JSON lebih sering digunakan dalam pengembangan aplikasi web modern karena sintaksnya lebih ringkas dan lebih mudah dibaca. Struktur JSON juga mirip dengan object dan array pada JavaScript, sehingga data dapat langsung digunakan oleh JavaScript pada sisi client tanpa proses yang terlalu panjang. Hal ini membuat JSON cocok digunakan untuk komunikasi antara frontend dan backend melalui API.

    Dibandingkan XML, JSON biasanya membutuhkan lebih sedikit karakter karena tidak menggunakan tag pembuka dan tag penutup untuk setiap data. Ukuran data yang lebih kecil dapat membantu mengurangi penggunaan bandwidth dan membuat proses pertukaran data menjadi lebih efisien. JSON juga didukung oleh banyak bahasa pemrograman dan framework web, termasuk Django, sehingga lebih praktis untuk digunakan.

    XML tetap memiliki kelebihan, terutama untuk dokumen yang membutuhkan struktur sangat kompleks, atribut, atau validasi skema yang ketat. Namun, untuk kebutuhan API dan pertukaran data pada aplikasi portofolio ini, JSON lebih sederhana, ringan, dan sesuai dengan kebutuhan.

3. Jawaban no 3:

    Pada proyek ini, alur pengembalian data Experience dalam format JSON dimulai ketika pengguna atau client mengakses URL API `/api/experience/`. URL tersebut diarahkan oleh `main/urls.py` ke fungsi `get_experience_json` pada `main/views.py`. View tersebut mengambil seluruh data Experience dari database menggunakan `Experience.objects.all()`.

    Data yang diperoleh dari query tersebut masih berupa object atau QuerySet Django, bukan data JSON biasa. Oleh karena itu, data tersebut diproses menggunakan `serializers.serialize("json", experiences)`. Hasil proses ini kemudian dikembalikan menggunakan `HttpResponse` dengan `content_type="application/json"`. Dengan content type tersebut, client dapat mengetahui bahwa response yang diterima memiliki format JSON.

    Serialization diperlukan karena object model Django tidak dapat langsung dikirim sebagai response JSON. Object tersebut masih memiliki struktur dan perilaku khusus dari Django, sedangkan JSON hanya mengenal tipe data sederhana seperti object, array, string, angka, boolean, dan null. Serialization mengubah data model menjadi representasi JSON yang berisi informasi model, primary key, dan field-field yang dimiliki objek. Dengan begitu, data dapat dikirim melalui HTTP dan digunakan oleh aplikasi lain atau diproses kembali oleh Django.


## DOKUMENTASI AI Tugas 3

### AI Disclosure

Dalam mengerjakan Tugas 3, saya menggunakan GitHub Copilot yang terpasang di VS Code dan Google Gemini sebagai alat bantu belajar. Saya menggunakan kedua tools tersebut dengan peran yang berbeda. GitHub Copilot lebih banyak saya gunakan untuk membaca struktur proyek, membantu melakukan debugging, dan mengarahkan langkah perbaikan pada kode. Sementara itu, Gemini saya gunakan untuk memahami konsep `ModelForm`, keamanan `{% csrf_token %}`, format JSON, XML, dan proses serialization pada Django. Saya juga meminta bantuan AI untuk memperbaiki gaya bahasa dokumentasi agar lebih rapi dan mudah dipahami, tetapi isi dan keputusan akhirnya tetap saya sesuaikan sendiri.

### Alur Pengerjaan Tugas 3

Alur pengerjaan saya pada Tugas 3 adalah sebagai berikut:

1. Saya membaca kembali materi Tutorial 03 mengenai penggunaan form, pengiriman data melalui request, format JSON dan XML, serta serialization pada Django.
2. Saya memeriksa struktur proyek yang sudah dibuat pada tugas sebelumnya, terutama `main/forms.py`, `main/views.py`, `main/urls.py`, `main/models.py`, serta template Experience, Education, dan Awards.
3. Saya menggunakan GitHub Copilot di VS Code untuk membantu menemukan bagian yang perlu diperiksa ketika menambahkan fitur form. Copilot membantu saya memahami hubungan antara `ModelForm`, `request.POST`, `request.FILES`, `multipart/form-data`, dan proses penyimpanan thumbnail Experience, serta pola CRUD untuk Education dan Awards.
4. Ketika menemukan bagian yang masih membingungkan, saya menggunakan Gemini untuk meminta penjelasan konsep dengan bahasa yang lebih mudah dipahami. Gemini membantu menjelaskan alasan penggunaan `ModelForm`, fungsi token CSRF, kelebihan JSON dibandingkan XML, dan alasan data model harus melalui proses serialization.
5. Saya menyesuaikan saran AI dengan struktur proyek saya. Saya mempertahankan penggunaan `ExperienceForm`, menambahkan `EducationForm` dan `AwardForm`, serta memproses file Experience di view sebelum URL file disimpan pada field `thumbnail`.
6. Setelah melakukan perubahan, saya memeriksa halaman form dan tombol CRUD melalui browser. Saya juga menjalankan `python manage.py check` serta `python manage.py test` untuk memastikan aplikasi tetap berjalan.

Selain membantu kode, saya juga meminta AI untuk merapikan gaya bahasa pada dokumentasi agar penjelasannya lebih singkat, santai, dan tetap sesuai dengan proses pengerjaan saya.

### Penggunaan GitHub Copilot

GitHub Copilot saya gunakan terutama sebagai pendamping debugging di VS Code. Saya meminta Copilot membaca file yang berkaitan sebelum memberikan perubahan, kemudian saya mencoba saran tersebut satu per satu. Bagian yang dibantu Copilot antara lain:

- memeriksa apakah `ExperienceForm` sudah memiliki `FileField` untuk menerima gambar;
- memeriksa apakah view sudah meneruskan `request.FILES` ketika membuat atau memperbarui Experience;
- memeriksa penggunaan `enctype="multipart/form-data"` pada template form;
- membantu mencari penyebab tampilan pilihan Link dan Upload tidak tersusun dengan baik;
- membantu menelusuri alur penyimpanan file ke `static/img` dan penyimpanan alamat file ke model;
- membantu membuat `EducationForm` dan `AwardForm` berdasarkan field pada model masing-masing;
- membantu menghubungkan tombol tambah, edit, dan hapus Education serta Awards ke URL dan view yang sesuai;
- membantu memeriksa error dan memastikan perubahan tidak merusak fitur Experience yang sudah ada.

Contoh langkah debugging yang saya lakukan bersama Copilot adalah ketika saya menyadari bahwa file upload tidak cukup ditangani hanya dengan `request.POST`. Dari pemeriksaan tersebut, saya memahami bahwa data teks dikirim melalui `request.POST`, sedangkan file dikirim melalui `request.FILES`. Saya kemudian memastikan pemanggilan form menggunakan:

```python
form = ExperienceForm(request.POST or None, request.FILES or None)
```

Saya juga memastikan template menggunakan:

```html
<form method="post" enctype="multipart/form-data">
```

### Penggunaan Gemini untuk Memahami Konsep

Gemini saya gunakan untuk memahami konsep, bukan hanya untuk menyalin kode. Beberapa hal yang saya tanyakan adalah sebagai berikut:

1. Mengapa `ModelForm` lebih praktis dan bagaimana Django memvalidasi datanya berdasarkan model.
2. Mengapa `{% csrf_token %}` diperlukan pada form POST untuk mencegah serangan CSRF.
3. Mengapa JSON lebih sering dipakai daripada XML dalam API modern.
4. Bagaimana alur endpoint `/api/experience/` dari URL sampai mengembalikan data JSON.
5. Mengapa object atau QuerySet Django perlu diubah menjadi JSON sebelum dikirim melalui HTTP.

Setelah mendapatkan penjelasan dari Gemini, saya mencocokkannya dengan kode proyek. Contohnya, penjelasan tentang serialization saya cocokkan dengan fungsi `get_experience_json` pada `main/views.py`, yaitu ketika data `Experience.objects.all()` diproses menggunakan `serializers.serialize("json", experiences)` sebelum dikembalikan melalui `HttpResponse`.

### Contoh Prompt yang Saya Gunakan

Berikut beberapa contoh prompt yang saya gunakan selama mengerjakan Tugas 3:

1.
    > Coba cek alur form Experience saya. Saya ingin menerima upload gambar, tetapi database saya masih menggunakan URLField. Jelaskan bagian mana yang harus ditambahkan dan bagaimana alurnya tanpa menambahkan library yang tidak diperlukan.

2.
    > Aku sempat bingung pada bagian add formnya, karena mengakses Json . Cara ceknya gimana?

3.
    > Jelaskan fungsi csrf_token pada form Django dan apa yang terjadi jika token tersebut tidak digunakan.

4.
    > Jelaskan alur get_experience_json dari URL, view, QuerySet, serialization, sampai menjadi HttpResponse JSON.

5.
    > Coba cek apakah dokumentasi README saya sudah memenuhi rubrik dokumentasi AI. Bagian mana yang perlu ditambahkan agar tools yang digunakan, bagian yang dibantu, dan proses verifikasinya terlihat jelas?
6.
    > Coba cek lagi pengerjaan saya, saya takut ada corner case yang membuat error

### Verifikasi Hasil

Saya tidak langsung menerima semua saran dari AI. Setiap perubahan saya periksa kembali dengan membaca file yang terkait, mencoba form Experience, Education, dan Awards melalui browser, menguji tombol tambah, edit, dan hapus, lalu menjalankan beberapa perintah berikut:

```bash
python manage.py check
python manage.py test
python manage.py showmigrations
```

Perintah `check` digunakan untuk memeriksa konfigurasi proyek, `test` digunakan untuk memastikan fungsi yang sudah ada tetap berjalan, sedangkan `showmigrations` digunakan untuk memeriksa status migration. Saya juga mencoba memilih sumber thumbnail Link dan Upload melalui browser, memeriksa pesan validasi ketika file belum dipilih, serta memastikan data Experience tetap dapat ditampilkan setelah disimpan.

Pada saat dokumentasi ini dibuat, `python manage.py check` tidak menemukan masalah dan seluruh 18 test Django berhasil dijalankan. Test tersebut mencakup model, halaman, validasi form, endpoint JSON, serta alur CRUD Education dan Awards. Hasil tersebut saya gunakan sebagai pembanding terhadap saran AI, sehingga keputusan akhir tidak hanya berdasarkan jawaban AI tetapi juga berdasarkan hasil pengujian langsung.

### Refleksi Penggunaan AI

Penggunaan Copilot membantu saya mempercepat proses membaca kode dan menemukan hubungan antarfile dalam proyek Django. Copilot juga membantu menunjukkan bagian yang perlu diperiksa ketika sebuah fitur belum berjalan. Gemini membantu saya memahami alasan di balik penggunaan kode tersebut, terutama konsep `ModelForm`, CSRF, JSON, dan serialization. Dengan membagi penggunaan keduanya, saya tidak hanya mendapatkan solusi, tetapi juga lebih memahami alur kerja Django.

Namun, AI tidak selalu memahami kondisi proyek secara lengkap. Beberapa saran perlu saya sesuaikan karena model `Experience` saya masih menyimpan thumbnail sebagai `URLField`, bukan `ImageField`. Saya juga menemukan bahwa perubahan tampilan form dapat terlihat berbeda karena dipengaruhi CSS yang sudah ada. Oleh karena itu, saya tetap memeriksa struktur file, mencoba hasilnya di browser, dan menjalankan test secara mandiri. Keputusan akhir, penyesuaian desain, dan pengecekan kebenaran implementasi tetap saya lakukan sendiri.

### Link Percakapan Gemini Tugas 3

Percakapan Gemini yang saya gunakan untuk memahami konsep dan melakukan cross-check akan saya sertakan pada bagian ini:

`https://share.gemini.google/tGohVOMAYoNV`

## Harap dibaca (Tugas 3)
Dikarenakan saya sudah terlanjur mengerjakannya sambilan tutorial kemarin.. ternyata ga sadar kalau refaktor semuanya itu ada di bagian Tugas 03. Jadi untuk memperlihatkan bahwa saya sudah mengerjakan progresnnya saja tandai dengan memberikan commentar. Lalu saya merefaktor semua bagian dengan tambahan button mengarah ke form masing masing. Jadi ga hanya 1 , tetapi juga ada education ,experience, dan awards.