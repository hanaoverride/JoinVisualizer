from typing import List, Dict, Any, Tuple, Optional


class JoinDescriptions:
    """
    핵심: 다양한 JOIN 유형에 대한 설명과 예시를 포함하는 정적 클래스입니다.
    """
    
    DESCRIPTIONS = {
        "INNER JOIN": {
            "text": """INNER JOIN은 두 테이블에서 조인 키가 일치하는 행만 반환합니다.
            
예시: 테이블 A에 ID [1,2,3]을 가진 사용자가 있고, 테이블 B에 dept_id [1,2,4]를 가진 부서가 있을 때, 
id=dept_id로 INNER JOIN을 수행하면 ID 1과 2의 행만 반환됩니다.""",
            "image": None  # 시각적 표현을 위한 이미지 경로 추가 가능
        },
        "LEFT OUTER JOIN": {
            "text": """LEFT OUTER JOIN은 테이블 A(왼쪽 테이블)의 모든 행과 테이블 B의 일치하는 행을 반환합니다.
테이블 B에서 일치하는 행이 없을 경우, 테이블 B 열에는 NULL 값이 사용됩니다.
            
예시: 테이블 A에 ID [1,2,3]을 가진 사용자가 있고, 테이블 B에 dept_id [1,2,4]를 가진 부서가 있을 때,
LEFT JOIN을 수행하면 ID 1, 2, 3의 행이 반환됩니다(ID 3의 경우 B 열에 NULL 값).""",
            "image": None
        },
        "RIGHT OUTER JOIN": {
            "text": """RIGHT OUTER JOIN은 테이블 B(오른쪽 테이블)의 모든 행과 테이블 A의 일치하는 행을 반환합니다.
테이블 A에서 일치하는 행이 없을 경우, 테이블 A 열에는 NULL 값이 사용됩니다.
            
예시: 테이블 A에 ID [1,2,3]을 가진 사용자가 있고, 테이블 B에 dept_id [1,2,4]를 가진 부서가 있을 때,
RIGHT JOIN을 수행하면 ID 1, 2, 4의 행이 반환됩니다(ID 4의 경우 A 열에 NULL 값).""",
            "image": None
        },
        "FULL OUTER JOIN": {
            "text": """FULL OUTER JOIN은 두 테이블의 모든 행을 반환합니다.
일치하는 행이 없을 경우, 다른 테이블의 열에는 NULL 값이 사용됩니다.
            
예시: 테이블 A에 ID [1,2,3]을 가진 사용자가 있고, 테이블 B에 dept_id [1,2,4]를 가진 부서가 있을 때,
FULL JOIN을 수행하면 ID 1, 2, 3, 4의 행이 반환됩니다(일치하지 않는 경우 적절한 NULL 값 포함).""",
            "image": None
        },
        "CROSS JOIN": {
            "text": """CROSS JOIN은 조인 키에 관계없이 테이블 A의 모든 행과 테이블 B의 모든 행을 조합한 
카티션 곱(Cartesian product)을 반환합니다.
            
예시: 테이블 A에 3개 행, 테이블 B에 3개 행이 있는 경우, CROSS JOIN은 9개(3×3)의 행을 반환하여
모든 가능한 조합을 보여줍니다.""",
            "image": None
        }
    }


class JoinResult:
    """
    핵심: JOIN 연산 결과를 저장하고 표현하는 클래스입니다.
    """
    def __init__(self, 
                 joined_rows: List[Tuple[Dict[str, Any], bool]],
                 join_type: str,
                 key_a: str,
                 key_b: str):
        self.joined_rows = joined_rows  # Tuple of (row, is_matched)
        self.join_type = join_type
        self.key_a = key_a
        self.key_b = key_b
        
    @property
    def matched_count(self) -> int:
        """
        핵심: 일치하는 행의 수를 반환합니다.
        """
        return sum(1 for _, matched in self.joined_rows if matched)
    
    @property
    def unmatched_count(self) -> int:
        """
        핵심: 일치하지 않는 행의 수를 반환합니다.(OUTER JOIN의 경우)
        """
        return len(self.joined_rows) - self.matched_count


class ExampleData:
    """
    핵심: 테스트 및 시연을 위한 예제 데이터를 제공합니다.
    """
    @staticmethod
    def get_table_a() -> List[Dict[str, Any]]:
        return [
            {"id": 1, "name": "홍길동"},
            {"id": 2, "name": "김철수"},
            {"id": 3, "name": "이영희"}
        ]
    
    @staticmethod
    def get_table_b() -> List[Dict[str, Any]]:
        return [
            {"dept_id": 1, "department": "인사부"},
            {"dept_id": 2, "department": "개발부"},
            {"dept_id": 4, "department": "마케팅부"}
        ]