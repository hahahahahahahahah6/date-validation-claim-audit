# Calendar claim audit

An offline static auditor compares documented claims about calendar input with Python call shapes. It does not execute the inspected code. Findings require human review.

```text
date-validation-claim-audit audit [repo] [--json] [--verbose] [--ignore PREFIX] [--fail-on high|medium]
```

The default root is the current directory. Repeat the ignore option for multiple path prefixes. The default threshold is high; medium includes test-only evidence. Exit status is 0 for pass, 2 when a finding meets the threshold, and 1 for usage or I/O errors. The module entry point is:

```text
python3 -m date_validation_claim_audit audit .
```

The identifiers are:

```text
documented-date-validation-claim-false
documented-no-date-validation-claim-false
```

Root README and Markdown under docs are scanned outside fenced blocks. Inline code counts. Denial phrases are removed before positive phrases are matched. Production and test sources are distinguished; fixtures, docs, examples and symbolic links are excluded. Syntax errors provide no evidence.

## Differentiation

This audit concerns whether a supplied calendar value is real and well formed. Neighbouring families cover generic input validation, authentication and one-time codes, password hashing and generation, PDF encryption, email and SMS sending, document extraction, barcode and QR decoding, email and phone number validation, password strength, JSON Schema, JSON decoding, regular expressions, URL parsing and fetching, URL and IP address validation, and domain validation. Other families address spreadsheets, word documents, presentations, PDF extraction, generation, merging, splitting, rotation, form filling, watermarking, redaction, compression and annotation, table extraction, OCR, e-signature, payments, screen recording, video generation, QR and barcode generation, audio mixing, generation and editing, source separation, speech recognition, text-to-speech, noise suppression, music generation and transcription.

## Limitations

- This phrase may refer to a database or remote policy instead of a code capability; review it manually.

  ```text
  validate date
  ```

- This phrase may refer to a manual runbook step instead of a code capability; review it manually.

  ```text
  check date
  ```

- This phrase may refer to a roadmap feature instead of a code capability; review it manually.

  ```text
  date validation
  ```

- This phrase may refer to a hosted page instead of a code capability; review it manually.

  ```text
  date validator
  ```

- This phrase may refer to reader advice instead of a code capability; review it manually.

  ```text
  valid date
  ```

- This phrase may refer to a successful lookup instead of a code capability; review it manually.

  ```text
  date is valid
  ```

- This phrase may refer to a past-time lookup instead of a code capability; review it manually.

  ```text
  date check
  ```

- This phrase may refer to a weekday service instead of a code capability; review it manually.

  ```text
  date checker
  ```

- This phrase may refer to a documented pattern instead of a code capability; review it manually.

  ```text
  date format check
  ```

- This phrase may refer to identity document proof instead of a code capability; review it manually.

  ```text
  verify date
  ```

- This phrase may refer to a length rule instead of a code capability; review it manually.

  ```text
  detect invalid date
  ```

- This phrase may refer to theoretical discussion instead of a code capability; review it manually.

  ```text
  date well formed
  ```

- This phrase may refer to a generated value instead of a code capability; review it manually.

  ```text
  is valid date
  ```

- This phrase may refer to a specification section instead of a code capability; review it manually.

  ```text
  date validity
  ```

- A call shape counts even when never executed.
- A numeric timestamp passed to the Arrow getter counts despite being a conversion.
- A parser reached through an untraced variable chain is missed.
- An import without a qualifying call is insufficient.
- A roadmap, changelog or TODO claim still counts.
- An unlisted denial paraphrase may be missed.
- Files outside the root README and docs tree are invisible.
- Evidence split across modules is missed.
- A locally defined route name shadows an import even for wrappers.
- Dead code counts.
- External subprocess commands are not evidence.
- A generic input check alone is insufficient.
- An email check alone is insufficient.
- A phone number check alone is insufficient.
- An extraction call alone is insufficient.
- A locally defined generic name is shadowed.
- Untraced generic alias chains are missed.
- Exact phrases are matched, not meaning.
- Only Python source is examined.
- Dynamic imports and runtime plugins are invisible; no network calls are made.
- Construction from integer parts alone is insufficient.
- Fetching the current time alone is insufficient.
- Formatting for output alone is insufficient.
- A regular expression alone is insufficient.
- A Django datetime parser alone is insufficient.
