#!/usr/bin/env python3
"""
데이터 파일 검증 스크립트

JSON 스키마를 사용하여 results.json과 samples.json의 유효성을 검증합니다.
"""

import json
import sys
from pathlib import Path

try:
    from jsonschema import validate, ValidationError, Draft7Validator
except ImportError:
    print("Error: jsonschema package is required. Install with: pip install jsonschema")
    sys.exit(1)


def load_json(path: Path) -> dict:
    """JSON 파일 로드"""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def validate_file(data_path: Path, schema_path: Path) -> tuple[bool, list[str]]:
    """
    데이터 파일을 스키마에 대해 검증

    Returns:
        (성공 여부, 에러 메시지 리스트)
    """
    errors = []

    try:
        data = load_json(data_path)
    except FileNotFoundError:
        return False, [f"File not found: {data_path}"]
    except json.JSONDecodeError as e:
        return False, [f"Invalid JSON in {data_path}: {e}"]

    try:
        schema = load_json(schema_path)
    except FileNotFoundError:
        return False, [f"Schema file not found: {schema_path}"]
    except json.JSONDecodeError as e:
        return False, [f"Invalid JSON in schema {schema_path}: {e}"]

    # 스키마 검증
    validator = Draft7Validator(schema)
    for error in validator.iter_errors(data):
        path = " -> ".join(str(p) for p in error.absolute_path) if error.absolute_path else "root"
        errors.append(f"[{path}] {error.message}")

    return len(errors) == 0, errors


def validate_references(results_path: Path, samples_path: Path) -> list[str]:
    """
    데이터 간 참조 무결성 검증
    - samples.json의 algorithm_id가 results.json에 존재하는지 확인
    """
    errors = []

    try:
        results_data = load_json(results_path)
        samples_data = load_json(samples_path)
    except (FileNotFoundError, json.JSONDecodeError):
        return []  # 파일 에러는 이미 validate_file에서 처리됨

    # 유효한 algorithm ID 집합
    valid_algorithms = {a["id"] for a in results_data.get("algorithms", [])}

    # samples.json의 results에서 참조하는 algorithm ID 확인
    for sample in samples_data.get("samples", []):
        for alg_id in sample.get("results", {}).keys():
            if alg_id not in valid_algorithms:
                errors.append(
                    f"Sample '{sample['id']}' references unknown algorithm '{alg_id}'"
                )

    return errors


def main():
    root_dir = Path(__file__).parent.parent

    results_path = root_dir / "data" / "benchmarks" / "results.json"
    samples_path = root_dir / "data" / "samples" / "samples.json"
    benchmark_schema = root_dir / "data" / "schemas" / "benchmark.schema.json"
    sample_schema = root_dir / "data" / "schemas" / "sample.schema.json"

    all_errors = []

    print("Validating data files...")
    print()

    # results.json 검증
    print(f"Checking {results_path.name}...")
    success, errors = validate_file(results_path, benchmark_schema)
    if success:
        print("  OK")
    else:
        print("  FAILED")
        all_errors.extend(errors)
        for e in errors:
            print(f"    - {e}")

    # samples.json 검증
    print(f"Checking {samples_path.name}...")
    success, errors = validate_file(samples_path, sample_schema)
    if success:
        print("  OK")
    else:
        print("  FAILED")
        all_errors.extend(errors)
        for e in errors:
            print(f"    - {e}")

    # 참조 무결성 검증
    print("Checking cross-references...")
    ref_errors = validate_references(results_path, samples_path)
    if not ref_errors:
        print("  OK")
    else:
        print("  FAILED")
        all_errors.extend(ref_errors)
        for e in ref_errors:
            print(f"    - {e}")

    print()

    if all_errors:
        print(f"Validation FAILED with {len(all_errors)} error(s)")
        sys.exit(1)
    else:
        print("All validations passed!")
        sys.exit(0)


if __name__ == "__main__":
    main()
