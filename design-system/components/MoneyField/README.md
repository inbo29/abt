# MoneyField

금액과 통화를 함께 받고, 환율이 주어지면 환산액과 적용 환율을 바로 아래에 보여준다.

- **label**, **amount**, **currency**, **currencies**(기본 MNT·KRW·USD), **rate** `{value, base, date}`, **help**, **error**, **tag**, **size**.
- 입력한 원래 통화와 금액을 그대로 저장하고, 환산액은 거래 당시 환율로 따로 저장한다는 원칙을 화면에서 보여준다.
- 가이드 현장 비용 등록은 `size="lg"`를 쓴다.
