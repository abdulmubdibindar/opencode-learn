## Apa yang dilakukan

Hari ini saya menulis README.md dengan bahasa Inggris dibantu skill `terjemahan-inggris`. Fail percakapannya bisa dilihat di [[assets/perbaiki-bahasa-inggris-readme-dengan-penjelasan.json|sini]].

## Apa yang saya pelajari

Kita bisa melihat langsung parameter-parameter dari LLM itu sendiri di dalam OpenCode dan saya baru mulai mengakrabkan diri dengan istilah-istilah tersebut.

![[diaries/assets/Cuplikan layar 2026-09-04 035524.png]]

- Context limit
- Tokens
	- Input tokens
	- Output tokens
	- Cache tokens
	- Reasoning tokens

## Pertanyaan yang muncul

- Apakah OpenCode bisa plan mode?
	- Jawab (2026-09-04 berjam-jam berikutnya): Bisa! Hanya saja tidak seperti Antigravity atau Claude Code yang membuat artifact baru berupa dokumen terpisah dan bisa kita komentari bagian-bagiannya dan menjadi respon dari artifact tersebut, melainkan langsung ditulis di kotak _prompt_
	- Saya mencoba membandingkan antarmuka di Zed dengan OpenCode Desktop (OCD). Bagi saya, Zed lebih memuaskan karena memungkinkan formatting dengan sintaks Markdown, seperti otomatis mengenali `-[spasi]` sebagai _bulleted list_, `#` sebagai heading. Sementara itu di OCD belum seperti itu. Selain itu, kotak prompt Zed serasa seperti laman Markdown biasa. Terasa luas dan seperti bisa menuliskan apa saja. Asal tidak lupa memencet Shift + Enter untuk baris baru.