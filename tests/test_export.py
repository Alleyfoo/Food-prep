"""Round 12 — Markdown export acceptance tests.

Asserts on the produced Markdown *string content* (the test_ui_handles.py
model), not on Streamlit internals. The export layer only serializes the
same computed dicts the UI/CLI use — these tests guard that contract:
every value in the Markdown must come from a query.* dict, never invented.
"""

from foodprep import export, query


# ---- 1. branch markdown includes every section from the branch_card dict ----

def test_branch_markdown_includes_all_sections(conn):
    md = export.branch_markdown(conn, "broccoli", "steam")
    assert md is not None
    # identity + product shape (from branch_card: ingredient/technique/component)
    assert "broccoli" in md
    assert "steam" in md
    assert "steamed_broccoli_component" in md
    # sections
    assert "## Tags" in md
    assert "## Risks" in md
    assert "## Missing roles" in md
    assert "## Uses" in md
    assert "## Next moves" in md
    assert "## Notes" in md  # footer
    # concrete values straight from the dict (tomato.yaml broccoli/steam)
    assert "tender_crisp" in md          # a tag value
    assert "sulfurous_if_overcooked" in md   # a risk
    assert "salt" in md                  # a missing role_name
    # every use the engine reports is rendered
    card = query.branch_card(conn, "broccoli", "steam")
    for use in card["uses"]:
        assert use in md


# ---- 2. branch markdown respects the available_items partition ----

def test_branch_markdown_respects_available_partition(conn):
    held = ["butter", "lemon", "sea_salt", "parmesan"]  # the steam Cook fillers
    md = export.branch_markdown(conn, "broccoli", "steam", held)
    # the partition replaces the plain Next-moves section
    assert "## Available now" in md
    assert "## Next moves" not in md
    assert "butter" in md
    # carb has no curated steam filler -> surfaces under Missing but useful
    assert "## Missing but useful" in md
    assert "carb" in md

    # with no available_items, the plain Try view renders (no partition headers)
    plain = export.branch_markdown(conn, "broccoli", "steam", None)
    assert "## Available now" not in plain
    assert "## Next moves" in plain


# ---- 3. component markdown resolves roasted_tomato_component ----

def test_component_markdown_resolves_roasted_tomato_component(conn):
    md = export.component_markdown(conn, "roasted_tomato_component")
    assert md is not None
    assert "roasted_tomato_component" in md
    # produced_by: tomato + roast (from the first producing transformation)
    assert "tomato" in md
    assert "roast" in md
    assert "came from:" in md
    assert "## Notes" in md


# ---- 4. plate markdown includes the core sections + risks/avoid ----

def test_plate_markdown_includes_core_sections(conn):
    # potato_gratin (h5) + hard_cheese (h4): leans heavy, carb flagged, all gaps.
    md = export.plate_markdown(conn, "potato_gratin and hard_cheese")
    assert "## Plate items" in md
    assert "## Already provides" in md
    assert "## Missing — hard gaps" in md
    assert "## May want more" in md     # flagged_more = carb (provided but flagged)
    assert "## Risks" in md             # leans heavy
    assert "## Avoid adding more of" in md
    assert "## Suggested next move" in md
    assert "## Notes" in md
    # real role values from the dict, not the brief's illustrative names
    assert "salt" in md
    assert "acid" in md
    assert "crunch" in md
    assert "carb" in md
    assert "leans heavy" in md


# ---- 5. plate markdown reports unknown available items honestly ----

def test_plate_markdown_reports_unknown_available_items(conn):
    md = export.plate_markdown(conn, "mashed_potatoes and chickpea_patty",
                               ["xyz_not_an_ingredient"])
    assert "## No match from selected items" in md
    assert "xyz_not_an_ingredient" in md   # reported, not silently dropped


# ---- 6. scout markdown includes the taste-first disclaimer ----

def test_scout_markdown_includes_disclaimer(conn):
    md = export.scout_markdown(conn)
    assert "Taste a small amount before serving." in md
    assert "Scout mode" in md


# ---- 7. cook markdown does not include scout-only (experimental) pairings ----

def test_cook_markdown_excludes_scout_only_pairings(conn):
    # lingonberry_vinegar is an experimental acid (Scout only).
    branch_md = export.branch_markdown(conn, "broccoli", "steam")
    plate_md = export.plate_markdown(conn, "mashed_potatoes and chickpea_patty")
    assert "lingonberry_vinegar" not in branch_md
    assert "lingonberry_vinegar" not in plate_md
    # but it DOES appear in the Scout export (sanity: the name is real)
    scout_md = export.scout_markdown(conn)
    assert "lingonberry_vinegar" in scout_md


# ---- 8. empty available_items matches the current unfiltered behaviour ----

def test_empty_available_matches_unfiltered(conn):
    plate_text = "mashed_potatoes and chickpea_patty"
    assert (export.plate_markdown(conn, plate_text, [])
            == export.plate_markdown(conn, plate_text, None))
    assert (export.branch_markdown(conn, "broccoli", "steam", [])
            == export.branch_markdown(conn, "broccoli", "steam", None))