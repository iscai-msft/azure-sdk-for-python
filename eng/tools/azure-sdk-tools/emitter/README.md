# TypeSpec Python Emitter

This directory holds files related to the TypeSpec Python emitter (`@azure-tools/typespec-python` and `@typespec/http-client-python`).

## Contents

- **`generated/`** — Auto-generated Python SDK test code produced by the emitter.
  These files are regenerated automatically by the [typespec-python-regenerate](./../../../.github/workflows/typespec-python-regenerate.yml) workflow whenever the emitter version in `eng/emitter-package.json` is updated.

> **Do not edit files in `generated/` by hand.** They will be overwritten on the next regeneration.
