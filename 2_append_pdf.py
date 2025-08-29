import fitz  # PyMuPDF
import shutil
import os

def move_first_n_pages_inplace(pdf1_path: str, pdf2_path: str, n: int):
    """
    把 pdf2 的前 n 页移动到 pdf1 末尾。
    只用备份文件方式，不使用内存流。
    """
    if n <= 0:
        return

    bak_path = pdf2_path + ".bak"

    # ---------- 1. 备份 pdf2 ----------
    shutil.copy2(pdf2_path, bak_path)

    try:
        # ---------- 2. 追加到 pdf1 ----------
        with fitz.open(pdf1_path) as doc1, \
             fitz.open(bak_path) as doc2_bak:
            n = min(n, len(doc2_bak))
            if n == 0:
                return
            doc1.insert_pdf(doc2_bak, to_page=n - 1)   # 追加前 n 页
            tmp1 = pdf1_path + ".tmp"
            doc1.save(tmp1)                            # 先写临时文件
        os.replace(tmp1, pdf1_path)                    # 原子替换

        # ---------- 3. 修改 pdf2 ----------
        with fitz.open(pdf2_path) as doc2:
            doc2.delete_pages(range(n))                # 删除前 n 页
            tmp2 = pdf2_path + ".tmp"
            doc2.save(tmp2)                            # 先写临时文件
        os.replace(tmp2, pdf2_path)                    # 原子替换

    finally:
        # ---------- 4. 清理备份 ----------
        if os.path.exists(bak_path):
            os.remove(bak_path)

# ------------------ 用法 ------------------
if __name__ == "__main__":
    pdf1 = r'D:\work_tools\分开pdf文件\pdf_output_v4\FusionServer服务器iBMC告警处理22第_1份.pdf'
    pdf2 = r'D:\work_tools\分开pdf文件\pdf_output_v4\FusionServer服务器iBMC告警处理22第_2份.pdf'
    move_first_n_pages_inplace(pdf1, pdf2, n=3)
