import source.py.feature.ast as ast


# https://github.com/subframe7536/maple-font/issues/348
def cv62_subst():
    return ast.subst_map(
        ["?", "questiondown", "??", "???", "?:", ":?", ":?>", "?.", ".?", "#?"],
        target_suffix=".cv62",
    )


cv62_name = "Alternative `?` with larger openings"
cv62_feat_regular = cv62_feat_italic = ast.CharacterVariant(
    id=62, desc=cv62_name, content=cv62_subst(), version="7.1", example="?"
)
