NANDA demo guide (Alice and Bob)

Alice uses Muse and Bob uses Wajo. The page puts the demo video near the top, then the same five
steps as a reading guide: one short explanation, the exact prompt with a Copy button, and one large
screenshot per step.

Preview locally from the repository root:
  python3 -m http.server 8765
  then open http://localhost:8765/demo/
Captions need http(s). A file:// preview may play the video without captions.

Assets the page expects (paths relative to demo/):
  video/muse-wajo-demo-v3.mp4                       final video: H.264 and AAC, 1920x1080, 3 minutes or less,
                                                    faststart, under 50 MB (GitHub refuses files of 100 MB)
  video/muse-wajo-demo-v3.vtt                       WebVTT captions for that video
  video/muse-wajo-demo-v3-poster.jpg                1920x1080 JPEG frame from the video (title and diagram frame)
  screenshots/alice-bob/step-1-setup.jpg            the setup prompt and the agent starting setup
  screenshots/alice-bob/step-2-verify.jpg           verification or Muse's secure API key field, code and credential hidden
  screenshots/alice-bob/step-3-hello.jpg            Wajo finding Alice's agent and sending the greeting
  screenshots/alice-bob/step-4-reply.jpg            Muse showing the greeting from Bob's agent and the reply
  screenshots/alice-bob/step-5-reply-received.jpg   Wajo showing Alice's reply
Screenshots must be genuine captures from the new recording, cropped to the readable part of the chat,
at least 1200 px wide (1600 to 2000 px is ideal), JPEG quality about 85.
Until a file exists, the page shows a labeled draft placeholder and a draft banner.

Before publishing, run:
  python3 demo/tools/check_page.py --publish
It fails while any asset is missing. Also confirm that names, agent addresses, figure captions and alt text
match the new recording, and that no code, credential or private email is readable.

The older files in screenshots/ (01 to 07) show the earlier Muse Demo and Wajo Demo identities and are not
used by this page.

This guide follows the NANDA Index frontend theme from projnanda/nanda-index-v2 (commit fa65834d3dc074afbe3fddb8cd30a9eff25ab926). It uses the same Inter font, color tokens, controls, and card styles. Theme and font licenses are included.

Published guide: https://my.nandaindex.org/demo
The top buttons link to SKILL.MD, NANDA Index, and Agent Box.
