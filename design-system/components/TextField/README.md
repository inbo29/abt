# TextField

라벨, 도움말, 오류 문장이 붙는 한 줄(또는 여러 줄) 입력이다.

- **label**(보이는 라벨이 없는 검색 칸은 **ariaLabel** · 마크업에서는 `aria-label`), **placeholder**, **help**, **error**, **required**("필수" 표시), **prefix**/**suffix**(단위: "명", "MNT"), **align**="end"(숫자).
- **locked**: 마감된 자료. 입력을 막고 "마감" 표시와 재개방 안내를 보인다.
- **multiline**+**rows**: 반려 사유, 조치 내용 같은 긴 글.
- **tag**="예상": 예상 값을 받는 칸. **size**: `sm` · `md` · `lg`(모바일).
- 오류는 무엇이 잘못됐고 어떻게 고치는지 쓴다: "반려 사유를 입력해 주세요."
