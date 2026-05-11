#!/usr/bin/env bash
# tree_to_readme.sh
# Runs `tree -L 3 --charset=C` and writes output to ~README.md,
# replacing each entry (file or directory) with an HTML anchor link,
# wrapped in <pre> so tree structure is preserved and links are clickable.
# Brought to you in part by, Mad Chillin Claude Vibez.
set -euo pipefail
OUTPUT="~README.md"
if ! command -v tree &>/dev/null; then
  echo "Error: 'tree' is not installed." >&2
  exit 1
fi

# ---------------------------------------------------------------------------
# render_tree ROOT_DIR HEADING LINK_PREFIX [EXTRA_TREE_FLAGS...]
#   ROOT_DIR          — directory to run `tree` on
#   HEADING           — markdown heading line (already formatted by caller)
#   LINK_PREFIX       — prepended to every relative path in anchor hrefs
#                       (use "." for the repo root, ".github" for the sub-tree)
#   EXTRA_TREE_FLAGS  — (optional) any additional flags forwarded to tree,
#                       e.g. -I ".github" to exclude a pattern
# ---------------------------------------------------------------------------
render_tree() {
  local root_dir="$1"
  local heading="$2"
  local link_prefix="$3"
  shift 3
  # Any remaining args are extra flags for tree (e.g. -I ".github")
  local -a extra_flags=("$@")

  local -a LINES
  IFS=$'\n' read -r -d '' -a LINES <<< "$(tree -L 3 -F --charset=C --noreport ${extra_flags[@]+"${extra_flags[@]}"} "$root_dir")"$'\0' || true

  local -a DIR_STACK
  DIR_STACK[0]="$root_dir"

  echo "# TREE ."
  echo ""
  echo "<env>"
  echo "<pre>"
  # First line is always the root dir label — emit as-is
  echo "${LINES[0]+"${LINES[0]}"}"

  for (( i=1; i<${#LINES[@]}; i++ )); do
    local line="${LINES[$i]}"

    # Skip any entry marked as private
    [[ "$line" == *🔒* ]] && continue

    # Isolate the prefix: everything before the first name character.
    local prefix="${line%%[^|\ \`\-]*}"
    local depth=$(( ${#prefix} / 4 ))

    # The raw entry is everything after the prefix (e.g. "file.txt" or "dir/")
    local raw="${line#"$prefix"}"

    # Strip any trailing tree -F classifier (/ * @ = | >)
    local name="${raw%%[/\*@=>|]}"

    # Rebuild the relative path from the directory stack
    local rel_path="$link_prefix"
    for (( d=1; d<depth; d++ )); do
      rel_path="$rel_path/${DIR_STACK[$d]}"
    done
    rel_path="$rel_path/$name"

    if [[ "$raw" == */ ]]; then
      # Directory — emit as an HTML anchor, then record in stack for children
      local html_link="<a href=\"$rel_path\">$name</a>"
      echo "${prefix}${html_link}/"
      DIR_STACK[$depth]="$name"
      for (( d=depth+1; d<${#DIR_STACK[@]}; d++ )); do
        unset "DIR_STACK[$d]"
      done
    else
      # File — emit as an HTML anchor
      local html_link="<a href=\"$rel_path\">$name</a>"
      echo "${prefix}${html_link}"
    fi
  done

  echo "</pre>"
  echo "</env>"
  echo ""
}

{
  # -------------------------------------------------------------------------
  # Part 1 — full working directory, .github excluded
  # -------------------------------------------------------------------------
  render_tree "." "" "." -I "_wpc_⧝/.gh"

  # -------------------------------------------------------------------------
  # Part 2 — .github sub-tree
  # -------------------------------------------------------------------------
  if [[ -d ".gh" ]]; then
    echo ""
    render_tree ".gh" "## .gh" ".gh"
  fi

} > "$OUTPUT"

echo "✓ Written to $OUTPUT"
