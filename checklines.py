import re
from pathlib import Path
import datetime

def analyze_thai_lines_between_markers(file_path, markers):
    try:

        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        thai_pattern = re.compile(r'[\u0E00-\u0E7F]')

        results = {}
        total_lines_overall = 0
        thai_lines_count_overall = 0

        for i in range(len(markers) - 1):
            start_marker = markers[i]
            end_marker = markers[i + 1]

            start_index = next((idx for idx, line in enumerate(lines) if start_marker in line), None)
            end_index = next((idx for idx, line in enumerate(lines) if end_marker in line), None)

            if start_index is not None and end_index is not None and start_index < end_index:
                total_lines = 0
                thai_lines_count = 0

                for line in lines[start_index + 1 : end_index]:
                
                    if not line.strip() or line.strip().startswith("#") or line.strip().startswith("##"):
                        continue

                    total_lines += 1

                    if thai_pattern.search(line):
                        thai_lines_count += 1

                total_lines_overall += total_lines
                thai_lines_count_overall += thai_lines_count

                thai_lines_percentage = (thai_lines_count / total_lines) * 100 if total_lines > 0 else 0
                results[f"{start_marker} to {end_marker}"] = (total_lines, thai_lines_count, thai_lines_percentage)

        overall_percentage = (thai_lines_count_overall / total_lines_overall) * 100 if total_lines_overall > 0 else 0
        summary = {
            "total_lines_overall": total_lines_overall,
            "thai_lines_count_overall": thai_lines_count_overall,
            "overall_percentage": overall_percentage,
        }

        return results, summary

    except Exception as e:
        return str(e)

filename = "th_TH.lang"
file_path = next(Path(".").rglob(filename), None)
markers = [ "## THLanguage_Bedrock", '## Ore UI', '## Editor', '## chemistry', '## education', '## END']

results, summary = analyze_thai_lines_between_markers(file_path, markers)

time = datetime.datetime.utcnow().strftime("%d/%m/%Y %H:%M:%S")

if isinstance(results, dict):
    print("THLanguage_Bedrock (MIT License) © MineGarp.PED")
    print(f"สร้างเมื่อ: {time} (UTC)\n")
    for key, (total, thai_count, percentage) in results.items():
        print(f"ตั้งแต่: {key}")
        print(f"  จำนวนบรรทัดทั้งหมด: {total}")
        print(f"  จำนวนบรรทัดที่มีภาษาไทย: {thai_count}")
        print(f"  คิดเป็นเปอร์เซ็นต์: {percentage:.2f}%\n")

    print("**สรุปข้อมูล**")
    print(f"  จำนวนบรรทัดทั้งหมด: {summary['total_lines_overall']}")
    print(f"  จำนวนบรรทัดที่มีภาษาไทย: {summary['thai_lines_count_overall']}")
    print(f"  คิดเป็นเปอร์เซ็นต์: {summary['overall_percentage']:.2f}%")
else:
    print(f"เกิดข้อผิดพลาด: {results}")

with open("summary.txt", "w", encoding="utf-8") as f:
    if isinstance(results, dict):
        f.write(f"THLanguage_Bedrock (MIT License) © MineGarp.PED\n")
        f.write(f"สร้างเมื่อ: {time} (UTC)\n\n")
        for key, (total, thai_count, percentage) in results.items():
           
            f.write(f"ตั้งแต่: {key}\n")
            f.write(f"  จำนวนบรรทัดทั้งหมด: {total}\n")
            f.write(f"  จำนวนบรรทัดที่มีภาษาไทย: {thai_count}\n")
            f.write(f"  คิดเป็นเปอร์เซ็นต์: {percentage:.2f}%\n\n")

        f.write("**สรุปข้อมูลรวม**\n")
        f.write(f"  จำนวนบรรทัดทั้งหมด: {summary['total_lines_overall']}\n")
        f.write(f"  จำนวนบรรทัดที่มีภาษาไทย: {summary['thai_lines_count_overall']}\n")
        f.write(f"  คิดเป็นเปอร์เซ็นต์: {summary['overall_percentage']:.2f}%\n")
    else:
        f.write(f"เกิดข้อผิดพลาด: {results}\n")

