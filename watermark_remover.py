import cv2
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import sys

class WatermarkRemover:
    def __init__(self):
        self.input_path = ""
        self.x = 0
        self.y = 0
        self.width = 0
        self.height = 0
        self.drawing = False
        self.ix, self.iy = -1, -1
        
        # 定义配色方案
        self.colors = {
            'primary': '#6C5CE7',      # 柔和的紫色
            'primary_hover': '#5B4BC4',
            'primary_pressed': '#4A3AA3',
            'secondary': '#A8A5E6',    # 浅紫色
            'background': '#F7F7FF',   # 带紫色的白色背景
            'surface': '#FFFFFF',      # 纯白表面
            'text': '#2D3436',         # 深色文字
            'text_secondary': '#636E72',# 次要文字
            'border': '#E5E5FF',       # 边框颜色
            'success': '#00B894',      # 成功色
            'error': '#FF7675'         # 错误色
        }
        
        # 创建主窗口
        self.root = tk.Tk()
        self.root.title("视频水印区域选择工具")
        self.root.geometry("800x600")
        self.root.configure(bg=self.colors['background'])
        
        # 设置窗口最小尺寸
        self.root.minsize(600, 450)
        
        self.setup_ui()
        self.setup_style()

    def setup_style(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        system_font = self.get_system_font()
        
        # 使用self.colors替代局部变量colors
        style.configure('iOS.TButton',
                       padding=(30, 15),
                       font=(system_font, 12),
                       background=self.colors['primary'],
                       foreground=self.colors['surface'],
                       borderwidth=0,
                       relief='flat',
                       anchor='center')
        
        style.map('iOS.TButton',
                 background=[('active', self.colors['primary_hover']), 
                            ('pressed', self.colors['primary_pressed'])],
                 relief=[('pressed', 'flat')])
        
        # 值标签样式
        style.configure('Value.TLabel',
                       font=(system_font, 12),
                       padding=(20, 12),
                       background=self.colors['surface'],
                       foreground=self.colors['text'],
                       borderwidth=1,
                       relief='solid')
        
        # 复制按钮样式
        style.configure('Copy.TButton',
                       padding=(12, 6),
                       font=(system_font, 10),
                       background=self.colors['surface'],
                       foreground=self.colors['primary'],
                       borderwidth=1,
                       relief='solid')
        
        style.map('Copy.TButton',
                 background=[('active', self.colors['border']), 
                            ('pressed', self.colors['background'])],
                 foreground=[('active', self.colors['primary_hover']), 
                            ('pressed', self.colors['primary_pressed'])])
        
        # 标题样式
        style.configure('Title.TLabel',
                       font=(system_font, 28, 'bold'),
                       padding=25,
                       foreground=self.colors['primary'],
                       background=self.colors['background'])
        
        # 普通标签样式
        style.configure('Modern.TLabel',
                       font=(system_font, 12),
                       padding=8,
                       foreground=self.colors['text'],
                       background=self.colors['background'])
        
        # 信息标签样式
        style.configure('Info.TLabel',
                       font=(system_font, 11),
                       foreground=self.colors['text_secondary'],
                       background=self.colors['background'],
                       padding=10)
        
        # 框架样式
        style.configure('Card.TFrame',
                       background=self.colors['surface'],
                       relief='flat',
                       borderwidth=0)
        
        # LabelFrame样式
        style.configure('Modern.TLabelframe',
                       background=self.colors['surface'],
                       padding=25,
                       relief='solid',
                       borderwidth=1,
                       bordercolor=self.colors['border'])
        
        style.configure('Modern.TLabelframe.Label',
                       font=(system_font, 13, 'bold'),
                       foreground=self.colors['primary'],
                       background=self.colors['surface'],
                       padding=(0, 5))
        
        # 分隔线样式
        style.configure('Separator.TFrame',
                       background=self.colors['border'],
                       height=1)
        
        # 使用说明文本样式
        style.configure('Help.TLabel',
                       font=(system_font, 11),
                       foreground=self.colors['text_secondary'],
                       background=self.colors['surface'],
                       padding=5,
                       spacing1=8,  # 段落间距
                       spacing2=2)  # 行间距
        
        # 高亮提示框样式
        style.configure('Highlight.TFrame',
                       background=self.colors['secondary'],
                       relief='flat',
                       borderwidth=1)
        
        # 高亮文本样式
        style.configure('Highlight.TLabel',
                       font=(system_font, 12),
                       foreground=self.colors['primary'],
                       background=self.colors['secondary'],
                       padding=10)

    def get_system_font(self):
        if sys.platform == 'darwin':  # macOS
            return '苹方-简'
        elif sys.platform == 'win32':  # Windows
            return '微软雅黑'
        else:  # Linux
            return 'Noto Sans CJK SC'

    def copy_coordinates(self):
        coords = f"X:{self.x}, Y:{self.y}, 宽:{self.width}, 高:{self.height}"
        # 使用 tkinter 的剪贴板功能替代 pyperclip
        self.root.clipboard_clear()
        self.root.clipboard_append(coords)
        self.status_label.config(text="坐标已复制到剪贴板")

    def copy_single_value(self, value, name):
        self.root.clipboard_clear()
        self.root.clipboard_append(str(value))
        self.status_label.config(text=f"{name}已复制到剪贴板")

    def setup_ui(self):
        # 设置窗口背景色和大小
        self.root.configure(bg=self.colors['background'])
        self.root.geometry("800x600")
        
        # 创建主容器，添加内边距
        main_container = ttk.Frame(self.root, style='Card.TFrame', padding=30)
        main_container.pack(fill=tk.BOTH, expand=True, padx=40, pady=40)
        
        # 标题区域（居中）
        title_frame = ttk.Frame(main_container, style='Card.TFrame')
        title_frame.pack(fill=tk.X, pady=(0, 30))
        
        title_label = ttk.Label(title_frame, 
                               text="视频水印区域选择工具",
                               style='Title.TLabel')
        title_label.pack(anchor='center')
        
        # 按钮区域（居中）
        button_frame = ttk.Frame(main_container, style='Card.TFrame')
        button_frame.pack(fill=tk.X, pady=10)
        
        # 创建按钮容器用于居中
        button_container = ttk.Frame(button_frame, style='Card.TFrame')
        button_container.pack(anchor='center')
        
        # 主按钮使用iOS风格
        select_btn = ttk.Button(button_container,
                               text="选择视频文件",
                               command=self.select_input_video,
                               style='iOS.TButton')
        select_btn.pack(side=tk.LEFT, padx=10)
        
        area_btn = ttk.Button(button_container,
                             text="选择水印区域",
                             command=self.select_watermark_area,
                             style='iOS.TButton')
        area_btn.pack(side=tk.LEFT, padx=10)
        
        # 信息显示区域
        info_frame = ttk.LabelFrame(main_container, 
                                  text="水印位置信息",
                                  style='Modern.TLabelframe',
                                  padding=20)
        info_frame.pack(fill=tk.X, pady=25)
        
        # 网格布局（居中）
        grid_frame = ttk.Frame(info_frame, style='Card.TFrame')
        grid_frame.pack(anchor='center')
        
        # 创建值容器框架
        value_frames = []
        for i in range(4):
            frame = ttk.Frame(grid_frame, style='Card.TFrame')
            value_frames.append(frame)
        
        # 创建标签对象和对应的复制按钮
        self.x_label = ttk.Label(value_frames[0], text="0", style='Value.TLabel', width=8)
        self.y_label = ttk.Label(value_frames[1], text="0", style='Value.TLabel', width=8)
        self.width_label = ttk.Label(value_frames[2], text="0", style='Value.TLabel', width=8)
        self.height_label = ttk.Label(value_frames[3], text="0", style='Value.TLabel', width=8)
        
        # 创建信息显示网格
        info_items = [
            ("X 坐标", self.x_label, lambda: self.copy_single_value(self.x, "X坐标")),
            ("Y 坐标", self.y_label, lambda: self.copy_single_value(self.y, "Y坐标")),
            ("宽　度", self.width_label, lambda: self.copy_single_value(self.width, "宽度")),
            ("高　度", self.height_label, lambda: self.copy_single_value(self.height, "高度"))
        ]
        
        for i, (label_text, value_label, copy_command) in enumerate(info_items):
            row = i // 2
            col = (i % 2) * 2
            
            # 创建值容器
            value_frame = value_frames[i]
            value_frame.grid(row=row, column=col + 1, padx=15, pady=10, sticky='w')
            
            # 标签文本
            ttk.Label(grid_frame, text=label_text, style='Modern.TLabel').grid(
                row=row, column=col, padx=(15, 5), pady=10, sticky='e')
            
            # 值标签
            value_label.pack(side=tk.LEFT, padx=(0, 5))
            
            # 复制按钮
            copy_btn = ttk.Button(value_frame,
                                text="复制",
                                command=copy_command,
                                style='Copy.TButton',
                                width=4)
            copy_btn.pack(side=tk.LEFT)

    def select_input_video(self):
        self.input_path = filedialog.askopenfilename(
            title="选择视频文件",
            filetypes=[
                ("视频文件", "*.mp4 *.avi *.mov"),
                ("所有文件", "*.*")
            ]
        )
        if self.input_path:
            filename = os.path.basename(self.input_path)
            self.status_label.config(text=f"已选择视频：{filename}")

    def mouse_drawing(self, event, x, y, flags, params):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.drawing = True
            self.ix, self.iy = x, y
        elif event == cv2.EVENT_MOUSEMOVE:
            if self.drawing:
                img_copy = self.frame.copy()
                cv2.rectangle(img_copy, (self.ix, self.iy), (x, y), (0, 255, 0), 2)
                cv2.imshow('选择水印区域 (按ESC确认)', img_copy)
        elif event == cv2.EVENT_LBUTTONUP:
            self.drawing = False
            self.x = min(self.ix, x)
            self.y = min(self.iy, y)
            self.width = abs(x - self.ix)
            self.height = abs(y - self.iy)
            
            self.x_label.config(text=str(self.x))
            self.y_label.config(text=str(self.y))
            self.width_label.config(text=str(self.width))
            self.height_label.config(text=str(self.height))
            
            cv2.rectangle(self.frame, (self.x, self.y), 
                         (self.x + self.width, self.y + self.height), 
                         (0, 255, 0), 2)
            cv2.imshow('选择水印区域 (按ESC确认)', self.frame)

    def select_watermark_area(self):
        if not self.input_path:
            messagebox.showerror("错误", "请先选择视频文件！")
            return
            
        cap = cv2.VideoCapture(self.input_path)
        ret, self.frame = cap.read()
        cap.release()
        
        if not ret:
            messagebox.showerror("错误", "无法读取视频帧！")
            return
            
        cv2.namedWindow('选择水印区域 (按ESC确认)')
        cv2.setMouseCallback('选择水印区域 (按ESC确认)', self.mouse_drawing)
        
        cv2.imshow('选择水印区域 (按ESC确认)', self.frame)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        
        if self.width > 0 and self.height > 0:
            messagebox.showinfo("成功", "水印位置选择完成！")
            self.status_label.config(text="水印位置已选择")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = WatermarkRemover()
    app.run() 