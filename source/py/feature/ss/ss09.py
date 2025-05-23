import source.py.feature.ast as ast


# https://github.com/subframe7536/maple-font/issues/352
def ss09_subst():
    return ast.subst_liga(
        "~=",  # Lua
        target=ast.gly("~=", ".ss09"),
        banner=[
            ast.ignore(ast.cls("~", "<", "="), "~", "="),
            ast.ignore(None, "~", ["=", ast.cls("~", "=", ">", "<", ":")]),
        ],
    )


ss09_name = "Asciitilde equal as not equal to ligature (`~=`)"
ss09_feat = ast.StylisticSet(
    id=9, desc=ss09_name, content=ss09_subst(), version="7.1", sample="~="
)
