# DecScape

Modified: 2024-06-08

### Setup

You will need `python3`:

```bash
git clone https://github.com/ztnel/decscape
cd decscape
python3 -m pip install -r requirements.txt
```

Find an archetype on `mtgtop8` scoping by format key:

| Format | Key |
| --- | --- |
| Modern | MO |
| Standard | ST |
| Pioneer | PI |
| Legacy | LE |

For example to search all modern archetypes listed on `mtgtop8` :

```bash
python3 -m decscape -f MO -ga
[
    {
        "archetype_name": "Rakdos Aggro",
        "archetype_uri": "https://www.mtgtop8.com/archetype?a=918&meta=54&f=MO",
        "meta_share": 12.0,
        "id": "b2149a785f9f4fa195ba70efd1864130"
    },
    {
        "archetype_name": "4/5c Aggro",
        "archetype_uri": "https://www.mtgtop8.com/archetype?a=300&meta=54&f=MO",
        "meta_share": 9.0,
        "id": "b2149a785f9f4fa195ba70efd1864130"
    },
    ...
]
```

Run the scraper for an archetype by passing the name to `-a`:

```bash
python3 -m decscape -f MO -a 'Rakdos Aggro'
```

The tool will generate 4 plots for the requested sample size:

1. Aggregate main board card counts
2. Aggregate sideboard card counts
3. Normalized main board card counts
4. Normalized side board card counts

For example, the most recent 20 results from the page described in the title has the following distribution of sideboard copies:

![img](/docs/plt.png)

The raw data from the scrape is exported to a `json` file in `tmp` for further processing if needed.

