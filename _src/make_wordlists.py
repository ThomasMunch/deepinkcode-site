"""Build _src/wordlist_data.json from the solver dictionaries in the MauiWFS8 repo.

Usage:  python3 _src/make_wordlists.py <path-to-MauiWFS8>
Reads TestServicesWFS8/WfDictionaries/Dictionary_*.txt (the full shipped word lists)
and the Wordfeud tile values in ServicesWFS8/StaticData/TileHelper_Wordfeud.cs.
Run again whenever the dictionaries change, then run build.py.
"""
import json, os, re, sys

# Site language -> (WfDictionary name, expensive letters to list)
LISTS = {
    "en": ("English_SOWPODS", ["Q", "Z", "X", "J"]),
    "da": ("Danish", ["Z", "X", "C"]),
    "nl": ("Dutch", ["Q", "X", "Y"]),
    "sv": ("Swedish_AllForms", ["Z", "X", "C"]),
    "no": ("Norwegian_Bok", ["C", "W", "Æ"]),
}
# Words left off the public pages even though the dictionary allows them (vulgar/slurs).
SKIP = {"JIZ", "LEZ"}

def tile_values(repo):
    src = open(os.path.join(repo, "ServicesWFS8/StaticData/TileHelper_Wordfeud.cs"), encoding="utf-8-sig").read()
    out = {}
    for m in re.finditer(r'\[WfDictionary\.(\w+)\]\s*=\s*new Dictionary<[^{]*\{(.*?)\n\s*\}', src, re.S):
        out[m.group(1)] = {k: int(p) for k, p, _ in
                           re.findall(r'\["(.)"\]\s*=\s*new TilePointsTotals\((\d+),\s*(\d+)\)', m.group(2))}
    return out

def main(repo):
    values = tile_values(repo)
    data = {}
    for lang, (dic, letters) in LISTS.items():
        path = os.path.join(repo, "TestServicesWFS8/WfDictionaries", f"Dictionary_{dic}.txt")
        short = sorted({w.strip().upper() for w in open(path, encoding="utf-8-sig")
                        if 2 <= len(w.strip()) <= 3} - SKIP)
        pts = values[dic]
        score = lambda w: sum(pts[c] for c in w)
        two = [[w, score(w)] for w in short if len(w) == 2]
        by_letter = []
        for L in letters:
            ws = sorted((w for w in short if L in w), key=lambda w: (-score(w), len(w), w))
            by_letter.append({"letter": L, "points": pts[L], "words": [[w, score(w)] for w in ws]})
        data[lang] = {"dictionary": dic, "two": two, "letters": by_letter}
        print(lang, dic, len(two), "two-letter,", {b["letter"]: len(b["words"]) for b in by_letter})
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "wordlist_data.json")
    json.dump(data, open(out, "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))

if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "../MauiWFS8")
