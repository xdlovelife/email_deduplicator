import tkinter as tk
from tkinter import filedialog, messagebox
import os

class EmailDuplicateRemover:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("邮件去重工具")
        self.window.geometry("400x250")
        
        # 创建界面元素
        self.create_widgets()
        
    def create_widgets(self):
        # 使用说明标签
        self.instruction_label = tk.Label(
            self.window, 
            text="使用说明：\n1. 请准备txt格式的邮件列表文件\n2. 每行一个邮件地址\n3. 处理后将直接覆盖原文件",
            justify=tk.LEFT,
            padx=20
        )
        self.instruction_label.pack(pady=20)
        
        # 选择并处理文件按钮
        self.input_button = tk.Button(
            self.window, 
            text="选择文件并处理", 
            command=self.process_file
        )
        self.input_button.pack(pady=20)
        
        # 状态标签
        self.status_label = tk.Label(self.window, text="")
        self.status_label.pack()
            
    def remove_duplicates(self, email_list):
        seen = set()
        unique_emails = []
        
        for email in email_list:
            email = email.strip()
            if email and email not in seen:
                seen.add(email)
                unique_emails.append(email)
                
        return unique_emails
    
    def process_file(self):
        try:
            # 打开文件选择对话框
            input_file = filedialog.askopenfilename(
                title="选择包含邮件地址的文件",
                filetypes=[("文本文件", "*.txt")]  # 只允许选择txt文件
            )
            
            if not input_file:
                return
                
            # 读取输入文件
            with open(input_file, 'r', encoding='utf-8') as f:
                emails = f.readlines()
            
            # 去重
            unique_emails = self.remove_duplicates(emails)
            
            # 直接覆盖原文件
            with open(input_file, 'w', encoding='utf-8') as f:
                for email in unique_emails:
                    f.write(email + '\n')
            
            # 显示结果
            result_message = (
                f"处理完成！\n"
                f"原始邮件数量: {len(emails)}\n"
                f"去重后邮件数量: {len(unique_emails)}\n"
                f"删除了 {len(emails) - len(unique_emails)} 个重复邮件"
            )
            messagebox.showinfo("处理结果", result_message)
            self.status_label.config(text="处理完成！")
                
        except Exception as e:
            messagebox.showerror("错误", f"处理文件时出错: {str(e)}")
            self.status_label.config(text="处理失败！")
    
    def run(self):
        self.window.mainloop()

# 运行程序
if __name__ == "__main__":
    app = EmailDuplicateRemover()
    app.run()