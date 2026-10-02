# Money

금액을 원래 통화 그대로 보여주고, 필요하면 환산액과 적용 환율을 아래 줄에 붙인다.

- **amount**(숫자), **currency**(`KRW` · `USD` · `MNT`)는 필수다. 소수 자리는 통화가 정한다(USD 2자리).
- **kind**="expected"이면 예상 금액이다: `ink-muted` 글자에 점선 밑줄. **tag**를 켜면 "예상" 표시도 붙는다.
- **converted** `{amount, currency}`와 **rate** `{value, date}`를 주면 "≈ 4,981,250 KRW · 0.3985 (10.01)" 줄이 붙는다. 환산은 저장된 거래 환율로 계산해서 넘기고, 화면에서 다시 계산하지 않는다.
- **lossTone**: 음수일 때 `critical` 글자(손익, 마진 열). **sign**="always"면 양수에 "+"를 붙인다. **compact**는 KPI용 "4,820만" 표기다.
- **align**: `end`(기본, 표의 금액 열) · `start`.
