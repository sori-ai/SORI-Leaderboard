# Contributing to Sori Tech Demo

Thank you for your interest in contributing to the Sori Tech Demo!

## Table of Contents

- [Adding New Benchmark Results](#adding-new-benchmark-results)
- [Adding New Samples](#adding-new-samples)
- [Adding New Models](#adding-new-models)
- [Code Style](#code-style)
- [Pull Request Guidelines](#pull-request-guidelines)

---

## Adding New Benchmark Results

### Method 1: Direct JSON Edit

1. Open `data/benchmarks/results.json`
2. Add a new model to the `models` array (if needed)
3. Add benchmark results to the `benchmark_results` array:

```json
{
  "model_id": "your-model-id",
  "benchmark_id": "maestro-v3-test",
  "tested_date": "2025-01-06",
  "metrics": {
    "note": {
      "f1": 97.0,
      "precision": 98.0,
      "recall": 96.0
    },
    "note_with_velocity": {
      "f1": 95.0,
      "precision": 96.0,
      "recall": 94.0
    },
    "note_with_offsets": {
      "f1": 85.0,
      "precision": 86.0,
      "recall": 84.0
    },
    "note_with_offsets_and_velocity": {
      "f1": 83.0,
      "precision": 84.0,
      "recall": 82.0
    }
  },
  "notes": "Description of the model or test conditions"
}
```

4. Regenerate README:
```bash
python scripts/generate_readme.py
```

5. Regenerate plot:
```bash
python scripts/generate_plot.py
```

### Important Notes

- Do not overwrite existing results; add new entries instead
- Always include accurate `tested_date`
- Use `null` for metrics that are not available

---

## Adding New Samples

### 1. Prepare Files

- Audio file: `assets/audio/{sample-id}.mp3`
- Ground truth MIDI: `assets/midi/ground-truth/{sample-id}.mid`
- Model results: `assets/midi/{model-id}/{sample-id}.mid`
- (Optional) Visualization: `assets/images/{sample-id}-comparison.png`

### 2. Add Metadata

Add to `data/samples/samples.json`:

```json
{
  "id": "sample-id",
  "title": "Sample Title",
  "difficulty": "intermediate",
  "duration_sec": 60
}
```

### 3. File Naming Convention

- Use **kebab-case** for all filenames
- No special characters or spaces
- Example: `chopin-nocturne-op9-2.mid`

---

## Adding New Models

### 1. Add Model Information

Add to `data/benchmarks/results.json` in the `models` array:

```json
{
  "id": "new-model-id",
  "name": "Display Name",
  "is_ours": false,
  "description": "Brief description of the model",
  "params_million": 10.5,
  "delay_ms": 200,
  "url": "https://github.com/example/model"
}
```

### 2. Add Benchmark Results

Add corresponding results in the `benchmark_results` array.

---

## Code Style

### Python
- Formatter: Black
- Import sorting: isort
- Type hints recommended

```bash
black scripts/
isort scripts/
```

### JSON
- 2-space indentation
- No trailing commas

### Git Commit Messages

```
<type>: <description>

[optional body]
```

Types:
- `benchmark`: Benchmark result changes
- `sample`: Sample additions/modifications
- `docs`: Documentation changes
- `fix`: Bug fixes
- `feat`: New features
- `chore`: Maintenance

Examples:
```
benchmark: Add MAESTRO v3 results for new model
docs: Update metric definitions
fix: Correct precision values in results.json
```

---

## Pull Request Guidelines

Before submitting a PR, please ensure:

- [ ] `python scripts/generate_readme.py` runs without errors
- [ ] `python scripts/generate_plot.py` runs without errors
- [ ] New files are in the correct locations
- [ ] Commit messages follow conventions
- [ ] No sensitive information is included

---

## Questions?

For inquiries, please contact: [taegyun.kwon@sori-ai.com](mailto:taegyun.kwon@sori-ai.com)
