# Sanskrit Vocabulary Master Rules

## 1. Purpose

This file is the authoritative ruleset for all vocabulary added under `study/vocab/`.

All vocabulary uploads MUST follow these rules exactly.
If there is uncertainty, the agent MUST stop and ask for clarification rather than guess.

---

## 2. Scope

The vocabulary area consists of the following files:

- `study/vocab/nouns.md`
- `study/vocab/verbs.md`
- `study/vocab/adjectives.md`
- `study/vocab/indeclinables.md`
- `study/vocab/master_rules.md`

All lexical items MUST be placed into the correct file.

---

## 3. File Classification Rules

### 3.1 Nouns
Place in `nouns.md`:
- substantives
- nominal stems used as nouns
- pronouns if the noun file is being used as the general nominal bucket unless a separate pronoun convention is later introduced

### 3.2 Verbs
Place in `verbs.md`:
- dhātus
- verbal entries built from dhātus
- prefixed verb forms when the project convention is to list them under the governing dhātu

### 3.3 Adjectives
Place in `adjectives.md`:
- adjectives
- adjectival stems
- participial adjectives when treated primarily as lexical adjectives

### 3.4 Indeclinables
Place in `indeclinables.md`:
- avyayas
- particles
- adverbs
- prepositions/postpositions in pedagogical glossing where relevant
- absolutives / gerunds when being treated as indeclinable lexical forms

### 3.5 Ambiguous Items
If an item could belong to multiple categories:
- prefer the category that reflects how the item is functioning in the user’s running master vocabulary project
- if still unclear, STOP and ask
- do not silently duplicate the same lexical item across files unless the user explicitly wants that

---

## 4. Required Table Structure

Vocabulary entries SHOULD be stored in markdown tables unless the user explicitly requests another structure.

### 4.1 Core columns
Use these core columns wherever applicable:

| Sanskrit | Transliteration | Grammatical Info / Derivation | Meaning | Source | Added Date |
|----------|-----------------|-------------------------------|---------|

### 4.2 Column meanings
- **Sanskrit**: Devanāgarī headword, dhātu, or prātipadika
- **Transliteration**: standard scholarly transliteration with diacritics
- **Grammatical Info / Derivation**: gender, stem type, derivation, samāsa type, kṛdanta/taddhita status, gaṇa/class, pāda, or other concise grammar information as relevant
- **Meaning**: concise English gloss only


### 4.3 Source column
- **Source** is mandatory for newly added rows.
- Use dictionary acronym list format when lookup-backed, for example: `[MW]`, `[Apte]`, `[MW, Apte]`.
- Use `LLM` when meaning/form was generated from model knowledge rather than dictionary evidence.
- Use `Manual Lookup` when supplied from analyst/manual research input.

### 4.4 Added Date column
- **Added Date** should be in `YYYY-MM-DD` format for new rows.
- Leave historical rows blank unless backfilled intentionally.

### 4.5 Concision rule
The grammatical column should be information-dense but concise.
Do not pad with obvious textbook explanations unless requested.

---

## 5. Headword Rules

### 5.1 Use lexical base forms
- Nouns and adjectives should normally be entered by **stem / prātipadika**, not by an arbitrary inflected form
- Verbs should normally be entered by **dhātu**, not by a finite conjugated form, unless the user explicitly wants a lexicalized finite form listed
- Indeclinables should be entered in their lexical citation form

### 5.2 Do not use inconsistent citation forms
Do not mix inflected forms and stems randomly.
If a special surface form is being recorded, say so explicitly in the grammar column.

---

## 6. Ordering Rules (CRITICAL)

### 6.1 Primary ordering principle
All entries within each file MUST be sorted in strict **Devanāgarī alphabetical order**.

### 6.2 Letter-by-letter ordering
Sorting MUST be done letter-by-letter, not by rough initial-letter grouping.
The full written form governs placement.

Example principle:
- do not group all words beginning with the same visible consonant cluster loosely
- compare entries sequentially character by character

### 6.3 No approximate ordering
Near-correct order is not acceptable.
If ordering is uncertain, the agent must check carefully before writing.

### 6.4 Maintain stable ordering on append
When adding new entries, place them in their correct sorted position relative to the existing file contents.
Do not simply append to the end if that breaks ordering.

---

## 7. Verb-Specific Ordering Rules

### 7.1 Group by core dhātu
Verbs should be organised by core dhātu.

### 7.2 Prefixed forms under the dhātu
If upasarga-prefixed forms are included, they should appear under the same core dhātu rather than being treated as entirely separate alphabetic headwords detached from the root.

### 7.3 Ordering within a dhātu group
Within the same dhātu group:
- list the unprefixed dhātu first unless the user specifies otherwise
- then list prefixed forms in a consistent order
- sort upasarga variants consistently within that dhātu grouping

### 7.4 Dhātu grouping overrides naive global alphabetisation
For verbs only, internal grouping by dhātu takes precedence over treating every prefixed form as a completely independent entry.
However, the broader sequence of dhātu groups should still be alphabetically ordered by the base dhātu.

---

## 8. Derivational Information Rules

### 8.1 Always include meaningful grammar metadata
Where relevant, include:
- gender
- stem class
- whether the item is a kṛdanta
- whether the item is a taddhitānta
- samāsa type
- verbal class / gaṇa
- pada
- transitivity or voice notes if useful

### 8.2 Compounds
For compounds, specify the samāsa type whenever reasonably knowable, such as:
- tatpuruṣa
- karmadhāraya
- bahuvrīhi
- dvandva
- avyayībhāva

### 8.3 Derivatives
For derivatives, note the derivational category when relevant, such as:
- kṛdanta
- taddhita
- desiderative
- causative
- intensive
- denominative

### 8.4 Do not fake certainty
If a derivation is uncertain, mark it as uncertain briefly or stop and ask.
Do not invent fine-grained grammatical analysis.

---

## 9. Meaning / Gloss Rules

### 9.1 Keep glosses concise
Use short, clear English meanings.

### 9.2 Avoid essay-style definitions
Do not overload the meaning field with commentary.
Additional nuance can be placed outside the table if explicitly requested.

### 9.3 Prefer core lexical meaning
Use the most central pedagogically useful gloss unless context demands otherwise.

---

## 10. Duplicate and Variant Handling

### 10.1 No accidental duplicates
Before adding an entry, check whether the same item already exists.
Do not duplicate entries with only trivial rewording.

### 10.2 Variant spellings or analyses
If there are genuine variants, either:
- include one entry with a concise note, or
- add separate entries only if the distinction is meaningful and intentional

### 10.3 Cleanup over accumulation
If the file has become inconsistent, cleanup and normalisation should be preferred over adding messy duplicates.

---

## 11. Formatting Rules

### 11.1 Use clean markdown
- Keep tables valid and readable
- Preserve diacritics correctly
- Preserve Devanāgarī correctly

### 11.2 No unnecessary prose repetition
Do not keep repeating generic notes such as:
- adjectives decline like nouns
- avyayas are indeclinable
unless the user explicitly wants such reminders

### 11.3 Consistency over ornament
Formatting should be plain, durable, and easy to maintain in git.

---

## 12. Write Behaviour Rules

### 12.1 Never violate file scope
- nouns go only to `nouns.md`
- verbs go only to `verbs.md`
- adjectives go only to `adjectives.md`
- indeclinables go only to `indeclinables.md`

### 12.2 Master rules are binding
All `/vocab` uploads MUST conform to this file.
If a proposed upload conflicts with these rules, the agent should stop and state the conflict.

### 12.3 Append-with-order discipline
Even when the command semantics say “append”, the resulting file must remain properly ordered and internally consistent.
That means insertion into the correct place is allowed and expected.

---

## 13. Quality Control Checklist

Before writing any vocab entry, verify:

1. The item is going to the correct vocab file
2. The headword form is the correct lexical citation form
3. The transliteration is present and properly diacriticised
4. The grammatical info is concise but meaningful
5. The English gloss is concise
6. The entry does not duplicate an existing one unnecessarily
7. The resulting file remains properly ordered
8. Verb entries respect dhātu grouping and upasarga ordering

If any check fails, STOP and fix it before writing.

---

## 14. Priority Rule

If there is a conflict between convenience and consistency:

**consistency with the master rules wins**.

If there is a conflict between a vague prior formatting habit and an explicit user instruction:

**the explicit user instruction wins**, and the rules should then be updated accordingly.
