# EnglishReviewer: Coding Agent Context

## Project purpose

EnglishReviewer is a small, early-stage desktop application for reviewing English vocabulary and phrases. The UI and README are primarily Chinese. The implemented workflow is a three-choice text quiz: the app hides configured phrases in an English context, offers three possible meanings/answers, records correct or incorrect attempts, and can reorder questions by a calculated review priority. Users can create vocabulary books with metadata and switch among vocabulary JSON files.

The README says image-, audio-, and video-based review and database storage are future goals. At present, media paths are only data fields, and all persistent data is stored in `data/ko.json`.

## Technology and execution model

- Language: Python.
- GUI: PyQt5 widgets.
- Persistence: a local JSON file.
- Entry point: `main.py`.
- There is no dependency manifest, packaging metadata, build system, CI configuration, or database.
- Run from the repository root because data paths are hard-coded relative paths:

  ```sh
  python3 main.py
  ```

- Required runtime dependency: `PyQt5` (not declared in the repository).
- The current environment's `python3` is 3.9.6 and does not have PyQt5 installed.

## Repository map

```text
.
├── main.py                 # Application entry point and nearly all GUI/controller behavior
├── README.md               # Short Chinese project description and basic run instructions
├── data/
│   └── ko.json             # Persistent knowledge-object/review data
├── src/
│   ├── __init__.py
│   ├── knowledgeObject.py  # Domain objects and review-priority calculation
│   ├── loadAndSave.py      # Knowledge-object JSON saving
│   ├── vocabularyFile.py   # Vocabulary validation, creation, and metadata sidecars
│   └── sort.py             # Design comment only; no executable implementation
└── test/
    ├── test.py             # Standalone PyQt tab demo; not an automated project test
    └── test_delete.py      # unittest for deleting the current item
```

Generated `__pycache__` directories are currently untracked and should not be treated as source.

## Architecture

This is a monolithic, widget-driven application rather than a layered MVC application. `main.py` imports the domain and persistence modules with wildcard imports.

### Domain model: `src/knowledgeObject.py`

`knowledgeObject` wraps one record in a mutable `body` dictionary. Its constructor creates default fields and then overlays keys supplied in `body`. Its methods are:

- `UpdatePS(mode)`: recalculates the scalar priority score `PS`.
- `UpdateLS()`: attempts to update a last-review timestamp.
- `UpdateRT(count)`: increments a review count.
- `UpdateCS(count)`: increments a correct count.
- `ToString()`: JSON-serializes `body`.

`knowledgeObjectList` holds the active objects, current review mode, and sorting logic:

- `objectList`: list of `knowledgeObject` instances.
- `mode`: active review-mode index; currently defaults to `0`.
- `sortList(reverse=True)`: recalculates every object's `PS`, then sorts descending by default.
- `PrintList()`: prints all records.

Important implementation detail: `knowledgeObjectList.objectList`, `tags`, and `mode` are class attributes, not initialized per instance. Multiple list instances in one process therefore share state unless this is refactored.

### Persistence: `src/loadAndSave.py`

- `LoadFile(fileName)` returns the raw list decoded from JSON.
- `SaveFile(fileName, data)` extracts `.body` from each domain object and overwrites the target JSON file.

There is no schema validation, migration, atomic write, backup, error handling, explicit encoding, or formatting configuration. Saving uses the standard `json.dump` defaults and rewrites the full dataset.

### UI/controller: `main.py`

`Example(QWidget)` is the application root. On initialization it:

1. Creates a `knowledgeObjectList`.
2. loads `data/ko.json` using an absolute project-relative path;
3. wraps each dictionary in a `knowledgeObject`;
4. builds the UI;
5. sets the current index to zero;
6. priority-sorts all objects;
7. displays the first question;
8. registers `Ctrl+D` for next and `Ctrl+A` for previous.

The first tab is assembled by `DefaultPanel` from row-oriented helper classes:

- `Row2`: mode buttons (`选择`, `听写`, `朗读`) and explicit save button. Only save is connected; mode switching is not implemented.
- `Row3`: masked context, CT/RT labels, delete, and edit controls.
- `Row4`: three answer buttons and answer-result handling.
- `Row5`: explanation display.
- `Row6`: priority re-sort, shuffle, previous/next navigation, and progress.

`AddOrEdit` implements the third tab, with fields for all user-editable record values and separate “save new” and “save changes” actions.

Above the tabs, `新增单词本` opens a metadata/create dialog and `选择单词表` opens an existing vocabulary JSON file. The current title, filename, and entry count are displayed next to the controls.

Four tabs are declared:

1. `默认模式` (default/review): implemented.
2. `Tag筛选` (tag filter): placeholder with no layout or behavior.
3. `新增/编辑` (add/edit): implemented.
4. `搜索` (search): placeholder with no layout or behavior.

## Main review flow

`Example.GoToPageX(pageNumber)` accepts a one-based page number, converts it to the zero-based `reviewIndex`, resets `correctNumber`, and calls `refreshDefaultTab()`.

`refreshDefaultTab()`:

1. Reads the current object's `context`, `HL`, `RT`, and `CT`.
2. Replaces every exact substring in `HL` with `___` in the displayed context.
3. Displays CT and RT for `kol.mode`.
4. Builds three answer choices using the current object and pseudo-random indexes from the full object list.
5. Sorts the selected indexes in descending numeric order and derives the correct button position from that order.
6. Uses each selected object's comma-joined `HL` list as button text.
7. Resets answer button enabled/style state and clears the explanation.
8. Updates progress and previous/next button availability.

Clicking an answer:

- reveals the current object's `contextExplanation`;
- colors only the clicked button green when correct or red when incorrect;
- increments `CT[mode]` on a correct answer;
- increments `RT[mode]` on an incorrect answer;
- disables all answer buttons to prevent repeated scoring.

The three answer handlers contain almost identical code.

Navigation, sorting, shuffling, adding, editing, deleting, and answering mutate only in-memory objects until the user clicks `保存文件` or chooses `Ok` in the close dialog. These actions save to `currentVocabularyPath`. Switching books offers Save, Discard, and Cancel choices.

## Vocabulary books and metadata

- Every vocabulary file remains a top-level JSON list compatible with the original `ko.json`.
- Optional metadata is stored beside it as `<stem>.meta.json`; for example, `ielts.json` uses `ielts.meta.json`.
- Metadata includes `title`, `description`, `sourceLanguage`, `targetLanguage`, `tags`, `version`, `createdAt`, and `updatedAt`.
- Legacy list files without a sidecar load with filename-derived default metadata.
- New vocabulary and sidecar writes are atomic and UTF-8 encoded.
- A new empty vocabulary is supported. The review tab shows an empty-state message and the add/edit tab can create its first entry.
- Books with one or two entries show only the available answer buttons rather than assuming three entries.
- `src/vocabularyFile.py` contains the non-GUI creation/loading logic. Keep it independently testable.

## Add, edit, and delete flows

### Add

`AddOrEdit.SaveAdded()` appends a new default `knowledgeObject`, populates it from the form, clears the form, and updates the displayed total. Semicolon-delimited fields (`HL`, `tags`, and `moreInfo`) are converted to lists. Empty inputs become `[""]`. `k` is parsed with `int()` and defaults to `1` only when the field is empty.

### Edit

`Row3.Edit()` switches to tab index `2` and fills the shared add/edit form from the current object. `AddOrEdit.saveChanges()` writes the form values back to whichever object `reviewIndex` points to at save time. It does not automatically return to or refresh the review tab, and it does not persist to disk.

### Delete

`Row3.Delete()` deletes the object at `reviewIndex`, clamps the index when deleting the last item, and refreshes the surviving item. If the final object is deleted, the review tab switches to its empty state. Deletion is not confirmed and is not persisted until an explicit or close-time save.

Delete behavior and its test are current uncommitted working-tree additions; preserve them unless the task explicitly changes them.

## Data schema

`data/ko.json` currently contains 267 objects. Every current record has these keys:

| Field | Current type | Meaning |
|---|---|---|
| `context` | string | Source word, phrase, sentence, or passage shown with highlights masked |
| `HL` | list of strings | Highlighted/hidden knowledge points; also used as answer text |
| `RT` | list of 4 numbers | Review/error counters indexed by mode |
| `CT` | list of 4 numbers | Correct counters indexed by mode |
| `LT` | list of 4 numbers | Last-review timestamps indexed by mode |
| `PS` | number | Calculated review priority |
| `k` | integer | Priority multiplier |
| `tags` | usually list; at least one current record is a dict | Classification tags |
| `audioPath` | string | Reserved media path |
| `videoPath` | string | Reserved media path |
| `imagePath` | string | Reserved media path |
| `contextExplanation` | string | Translation/explanation revealed after answering |
| `moreInfo` | list of strings | Additional information |

The model's default for `tags` is `{}`, but the form and current UI expect a list (`";".join(...)`). Current persisted data contains both list and dictionary values, so code touching tags must handle or normalize this mismatch.

Mode documentation is inconsistent. `knowledgeObjectList.mode` says `0=选择, 1=朗读, 2=听写`, while field comments use other orders. Only mode `0` is presently reachable because mode buttons have no handlers.

## Priority calculation

For every object, `UpdatePS(mode)` computes approximately:

```text
PS = k * (current_unix_time - LT[mode]) / (CT[mode] + random_0_to_0.1) * (RT[mode] + 1)
```

`sortList()` recalculates and sorts by this value descending, so older, less-correct, and more-error-prone items tend to appear first.

The method reseeds the global random generator with the current integer second for every object. This produces the same random term for all objects updated in one second and also affects later choice generation. Most current `LT` values are zero, so scores are dominated by time since the Unix epoch. Review answers do not update `LT`, and `UpdateLS()` references `body["mode"]`, a field that normal records do not contain.

## Tests and verification

Run all project-focused automated tests with:

```sh
python3 -m unittest discover -s test -p 'test_*.py' -v
```

`test/test_delete.py` sets `QT_QPA_PLATFORM=offscreen`, creates a minimal dummy root, clicks the delete button, and verifies that the first of two objects is removed and the index remains valid.

`test/test_vocabulary_file.py` tests new-book creation and metadata, legacy files without sidecars, and invalid top-level JSON. It has no PyQt dependency and can be run independently:

```sh
python3 -m unittest test.test_vocabulary_file -v
```

In the current environment the command fails during import with:

```text
ModuleNotFoundError: No module named 'PyQt5'
```

`test/test.py` is an independently runnable PyQt tabs example. It contains old commented manual checks for sorting and persistence; it is not a `unittest`/pytest suite despite its filename.

For GUI changes, useful verification should include:

- running unit tests with PyQt5 installed and the offscreen platform;
- launching the app from the repository root;
- checking first/last navigation and datasets with fewer than three objects;
- checking answer scoring and subsequent sorting;
- checking add/edit/delete followed by explicit save and reload;
- checking close with and without saving;
- confirming `data/ko.json` was not unintentionally reordered or rewritten.

## Known risks and sharp edges

- Startup assumes the default JSON file exists, is valid, and contains correctly shaped records.
- Exact `str.replace` masking is case-sensitive, masks all occurrences, and does nothing when an `HL` value is a translation rather than a substring of `context`.
- `Row3.Edit()` can fail on non-list `tags`.
- Numeric `k` input can raise `ValueError`.
- Shared class attributes and mutable default arguments (`body={}`, `hl=[]`) are unsafe for multiple instances/tests.
- `UpdateLS()` is inconsistent with the rest of the model and currently unusable for normal records.
- The context and explanation displays are editable `QTextEdit` widgets, but direct edits there do not update the model.
- Saving entries overwrites the active vocabulary file non-atomically; only new-book creation uses atomic writes.
- The close handler asks whether to save but does not explicitly call `event.accept()` or `event.ignore()`.
- The application uses wildcard imports, duplicated imports, repeated code, print debugging, semicolons, and spelling inconsistencies such as `lableCorect`, `btRewnew`, and `UpdateCS`.

## Working-tree caution

At the time this context was generated, the repository already had user changes:

- modified: `main.py`;
- modified: `data/ko.json`;
- untracked: `test/test_delete.py`;
- untracked generated `__pycache__` files.

Do not discard, normalize, regenerate, or broadly reformat these files as incidental cleanup. In particular, launching the app recalculates in-memory priority/order, and saving can produce a very large data diff.

## Guidance for future coding agents

- Read the current working-tree diff before editing; this repository may contain active user data and unfinished changes.
- Treat `data/ko.json` as user-owned persistent state, not a test fixture. Use temporary files and small synthetic object lists in tests.
- Keep the distinction between zero-based `reviewIndex` and one-based `GoToPageX()` arguments explicit.
- Preserve all 13 persisted fields unless implementing an intentional migration.
- Avoid adding behavior to the placeholder tag/search tabs unless requested.
- When changing review modes, first establish and document one consistent index mapping across `RT`, `CT`, `LT`, buttons, and comments.
- Prefer extracting model/persistence logic from widgets incrementally and adding tests before broad refactors.
- If persistence is changed, prioritize explicit UTF-8, atomic replacement, validation, and actionable error reporting.
- Add a dependency manifest and documented Python version when build/dependency work is in scope.
