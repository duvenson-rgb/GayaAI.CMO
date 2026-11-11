# Visuals playbook

Every post in Buffer gets a visual. This playbook says how to make each kind, where to store it,
and how to get it into Buffer. CLAUDE.md still wins where the two disagree.

## The rule

A visual task is done only when the visual exists as a file and is in Buffer. A plan, a request
or an inventory is not a visual. Produce visuals from the first run of a task.

## Pick the type

Each idea's NOTES have a "Visual:" line with a type, a brief and a fallback. Follow it. If there is
no Visual line, make a Design that shows the post's main point.

| Type | You make it | How |
|---|---|---|
| Design (image, card, illustration) | Yes | gaya-design skill, rendered to PNG |
| Screenshot from a Fireflies call | Yes | Frame from the call recording |
| Video clip from a Fireflies call | Yes | Cut, captioned and cleaned from the call recording |
| Screenshot of staging or a demo account | No | Request + build the fallback Design |
| Photo of the author | No | Request + build the fallback Design |

Only the last two need a person. Everything else, you make.

## Design

1. Read the gaya-design skill first. Use its colors, Montserrat type, spacing and templates.
2. Build the visual as an HTML page at 1080x1350 (LinkedIn portrait) unless the brief says another
   size.
3. Use only words, numbers and quotes that are in the post itself. Never invent a quote, a name, a
   statistic or a URL. Customer quotes are attributed the way the post does (for example
   "Agency principal, Virginia"), never by name unless the notes say permission was given.
4. Render it to PNG with headless Chromium (Playwright), at 2x device scale, then check the image:
   no text cut off, nothing overlapping, readable on a phone.
5. Don't use Canva's AI generator for post visuals. It invents content.

## Screenshot from a Fireflies call

1. Get the call's recording with the Fireflies tools (the transcript's video or recording URL) and
   download it inside the run. If the call has no video, use the fallback from the brief.
2. Grab the frame at the second the brief gives: `ffmpeg -ss <seconds> -i call.mp4 -frames:v 1 frame.png`.
   Try a few frames around that second and keep the sharpest.
3. Crop to what the post is about. Cut out other people's video tiles, browser tabs and anything
   unrelated.
4. **Remove customer information.** Blur or crop out names, addresses, emails, phone numbers,
   policy or license numbers, dates of birth and any client data on screen. When in doubt, blur it.
5. Place the screenshot on a 1080x1350 Gaya frame (gaya-design) with a short caption from the post.

## Video clip from a Fireflies call

Use the short-form-video-edit skill if it is available, and these rules either way:

1. Download the recording and cut the clip at the brief's timestamps with ffmpeg. Keep it under
   60 seconds. Start on a strong line, end on a complete sentence.
2. Frame it for LinkedIn: 1080x1350 (4:5), cropped to the speaker. Crop out other participants'
   tiles unless the brief wants them.
3. **Captions:** transcribe the clip (faster-whisper) or use the Fireflies sentence timestamps,
   make an SRT, check every word against the audio, then burn them in: Montserrat, white with a
   dark outline or Gaya-orange highlight, lower third, at most 2 lines.
4. **Remove customer information.** Blur any on-screen names, addresses, licenses, client records
   and contact details for the whole time they are visible. Cut out spoken personal details
   (addresses, dates of birth, card or policy numbers) entirely. Follow every warning in the notes,
   such as "avoid 09:02–09:30".
5. Export MP4 (H.264, AAC), under 100 MB. Save the SRT next to it.
6. If the notes say the customer must give permission, still make the clip, but mark it
   **Needs consent – don't publish** in the table and in the file name.

## Storing the files

1. Upload every file to Google Drive, in the folder **Gaya – Buffer visuals**, inside a subfolder
   for the week (for example `2026-11-10`). Create them if they don't exist.
2. Name each file after the idea's title, lowercase with hyphens (for example
   `10b-the-rater-was-never-the-whole-job.png`).
3. Share each file as "anyone with the link can view". Only files in this folder.
4. The link Buffer needs is a direct file link, not the Drive preview page. Try
   `https://drive.google.com/uc?export=download&id=<FILE_ID>` first. If Buffer refuses it, try
   `https://lh3.googleusercontent.com/d/<FILE_ID>`. If both fail, stop and file a decision card:
   the visuals need public file storage.

## Getting it into Buffer

The Buffer connection can't attach media to an existing idea or move ideas between columns, and
ideas only take images. So for each idea:

1. Create a **new idea** with `create_idea`:
   - title: `🖼 ` + the original title
   - text: the original text exactly as it is (hooks and notes included), plus one last line:
     `VISUAL: <Drive link> (<type>)`
   - media: the image. For a video, attach a still frame from the clip as the image, and put the
     MP4's Drive link in the VISUAL line.
   - services: the same as the original
2. Never edit or delete the original idea. Duvenson moves the new copy into his Assigned column and
   archives the original.

## The table

Fill the task's table for every idea, with no "Todo" rows left behind: idea title, author, visual
type, Drive link, the new Buffer idea, what still needs a person, and flags (consent, anonymized,
fact check). Copy the consent and anonymization flags from the idea's notes.

## Before you end a run

- Count the visuals you finished in this run and write the number on the task.
- Open one of the new Buffer ideas and check the image loads.
- If something blocked you (a tool, a download, a permission), say exactly what and where on the
  task, and file a decision card if Duvenson has to act.
