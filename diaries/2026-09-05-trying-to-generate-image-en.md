# Trying to Generate Images

## What I did

Today I tried generating images using DeepSeek V4 Flash Vision Exp. However, it turns out this model apparently isn't an _image generator_. It can read images, but it can't produce new ones.

Then, I went to Google AI Studio. There, I created an API key for the _free tier_. After I copied and pasted the API key into my code, it turned out this _tier_ has no quota at all for generating images using Gemini 3.5 Nano Banana.

## What I learned

- Yesterday's usage didn't even reach $3! Could $10 really last a whole month?? If so, that's an absolute steal.
- How do you even generate images with DeepSeek? Is the DeepSeek model really only for _coding_ and writing? Or do I need to use a different _model_? I wonder.
- In Antigravity I've tried extracting a scientific article from PDF to neatly formatted Markdown (separate images, well-_parsed_ tables) using `/teamwork-preview`, and my _usage_ quota got drained straight to 80%. I still don't know how to orchestrate multiple agents in OpenCode and how much _usage_ it would consume.

## Questions that came up

- What alternative models are there for generating images besides OpenAI or Google?
- How do you do multi-agent orchestration work in OpenCode like `/teamwork-preview` in Antigravity?
