"""
참조를 위해 새 창에서 입력 테이블을 표시합니다.

매개변수:
root: 루트 창
table_a: 테이블 A 데이터
table_b: 테이블 B 데이터
"""
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from typing import Callable, Dict, Any
import models
import widgets


class InputPanel:
    """
    핵심: 사용자 입력 설정을 위한 패널.
    테이블 입력 필드, 조인 구성 및 설명 영역을 포함합니다.
    """
    def __init__(self, parent, on_join_type_change: Callable, on_run_simulation: Callable, on_show_help: Callable):
        """
        핵심:입력 패널을 초기화합니다.
        
        매개변수:
            parent: 부모 위젯
            on_join_type_change: 조인 유형 변경 콜백
            on_run_simulation: 시뮬레이션 실행 콜백
            on_show_help: 도움말 표시 콜백
        """
        self.parent = parent
        self.on_join_type_change = on_join_type_change
        self.on_run_simulation = on_run_simulation
        self.on_show_help = on_show_help
        
        # 메인 프레임 생성
        self.frame = ttk.LabelFrame(parent, text="입력 설정")
        self.frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # UI 구성 함수 호출
        self._setup_tables_frame()
        self._setup_join_config()
        self._setup_explanation_frame()
    def _setup_tables_frame(self):
        """
        핵심: 테이블 입력 섹션을 설정합니다.
        """
        tables_frame = ttk.Frame(self.frame)
        tables_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 테이블 A
        table_a_frame = ttk.LabelFrame(tables_frame, text="테이블 A")
        table_a_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        
        ttk.Label(table_a_frame, text="테이블 A 데이터 입력 (딕셔너리 리스트):").pack(anchor=tk.W, padx=5, pady=2)
        self.table_a_input = scrolledtext.ScrolledText(table_a_frame, height=10, width=40, wrap=tk.WORD)
        self.table_a_input.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        ttk.Label(table_a_frame, text="테이블 A의 조인 키:").pack(anchor=tk.W, padx=5, pady=2)
        self.key_a_input = ttk.Entry(table_a_frame)
        self.key_a_input.pack(fill=tk.X, padx=5, pady=5)
        
        # 테이블 B
        table_b_frame = ttk.LabelFrame(tables_frame, text="테이블 B")
        table_b_frame.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")
        
        ttk.Label(table_b_frame, text="테이블 B 데이터 입력 (딕셔너리 리스트):").pack(anchor=tk.W, padx=5, pady=2)
        self.table_b_input = scrolledtext.ScrolledText(table_b_frame, height=10, width=40, wrap=tk.WORD)
        self.table_b_input.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        ttk.Label(table_b_frame, text="테이블 B의 조인 키:").pack(anchor=tk.W, padx=5, pady=2)
        self.key_b_input = ttk.Entry(table_b_frame)
        self.key_b_input.pack(fill=tk.X, padx=5, pady=5)
        
        # 그리드 가중치 구성
        tables_frame.columnconfigure(0, weight=1)
        tables_frame.columnconfigure(1, weight=1)
        tables_frame.rowconfigure(0, weight=1)
    def _setup_join_config(self):
        """
        핵심: JOIN 구성 섹션을 설정합니다.
        """
        join_config_frame = ttk.Frame(self.frame)
        join_config_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(join_config_frame, text="JOIN 유형 선택:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.join_type = ttk.Combobox(join_config_frame, 
                                    values=["INNER JOIN", "LEFT OUTER JOIN", "RIGHT OUTER JOIN", "FULL OUTER JOIN", "CROSS JOIN"])
        self.join_type.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        self.join_type.configure(width=30)
        self.join_type.current(0)  # 기본은 INNER JOIN
        self.join_type.bind("<<ComboboxSelected>>", self.on_join_type_change)
        
        # 실행 버튼
        self.run_button = ttk.Button(join_config_frame, text="JOIN 시뮬레이션 실행", command=self.on_run_simulation)
        self.run_button.grid(row=0, column=2, padx=5, pady=5, sticky="ew")
        
        # 도움말 버튼
        help_button = ttk.Button(join_config_frame, text="도움말", command=self.on_show_help)
        help_button.grid(row=0, column=3, padx=5, pady=5, sticky="ew")
        
        # 그리드 가중치 구성
        join_config_frame.columnconfigure(0, weight=0)  # Label - fixed size
        join_config_frame.columnconfigure(1, weight=1, minsize=300)  # Combobox - controlled expansion
        join_config_frame.columnconfigure(2, weight=0, minsize=150)  # Run button - fixed minimum size
        join_config_frame.columnconfigure(3, weight=0, minsize=100)  # Help button - fixed minimum size
        
        # 버튼의 최소 너비 설정
        self.run_button.config(width=20)
        help_button.config(width=10)
    
    def _setup_explanation_frame(self):
        """
        핵심: JOIN 유형에 대한 설명을 표시하는 프레임입니다.
        """
        self.explanation_frame = ttk.LabelFrame(self.frame, text="JOIN 유형 설명")
        self.explanation_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.explanation_text = scrolledtext.ScrolledText(self.explanation_frame, height=6, wrap=tk.WORD)
        self.explanation_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.explanation_text.insert(tk.END, models.JoinDescriptions.DESCRIPTIONS["INNER JOIN"]["text"])
        self.explanation_text.config(state=tk.DISABLED)
    def update_explanation(self, join_type):
        """
        핵심: JOIN 유형에 따라 설명 텍스트를 업데이트합니다.
        
        매개변수:
            join_type: JOIN의 유형
        """
        explanation = models.JoinDescriptions.DESCRIPTIONS.get(join_type, {"text": "설명이 없습니다."})
        
        self.explanation_text.config(state=tk.NORMAL)
        self.explanation_text.delete(1.0, tk.END)
        self.explanation_text.insert(tk.END, explanation["text"])
        self.explanation_text.config(state=tk.DISABLED)
    def get_table_a_input(self):
        """
        핵심: 테이블 A 입력의 텍스트 내용을 가져옵니다.
        """
        return self.table_a_input.get(1.0, tk.END)
    
    def get_table_b_input(self):
        """
        핵심: 테이블 B 입력의 텍스트 내용을 가져옵니다.
        """
        return self.table_b_input.get(1.0, tk.END)
    
    def get_key_a(self):
        """
        핵심: 테이블 A의 조인 키를 가져옵니다.
        """
        return self.key_a_input.get().strip()
    
    def get_key_b(self):
        """
        핵심: 테이블 B의 조인 키를 가져옵니다.
        """
        return self.key_b_input.get().strip()
    
    def get_join_type(self):
        """
        핵심: 선택된 JOIN 유형을 가져옵니다.
        """
        return self.join_type.get()
    
    def set_table_a_input(self, text):
        """
        핵심: 테이블 A 입력의 텍스트 내용을 설정합니다.
        """
        self.table_a_input.delete(1.0, tk.END)
        self.table_a_input.insert(tk.END, text)
    
    def set_table_b_input(self, text):
        """
        핵심: 테이블 B 입력의 텍스트 내용을 설정합니다.
        """
        self.table_b_input.delete(1.0, tk.END)
        self.table_b_input.insert(tk.END, text)
    
    def set_key_a(self, text):
        """
        핵심: 테이블 A의 조인 키를 설정합니다.
        """
        self.key_a_input.delete(0, tk.END)
        self.key_a_input.insert(0, text)
    
    def set_key_b(self, text):
        """
        핵심: 테이블 B의 조인 키를 설정합니다.
        """
        self.key_b_input.delete(0, tk.END)
        self.key_b_input.insert(0, text)


class OutputPanel:
    """
    핵심: JOIN 연산의 출력을 표시하기 위한 패널.
    카티션 곱, JOIN 결과, JOIN 설명 및 애니메이션을 위한 탭을 포함합니다.
    """
    
    def __init__(self, parent, on_prev_step: Callable, on_next_step: Callable):
        """
        핵심: 출력 패널을 초기화합니다.
        
        매개변수:
            parent: 부모 위젯
            on_prev_step: 이전 애니메이션 단계를 위한 콜백
            on_next_step: 다음 애니메이션 단계를 위한 콜백
        """
        self.parent = parent
        self.on_prev_step = on_prev_step
        self.on_next_step = on_next_step
        
        # 메인 프레임 생성
        self.frame = ttk.LabelFrame(parent, text="JOIN 시각화")
        self.frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 탭 생성
        self._setup_tabs()
        self._setup_cartesian_tab()
        self._setup_join_result_tab()
        self._setup_explanation_tab()
        self._setup_animation_tab()
    
    def _setup_tabs(self):
        """
        핵심: 다양한 시각화를 위한 탭을 설정합니다.
        """
        self.output_tabs = ttk.Notebook(self.frame)
        self.output_tabs.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 탭 생성
        self.tab_cartesian = ttk.Frame(self.output_tabs)
        self.tab_join_result = ttk.Frame(self.output_tabs)
        self.tab_explanation = ttk.Frame(self.output_tabs)
        self.tab_animation = ttk.Frame(self.output_tabs)
        
        self.output_tabs.add(self.tab_cartesian, text="카티션 곱")
        self.output_tabs.add(self.tab_join_result, text="JOIN 결과")
        self.output_tabs.add(self.tab_explanation, text="JOIN 설명")
        self.output_tabs.add(self.tab_animation, text="단계별 애니메이션")
    
    def _setup_cartesian_tab(self):
        """
        핵심: 카티션 곱 탭을 설정합니다.
        """
        self.cartesian_frame = ttk.Frame(self.tab_cartesian)
        self.cartesian_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 툴팁 정보 추가
        self.cartesian_info = ttk.Label(self.tab_cartesian, text="""        
카티션 곱(Cartesian product)은 테이블 A와 테이블 B의 모든 행 조합을 보여줍니다.
이는 모든 JOIN 연산의 기초가 됩니다. JOIN은 특정 조건에 따라 이 곱을 필터링합니다.
        """, wraplength=800, justify=tk.LEFT)
        self.cartesian_info.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
    
    def _setup_join_result_tab(self):
        """
        핵심: JOIN 결과 탭을 설정합니다.
        """
        self.join_result_frame = ttk.Frame(self.tab_join_result)
        self.join_result_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    
    def _setup_explanation_tab(self):
        """
        핵심: JOIN 설명 탭을 설정합니다.
        """
        self.explanation_result_frame = ttk.Frame(self.tab_explanation)
        self.explanation_result_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    
    def _setup_animation_tab(self):
        """
        핵심: 애니메이션 탭을 설정합니다.
        """
        self.animation_frame = ttk.Frame(self.tab_animation)
        self.animation_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 애니메이션 컨트롤
        self.animation_controls = ttk.Frame(self.tab_animation)
        self.animation_controls.pack(fill=tk.X, side=tk.BOTTOM, padx=5, pady=5)
        
        self.prev_button = ttk.Button(self.animation_controls, text="이전 단계", command=self.on_prev_step)
        self.prev_button.pack(side=tk.LEFT, padx=5, pady=5)
        
        self.next_button = ttk.Button(self.animation_controls, text="다음 단계", command=self.on_next_step)
        self.next_button.pack(side=tk.LEFT, padx=5, pady=5)
        
        self.step_label = ttk.Label(self.animation_controls, text="단계 0/0")
        self.step_label.pack(side=tk.LEFT, padx=5, pady=5)
    
    def select_tab(self, index):
        """
        핵심: 특정 탭을 선택합니다.
        
        매개변수:
            index: 선택할 탭의 인덱스
        """
        self.output_tabs.select(index)
    
    def get_cartesian_frame(self):
        """
        핵심: 카티션 곱 시각화를 위한 프레임을 가져옵니다.
        """
        return self.cartesian_frame
    
    def get_join_result_frame(self):
        """
        핵심: JOIN 결과 시각화를 위한 프레임을 가져옵니다.
        """
        return self.join_result_frame
    
    def get_explanation_frame(self):
        """
        핵심: JOIN 설명 시각화를 위한 프레임을 가져옵니다.
        """
        return self.explanation_result_frame
    
    def get_animation_frame(self):
        """
        핵심: 애니메이션 시각화를 위한 프레임을 가져옵니다.
        """
        return self.animation_frame
    
    def get_step_label(self):
        """
        핵심: 애니메이션 단계 레이블을 가져옵니다.
        """
        return self.step_label


class HelpDialog:
    """
    핵심: 도움말 정보를 표시하기 위한 대화 상자입니다.
    """
    
    @staticmethod
    def show(parent, help_text):
        """
        핵심: 도움말 대화 상자를 표시합니다.
        
        매개변수:
            parent: 부모 위젯
            help_text: 표시할 도움말 텍스트
        """
        help_window = tk.Toplevel(parent)
        help_window.title("SQL JOIN Visualizer 도움말")
        help_window.geometry("600x500")
        
        text_widget = scrolledtext.ScrolledText(help_window, wrap=tk.WORD)
        text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        text_widget.insert(tk.END, help_text)
        text_widget.configure(state="disabled")


class ResultDisplayManager:
    """
    핵심: 출력 패널에 결과 표시를 관리합니다.
    """
    
    @staticmethod
    def display_cartesian_product(parent_frame, cartesian_product, key_a, key_b, join_type):
        """
        핵심: 일치하는 행에 대한 강조 표시와 함께 카티션 곱을 그리드에 표시합니다.
        
        매개변수:
            parent_frame: 표시할 프레임
            cartesian_product: 카티션 곱 데이터
            key_a: 테이블 A의 조인 키
            key_b: 테이블 B의 조인 키
            join_type: JOIN의 유형
        """
        # 이전 내용 지우기
        for widget in parent_frame.winfo_children():
            widget.destroy()
            
        # 스크롤 가능한 프레임 생성
        scrollable = widgets.ScrollableFrame(parent_frame)
        content_frame = scrollable.get_frame()
        
        # 헤더 추가
        ttk.Label(content_frame, text="카르테시안 곱 시각화", font=("TkDefaultFont", 12, "bold")).grid(
            row=0, column=0, columnspan=3, pady=10, sticky=tk.W)
        
        # 열 헤더
        ttk.Label(content_frame, text="행 A", font=("TkDefaultFont", 10, "bold")).grid(
            row=1, column=0, padx=10, pady=5, sticky=tk.W)
        ttk.Label(content_frame, text="행 B", font=("TkDefaultFont", 10, "bold")).grid(
            row=1, column=1, padx=10, pady=5, sticky=tk.W)
        ttk.Label(content_frame, text="일치 여부", font=("TkDefaultFont", 10, "bold")).grid(
            row=1, column=2, padx=10, pady=5, sticky=tk.W)
        
        # 카티션 곱에서 각 쌍 표시
        for i, (row_a, row_b) in enumerate(cartesian_product):
            # 행 데이터 형식화
            row_a_str = ", ".join([f"{k}: {v}" for k, v in row_a.items()])
            row_b_str = ", ".join([f"{k}: {v}" for k, v in row_b.items()])
            
            # 이 행이 JOIN 결과에 포함되는지 확인
            matched = False
            match_explanation = ""
            
            if join_type == "CROSS JOIN":
                matched = True
                match_explanation = "모든 행이 CROSS JOIN에 포함됩니다. 키에 관계없이 모든 행이 포함됩니다."
            elif key_a in row_a and key_b in row_b:
                if row_a[key_a] == row_b[key_b]:
                    matched = True
                    match_explanation = f"키가 일치합니다: {key_a}={row_a[key_a]}는 {key_b}={row_b[key_b]}와 같습니다."
                else:
                    match_explanation = f"키가 일치하지 않습니다: {key_a}={row_a[key_a]}는 {key_b}={row_b[key_b]}와 같지 않습니다."
            else:
                if key_a not in row_a:
                    match_explanation = f"행 A에 키 {key_a}가 없습니다."
                elif key_b not in row_b:
                    match_explanation = f"행 B에 키 {key_b}가 없습니다."
            
            # Create frame for this row and set background color
            row_frame = ttk.Frame(content_frame)
            row_frame.grid(row=i+2, column=0, columnspan=3, padx=5, pady=2, sticky=tk.W+tk.E)
            
            # 일치하는 행에 대한 특정 스타일 사용
            bg_color = "#e6ffe6" if matched else "#fff0f0"  # 일치하는 경우 연한 녹색, 일치하지 않는 경우 연한 빨강색
            
            # 배경색이 있는 레이블 사용
            cell_a = tk.Label(row_frame, text=row_a_str, anchor=tk.W, bg=bg_color)
            cell_a.grid(row=0, column=0, padx=5, pady=2, sticky=tk.W)
            
            cell_b = tk.Label(row_frame, text=row_b_str, anchor=tk.W, bg=bg_color)
            cell_b.grid(row=0, column=1, padx=5, pady=2, sticky=tk.W)
            
            # 일치 상태에 대한 체크/십자 표시 사용
            match_text = "✅" if matched else "❌"
            cell_match = tk.Label(row_frame, text=match_text, anchor=tk.W, bg=bg_color, font=("TkDefaultFont", 10, "bold"))
            cell_match.grid(row=0, column=2, padx=5, pady=2, sticky=tk.W)
            
            # 일치 설명에 대한 툴팁 추가
            widgets.TooltipManager.create_tooltip(cell_match, match_explanation)
            
            # 그리드 구성
            row_frame.columnconfigure(0, weight=1, minsize=200)
            row_frame.columnconfigure(1, weight=1, minsize=200)
            row_frame.columnconfigure(2, weight=0, minsize=50)
    
    @staticmethod
    def display_join_result(parent_frame, join_result):
        """
        핵심: JOIN 결과를 테이블에 표시합니다.
        
        매개변수:
            parent_frame: 표시할 프레임
            join_result: JOIN 결과 데이터
        """
        # 이전 내용 지우기
        for widget in parent_frame.winfo_children():
            widget.destroy()
        
        if not join_result:
            ttk.Label(parent_frame, text="표시할 결과가 없습니다").pack(pady=20)
            return
        
        # 테이블 표시를 위한 트리뷰 생성
        tree_frame = ttk.Frame(parent_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        # 수평 스크롤바 생성
        h_scrollbar = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # 수직 스크롤바 생성
        v_scrollbar = ttk.Scrollbar(tree_frame)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 트리뷰 생성
        tree = ttk.Treeview(tree_frame, xscrollcommand=h_scrollbar.set, yscrollcommand=v_scrollbar.set)
        tree.pack(fill=tk.BOTH, expand=True)
        
        # 스크롤바 구성
        h_scrollbar.config(command=tree.xview)
        v_scrollbar.config(command=tree.yview)
        
        # 열 정의
        columns = list(join_result[0][0].keys()) if join_result else []
        tree["columns"] = columns
        tree.column("#0", width=40, stretch=tk.NO)
        tree.heading("#0", text="행")
        
        for col in columns:
            tree.column(col, anchor=tk.W, width=100)
            tree.heading(col, text=col)
        
        # 트리뷰에 데이터 추가
        for i, (row, matched) in enumerate(join_result):
            values = [row.get(col, "") for col in columns]
            item_id = tree.insert("", tk.END, text=str(i+1), values=values)
            
            # 색상 지정
            if not matched:
                tree.tag_configure("unmatched", background="#fff0f0")  # 일치하지 않는 행은 연한 빨강색
                tree.item(item_id, tags=("unmatched",))
            else:
                tree.tag_configure("matched", background="#e6ffe6")  # 일치하는 행은 연한 녹색
                tree.item(item_id, tags=("matched",))
        
        # 요약 정보 추가
        matched_count = sum(1 for _, matched in join_result if matched)
        unmatched_count = len(join_result) - matched_count
        
        summary_frame = ttk.Frame(parent_frame)
        summary_frame.pack(fill=tk.X, pady=10)
        
        summary_text = f"결과 총 {len(join_result)}개 행 " + \
                      f"({matched_count}개 직접 일치, {unmatched_count}개 OUTER JOIN으로 추가)"
        
        ttk.Label(summary_frame, text=summary_text).pack(anchor=tk.W, padx=10)
    
    @staticmethod
    def display_join_explanation(parent_frame, cartesian_product, key_a, key_b, join_type):
        """
        핵심: JOIN 결과에 행이 포함되거나 제외되는 이유에 대한 자세한 설명을 표시합니다.
        
        매개변수:
            parent_frame: 표시할 프레임
            cartesian_product: 카티션 곱 데이터
            key_a: 테이블 A의 조인 키
            key_b: 테이블 B의 조인 키
            join_type: JOIN의 유형
        """
        # 이전 내용 지우기
        for widget in parent_frame.winfo_children():
            widget.destroy()
        
        # 설명을 위한 스크롤 텍스트 위젯 생성
        explanation_text = widgets.ExplanationText(parent_frame, wrap=tk.WORD)
        explanation_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 제목 추가
        explanation_text.add_title(f"{join_type}에 대한 자세한 설명\n\n")
        
        # 사전 계산: 일치하는 행 식별
        matched_a_ids = set()
        matched_b_ids = set()
        unmatched_a_ids = set()
        unmatched_b_ids = set()
        
        # 각 테이블에서 고유한 행 추적
        unique_rows_a = []
        unique_rows_b = []
        seen_a_ids = set()
        seen_b_ids = set()
        
        for row_a, row_b in cartesian_product:
            # 고유 행 추적
            if id(row_a) not in seen_a_ids:
                seen_a_ids.add(id(row_a))
                unique_rows_a.append(row_a)
                
            if id(row_b) not in seen_b_ids:
                seen_b_ids.add(id(row_b))
                unique_rows_b.append(row_b)
                
            # 일치하는 행 식별
            if join_type != "CROSS JOIN" and key_a in row_a and key_b in row_b and row_a[key_a] == row_b[key_b]:
                matched_a_ids.add(id(row_a))
                matched_b_ids.add(id(row_b))
        
        # 일치하지 않는 행 식별
        for row_a in unique_rows_a:
            if id(row_a) not in matched_a_ids:
                unmatched_a_ids.add(id(row_a))
                
        for row_b in unique_rows_b:
            if id(row_b) not in matched_b_ids:
                unmatched_b_ids.add(id(row_b))
        
        # 행 수 및 설명된 조합 추적
        included_count = 0
        explained_rows = set()  # 이미 설명된 고유한 행 조합 추적
        processed_unmatched_a = set()  # 이미 처리된 일치하지 않는 A 행 추적
        processed_unmatched_b = set()  # 이미 처리된 일치하지 않는 B 행 추적
        
        # 첫 번째 단계: 모든 직접 일치 설명
        for i, (row_a, row_b) in enumerate(cartesian_product):
            # 행 데이터 형식화
            row_a_str = ", ".join([f"{k}: {v}" for k, v in row_a.items()])
            row_b_str = ", ".join([f"{k}: {v}" for k, v in row_b.items()])
            
            # 이 조합이 이미 설명되었는지 확인
            pair_key = (id(row_a), id(row_b))
            if pair_key in explained_rows:
                continue
                
            # CROSS JOIN 또는 일치하는 키 처리
            if join_type == "CROSS JOIN" or (key_a in row_a and key_b in row_b and row_a[key_a] == row_b[key_b]):
                # 행 헤더 추가
                explanation_text.add_row_header(f"행 {i+1}: 비교 중\n")
                explanation_text.add_explanation(f"   테이블 A: {{{row_a_str}}}\n")
                explanation_text.add_explanation(f"   테이블 B: {{{row_b_str}}}\n")
                
                if join_type == "CROSS JOIN":
                    explanation = "모든 조합이 CROSS JOIN에 포함됩니다."
                else:
                    a_value = row_a[key_a]
                    b_value = row_b[key_b]
                    explanation = f"{key_a}={a_value}와 {key_b}={b_value} 비교: 일치합니다! 키가 일치하므로 {join_type}에 이 행이 포함됩니다."
                
                explanation_text.add_included(f"   결과: {explanation}\n")
                explanation_text.add_included(f"   → 결과에 행 포함\n\n")
                explained_rows.add(pair_key)
                included_count += 1
                continue
                
            # 키가 일치하지 않음, INNER JOIN의 일부 아님
            if join_type == "INNER JOIN":
                # 행 헤더 추가
                explanation_text.add_row_header(f"행 {i+1}: 비교 중\n")
                explanation_text.add_explanation(f"   테이블 A: {{{row_a_str}}}\n")
                explanation_text.add_explanation(f"   테이블 B: {{{row_b_str}}}\n")
                
                explanation = ""
                if key_a not in row_a:
                    explanation = f"행 A에 키 {key_a}가 없습니다. "
                elif key_b not in row_b:
                    explanation = f"행 B에 키 {key_b}가 없습니다. "
                else:
                    a_value = row_a[key_a]
                    b_value = row_b[key_b]
                    explanation = f"{key_a}={a_value}와 {key_b}={b_value} 비교: 일치하지 않습니다. 키가 일치하지 않으므로 이 행은 INNER JOIN에서 제외됩니다."
                
                explanation_text.add_excluded(f"   결과: {explanation}\n")
                explanation_text.add_excluded(f"   → 결과에서 행 제외\n\n")
                explained_rows.add(pair_key)
        
        # 두 번째 단계: OUTER JOIN에 대한 일치하지 않는 행 처리
        # LEFT OUTER JOIN 일치하지 않는 A 행
        if join_type in ["LEFT OUTER JOIN", "FULL OUTER JOIN"]:
            for row_a in unique_rows_a:
                if id(row_a) in unmatched_a_ids and id(row_a) not in processed_unmatched_a:
                    row_a_str = ", ".join([f"{k}: {v}" for k, v in row_a.items()])
                    
                    explanation_text.add_row_header(f"LEFT JOIN 추가 행: 일치하지 않는 A 행\n")
                    explanation_text.add_explanation(f"   테이블 A: {{{row_a_str}}}\n")
                    explanation_text.add_explanation(f"   테이블 B: NULL 값\n")
                    
                    explanation = f"테이블 A의 행이 테이블 B의 어떤 행과도 일치하지 않아 NULL 값으로 채워진 B 열과 함께 결과에 포함됩니다."
                    
                    explanation_text.add_included(f"   결과: {explanation}\n")
                    explanation_text.add_included(f"   → 결과에 행 포함 (NULL 채움)\n\n")
                    
                    processed_unmatched_a.add(id(row_a))
                    included_count += 1
        
        # RIGHT OUTER JOIN 일치하지 않는 B 행
        if join_type in ["RIGHT OUTER JOIN", "FULL OUTER JOIN"]:
            for row_b in unique_rows_b:
                if id(row_b) in unmatched_b_ids and id(row_b) not in processed_unmatched_b:
                    row_b_str = ", ".join([f"{k}: {v}" for k, v in row_b.items()])
                    
                    explanation_text.add_row_header(f"RIGHT JOIN 추가 행: 일치하지 않는 B 행\n")
                    explanation_text.add_explanation(f"   테이블 A: NULL 값\n")
                    explanation_text.add_explanation(f"   테이블 B: {{{row_b_str}}}\n")
                    
                    explanation = f"테이블 B의 행이 테이블 A의 어떤 행과도 일치하지 않아 NULL 값으로 채워진 A 열과 함께 결과에 포함됩니다."
                    
                    explanation_text.add_included(f"   결과: {explanation}\n")
                    explanation_text.add_included(f"   → 결과에 행 포함 (NULL 채움)\n\n")
                    
                    processed_unmatched_b.add(id(row_b))
                    included_count += 1
        
        # 마지막에 요약 추가
        explanation_text.add_row_header(f"\n요약: {included_count}개의 고유한 행이 {join_type} 결과에 포함되었습니다.\n")
        
        # 읽기 전용으로 설정
        explanation_text.set_read_only(True)
    
    @staticmethod
    def display_tables(root, table_a, table_b):
        """
        핵심: 참조를 위해 새 창에서 입력 테이블을 표시합니다.

        매개변수:
            root: 루트 창
            table_a: 테이블 A 데이터
            table_b: 테이블 B 데이터
        """
        tables_window = tk.Toplevel(root)
        tables_window.title("입력 테이블")
        tables_window.geometry("800x400")
        
        # 테이블 A 표시
        frame_a = ttk.LabelFrame(tables_window, text="테이블 A")
        frame_a.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 테이블 A에 대한 TableView 생성
        table_view_a = widgets.TableView(frame_a, columns=list(table_a[0].keys()) if table_a else [])
        table_view_a.pack(fill=tk.BOTH, expand=True)
        
        # 테이블 A에 데이터 추가
        for i, row in enumerate(table_a):
            values = [row.get(col, "") for col in table_view_a.columns]
            table_view_a.add_row(values, i)
        
        # 테이블 B 표시
        frame_b = ttk.LabelFrame(tables_window, text="테이블 B")
        frame_b.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 테이블 B에 대한 TableView 생성
        table_view_b = widgets.TableView(frame_b, columns=list(table_b[0].keys()) if table_b else [])
        table_view_b.pack(fill=tk.BOTH, expand=True)
        
        # 테이블 B에 데이터 추가
        for i, row in enumerate(table_b):
            values = [row.get(col, "") for col in table_view_b.columns]
            table_view_b.add_row(values, i)