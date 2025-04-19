"""
핵심: 특정 행 쌍이 일치하는지 여부에 대한 설명을 생성합니다.

매개변수:
row_a: 테이블 A의 행
row_b: 테이블 B의 행


--- chunk 11 ---

key_a: 테이블 A의 JOIN 키
key_b: 테이블 B의 JOIN 키
join_type: JOIN 유형

반환값:
일치 상태에 대한 설명 문자열
"""
from typing import List, Dict, Any, Tuple, Set
import utils


class JoinEngine:
    """
    핵심 : SQL JOIN 연산을 처리하는 엔진
    
    주요 기능:
    - 다양한 JOIN 유형(INNER, LEFT OUTER, RIGHT OUTER, FULL OUTER, CROSS)에 대한 로직 처리
    - 테이블 간 JOIN 조건에 따른 행 필터링
    - 카르테시안 곱 결과에 대한 연산 처리
    - JOIN 결과 생성 및 데이터 병합
    """
    @staticmethod
    def filter_join_result(cartesian_product: List[Tuple[Dict, Dict]], 
                         key_a: str, key_b: str, join_type: str) -> List[Tuple[Dict, bool]]:
        """
        핵심 : 지정된 JOIN 유형과 키에 따라 카르테시안 곱을 필터링합니다.
        
        매개변수:
            cartesian_product: 카르테시안 곱에서 생성된 튜플 리스트
            key_a: 테이블 A의 JOIN 키
            key_b: 테이블 B의 JOIN 키
            join_type: JOIN 유형 (INNER, LEFT OUTER, RIGHT OUTER, FULL OUTER, CROSS)
            
        반환값:
            (병합된_행, 일치_여부) 튜플의 리스트, 일치_여부는 키가 직접 일치하는지를 나타냅니다.
        """
        result = []
        
        # 각 테이블에서 일치하는 행 추적
        table_a_matched = set()
        table_b_matched = set()
        
        # 첫 번째 패스: 일치하는 행 식별 및 결합된 행 생성
        for row_a, row_b in cartesian_product:
            # 조인 키가 존재하고 일치하는지 확인
            a_key_exists = key_a in row_a
            b_key_exists = key_b in row_b
            
            # CROSS JOIN은 키에 관계없이 모든 조합을 포함합니다
            if join_type == "CROSS JOIN":
                merged_row = {**row_a, **{f"B_{k}": v for k, v in row_b.items()}}
                result.append((merged_row, True))  # All rows are considered "matched" in CROSS JOIN
                table_a_matched.add(id(row_a))
                table_b_matched.add(id(row_b))
                continue
                
            if not a_key_exists or not b_key_exists:
                continue
                
            keys_match = row_a[key_a] == row_b[key_b]
            
            # CROSS를 제외한 모든 JOIN에 대해 키가 일치하는지 확인
            if keys_match:
                merged_row = {**row_a, **{f"B_{k}": v for k, v in row_b.items()}}
                result.append((merged_row, True))  # Matched row
                table_a_matched.add(id(row_a))
                table_b_matched.add(id(row_b))
        
        # 두 번째 패스: OUTER JOIN의 일치하지 않는 행 처리
        if join_type in ["LEFT OUTER JOIN", "FULL OUTER JOIN"]:
            # 테이블 A에서 고유한 행 가져오기
            unique_rows_a, _ = utils.get_unique_rows(cartesian_product)
            
            for row_a in unique_rows_a:
                if id(row_a) not in table_a_matched:
                    # B에 대해 NULL 값으로 일치하지 않는 A의 행 추가
                    sample_row_b = cartesian_product[0][1] if cartesian_product else {}
                    null_b = {f"B_{k}": None for k, v in sample_row_b.items()}
                    merged_row = {**row_a, **null_b}
                    result.append((merged_row, False))  # Unmatched row
        
        if join_type in ["RIGHT OUTER JOIN", "FULL OUTER JOIN"]:
            # 테이블 B에서 고유한 행 가져오기
            _, unique_rows_b = utils.get_unique_rows(cartesian_product)
                    
            for row_b in unique_rows_b:
                if id(row_b) not in table_b_matched:
                    # A에 대해 NULL 값으로 일치하지 않는 B의 행 추가
                    sample_row_a = cartesian_product[0][0] if cartesian_product else {}
                    null_a = {k: None for k, v in sample_row_a.items()}
                    b_data = {f"B_{k}": v for k, v in row_b.items()}
                    merged_row = {**null_a, **b_data}
                    result.append((merged_row, False))  # Unmatched row
        
        return result
    @staticmethod
    def identify_matched_rows(cartesian_product: List[Tuple[Dict, Dict]], 
                            key_a: str, key_b: str) -> Tuple[Set[int], Set[int]]:
        """
        핵심 : 테이블 A와 B에서 키가 일치하는 행을 식별합니다.
        
        매개변수:
            cartesian_product: 카르테시안 곱에서 생성된 튜플 리스트
            key_a: 테이블 A의 JOIN 키
            key_b: 테이블 B의 JOIN 키
            
        반환값:
            (일치하는_A_행_ID, 일치하는_B_행_ID) 세트 튜플
        """
        matched_a_ids = set()
        matched_b_ids = set()
        
        for row_a, row_b in cartesian_product:
            if key_a in row_a and key_b in row_b and row_a[key_a] == row_b[key_b]:
                matched_a_ids.add(id(row_a))
                matched_b_ids.add(id(row_b))
                
        return matched_a_ids, matched_b_ids
    @staticmethod
    def get_match_explanation(row_a: Dict[str, Any], row_b: Dict[str, Any], 
                           key_a: str, key_b: str, join_type: str) -> str:
        """
        핵심 : 특정 행 쌍이 일치하는지 여부에 대한 설명을 생성합니다.
        
        매개변수:
            row_a: 테이블 A의 행
            row_b: 테이블 B의 행
            key_a: 테이블 A의 JOIN 키
            key_b: 테이블 B의 JOIN 키
            join_type: JOIN 유형
            
        반환값:
            일치 상태에 대한 설명 문자열
        """
        if join_type == "CROSS JOIN":
            return "모든 행이 CROSS JOIN에 포함됩니다. 키에 관계없이 모든 행이 포함됩니다."
            
        # 조인 키가 존재하는지 확인
        a_key_exists = key_a in row_a
        b_key_exists = key_b in row_b
        
        if not a_key_exists or not b_key_exists:
            explanation = ""
            if not a_key_exists:
                explanation += f"행 A에 키 {key_a}가 없습니다. "
            if not b_key_exists:
                explanation += f"행 B에 키 {key_b}가 없습니다. "
            return explanation
        
        # 키가 일치하는지 확인
        if row_a[key_a] == row_b[key_b]:
            return f"키가 일치합니다: {key_a}={row_a[key_a]}는 {key_b}={row_b[key_b]}와 같습니다."
        else:
            return f"키가 일치하지 않습니다: {key_a}={row_a[key_a]}는 {key_b}={row_b[key_b]}와 같지 않습니다."