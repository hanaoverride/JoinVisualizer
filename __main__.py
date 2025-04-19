"""
JoinVisualizer 패키지의 진입점입니다.
이 파일은 패키지가 직접 실행될 때 호출됩니다.
"""

import tkinter as tk
from app import JoinVisualizerApp


def main():
    """
    핵심: 애플리케이션을 시작하는 메인 함수입니다.
    """
    root = tk.Tk()
    app = JoinVisualizerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
