# Python for Data Science · course materials (modules 4–8)

**ESADE · Master in Business Analytics (MIBA) · Autumn 2026 · Alberto Cámara**

This repository is the course project for modules 4 to 8. It holds each session's notebooks and
slides, the course environment, and a script that downloads the data. You clone it once and
**pull** before every session.

All term we work with one real dataset, orders from **Olist**, a Brazilian marketplace, and
one question:

> *Do late deliveries hurt review scores, and where should operations act first?*

Every lab builds one piece of the answer. In Module 8 we put the pieces together.

---

## 1. Set up (once, about 15 minutes)

You need what you installed in modules 0–3: Anaconda or Miniconda with the `pds` environment,
VS Code with the Python and Jupyter extensions, and GitHub Desktop.

### 1.1 Clone this repository

In **GitHub Desktop**: *File → Clone repository → URL*, paste

```text
https://github.com/ber2/2026-esade-pds-course-materials
```

and choose where to put it on your computer (remember the folder). Then open that folder in
VS Code: *File → Open Folder…*.

### 1.2 Update the `pds` environment

Open a terminal **in the repository folder**. In VS Code: *Terminal → New Terminal*. On Windows,
if `conda` is not recognised there, use the *Anaconda Prompt* and `cd` into the folder.

```bash
conda activate pds
conda env update -f environment.yml --prune
```

This adds `nbformat` (so plotly charts show up in VS Code) and makes sure pandas stays on 2.x.

<details>
<summary>No <code>pds</code> environment, or it is broken?</summary>

Create it from scratch:

```bash
conda env remove -n pds
conda env create -f environment.yml
```

</details>

### 1.3 Download the data

Still in the same terminal, with `pds` active:

```bash
python scripts/download_data.py
```

It downloads about 29 MB, checks the file is complete, and puts eight CSV files into
`data/raw/`. Run it again any time: if the data is there, it does nothing.

### 1.4 Check everything

```bash
python scripts/check_setup.py
```

Every line should start with `[OK  ]`. A `[FAIL]` line says what to run. If you cannot fix it,
bring the output to class or send it to me before the session.

### 1.5 Pick the kernel in VS Code

Open any notebook, click **Select Kernel** (top right) → *Python Environments* → **pds**.

---

## 2. How the folders work

```text
2026-esade-pds-course-materials/
├── sessions/          ← material for each session. Read it, run it, never edit it.
│   └── m04/
│       ├── python-warmup.ipynb
│       ├── lab.ipynb
│       ├── slides.pdf
│       └── demo.ipynb       (follow-along before the session, full version after)
├── work/              ← YOUR copies. Git ignores this folder.
│   └── m04/
├── data/
│   ├── raw/           ← the Olist CSVs. Never edit, never write here.
│   ├── clean/         ← typed, checked tables your notebooks write (from Module 5)
│   └── mart/          ← tables ready to answer a question (from Module 5)
├── scripts/
│   ├── download_data.py
│   └── check_setup.py
└── environment.yml
```

### The one rule: work in `work/`, never in `sessions/`

Before you start a lab, **copy it** into `work/`, into a folder with the same session name:

- In VS Code's file explorer: right-click `sessions/m04/lab.ipynb` → *Copy*, then right-click
  `work/` → *New Folder…* `m04`, right-click it → *Paste*.

Why:

- **`git pull` always works.** Your edits live in `work/`, which git ignores, so there is
  nothing to conflict with when new sessions arrive.
- **The paths still work.** `work/m04/` sits at the same depth as `sessions/m04/`, so
  `../../data/raw/` points to the data from both.

If you edited something in `sessions/` by accident and GitHub Desktop refuses to pull: right-click
the changed file in GitHub Desktop → *Discard changes*. Copy your work into `work/` first if you
want to keep it.

---

## 3. Every week

1. **Before the session**: in GitHub Desktop, *Fetch origin* → *Pull origin*. Then copy the
   demo and the lab into `work/mNN/`.
2. **In the session**: follow the demo and do the lab in your copies in `work/mNN/`.
3. **After the session**: pull again. The full demo replaces the follow-along one, and from the
   next session on the lab solution is there too.

| Session | Date | Topic |
|---|---|---|
| `m04` | Wed 4 Nov | Recap, Python through data, intro to pandas |
| `m05` | Wed 11 Nov | Grain, group-by, joins |
| `m06` | Wed 18 Nov | Data visualisation with plotly |
| `m07` | Wed 25 Nov, 9:00–12:00 | Better charts, maps |
| `m08` | Wed 25 Nov, 14:00–17:00 | End-to-end case and exam preparation |

Checkpoints, the hackathon brief and submissions are on **Moodle**, not here.

---

## 4. Before Module 4

1. Set up (section 1).
2. Do `sessions/m04/python-warmup.ipynb`: copy it into `work/m04/` first. It checks itself and
   takes 30–45 minutes, or about 15 if you did the Data Science Pre-Program.

---

## 5. Licences

- Teaching material (notebooks, slides, this README): CC BY 4.0. See `LICENSE-content.md`.
- Code in `scripts/`: MIT. See `LICENSE`.
- Data: © Olist, CC BY-NC-SA 4.0, downloaded from this repository's releases, never committed.
  See `data/README.md`.

---

## For the lecturer

```bash
uv sync                                   # Python 3.12, pandas<3, plotly, jupyter, nbconvert
uv run python scripts/download_data.py
uv run python scripts/check_setup.py
cd sessions/m04 && uv run jupyter nbconvert --to notebook --execute --inplace <notebook>
```

`uv` and conda must resolve the same major versions of pandas and plotly. Data release: build
`release/olist-data.zip` (ignored by git) and attach it to the GitHub release `olist-v1`. Its
SHA-256 is pinned in `scripts/download_data.py`.
