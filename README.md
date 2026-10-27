# 🪶 INT4 W4A8 for Forge Neo

<div align="center">

[![Forge Neo](https://img.shields.io/badge/Forge-Neo-blue)](https://github.com/Haoming02/sd-webui-forge-classic/tree/neo)
[![Gradio](https://img.shields.io/badge/Gradio-4.40.0-orange)](https://gradio.app/)
[![Version](https://img.shields.io/badge/Version-0.1.0-brightgreen)](https://github.com/eduardoabreu81/forge-neo-int4-w4a8)
[![License](https://img.shields.io/badge/License-AGPL--3.0-green.svg)](LICENSE)

> **Extension for [Stable Diffusion WebUI Forge - Neo](https://github.com/Haoming02/sd-webui-forge-classic/tree/neo)**

</div>

Cleaner pictures from the small **INT4 checkpoints** shared by the community - the ones made for 8 GB cards, for Krea 2, MOSS-Image and other models. Same file, same memory, no conversion: the extension just runs them with more precision.

> [!Important]
> This extension requires an up-to-date **Forge Neo** (the `neo` branch). If something goes wrong it says so in the console and the checkpoint runs the way the file asks - Forge Neo itself keeps working as usual.

---

## 📋 Table of Contents

- [What's New](#-whats-new)
- [Features](#-features)
- [Installation](#-installation)
- [Tips](#-tips)
- [Credits](#-credits)

---

## 🆕 What's New

### v0.1.0 - First Release

- **INT4 checkpoints look better** - INT4 ConvRot checkpoints run with 8-bit working numbers instead of 4-bit ones, for every model
- **One setting** under **Settings → Stable Diffusion** to go back to the way the file asks, applied at the next generation with no restart
- Takes over the INT4 setting that [MOSS-Image for Forge Neo](https://github.com/eduardoabreu81/moss-image-forge-neo) had in v0.1.5 and v0.1.6, now for Krea 2 and every other model too

---

## 🎯 Features

<p align="center"><img src=".github/images/krea2-w4a4-vs-w4a8.jpg" alt="The same Krea 2 picture from an INT4 checkpoint: as the file asks, the hand and cup come out wrong, with a stray straw; with the extension they come out right" width="900"></p>

### 🔢 What Changes

- Many INT4 checkpoints (the **INT4 ConvRot** ones) ask Forge Neo to squeeze both the model and its working numbers into 4 bits - only 15 levels for every number the model computes along the way
- That is what makes some of them look crunchy, over-sharpened, or a little off: hands, small objects and scenes that don't quite hold together
- With this extension the model stays in 4 bits, so the file and the memory are the same, but its working numbers use 8 bits
- It is a little slower: on an RTX 2070, an 896x1152 MOSS-Image picture at 8 steps took 15 s instead of 13 s

<p align="center"><img src=".github/images/moss-w4a4-vs-w4a8.jpg" alt="The same MOSS-Image picture from an INT4 checkpoint, as the file asks (left) and with the extension (right)" width="900"></p>

### 🎚️ The Setting

Under **Settings → Stable Diffusion → [INT4 W4A8] Activations of INT4 ConvRot checkpoints**:

| Choice | What it does |
| :--- | :--- |
| **INT8 (W4A8)** - default | 4-bit model, 8-bit working numbers: the cleaner picture |
| **As stored (W4A4)** | the way the file asks for, 4 bits for both |

The change applies at the next generation, with no restart and no reload of the checkpoint.

### 🧩 Which Checkpoints

- Any checkpoint quantized as **INT4 ConvRot** (`convrot_w4a4`), whatever the model: Krea 2, MOSS-Image and the others that ship such files
- The console says `[INT4 W4A8] INT4 checkpoint activations: INT8 (W4A8)` when it switches one
- Other checkpoints - INT8, FP8, NVFP4, GGUF, BF16 - are not affected
- Works on every card that already runs these INT4 files

### 🛡️ Safe by Design

- Changes no Forge Neo file - remove the extension and everything is as it was
- Never touches the checkpoint file: the switch happens in memory, on the model already loaded
- Only the INT4 ConvRot layers change; everything else runs exactly as Forge Neo runs it
- If the switch fails, the generation goes on the way the file asks

---

## 📦 Installation

1. Open Forge Neo WebUI
2. Go to **Extensions** → **Install from URL**
3. Paste: `https://github.com/eduardoabreu81/forge-neo-int4-w4a8`
4. Click **Install** and restart the WebUI

That's it: INT4 ConvRot checkpoints run with INT8 working numbers from the next generation on.

> [!Note]
> Tested on an RTX 2070 (8 GB), Forge Neo 2.31, with [Muse by Stable Yogi v4.0 INT4](https://civitai.com/models/2741166?modelVersionId=3416981) and [KREA 2 Turbo v10 INT4](https://civitai.com/models/2873257?modelVersionId=3368672) (Krea 2), and [Realism by Stable Yogi v1.0 INT4](https://civitai.com/models/3014108?modelVersionId=3421158) (MOSS-Image). Other models with INT4 ConvRot files have not been tested yet.

---

## 💡 Tips

- An INT4 file still loses some detail next to an INT8 one: if your card has room, the INT8 file of the same model gives the best picture
- Comparing the two choices? Keep the same seed and switch the setting between generations - no restart needed
- Using [MOSS-Image for Forge Neo](https://github.com/eduardoabreu81/moss-image-forge-neo) v0.1.5 or v0.1.6? Update it: the INT4 setting moved here, and the two would otherwise show the same option twice

---

## 📄 Credits

- **[Forge Neo](https://github.com/Haoming02/sd-webui-forge-classic/tree/neo)** by Haoming02
- **[comfy-kitchen](https://github.com/Comfy-Org/comfy-kitchen)** by Comfy-Org - the INT4 ConvRot format and both of its paths, W4A4 and W4A8

---

## 📜 License

AGPL-3.0 - see [LICENSE](LICENSE)

---

<div align="center">

Made with ❤️ for the Stable Diffusion community

**[Report Bug](https://github.com/eduardoabreu81/forge-neo-int4-w4a8/issues)** • **[Request Feature](https://github.com/eduardoabreu81/forge-neo-int4-w4a8/issues)** • **[☕ Ko-fi](https://ko-fi.com/eduardoabreu81)**

</div>
