# AGT brand assets

These are the fonts and the logo that AGT web apps bundle (UI-3, UI-5, UI-14, UI-15). Apps copy them from this
directory at the tag of the spec version they follow, unmodified, to the `public/` paths those rules name
(`public/<file>` for the logo and the NMS fonts, `public/fonts/` for the flag font and its licence file).
`scripts/check_spec.py` checks that every file here matches its SHA-256 below.

| File | Used for | SHA-256 |
| --- | --- | --- |
| `AgtOfficialLogo.webp` | Favicon and header brand lockup (UI-5); required | `8bed1e5481a7ca2fc47728d67cebaa7a0e86412499b886d5755ed99bc9456674` |
| `fonts/NMSFuturaProBook_Kerned.ttf` | `NMS Futura`, the UI text font (UI-3); required | `08ad168f7fe58780fcb11c9369c9762ab83f30356fe4192ed60050a216a9798b` |
| `fonts/NMS-Glyphs-Mono-fixed2026.ttf` | `NMS Glyphs Mono`, portal glyphs (UI-14); required where portal codes are shown | `bd996c81bd0c4660adf10087335ab9fd1ce420c2036ed2346676c68e8ce387fc` |
| `fonts/TwemojiCountryFlags.woff2` | `Twemoji Country Flags` (UI-3); required where flags are shown | `9f04f14429bb6a9f415c7a4dd902a918d7e81a4f7526c415496fdb063954e3b8` |
| `fonts/nms-alphabet.ttf` | `NMS Alphabet`, the in-game Expedition alphabet; optional (UI-3) | `8a1ce0a2c079c5227e400d44fc27ee0cf73f33d1c15bfd16aacf1c7fdbbb58d0` |

## Sources and licences

| File | Credit (copyright / authors) | Source | Licence | What apps must do |
| --- | --- | --- | --- | --- |
| `AgtOfficialLogo.webp` | © Alliance of Galactic Travellers. All rights reserved | Alliance of Galactic Travellers | None granted. Use only in AGT apps | Do not modify it or use it outside AGT apps |
| `NMSFuturaProBook_Kerned.ttf` | Embedded: No Man's Sky Community Developers & Designers (NMSCD), designer Blend3rman; licence notice © 2020 Hector Javier Gonzalez Rivera. Original game typeface: Hello Games (No Man's Sky) | [NMSCD/No-Mans-Sky-Universal-Font](https://github.com/NMSCD/No-Mans-Sky-Universal-Font/blob/master/assets/font/NMSFuturaProBook_Kerned/Web-TT/NMSFuturaProBook_Kerned.ttf) | [SIL Open Font License 1.1](licenses/NMSFuturaProBook-OFL.txt) | Ship `licenses/NMSFuturaProBook-OFL.txt` with the font. Credit NMSCD, Blend3rman and Hello Games. Never sell the font on its own |
| `NMS-Glyphs-Mono-fixed2026.ttf` | Embedded: © 2017 Hello Games & Stephan van der Feest. Portal glyph designs: Hello Games (No Man's Sky) | [No Man's Sky Wiki: File:NMS-Glyphs-Mono.ttf](https://nms.miraheze.org/wiki/File:NMS-Glyphs-Mono.ttf) | [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/) | Credit Stephan van der Feest, Hello Games and the licence (README credits). Non-commercial use only. Do not modify it: a modified version would have to be marked as changed and shared under the same licence |
| `TwemojiCountryFlags.woff2` | Flag artwork: Twitter, Inc. and other contributors (Twemoji); font packaging: © 2022 TalkJS | [talkjs/country-flag-emoji-polyfill](https://github.com/talkjs/country-flag-emoji-polyfill) 0.1.10 | Artwork [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/), packaging MIT ([licence file](licenses/TwemojiCountryFlags-LICENSE.md)) | Ship `licenses/TwemojiCountryFlags-LICENSE.md` next to the font |
| `nms-alphabet.ttf` | Embedded: © 2022 seontonppa, built with FontStruct. Expedition alphabet designs: Hello Games (No Man's Sky) | [NMSCD/Expedition-Alphabet](https://github.com/NMSCD/Expedition-Alphabet/blob/main/public/assets/font/nms-alphabet.ttf) | [FontStruct licence](https://fontstruct.com/licenses/demo/9) | Follow the FontStruct licence linked here; credit seontonppa and Hello Games |

Apps credit the fonts in their README (DOC-1) with each font's name, everyone in its **Credit** column (for the
three No Man's Sky fonts that includes Hello Games, whose game the designs come from), its licence and its source
link, as in the table above.

## Provenance notes

- **Who wrote this table.** The maintainer supplied the sources and licences. The credits are each font's embedded
  authors plus Hello Games, the maker of No Man's Sky, whose typeface, portal glyphs and Expedition alphabet the
  three game fonts reproduce. The Futura licence text was read from its source repository. The Miraheze and
  FontStruct pages could not be opened when this table was written, so the CC BY-NC-SA 4.0 and FontStruct licence
  entries are as given by the maintainer, not checked against those pages.
- **NMS Futura** is described by NMSCD as datamined from No Man's Sky's game files and "based on the Futura Pro
  font family". The OFL covers NMSCD's kerned version; it cannot grant rights that the original font's owners did
  not.
- **NMS Glyphs Mono** is the wiki's original file, unmodified: the maintainer supplied the copy from the No Man's
  Sky Wiki, and it is byte-identical to `NMS-Glyphs-Mono-fixed2026.ttf` (same SHA-256). Despite its name, the
  `-fixed2026` file is not a changed version; the name is kept because UI-14 and existing apps use it.
- **Non-commercial use.** Because of NMS Glyphs Mono's licence, an AGT app that shows portal glyphs must not be
  used commercially.
