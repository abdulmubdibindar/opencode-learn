# Mencoba Menghasilkan Gambar

## Apa yang Saya lakukan

Hari ini saya mencoba menghasilkan gambar menggunakan DeepSeek V4 Flash Vision Exp. Akan tetapi, ternyata model ini kelihatannya bukan model _image generator_. Ia bisa membaca gambar, tapi tidak memproduksi gambar baru.

Kemudian, saya pergi ke Google AI Studio. Di sana, saya membuat API key untuk _free tier_. Setelah saya salin-tempel API key ke dalam kode saya, ternyata _tier_ ini tidak memiliki kuota sama sekali untuk menghasilkan gambar menggunakan Gemini 3.5 Nano Banana.

## Apa yang Saya Pelajari

- Pemakaian kemarin tidak sampai $3! Apakah bisa bertahan selama satu bulan dengan $10 saja?? Kalau ya, ini sih gacor banget'
- Gimana ya menghasilkan gambar dengan DeepSeek? Apa model DeepSeek memang hanya untuk _coding_ dan tulisan? Atau harus pakai _mocin_ lain? Apa ya?
- Di Antigravity saya sudah pernah mencoba mengekstrak artikel ilmiah dari PDF ke Markdown yang terformat rapi (gambar terpisah, tabel ter-_parsing_ bagus) menggunakan `/teamwork-preview` dan kuota _usage_ saya langsung tersedot sampai 80%. Saya masih belum tahu bagaimana mengorkestrasi banyak agen di OpenCode dan berapa persen usage yang akan dihabiskan.

## Pertanyaan yang Muncul

- Apa model alternatif untuk menghasilkan gambar selain dari OpenAI atau Google?
- Bagaimana cara melakukan pekerjaan dengan orkestrasi multi-agent di OpenCode seperti `/teamwork-preview` di Antigravity?
