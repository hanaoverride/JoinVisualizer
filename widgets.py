"""
핵심: JoinVisualizer 애플리케이션을 위한 사용자 정의 위젯 및 UI 유틸리티.
툴팁 기능 및 사용자 정의 위젯 확장을 포함합니다.
"""
import tkinter as tk
from tkinter import ttk, scrolledtext
from typing import List, Dict, Any, Callable


class TooltipManager:
    """
    핵심: 위젯에 대한 툴팁을 생성하고 관리하는 클래스.
    """
    
    @staticmethod
    def create_tooltip(widget, text):
        """
        핵심: 주어진 위젯에 대한 툴팁을 생성합니다.
        
        매개변수:
            widget: 툴팁을 추가할 위젯
            text: 툴팁에 표시할 텍스트
        """
        tooltip = None
        
        def enter(event):
            """
            핵심: 위젯에 마우스가 들어갈 때 툴팁을 표시합니다.
            """
            nonlocal tooltip
            x, y, _, _ = widget.bbox("insert")
            x += widget.winfo_rootx() + 25
            y += widget.winfo_rooty() + 20
            
            # 툴팁 창 생성
            tooltip = tk.Toplevel(widget)
            tooltip.wm_overrideredirect(True)
            tooltip.wm_geometry(f"+{x}+{y}")
            
            label = ttk.Label(tooltip, text=text, justify=tk.LEFT,
                             background="#ffffe0", relief="solid", borderwidth=1,
                             wraplength=250)
            label.pack(padx=3, pady=3)
            
        def leave(event):
            """
            핵심: 위젯에서 마우스가 나갈 때 툴팁을 숨깁니다.
            """
            nonlocal tooltip
            if tooltip:
                tooltip.destroy()
                tooltip = None
                
        widget.bind("<Enter>", enter)
        widget.bind("<Leave>", leave)


class ScrollableFrame:
    """
    핵심: 필요할 때 자동으로 스크롤바가 나타나는 사용자 정의 프레임.
    """
    
    def __init__(self, parent, **kwargs):
        """
        핵심: 선택적 스크롤바가 있는 프레임을 생성합니다.
        
        매개변수:
            parent: 부모 위젯
            **kwargs: 프레임에 대한 추가 인수
        """
        self.parent = parent
        
        # 캔버스와 스크롤바가 있는 프레임 생성
        self.frame = ttk.Frame(parent)
        self.frame.pack(fill=tk.BOTH, expand=True, **kwargs)
        
        # 수평 스크롤바 생성
        self.h_scrollbar = ttk.Scrollbar(self.frame, orient=tk.HORIZONTAL)
        self.h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # 수직 스크롤바 생성
        self.v_scrollbar = ttk.Scrollbar(self.frame)
        self.v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 캔버스 생성
        self.canvas = tk.Canvas(self.frame, 
                               xscrollcommand=self.h_scrollbar.set,
                               yscrollcommand=self.v_scrollbar.set)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # 스크롤바 설정
        self.h_scrollbar.config(command=self.canvas.xview)
        self.v_scrollbar.config(command=self.canvas.yview)
        
        # 캔버스 내부에 프레임 생성
        self.content_frame = ttk.Frame(self.canvas)
        self.canvas_window = self.canvas.create_window((0, 0), window=self.content_frame, anchor=tk.NW)
        
        # 스크롤을 위한 이벤트 바인딩
        self.content_frame.bind("<Configure>", self._on_frame_configure)
        self.canvas.bind("<Configure>", self._on_canvas_configure)
    
    def _on_frame_configure(self, event=None):
        """
        핵심: 내부 프레임의 크기가 변경될 때 스크롤 영역을 업데이트합니다.
        """
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
    
    def _on_canvas_configure(self, event=None):
        """
        핵심: 캔버스 크기가 변경될 때 내부 프레임의 크기를 조정합니다.
        """
        canvas_width = event.width
        self.canvas.itemconfig(self.canvas_window, width=canvas_width)
    
    def get_frame(self):
        """
        핵심: 위젯을 추가하기 위한 콘텐츠 프레임을 가져옵니다.
        """
        return self.content_frame


class TableView:
    """
    핵심: Treeview를 사용하여 표 형식 데이터를 표시하는 위젯.
    """
    
    def __init__(self, parent, columns=None, show_row_numbers=True):
        """
        핵심: 테이블 뷰 위젯을 생성합니다.
        
        매개변수:
            parent: 부모 위젯
            columns: 열 이름 목록
            show_row_numbers: 행 번호 표시 여부
        """
        self.parent = parent
        self.columns = columns or []
        self.show_row_numbers = show_row_numbers
        
        # 스크롤바가 있는 프레임 생성
        self.frame = ttk.Frame(parent)
        
        # 수평 스크롤바 생성
        h_scrollbar = ttk.Scrollbar(self.frame, orient=tk.HORIZONTAL)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # 수직 스크롤바 생성
        v_scrollbar = ttk.Scrollbar(self.frame)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 트리뷰 생성
        self.tree = ttk.Treeview(self.frame, 
                               columns=self.columns,
                               xscrollcommand=h_scrollbar.set,
                               yscrollcommand=v_scrollbar.set)
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # 스크롤바 설정
        h_scrollbar.config(command=self.tree.xview)
        v_scrollbar.config(command=self.tree.yview)
        
        # 열 설정
        if show_row_numbers:
            self.tree.column("#0", width=40, stretch=tk.NO)
            self.tree.heading("#0", text="행")
        else:
            self.tree.column("#0", width=0, stretch=tk.NO)
            
        for col in self.columns:
            self.tree.column(col, anchor=tk.W, width=100)
            self.tree.heading(col, text=col)
            
        # 스타일링을 위한 태그 생성
        self.tree.tag_configure("matched", background="#e6ffe6")  # 일치하는 행을 위한 연한 녹색
        self.tree.tag_configure("unmatched", background="#fff0f0")  # 일치하지 않는 행을 위한 연한 빨간색
    
    def clear(self):
        """
        핵심: 테이블에서 모든 항목을 지웁니다.
        """
        for item in self.tree.get_children():
            self.tree.delete(item)
    
    def add_row(self, values, row_num=None, tags=None):
        """
        핵심: 테이블에 행을 추가합니다.
        
        매개변수:
            values: 행의 값 목록
            row_num: 표시할 행 번호 (None인 경우 자동 증가)
            tags: 행 스타일링을 위한 태그
        """
        # 태그 매개변수가 None이 아닌 경우에만 포함
        if tags is None:
            if self.show_row_numbers:
                return self.tree.insert("", tk.END, text=str(row_num) if row_num is not None else "", values=values)
            else:
                return self.tree.insert("", tk.END, text="", values=values)
        else:
            if self.show_row_numbers:
                return self.tree.insert("", tk.END, text=str(row_num) if row_num is not None else "", values=values, tags=tags)
            else:
                return self.tree.insert("", tk.END, text="", values=values, tags=tags)
    
    def pack(self, **kwargs):
        """
        핵심: 프레임을 패킹합니다.
        """
        self.frame.pack(**kwargs)
        
    def grid(self, **kwargs):
        """
        핵심: 프레임을 그리드 배치합니다.
        """
        self.frame.grid(**kwargs)


class ExplanationText(scrolledtext.ScrolledText):
    """
    핵심: 스타일이 지정된 텍스트를 지원하는 향상된 ScrolledText 위젯.
    """
    
    def __init__(self, parent, **kwargs):
        """
        핵심: 설명 텍스트 위젯을 초기화합니다.
        """
        super().__init__(parent, **kwargs)
        
        # 스타일링을 위한 태그 설정
        self.tag_configure("title", font=("TkDefaultFont", 12, "bold"))
        self.tag_configure("row_header", font=("TkDefaultFont", 10, "bold"))
        self.tag_configure("explanation", font=("TkDefaultFont", 10))
        self.tag_configure("included", foreground="green")
        self.tag_configure("excluded", foreground="red")
        
    def add_title(self, text):
        """
        핵심: 설명에 제목을 추가합니다.
        """
        self.insert(tk.END, text, "title")
        
    def add_row_header(self, text):
        """
        핵심: 설명에 행 헤더를 추가합니다.
        """
        self.insert(tk.END, text, "row_header")
        
    def add_explanation(self, text):
        """
        핵심: 설명 텍스트를 추가합니다.
        """
        self.insert(tk.END, text, "explanation")
        
    def add_included(self, text):
        """
        핵심: 결과에 포함되었음을 나타내는 텍스트를 추가합니다.
        """
        self.insert(tk.END, text, "included")
        
    def add_excluded(self, text):
        """
        핵심: 결과에서 제외되었음을 나타내는 텍스트를 추가합니다.
        """
        self.insert(tk.END, text, "excluded")
        
    def set_read_only(self, read_only=True):
        """
        핵심: 위젯을 읽기 전용 모드로 설정합니다.
        """
        if read_only:
            self.config(state=tk.DISABLED)
        else:
            self.config(state=tk.NORMAL)
