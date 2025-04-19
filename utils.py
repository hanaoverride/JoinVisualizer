import json
import re
from typing import List, Dict, Any, Tuple
import tkinter as tk


def parse_table_input(input_text: str) -> List[Dict[str, Any]]:
    """
    입력 텍스트를 딕셔너리 목록으로 파싱합니다.
    JSON 형식 및 Python dict 리터럴 형식 모두 처리합니다.

    인수:
    input_text: JSON 또는 Python과 유사한 dict 표현을 포함하는 문자열

    반환값:
    테이블 데이터를 나타내는 딕셔너리 목록
    """
    try:
        # 먼저 JSON으로 파싱 시도
        return json.loads(input_text)
    except json.JSONDecodeError:
        try:
            # JSON 파싱이 실패하면 Python 리터럴로 평가 시도
            # JSON 파싱을 위해 작은따옴표를 큰따옴표로 대체
            input_text = re.sub(r"'", '"', input_text)
            return json.loads(input_text)
        except Exception as e:
            # 실패 시 빈 목록 반환
            print(f"Error parsing table input: {str(e)}")
            return []


def compute_cartesian_product(table_a: List[Dict], table_b: List[Dict]) -> List[Tuple[Dict, Dict]]:
    """
    두 테이블의 카르테시안 곱을 계산합니다.
    테이블 A의 각 행과 테이블 B의 각 행을 포함하는 튜플 목록을 반환합니다.

    인자:
    table_a: 테이블 A를 나타내는 딕셔너리 목록
    table_b: 테이블 B를 나타내는 딕셔너리 목록

    반환:
    테이블 A의 각 행과 테이블 B의 각 행을 포함하는 튜플 목록
    """
    cartesian_product = []
    for row_a in table_a:
        for row_b in table_b:
            cartesian_product.append((row_a, row_b))
    return cartesian_product


def get_unique_rows(cartesian_product: List[Tuple[Dict, Dict]]) -> Tuple[List[Dict], List[Dict]]:
    """
    카르테시안 곱에서 테이블 A와 테이블 B의 고유한 행을 추출합니다.
    
    인자:
        cartesian_product: compute_cartesian_product에서 반환된 튜플 목록
        
    반환:
        (unique_rows_a, unique_rows_b) 형태의 튜플
    """
    # 테이블 A에서 고유한 행 추출
    unique_rows_a = []
    seen_a = set()
    for row_a, _ in cartesian_product:
        if id(row_a) not in seen_a:
            seen_a.add(id(row_a))
            unique_rows_a.append(row_a)
    
    # 테이블 B에서 고유한 행 추출
    unique_rows_b = []
    seen_b = set()
    for _, row_b in cartesian_product:
        if id(row_b) not in seen_b:
            seen_b.add(id(row_b))
            unique_rows_b.append(row_b)
    
    return unique_rows_a, unique_rows_b


def format_row_as_string(row: Dict[str, Any]) -> str:
    """
    행 딕셔너리를 가독성 있는 문자열로 형식화합니다.
    
    인자:
        row: 행을 나타내는 딕셔너리
        
    반환:
        행의 문자열 표현
    """
    return ", ".join([f"{k}: {v}" for k, v in row.items()])


def create_help_text() -> str:
    """
    애플리케이션의 도움말 텍스트를 생성합니다.
    
    반환:
        문자열 형태의 도움말 텍스트
    """
    return """
SQL JOIN 연산 시각화 도구 - 도움말

카르테시안 곱:
카르테시안 곱은 첫 번째 테이블의 모든 행과 두 번째 테이블의 모든 행을 결합한 결과입니다.
SQL의 모든 JOIN 연산의 기초를 형성합니다.

JOIN 유형:

1. INNER JOIN:
   조인 키를 기준으로 두 테이블 모두에서 일치하는 행만 반환합니다.
   
2. LEFT OUTER JOIN:
   왼쪽 테이블(테이블 A)의 모든 행과 오른쪽 테이블(테이블 B)의 일치하는 행을 반환합니다.
   일치하지 않는 경우, 결과의 오른쪽은 NULL로 표시됩니다.
   
3. RIGHT OUTER JOIN:
   오른쪽 테이블(테이블 B)의 모든 행과 왼쪽 테이블(테이블 A)의 일치하는 행을 반환합니다.
   일치하지 않는 경우, 결과의 왼쪽은 NULL로 표시됩니다.
   
4. FULL OUTER JOIN:
   두 테이블에서 일치하는 모든 행을 반환합니다.
   일치하지 않는 경우, 한쪽 테이블의 결과는 NULL로 표시됩니다.
   
5. CROSS JOIN:
   두 테이블의 카르테시안 곱을 반환합니다(모든 행 조합).
   CROSS JOIN에는 조인 키가 필요하지 않습니다.

이 도구 사용법:
1. 테이블 A 및 테이블 B에 대한 데이터를 딕셔너리 목록 형식으로 입력합니다.
2. 각 테이블에 대한 조인 키를 지정합니다(테이블 B의 경우 dept_id).
3. 드롭다운 메뉴에서 JOIN 유형을 선택합니다.
4. "JOIN 시뮬레이션 실행"을 클릭하여 결과를 확인합니다.

카르테시안 곱 탭은 두 테이블의 모든 행 조합을 보여주며,
일치하는 조합은 녹색으로 강조 표시됩니다.

JOIN 결과 탭은 JOIN 연산의 최종 결과를 보여줍니다.
"""