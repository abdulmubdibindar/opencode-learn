# My First Work on OpenCode

## What I did

Today I wrote README.md in English with the help of the `terjemahan-inggris` skill. The conversation file can be seen [[assets/perbaiki-bahasa-inggris-readme-dengan-penjelasan.json|here]].

## What I learned

We can directly see the parameters of the LLM itself inside OpenCode, and I'm just starting to familiarize myself with those terms.

![[diaries/assets/Cuplikan layar 2026-09-04 035524.png]]

- Context limit
- Tokens
	- Input tokens
	- Output tokens
	- Cache tokens
	- Reasoning tokens

## Questions that came up

- Can OpenCode do plan mode?
	- Answer (2026-09-04, hours later): Yes! It's just not like Antigravity or Claude Code, which create a new artifact as a separate document whose parts you can comment on and which become a response from that artifact; instead, it's written directly in the _prompt_ box.
	- I tried comparing the interface in Zed with OpenCode Desktop (OCD). For me, Zed is more satisfying because it allows Markdown syntax formatting, like automatically recognizing `-[space]` as a _bulleted list_, and `#` as a heading. OCD doesn't do that yet. Besides, Zed's prompt box feels like a regular Markdown page. It feels spacious and like you can write anything, as long as you don't forget to press Shift + Enter for a new line.
