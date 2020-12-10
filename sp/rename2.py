import pathlib

cwd = pathlib.Path(__file__).parent.absolute()

# print(list(cwd.glob('*/*.dat')))
# print(list(cwd.glob('*/*.json')))

# for p in cwd.glob("*/*.json"):
#     p.rename(p.parent / (p.stem + "_220.json"))


# for p in cwd.glob("*/*.dat"):
#     p.rename(p.parent / (p.stem + "_220.dat"))


for extension in ["json", "yml", "dat"]:
    for src in cwd.glob(f"*/*.{extension}"):
        suffix = src.suffix
        name = src.stem
        dirpath = src.parent
        f = name.split("_")
        name2 = "_".join(f[:-1] + ["S" + f[-1]])
        dst = dirpath / str(name2 + suffix)
        print(dst)
        src.rename(dst)
