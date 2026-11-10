![alt text](<screenshot/Screenshot 2026-11-10 105237.png>)
![alt text](<screenshot/Screenshot 2026-11-10 110928.png>)

1. Mengubah judul permainan
- Sebelumnya menggunakan judul Block Breaker.
- Diubah menjadi Peach Block Breaker agar sesuai dengan tema permainan yang baru.

2. Mengubah warna balok (Class Block)
- Sebelumnya balok memiliki warna putih dan hijau.
- Diubah menjadi warna pink dan putih menggunakan random.choice([PINK, WHITE]).
- Tujuannya agar balok memiliki tampilan yang lebih menarik dan sesuai dengan tema peach.

3. Mengubah bentuk bola (Class Ball)
- Sebelumnya bola hanya berbentuk lingkaran berwarna putih.
- Diubah menjadi bentuk buah peach menggunakan kombinasi beberapa lingkaran dan oval.
- Menggunakan pygame.draw.circle() untuk menggambar bagian buah dan pygame.draw.ellipse() untuk menggambar daun.

4. Mengubah warna striker (Class Striker)
- Sebelumnya striker menggunakan warna putih.
- Diubah menjadi warna pink muda (LIGHT_PINK).
- Ditambahkan border_radius=8 agar sudut striker terlihat membulat.

5. Memperbaiki posisi dan area tabrakan bola
- Menambahkan pembaruan posisi ballRect setiap kali bola bergerak.
- Tujuannya agar sistem pendeteksi tabrakan sesuai dengan posisi bola yang sebenarnya.

6. Memperbaiki sistem pantulan bola
- Menambahkan pengaturan posisi bola ketika menyentuh sisi kiri, kanan, dan atas layar.
- Tujuannya agar bola tidak keluar dari batas permainan ketika memantul.

7. Memperbaiki sistem tabrakan (Collision Check)
- Memperbaiki pengecekan tabrakan antara bola dengan striker maupun balok.
- Menambahkan break setelah bola mengenai balok agar satu benturan tidak langsung dihitung mengenai beberapa balok.

8. Memperbaiki sistem pengurangan nyawa
- Ketika bola jatuh melewati bagian bawah layar, jumlah nyawa pemain akan berkurang satu.
- Posisi bola kemudian dikembalikan ke posisi awal.

9. Memperbaiki tampilan Game Over
- Menambahkan tampilan tulisan GAME OVER - Press SPACE to Restart.
- Pemain dapat menekan tombol spasi untuk memulai permainan kembali atau menutup permainan.

10. Memperbaiki sistem restart permainan
- Ketika permainan dimulai ulang, skor dikembalikan menjadi 0 dan nyawa menjadi 3.
- Posisi bola dan striker dikembalikan ke posisi awal.
- Balok dibuat kembali seperti permainan baru.

11. Memperbaiki struktur dan indentasi kode
- Memperbaiki susunan spasi pada bagian while running dan if __name__ == "__main__":.
- Merapikan tanda kurung dan susunan perintah agar tidak menyebabkan syntax error atau indentation error.

12. Menambahkan komentar pada setiap bagian kode
- Menambahkan komentar menggunakan tanda # untuk menjelaskan fungsi setiap bagian program.
- Tujuannya agar kode lebih mudah dipahami dan memudahkan proses pembelajaran serta pengembangan program.