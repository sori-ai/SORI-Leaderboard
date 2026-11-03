#!/usr/bin/env python3
"""
README.md 자동 생성 스크립트

data/benchmarks/results.json과 data/samples/samples.json을 읽어서
README.md의 마커 섹션들을 자동으로 업데이트합니다.
"""

import json
import argparse
import sys
from datetime import datetime
from pathlib import Path


def load_json(path: Path) -> dict:
    """JSON 파일 로드"""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def generate_benchmark_table(results_data: dict) -> str:
    """벤치마크 테이블 Markdown 생성"""
    models = {m["id"]: m for m in results_data["models"]}
    benchmarks = {b["id"]: b for b in results_data["benchmarks"]}

    # 벤치마크별로 결과 그룹화
    results_by_benchmark = {}
    for result in results_data["benchmark_results"]:
        bm_id = result["benchmark_id"]
        if bm_id not in results_by_benchmark:
            results_by_benchmark[bm_id] = []
        results_by_benchmark[bm_id].append(result)

    output_lines = []

    for benchmark_id, results in results_by_benchmark.items():
        benchmark = benchmarks[benchmark_id]
        num_tracks = benchmark.get("num_tracks", "")
        num_str = f" ({num_tracks}곡)" if num_tracks else ""

        # Table header
        num_str_en = f" ({num_tracks} tracks)" if num_tracks else ""
        output_lines.append(f"### {benchmark['name']}{num_str_en}")
        output_lines.append("")
        output_lines.append("| Model | Note F1 | Note+Vel F1 | Note+Off F1 | Note+Off+Vel F1 | Params | Delay |")
        output_lines.append("|:------|:-------:|:-----------:|:-----------:|:---------------:|:------:|:-----:|")

        # note f1 기준 정렬 (내림차순)
        sorted_results = sorted(
            results,
            key=lambda x: x["metrics"]["note"]["f1"],
            reverse=True
        )

        # 최고 성능 찾기 (소리 모델 중에서)
        sori_results = [r for r in results if models[r["model_id"]].get("is_ours")]
        best_f1 = max(r["metrics"]["note"]["f1"] for r in sori_results) if sori_results else 0

        def fmt_metric(val):
            """Format metric value, handling None/null"""
            if val is None:
                return "N/A"
            return f"{val:.2f}"

        for result in sorted_results:
            model = models[result["model_id"]]
            metrics = result["metrics"]

            # 소리 모델이고 최고 성능이면 강조
            is_best = metrics["note"]["f1"] == best_f1
            name = f"**{model['name']}**" if model.get("is_ours") else model["name"]

            # 메트릭 포맷팅
            note_f1 = fmt_metric(metrics['note']['f1'])
            note_vel_f1 = fmt_metric(metrics['note_with_velocity']['f1'])
            note_off_f1 = fmt_metric(metrics['note_with_offsets']['f1'])
            note_off_vel_f1 = fmt_metric(metrics['note_with_offsets_and_velocity']['f1'])

            # 모델 정보
            params_val = model.get('params_million')
            if params_val:
                if params_val < 0.1:
                    params = f"{int(params_val * 1000)}K"
                else:
                    params = f"{params_val}M"
            else:
                params = "N/A"
            delay = f"{model.get('delay_ms')}ms" if model.get('delay_ms') else "Offline"

            row = [name, note_f1, note_vel_f1, note_off_f1, note_off_vel_f1, params, delay]
            output_lines.append("| " + " | ".join(row) + " |")

        # Detailed metrics (Sori models only)
        output_lines.append("")
        output_lines.append("<details>")
        output_lines.append("<summary>View Detailed Metrics</summary>")
        output_lines.append("")

        for result in sorted_results:
            model = models[result["model_id"]]
            if not model.get("is_ours"):
                continue
            metrics = result["metrics"]

            output_lines.append(f"#### {model['name']}")
            output_lines.append("")
            output_lines.append("| Metric | F1 | Precision | Recall |")
            output_lines.append("|:-------|:--:|:---------:|:------:|")
            output_lines.append(f"| Note (onset only) | {fmt_metric(metrics['note']['f1'])} | {fmt_metric(metrics['note']['precision'])} | {fmt_metric(metrics['note']['recall'])} |")
            output_lines.append(f"| Note + Velocity | {fmt_metric(metrics['note_with_velocity']['f1'])} | {fmt_metric(metrics['note_with_velocity']['precision'])} | {fmt_metric(metrics['note_with_velocity']['recall'])} |")
            output_lines.append(f"| Note + Offsets | {fmt_metric(metrics['note_with_offsets']['f1'])} | {fmt_metric(metrics['note_with_offsets']['precision'])} | {fmt_metric(metrics['note_with_offsets']['recall'])} |")
            output_lines.append(f"| Note + Offsets + Velocity | {fmt_metric(metrics['note_with_offsets_and_velocity']['f1'])} | {fmt_metric(metrics['note_with_offsets_and_velocity']['precision'])} | {fmt_metric(metrics['note_with_offsets_and_velocity']['recall'])} |")
            output_lines.append("")

        output_lines.append("</details>")
        output_lines.append("")

    return "\n".join(output_lines)


def generate_sample_gallery(samples_data: dict) -> str:
    """Generate sample gallery Markdown (for GT MIDI)"""
    samples = samples_data.get("samples_gt_midi", [])
    if not samples:
        return "*Samples will be displayed here when added.*"

    output_lines = []
    difficulty_names = {
        "beginner": "Beginner",
        "intermediate": "Intermediate",
        "advanced": "Advanced"
    }

    for i, sample in enumerate(samples, 1):
        diff_name = difficulty_names.get(sample.get("difficulty", ""), sample.get("difficulty", ""))
        title = sample.get("title", f"Sample {i}")
        diff_str = f" ({diff_name})" if diff_name else ""

        output_lines.append(f"### Sample {i}: {title}{diff_str}")
        output_lines.append("")
        output_lines.append("---")
        output_lines.append("")

    # 마지막 구분선 제거
    if output_lines and output_lines[-1] == "":
        output_lines.pop()
    if output_lines and output_lines[-1] == "---":
        output_lines.pop()

    return "\n".join(output_lines) if output_lines else "*Samples will be displayed here when added.*"


def generate_last_updated(results_data: dict) -> str:
    """Generate last updated info"""
    last_updated = results_data.get("last_updated", datetime.now().strftime("%Y-%m-%d"))
    version = results_data.get("version", "unknown")
    return f"*Last updated: {last_updated} | Data version: v{version}*"


def update_readme_section(readme_content: str, start_marker: str, end_marker: str, new_content: str) -> str:
    """README의 특정 마커 섹션 업데이트"""
    start_idx = readme_content.find(start_marker)
    end_idx = readme_content.find(end_marker)
    
    if start_idx == -1 or end_idx == -1:
        print(f"Warning: Markers not found: {start_marker} / {end_marker}")
        return readme_content
    
    before = readme_content[:start_idx + len(start_marker)]
    after = readme_content[end_idx:]
    
    return before + "\n" + new_content + "\n" + after


def main():
    parser = argparse.ArgumentParser(description="Generate README from data files")
    parser.add_argument("--check", action="store_true", help="Check if README is up to date without modifying")
    args = parser.parse_args()
    
    # 경로 설정
    root_dir = Path(__file__).parent.parent
    results_path = root_dir / "data" / "benchmarks" / "results.json"
    samples_path = root_dir / "data" / "samples" / "samples.json"
    readme_path = root_dir / "README.md"
    
    # 데이터 로드
    results_data = load_json(results_path)
    samples_data = load_json(samples_path)
    
    # 현재 README 로드
    with open(readme_path, "r", encoding="utf-8") as f:
        readme_content = f.read()
    
    # 각 섹션 생성 및 업데이트
    benchmark_table = generate_benchmark_table(results_data)
    sample_gallery = generate_sample_gallery(samples_data)
    last_updated = generate_last_updated(results_data)
    
    new_readme = readme_content
    new_readme = update_readme_section(
        new_readme,
        "<!-- BENCHMARK_TABLE_START -->",
        "<!-- BENCHMARK_TABLE_END -->",
        benchmark_table
    )
    new_readme = update_readme_section(
        new_readme,
        "<!-- SAMPLE_GALLERY_START -->",
        "<!-- SAMPLE_GALLERY_END -->",
        sample_gallery
    )
    new_readme = update_readme_section(
        new_readme,
        "<!-- LAST_UPDATED_START -->",
        "<!-- LAST_UPDATED_END -->",
        last_updated
    )
    
    if args.check:
        if new_readme != readme_content:
            print("ERROR: README is out of date. Run 'python scripts/generate_readme.py' to update.")
            sys.exit(1)
        else:
            print("README is up to date.")
            sys.exit(0)
    
    # README 저장
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(new_readme)
    
    print(f"✅ README.md updated successfully!")
    print(f"   - Benchmark tables: {len(results_data['benchmarks'])} benchmarks")
    print(f"   - Models: {len(results_data['models'])} models")
    print(f"   - Sample gallery (GT MIDI): {len(samples_data.get('samples_gt_midi', []))} samples")
    print(f"   - Sample gallery (MusicXML): {len(samples_data.get('samples_musicxml', []))} samples")


if __name__ == "__main__":
    main()
