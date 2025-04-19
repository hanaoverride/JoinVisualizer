"""
핵심 : JoinVisualizer 애플리케이션의 메인 컨트롤러.
UI 컴포넌트와 JOIN 엔진 간의 상호작용을 조정합니다.
"""
import tkinter as tk
import json
import platform
from typing import List, Dict, Any, Tuple

import models
import utils
import join_engine
import gui_layout
import animation
import widgets


class JoinVisualizerApp:
    """
    핵심 : JoinVisualizer 애플리케이션의 메인 컨트롤러입니다.
    UI 컴포넌트와 JOIN 엔진 간의 상호작용을 조정합니다.
    
    주요 기능:
    - 사용자 입력 처리
    - JOIN 연산 실행
    - 결과 시각화
    - 애니메이션 단계 제어
    """
    def __init__(self, root):
        """
        핵심 : 애플리케이션을 초기화합니다.
        
        매개변수:
            root: 루트 Tkinter 윈도우
        """
        self.root = root
        self.setup_root_window()
          # 애니메이션 변수 초기화
        self.animation_manager = None
        
        # UI 컴포넌트 생성
        self.input_panel = gui_layout.InputPanel(
            self.root,
            on_join_type_change=self.on_join_type_change,
            on_run_simulation=self.run_join_simulation,
            on_show_help=self.show_help
        )
        
        self.output_panel = gui_layout.OutputPanel(
            self.root,
            on_prev_step=self.prev_animation_step,
            on_next_step=self.next_animation_step
        )
          # 애니메이션 관리자 초기화
        self.animation_manager = animation.AnimationManager(
            self.output_panel.get_animation_frame(),
            self.output_panel.get_step_label()
        )
        
        # 예제 데이터로 채우기
        self.populate_example_data()
    def setup_root_window(self):
        """
        핵심 : 루트 윈도우 속성을 설정합니다.
        
        윈도우 크기, 제목, 화면 위치 등을 구성합니다.
        """
        self.root.title("JoinVisualizer")
          # 화면 크기를 계산하고 윈도우 크기를 화면의 85%로 설정
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        window_width = int(screen_width * 0.85)
        window_height = int(screen_height * 0.85)
        self.root.geometry(f"{window_width}x{window_height}")
          # 시작 시 전체 화면 모드로 설정
        # Windows는 'zoomed' 상태를 사용하고, 다른 플랫폼은 attributes를 사용함
        if platform.system() == "Windows":
            self.root.state('zoomed')  # Windows 전체 화면
        else:
            self.root.attributes('-zoomed', True)  # Linux 전체 화면
            # Mac에서는 다음을 사용: self.root.attributes('-fullscreen', True)
        
        self.root.configure(padx=10, pady=10)
    def on_join_type_change(self, event=None):
        """
        핵심 : JOIN 유형 선택 변경을 처리합니다.
        
        매개변수:
            event: 선택 이벤트 (기본값: None)
        """
        join_type = self.input_panel.get_join_type()
        self.input_panel.update_explanation(join_type)
    def run_join_simulation(self):
        """
        핵심 : 현재 설정으로 JOIN 시뮬레이션을 실행합니다.
        
        사용자 입력을 처리하고, 카르테시안 곱과 JOIN 결과를 계산하며,
        결과를 시각적으로 표시합니다.
        """
        try:            # 테이블 입력 파싱
            table_a = utils.parse_table_input(self.input_panel.get_table_a_input())
            table_b = utils.parse_table_input(self.input_panel.get_table_b_input())
            
            if not table_a or not table_b:
                tk.messagebox.showerror("입력 오류", "테이블은 비어있으면 안됩니다.")
                return
              # 조인 키와 조인 유형 가져오기
            key_a = self.input_panel.get_key_a()
            key_b = self.input_panel.get_key_b()
            join_type = self.input_panel.get_join_type()
              # CROSS JOIN은 키가 필요하지 않음
            if join_type != "CROSS JOIN" and (not key_a or not key_b):
                tk.messagebox.showerror("입력 오류", "비-CROSS JOIN 작업을 위한 조인 키를 지정해야 합니다.")
                return
              # 데카르트 곱(Cartesian product) 계산
            cartesian_product = utils.compute_cartesian_product(table_a, table_b)
              # JOIN 결과 필터링
            join_result = join_engine.JoinEngine.filter_join_result(cartesian_product, key_a, key_b, join_type)
              # 참조를 위한 입력 테이블 표시
            gui_layout.ResultDisplayManager.display_tables(self.root, table_a, table_b)
              # 데카르트 곱 표시
            gui_layout.ResultDisplayManager.display_cartesian_product(
                self.output_panel.get_cartesian_frame(),
                cartesian_product,
                key_a,
                key_b,
                join_type
            )
              # JOIN 결과 표시
            gui_layout.ResultDisplayManager.display_join_result(
                self.output_panel.get_join_result_frame(),
                join_result
            )
              # JOIN 설명 표시
            gui_layout.ResultDisplayManager.display_join_explanation(
                self.output_panel.get_explanation_frame(),
                cartesian_product,
                key_a,
                key_b,
                join_type
            )
              # 애니메이션 설정
            self.animation_manager.setup_step_animation(
                cartesian_product,
                key_a,
                key_b,
                join_type,
                lambda: self.output_panel.select_tab(1)  # JOIN 결과 탭을 표시하기 위한 콜백
            )
              # 먼저 데카르트 곱 탭으로 전환
            self.output_panel.select_tab(0)
            
        except Exception as e:
            tk.messagebox.showerror("오류", f"오류 발생: {str(e)}")
            import traceback
            traceback.print_exc()
    def prev_animation_step(self):
        """
        핵심 : 이전 애니메이션 단계로 이동합니다.
        
        애니메이션 관리자에게 이전 단계 표시를 요청합니다.
        """
        if self.animation_manager:
            self.animation_manager.prev_animation_step()
    def next_animation_step(self):
        """
        핵심 : 다음 애니메이션 단계로 이동합니다.
        
        애니메이션 관리자에게 다음 단계 표시를 요청합니다.
        """
        if self.animation_manager:
            self.animation_manager.next_animation_step()
    def show_help(self):
        """
        핵심 : 도움말 대화상자를 표시합니다.
        
        애플리케이션 사용법과 JOIN 연산 기초에 대한 정보를 제공합니다.
        """
        help_text = utils.create_help_text()
        gui_layout.HelpDialog.show(self.root, help_text)
    def populate_example_data(self):
        """
        핵심 : 입력 필드에 예제 데이터를 채웁니다.
        
        사용자에게 애플리케이션 작동 방식을 빠르게 확인할 수 있는
        샘플 데이터를 제공합니다.
        """
        example_a = models.ExampleData.get_table_a()
        example_b = models.ExampleData.get_table_b()
        
        self.input_panel.set_table_a_input(json.dumps(example_a, indent=2))
        self.input_panel.set_table_b_input(json.dumps(example_b, indent=2))
        self.input_panel.set_key_a("id")
        self.input_panel.set_key_b("dept_id")
