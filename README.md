About
---

CLI tool to analyse the different curricula of UFRJ's Astronomy undergraduate program.


Installation
---

1. Install `graphviz` on your system:
    - Archlinux: `pacman -S graphviz`
1. Clone this repo
1. Install the dependencies:
    - `pip install -r requirements.txt`



Usage
---

```bash
python main.py --csv  # generates csv files to ./output/
python main.py --graph  # generates pdf files to ./output/
```


Roadmap
---
- Add tests;
- Create interactive graph;
- Properly handle requirement equivalence;
- Create a web application.

