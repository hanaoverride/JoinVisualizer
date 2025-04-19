from tkinter import ttk
import tkinter as tk
from typing import List, Dict, Any, Tuple, Callable
from join_engine import JoinEngine
import utils

"""
핵심: JOIN 연산의 단계별 애니메이션을 관리하는 클래스입니다.
"""

class AnimationManager:
    """
    핵심 : JOIN 연산의 단계별 애니메이션을 관리합니다.
    
    주요 기능:
    - JOIN 연산의 각 단계를 시각적으로 보여주는 애니메이션 생성
    - 단계별 프레임 관리 및 렌더링
    - 다양한 JOIN 유형에 대한 시각적 설명 제공
    - 사용자 인터페이스 상호작용 처리
    """
    def __init__(self, parent_frame, step_label):
        """
        핵심 : 애니메이션 관리자를 초기화합니다.
        
        매개변수:
            parent_frame: 애니메이션 프레임을 표시할 상위 프레임
            step_label: 현재 단계 정보를 표시할 레이블
        """
        self.parent_frame = parent_frame
        self.step_label = step_label
        self.animation_frames = []
        self.current_step = 0
        self.animation_active = False
        
    def setup_step_animation(self, cartesian_product: List[Tuple[Dict, Dict]], 
                         key_a: str, key_b: str, join_type: str, 
                         callback_show_results: Callable = None):
        """
        핵심 : JOIN 프로세스의 단계별 애니메이션을 설정합니다.
        
        매개변수:
            cartesian_product: 카르테시안 곱에서 생성된 튜플 리스트
            key_a: 테이블 A의 JOIN 키
            key_b: 테이블 B의 JOIN 키
            join_type: JOIN 유형 (INNER, LEFT, RIGHT, FULL, CROSS)
            callback_show_results: 결과 탭을 표시하기 위한 선택적 콜백 함수
        """
        # 기존 프레임 제거
        for frame in self.animation_frames:
            frame.destroy()
        self.animation_frames = []
        
        # 카르테시안 곱에서 테이블 추출
        table_a, table_b = [], []
        seen_a, seen_b = set(), set()
        
        for row_a, row_b in cartesian_product:
            if id(row_a) not in seen_a:
                seen_a.add(id(row_a))
                table_a.append(row_a)
            if id(row_b) not in seen_b:
                seen_b.add(id(row_b))
                table_b.append(row_b)
        
        # 프레임 0 생성: 초기 상태 - 두 테이블을 별도로 표시
        initial_frame = self._create_initial_frame(table_a, table_b, join_type)
        self.animation_frames.append(initial_frame)
        
        # 프레임 1 생성: 카르테시안 곱 설명
        cartesian_frame = self._create_cartesian_frame(cartesian_product, table_a, table_b)
        self.animation_frames.append(cartesian_frame)
        
        # 프레임 2 생성: JOIN 유형 설명
        join_explanation_frame = self._create_join_explanation_frame(join_type, key_a, key_b)
        self.animation_frames.append(join_explanation_frame)
        
        # 프레임 3+ 생성: 개별 행 평가
        max_rows = min(10, len(cartesian_product))  # 성능을 위해 10개 프레임으로 제한
        for i in range(max_rows):
            row_frame = self._create_row_evaluation_frame(
                i, cartesian_product[i][0], cartesian_product[i][1], 
                key_a, key_b, join_type, cartesian_product
            )
            self.animation_frames.append(row_frame)
        
        # 최종 프레임 생성: 요약
        summary_frame = self._create_summary_frame(
            cartesian_product, key_a, key_b, join_type, callback_show_results
        )
        self.animation_frames.append(summary_frame)
        
        # 애니메이션 상태 초기화
        self.current_step = 0
        self.animation_active = True
        self.show_animation_frame(0)
        
        # 단계 레이블 업데이트
        self.step_label.config(text=f"단계 1/{len(self.animation_frames)}")
        
    def _create_initial_frame(self, table_a, table_b, join_type):
        """
        핵심 : 두 테이블을 개별적으로 보여주는 초기 프레임을 생성합니다.
        
        매개변수:
            table_a: 테이블 A의 데이터
            table_b: 테이블 B의 데이터
            join_type: JOIN 유형
            
        반환값:
            생성된 프레임
        """
        frame = ttk.Frame(self.parent_frame)
        
        ttk.Label(frame, text="단계 1: 두 개의 별도 테이블로 시작", 
                font=("TkDefaultFont", 12, "bold")).pack(pady=10)
        
        tables_frame = ttk.Frame(frame)
        tables_frame.pack(fill=tk.BOTH, expand=True)
        
        # 테이블 A
        table_a_frame = ttk.LabelFrame(tables_frame, text="테이블 A")
        table_a_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)
        
        self._create_table_display(table_a_frame, table_a)
        
        # 테이블 B
        table_b_frame = ttk.LabelFrame(tables_frame, text="테이블 B")
        table_b_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10)
        
        self._create_table_display(table_b_frame, table_b)
        
        # 설명
        explanation = ttk.Label(frame, text=f"이 테이블들 간의 {join_type}를 시각화합니다.",
                              wraplength=600, justify=tk.LEFT)
        explanation.pack(pady=10, fill=tk.X)
        
        return frame
        
    def _create_cartesian_frame(self, cartesian_product, table_a, table_b):
        """
        핵심 : 카르테시안 곱 설명 프레임을 생성합니다.
        
        매개변수:
            cartesian_product: 카르테시안 곱 데이터
            table_a: 테이블 A의 데이터
            table_b: 테이블 B의 데이터
            
        반환값:
            생성된 프레임
        """
        frame = ttk.Frame(self.parent_frame)
        
        ttk.Label(frame, text="단계 2: 카르테시안 곱 형성 (모든 가능한 조합)",
                font=("TkDefaultFont", 12, "bold")).pack(pady=10)
        
        cartesian_explanation = ttk.Label(frame, 
                                        text="카르테시안 곱은 테이블 A의 모든 행을 테이블 B의 모든 행과 결합합니다.\n"
                                             f"테이블 A에 {len(table_a)}개의 행이 있고 테이블 B에 {len(table_b)}개의 행이 있을 때, "
                                             f"{len(table_a) * len(table_b)}개의 조합이 생성됩니다.",
                                        wraplength=600, justify=tk.LEFT)
        cartesian_explanation.pack(pady=10, fill=tk.X)
        
        # 카르테시안 곱의 작은 샘플 표시
        sample_frame = ttk.Frame(frame)
        sample_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # 개념을 설명하기 위한 작은 테이블 생성
        sample_tree = ttk.Treeview(sample_frame)
        sample_tree.pack(fill=tk.BOTH, expand=True)
        
        # 샘플 트리 구성
        sample_tree["columns"] = ["table_a", "table_b"]
        sample_tree.column("#0", width=60, stretch=tk.NO)
        sample_tree.column("table_a", width=200, anchor=tk.W)
        sample_tree.column("table_b", width=200, anchor=tk.W)
        
        sample_tree.heading("#0", text="조합")
        sample_tree.heading("table_a", text="테이블 A 행")
        sample_tree.heading("table_b", text="테이블 B 행")
        
        # 몇 개의 샘플 행 추가
        for i, (row_a, row_b) in enumerate(cartesian_product[:min(5, len(cartesian_product))]):
            row_a_str = utils.format_row_as_string(row_a)
            row_b_str = utils.format_row_as_string(row_b)
            sample_tree.insert("", tk.END, text=f"{i+1}", values=(row_a_str, row_b_str))
        
        if len(cartesian_product) > 5:
            sample_tree.insert("", tk.END, text="...", values=("...", "..."))
        
        return frame
        
    def _create_join_explanation_frame(self, join_type, key_a, key_b):
        """
        핵심 : JOIN 유형 논리를 설명하는 프레임을 생성합니다.
        
        매개변수:
            join_type: JOIN 유형
            key_a: 테이블 A의 JOIN 키
            key_b: 테이블 B의 JOIN 키
            
        반환값:
            생성된 프레임
        """
        from models import JoinDescriptions
        
        frame = ttk.Frame(self.parent_frame)
        
        ttk.Label(frame, text=f"단계 3: {join_type} 필터 로직 적용",
                font=("TkDefaultFont", 12, "bold")).pack(pady=10)
        
        # 모델에서 설명 텍스트 가져오기
        join_text = JoinDescriptions.DESCRIPTIONS[join_type]["text"]
        ttk.Label(frame, text=join_text, wraplength=600, justify=tk.LEFT).pack(pady=10, fill=tk.X)
        
        # JOIN 작동 방식의 시각적 표현
        filter_frame = ttk.Frame(frame)
        filter_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self._create_join_filter_visualization(filter_frame, join_type, key_a, key_b)
        
        return frame
        
    def _create_row_evaluation_frame(self, index, row_a, row_b, key_a, key_b, join_type, cartesian_product):
        """
        핵심 : 단일 행 조합을 평가하기 위한 프레임을 생성합니다.
        
        매개변수:
            index: 행 평가 인덱스
            row_a: 테이블 A의 행
            row_b: 테이블 B의 행
            key_a: 테이블 A의 JOIN 키
            key_b: 테이블 B의 JOIN 키
            join_type: JOIN 유형
            cartesian_product: 카르테시안 곱 데이터
            
        반환값:
            생성된 프레임
        """
        frame = ttk.Frame(self.parent_frame)
        
        ttk.Label(frame, text=f"단계 {index+4}: 행 조합 {index+1} 평가",
                font=("TkDefaultFont", 12, "bold")).pack(pady=10)
        
        # 행 데이터 형식 지정
        row_a_str = utils.format_row_as_string(row_a)
        row_b_str = utils.format_row_as_string(row_b)
        
        ttk.Label(frame, text=f"테이블 A: {{{row_a_str}}}", wraplength=600, justify=tk.LEFT).pack(anchor=tk.W, pady=2)
        ttk.Label(frame, text=f"테이블 B: {{{row_b_str}}}", wraplength=600, justify=tk.LEFT).pack(anchor=tk.W, pady=2)
          # 상세 평가
        matched = self._evaluate_match(row_a, row_b, key_a, key_b, join_type)
        explanation = self._generate_evaluation_explanation(
            row_a, row_b, key_a, key_b, join_type, cartesian_product
        )
        
        # 결과 레이블 (색상 코딩 적용)
        result_text = "결과에 포함됨 ✅" if matched else "결과에서 제외됨 ❌"
        result_color = "#e6ffe6" if matched else "#fff0f0"  # 포함된 경우 녹색, 제외된 경우 빨간색
        
        result_label = tk.Label(frame, text=result_text, bg=result_color, 
                              font=("TkDefaultFont", 10, "bold"), padx=5, pady=5)
        result_label.pack(fill=tk.X, pady=10)
        
        # 설명
        explanation_label = ttk.Label(frame, text=explanation, wraplength=600, justify=tk.LEFT)
        explanation_label.pack(fill=tk.X, pady=5)
        
        return frame
        
    def _create_summary_frame(self, cartesian_product, key_a, key_b, join_type, callback_show_results):
        """
        핵심 : 최종 결과가 포함된 요약 프레임을 생성합니다.
        
        매개변수:
            cartesian_product: 카르테시안 곱 데이터
            key_a: 테이블 A의 JOIN 키
            key_b: 테이블 B의 JOIN 키
            join_type: JOIN 유형
            callback_show_results: 결과 탭을 표시하기 위한 콜백 함수
            
        반환값:
            생성된 프레임
        """
        frame = ttk.Frame(self.parent_frame)
        
        ttk.Label(frame, text=f"최종 단계: {join_type} 결과",
                font=("TkDefaultFont", 12, "bold")).pack(pady=10)
        
        # 일치하는 행 수 세기
        matched_count = self._count_matched_rows(cartesian_product, key_a, key_b, join_type)
        
        summary_text = f"카르테시안 곱의 {len(cartesian_product)}개의 가능한 조합 중:\n\n" \
                      f"- {matched_count}개의 조합이 {join_type} 결과에 직접 포함됩니다.\n"
        
        # OUTER JOIN의 null 행에 대한 설명 추가 (해당되는 경우)
        if join_type in ["LEFT OUTER JOIN", "RIGHT OUTER JOIN", "FULL OUTER JOIN"]:
            unmatched_count = self._count_unmatched_rows(cartesian_product, key_a, key_b, join_type)
            summary_text += f"- {unmatched_count}개의 추가 행이 OUTER JOIN 논리로 인해 NULL 값으로 포함됩니다.\n"
            summary_text += f"\n결과의 총 행 수: {matched_count + unmatched_count}"
        else:
            summary_text += f"\n결과의 총 행 수: {matched_count}"
        
        ttk.Label(frame, text=summary_text, wraplength=600, justify=tk.LEFT).pack(pady=10, fill=tk.X)
        
        # 전체 결과를 보기 위한 버튼 추가
        if callback_show_results:
            view_result_button = ttk.Button(frame, text="전체 결과 보기", command=callback_show_results)
            view_result_button.pack(pady=10)
        
        return frame
        
    def show_animation_frame(self, index):
        """
        핵심 : 애니메이션 시퀀스에서 특정 프레임을 표시합니다.
        
        매개변수:
            index: 표시할 프레임의 인덱스
        """
        if not self.animation_frames:
            return
            
        # 모든 프레임 숨기기
        for frame in self.animation_frames:
            frame.pack_forget()
            
        if 0 <= index < len(self.animation_frames):
            # 요청된 프레임 표시
            self.animation_frames[index].pack(fill=tk.BOTH, expand=True)
            self.current_step = index
            
    def next_animation_step(self):
        """
        핵심 : 애니메이션의 다음 단계로 이동합니다.
        """
        if not self.animation_active or not self.animation_frames:
            return
            
        next_step = min(self.current_step + 1, len(self.animation_frames) - 1)
        self.show_animation_frame(next_step)
        self.step_label.config(text=f"단계 {next_step+1}/{len(self.animation_frames)}")
        
    def prev_animation_step(self):
        """
        핵심 : 애니메이션의 이전 단계로 이동합니다.
        """
        if not self.animation_active or not self.animation_frames:
            return
            
        prev_step = max(self.current_step - 1, 0)
        self.show_animation_frame(prev_step)
        self.step_label.config(text=f"단계 {prev_step+1}/{len(self.animation_frames)}")
        
    def _create_table_display(self, parent, table_data):
        """
        핵심 : 주어진 데이터에 대한 간단한 테이블 디스플레이를 생성합니다.
        
        매개변수:
            parent: 부모 위젯
            table_data: 표시할 테이블 데이터
        """
        if not table_data:
            ttk.Label(parent, text="데이터가 없습니다").pack(pady=10)
            return
            
        tree = ttk.Treeview(parent)
        tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 열 구성
        columns = list(table_data[0].keys())
        tree["columns"] = columns
        tree.column("#0", width=0, stretch=tk.NO)
        
        for col in columns:
            tree.column(col, anchor=tk.W, width=100)
            tree.heading(col, text=col)
        
        # 데이터 행 추가
        for i, row in enumerate(table_data):
            values = [row.get(col, "") for col in columns]
            tree.insert("", tk.END, text=str(i+1), values=values)
            
    def _create_join_filter_visualization(self, parent, join_type, key_a, key_b):
        """
        핵심 : JOIN 필터가 작동하는 방식을 시각적으로 표현합니다.
        
        매개변수:
            parent: 부모 위젯
            join_type: JOIN 유형
            key_a: 테이블 A의 JOIN 키
            key_b: 테이블 B의 JOIN 키
        """
        if join_type == "INNER JOIN":
            self._create_inner_join_visualization(parent, key_a, key_b)
        elif join_type == "LEFT OUTER JOIN":
            self._create_left_join_visualization(parent, key_a, key_b)
        elif join_type == "RIGHT OUTER JOIN":
            self._create_right_join_visualization(parent, key_a, key_b)
        elif join_type == "FULL OUTER JOIN":
            self._create_full_join_visualization(parent, key_a, key_b)
        elif join_type == "CROSS JOIN":
            self._create_cross_join_visualization(parent)
            
    def _create_inner_join_visualization(self, parent, key_a, key_b):
        """
        핵심 : INNER JOIN에 대한 시각화를 생성합니다.
        
        매개변수:
            parent: 부모 위젯
            key_a: 테이블 A의 JOIN 키
            key_b: 테이블 B의 JOIN 키
        """
        canvas = tk.Canvas(parent, width=400, height=200, bg="white")
        canvas.pack(pady=10)
        
        # 두 개의 겹치는 사각형 그리기
        canvas.create_rectangle(50, 50, 200, 150, outline="blue", width=2)
        canvas.create_rectangle(150, 50, 300, 150, outline="red", width=2)
        
        # 사각형에 레이블 붙이기
        canvas.create_text(125, 40, text="테이블 A", fill="blue")
        canvas.create_text(225, 40, text="테이블 B", fill="red")
        
        # 교차점 강조 표시
        canvas.create_rectangle(150, 50, 200, 150, fill="#e6ffe6", outline="")
        
        # JOIN 키로 레이블 붙이기
        canvas.create_text(175, 100, text=f"{key_a} = {key_b}", fill="green")
        
        # 설명 추가
        ttk.Label(parent, text="INNER JOIN은 키가 일치하는 행만 유지합니다(녹색 영역).",
                wraplength=400, justify=tk.LEFT).pack(pady=5)
                
    def _create_left_join_visualization(self, parent, key_a, key_b):
        """
        핵심 : LEFT OUTER JOIN에 대한 시각화를 생성합니다.
        
        매개변수:
            parent: 부모 위젯
            key_a: 테이블 A의 JOIN 키
            key_b: 테이블 B의 JOIN 키
        """
        canvas = tk.Canvas(parent, width=400, height=200, bg="white")
        canvas.pack(pady=10)
        
        # 두 개의 겹치는 사각형 그리기
        canvas.create_rectangle(50, 50, 200, 150, outline="blue", width=2, fill="#e6ffe6")
        canvas.create_rectangle(150, 50, 300, 150, outline="red", width=2)
        
        # 사각형에 레이블 붙이기
        canvas.create_text(125, 40, text="테이블 A", fill="blue")
        canvas.create_text(225, 40, text="테이블 B", fill="red")
        
        # 더 어두운 녹색으로 교차점 강조 표시
        canvas.create_rectangle(150, 50, 200, 150, fill="#c2f0c2", outline="")
        
        # JOIN 키로 레이블 붙이기
        canvas.create_text(175, 100, text=f"{key_a} = {key_b}", fill="green")
        
        # 설명 추가
        ttk.Label(parent, text="LEFT OUTER JOIN은 테이블 A의 모든 행(녹색 영역)과 테이블 B의 일치하는 행을 유지합니다.",
                wraplength=400, justify=tk.LEFT).pack(pady=5)
                
    def _create_right_join_visualization(self, parent, key_a, key_b):
        """
        핵심 : RIGHT OUTER JOIN에 대한 시각화를 생성합니다.
        
        매개변수:
            parent: 부모 위젯
            key_a: 테이블 A의 JOIN 키
            key_b: 테이블 B의 JOIN 키
        """
        canvas = tk.Canvas(parent, width=400, height=200, bg="white")
        canvas.pack(pady=10)
        
        # 두 개의 겹치는 사각형 그리기
        canvas.create_rectangle(50, 50, 200, 150, outline="blue", width=2)
        canvas.create_rectangle(150, 50, 300, 150, outline="red", width=2, fill="#e6ffe6")
        
        # 사각형에 레이블 붙이기
        canvas.create_text(125, 40, text="테이블 A", fill="blue")
        canvas.create_text(225, 40, text="테이블 B", fill="red")
        
        # 교차 부분을 더 어두운 녹색으로 강조하기
        canvas.create_rectangle(150, 50, 200, 150, fill="#c2f0c2", outline="")
        
        # 조인 키로 레이블 붙이기
        canvas.create_text(175, 100, text=f"{key_a} = {key_b}", fill="green")
        
        # 설명 추가하기
        ttk.Label(parent, text="RIGHT OUTER JOIN은 테이블 B의 모든 행(녹색 영역)과 테이블 A의 일치하는 행을 유지합니다.",
                wraplength=400, justify=tk.LEFT).pack(pady=5)
                
    def _create_full_join_visualization(self, parent, key_a, key_b):
        """
        핵심 : FULL OUTER JOIN에 대한 시각화를 생성합니다.
        
        매개변수:
            parent: 부모 위젯
            key_a: 테이블 A의 JOIN 키
            key_b: 테이블 B의 JOIN 키
        """
        canvas = tk.Canvas(parent, width=400, height=200, bg="white")
        canvas.pack(pady=10)
        
        # 두 개의 겹치는 사각형 그리기
        canvas.create_rectangle(50, 50, 200, 150, outline="blue", width=2, fill="#e6ffe6")
        canvas.create_rectangle(150, 50, 300, 150, outline="red", width=2, fill="#e6ffe6")
        
        # 사각형에 레이블 붙이기
        canvas.create_text(125, 40, text="테이블 A", fill="blue")
        canvas.create_text(225, 40, text="테이블 B", fill="red")
        
        # 교차 부분을 더 어두운 녹색으로 강조하기
        canvas.create_rectangle(150, 50, 200, 150, fill="#c2f0c2", outline="")
        
        # 조인 키로 레이블 붙이기
        canvas.create_text(175, 100, text=f"{key_a} = {key_b}", fill="green")
        
        # 설명 추가하기
        ttk.Label(parent, text="FULL OUTER JOIN은 두 테이블의 모든 행(녹색 영역)을 유지하며, 일치하지 않는 경우 NULL 값을 사용합니다.",
                wraplength=400, justify=tk.LEFT).pack(pady=5)
                
    def _create_cross_join_visualization(self, parent):
        """
        핵심 : CROSS JOIN에 대한 시각화를 생성합니다.
        
        매개변수:
            parent: 부모 위젯
        """
        canvas = tk.Canvas(parent, width=400, height=200, bg="white")
        canvas.pack(pady=10)
        
        # 모든 조합을 나타내는 그리드 패턴 그리기
        for i in range(3):
            for j in range(3):
                canvas.create_rectangle(50 + i*100, 50 + j*40, 100 + i*100, 90 + j*40, 
                                      fill="#e6ffe6", outline="black")
                canvas.create_text(75 + i*100, 70 + j*40, 
                                 text=f"A{i+1}×B{j+1}")
        
        # 테이블에 레이블 붙이기
        canvas.create_text(75, 30, text="테이블 A의 행", fill="blue")
        canvas.create_text(175, 30, text="테이블 B의 행", fill="red")
        
        # 설명 추가하기
        ttk.Label(parent, text="CROSS JOIN은 두 테이블 간의 모든 가능한 행 조합을 생성합니다(카르테시안 곱).",
                wraplength=400, justify=tk.LEFT).pack(pady=5)
                
    def _evaluate_match(self, row_a, row_b, key_a, key_b, join_type):
        """
        핵심 : 두 행이 JOIN 조건과 일치하는지 평가합니다.
        
        매개변수:
            row_a: 테이블 A의 행
            row_b: 테이블 B의 행
            key_a: 테이블 A의 JOIN 키
            key_b: 테이블 B의 JOIN 키
            join_type: JOIN 유형
            
        반환값:
            행 쌍이 JOIN 결과에 포함되는지 여부(Boolean)
        """
        # CROSS JOIN의 경우 모든 조합이 포함됨
        if join_type == "CROSS JOIN":
            return True
            
        # 조인 키가 존재하는지 확인하기
        a_key_exists = key_a in row_a
        b_key_exists = key_b in row_b
        
        if not a_key_exists or not b_key_exists:
            return False
            
        # 키가 일치하는지 확인하기
        keys_match = row_a[key_a] == row_b[key_b]
        
        return keys_match
        
    def _generate_evaluation_explanation(self, row_a, row_b, key_a, key_b, join_type, cartesian_product):
        """
        핵심 : 행 쌍의 평가에 대한 설명을 생성합니다.
        
        매개변수:
            row_a: 테이블 A의 행
            row_b: 테이블 B의 행
            key_a: 테이블 A의 JOIN 키
            key_b: 테이블 B의 JOIN 키
            join_type: JOIN 유형
            cartesian_product: 카르테시안 곱 데이터
            
        반환값:
            평가 설명 문자열
        """
        # JoinEngine에서 일치 설명 가져오기
        from join_engine import JoinEngine
        match_explanation = JoinEngine.get_match_explanation(row_a, row_b, key_a, key_b, join_type)
        
        # 조인 유형에 따른 구체적인 설명 추가하기
        if join_type == "INNER JOIN":
            if self._evaluate_match(row_a, row_b, key_a, key_b, join_type):
                return f"{match_explanation}\n\n키가 일치하므로 이 행 쌍은 INNER JOIN 결과에 포함됩니다."
            else:
                return f"{match_explanation}\n\n키가 일치하지 않으므로 이 행 쌍은 INNER JOIN 결과에서 제외됩니다."
                
        elif join_type == "LEFT OUTER JOIN":
            if self._evaluate_match(row_a, row_b, key_a, key_b, join_type):
                return f"{match_explanation}\n\n키가 일치하므로 이 행 쌍은 LEFT JOIN 결과에 포함됩니다."
            else:
                return f"{match_explanation}\n\n키가 일치하지 않지만, LEFT JOIN에서 테이블 A의 모든 행은 포함되어야 합니다."
                
        elif join_type == "RIGHT OUTER JOIN":
            if self._evaluate_match(row_a, row_b, key_a, key_b, join_type):
                return f"{match_explanation}\n\n키가 일치하므로 이 행 쌍은 RIGHT JOIN 결과에 포함됩니다."
            else:
                return f"{match_explanation}\n\n키가 일치하지 않지만, RIGHT JOIN에서 테이블 B의 모든 행은 포함되어야 합니다."
                
        elif join_type == "FULL OUTER JOIN":
            if self._evaluate_match(row_a, row_b, key_a, key_b, join_type):
                return f"{match_explanation}\n\n키가 일치하므로 이 행 쌍은 FULL JOIN 결과에 포함됩니다."
            else:
                return f"{match_explanation}\n\n키가 일치하지 않지만, FULL JOIN에서 두 테이블의 모든 행은 포함되어야 합니다."
                
        elif join_type == "CROSS JOIN":
            return "CROSS JOIN은 키 일치 여부에 관계없이 모든 행 조합을 포함합니다."
            
        return match_explanation
        
    def _count_matched_rows(self, cartesian_product, key_a, key_b, join_type):
        """
        핵심 : JOIN 결과에서 일치하는 행의 수를 계산합니다.
        
        매개변수:
            cartesian_product: 카르테시안 곱 데이터
            key_a: 테이블 A의 JOIN 키
            key_b: 테이블 B의 JOIN 키
            join_type: JOIN 유형
            
        반환값:
            일치하는 행의 수
        """
        count = 0
        for row_a, row_b in cartesian_product:
            if self._evaluate_match(row_a, row_b, key_a, key_b, join_type):
                count += 1
        return count
        
    def _count_unmatched_rows(self, cartesian_product, key_a, key_b, join_type):
        """
        핵심 : OUTER JOIN에서 NULL 값으로 포함될 행의 수를 계산합니다.
        
        매개변수:
            cartesian_product: 카르테시안 곱 데이터
            key_a: 테이블 A의 JOIN 키
            key_b: 테이블 B의 JOIN 키
            join_type: JOIN 유형
            
        반환값:
            외부 조인에 추가될 행의 수
        """
        # 일치하는 행 식별하기
        matched_a_ids, matched_b_ids = JoinEngine.identify_matched_rows(
            cartesian_product, key_a, key_b
        )
        
        # 카르테시안 곱에서 고유한 행 추출하기
        unique_rows_a, unique_rows_b = utils.get_unique_rows(cartesian_product)
        
        unmatched_count = 0
        
        # 조인 유형에 따라 일치하지 않는 행 계산하기
        if join_type in ["LEFT OUTER JOIN", "FULL OUTER JOIN"]:
            for row_a in unique_rows_a:
                if id(row_a) not in matched_a_ids:
                    unmatched_count += 1
                    
        if join_type in ["RIGHT OUTER JOIN", "FULL OUTER JOIN"]:
            for row_b in unique_rows_b:
                if id(row_b) not in matched_b_ids:
                    unmatched_count += 1
                    
        return unmatched_count