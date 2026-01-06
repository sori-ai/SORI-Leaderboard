#!/usr/bin/env python3
"""
벤치마크 결과 추가 헬퍼 스크립트

커맨드라인에서 새 벤치마크 결과를 쉽게 추가할 수 있습니다.
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path


def load_json(path: Path) -> dict:
    """JSON 파일 로드"""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path: Path, data: dict) -> None:
    """JSON 파일 저장 (2-space indent)"""
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")


def main():
    parser = argparse.ArgumentParser(
        description="Add a new benchmark result to results.json",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python add_benchmark.py --algorithm sori-v2 --dataset maestro-v3 \\
    --note-f1 0.935 --note-precision 0.944 --note-recall 0.926 \\
    --onset-f1 0.915 --offset-f1 0.870 --velocity-mae 6.5 \\
    --inference-time 30 --notes "New optimization applied"
        """,
    )

    parser.add_argument(
        "--algorithm", "-a", required=True, help="Algorithm ID (e.g., sori-v2)"
    )
    parser.add_argument(
        "--dataset", "-d", required=True, help="Dataset ID (e.g., maestro-v3)"
    )
    parser.add_argument(
        "--note-f1", type=float, required=True, help="Note F1 score (0-1)"
    )
    parser.add_argument(
        "--note-precision", type=float, required=True, help="Note precision (0-1)"
    )
    parser.add_argument(
        "--note-recall", type=float, required=True, help="Note recall (0-1)"
    )
    parser.add_argument("--onset-f1", type=float, help="Onset F1 score (0-1)")
    parser.add_argument("--offset-f1", type=float, help="Offset F1 score (0-1)")
    parser.add_argument(
        "--velocity-mae", type=float, help="Velocity MAE (0-127)"
    )
    parser.add_argument(
        "--inference-time", type=float, help="Inference time in ms per second of audio"
    )
    parser.add_argument("--notes", default="", help="Additional notes")
    parser.add_argument(
        "--date",
        default=datetime.now().strftime("%Y-%m-%d"),
        help="Test date (default: today)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be added without modifying the file",
    )

    args = parser.parse_args()

    # 경로 설정
    root_dir = Path(__file__).parent.parent
    results_path = root_dir / "data" / "benchmarks" / "results.json"

    # 데이터 로드
    try:
        data = load_json(results_path)
    except FileNotFoundError:
        print(f"Error: {results_path} not found")
        sys.exit(1)

    # algorithm_id 검증
    valid_algorithms = {a["id"] for a in data["algorithms"]}
    if args.algorithm not in valid_algorithms:
        print(f"Error: Unknown algorithm '{args.algorithm}'")
        print(f"Valid algorithms: {', '.join(sorted(valid_algorithms))}")
        sys.exit(1)

    # dataset_id 검증
    valid_datasets = {d["id"] for d in data["datasets"]}
    if args.dataset not in valid_datasets:
        print(f"Error: Unknown dataset '{args.dataset}'")
        print(f"Valid datasets: {', '.join(sorted(valid_datasets))}")
        sys.exit(1)

    # 새 결과 객체 생성
    new_result = {
        "algorithm_id": args.algorithm,
        "dataset_id": args.dataset,
        "metrics": {
            "note_f1": args.note_f1,
            "note_precision": args.note_precision,
            "note_recall": args.note_recall,
        },
        "tested_date": args.date,
        "notes": args.notes,
    }

    # 선택적 메트릭 추가
    if args.onset_f1 is not None:
        new_result["metrics"]["onset_f1"] = args.onset_f1
    if args.offset_f1 is not None:
        new_result["metrics"]["offset_f1"] = args.offset_f1
    if args.velocity_mae is not None:
        new_result["metrics"]["velocity_mae"] = args.velocity_mae
    if args.inference_time is not None:
        new_result["inference_time_ms"] = args.inference_time

    # 기존 결과 확인 (같은 algorithm + dataset 조합)
    existing_idx = None
    for i, result in enumerate(data["results"]):
        if (
            result["algorithm_id"] == args.algorithm
            and result["dataset_id"] == args.dataset
        ):
            existing_idx = i
            break

    print("New benchmark result:")
    print(json.dumps(new_result, indent=2, ensure_ascii=False))
    print()

    if existing_idx is not None:
        print(f"Warning: Existing result found for {args.algorithm} on {args.dataset}")
        print("This will ADD a new entry (not replace). Consider removing the old one if needed.")
        print()

    if args.dry_run:
        print("Dry run - no changes made")
        return

    # 결과 추가
    data["results"].append(new_result)

    # 마지막 업데이트 날짜 갱신
    data["last_updated"] = args.date

    # 저장
    save_json(results_path, data)
    print(f"Result added to {results_path}")
    print()
    print("Next steps:")
    print("  1. python scripts/validate_data.py")
    print("  2. python scripts/generate_readme.py")
    print("  3. git add && git commit && git push")


if __name__ == "__main__":
    main()
