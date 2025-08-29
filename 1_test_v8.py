import fitz  # pip install pymupdf
import os
import math

# ------------------ 参数 ------------------
input_pdf = 'FusionServer服务器iBMC告警处理22.pdf'
base_name = os.path.splitext(input_pdf)[0]

skip = 31        # 跳过前 31 页
parts = 8        # 分成 8 份

# ------------------ 打开 PDF ------------------
doc = fitz.open(input_pdf)
total = doc.page_count
if skip >= total:
    print('⚠️ 跳过页数 ≥ 总页数，无需拆分。')
    doc.close(); exit()

remain = total - skip
step = math.ceil(remain / parts)   # 向上取整，保证最后一份不溢出

print(f'📊 共 {total} 页，跳过前 {skip} 页，剩余 {remain} 页')
print(f'📄 每份约 {step} 页 → 将生成 {parts} 个文件')

# ------------------ 逐份导出 ------------------
for i in range(parts):
    start = skip + i * step
    end   = min(start + step, total)
    if start >= end:           # 已分完
        break

    out_doc = fitz.open()
    out_doc.insert_pdf(doc, from_page=start, to_page=end - 1)
    out_path = f'./pdf_output_v4/{base_name}第_{i+1}份.pdf'
    out_doc.save(out_path)
    out_doc.close()
    print(f'✅ 已保存：{out_path}  （第 {start+1}-{end} 页，共 {end-start} 页）')

doc.close()
print('🎉 全部完成！')
