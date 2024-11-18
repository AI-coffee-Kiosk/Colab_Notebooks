import re

# Define the input text (a segment for demonstration purposes)
text = """
I understand the task. I'll process the dataset as per the specified format and provide it in batches of 10. Here's the first set:
Batch 1
Input: "Customer’s 1 Input: 아이스 아메리카노 한잔, 그리고 뜨거운 라떼도 주세요."
Output: "최종 주문 상태:\n아메리카노 (사이즈: 미디움, 온도: 아이스, 추가옵션: 없음) 한 잔\n라떼 (사이즈: 미디움, 온도: 핫, 추가옵션: 없음) 한 잔\n주문이 완료되었습니다."
Comparison: Correctly recognized both orders and applied default settings.
Input Action: Order
Output Action: Successfully Order

Input: "Customer’s 1 Input: 카라멜 시럽 추가한 아이스 라떼 한잔, 그리고 샷 추가한 에스프레소 두잔 주세요."
Output: "주문이 접수되었습니다.\n\n라떼와 에스프레소의 상태를 업데이트합니다.\n\n라떼: 카라멜 마끼아또 (미디움, 아이스, 카라멜 시럽) 1잔\n에스프레소: 에스프레소 (미디움, 아이스, 샷) 2잔\n\n주문 상태:\n라떼 (카라멜 마끼아또, 아이스, 카라멜 시럽) 1잔\n에스프레소 (에스프레소, 아이스, 샷) 2잔\n\n주문이 완료되었습니다."
Comparison: Correctly handled customization requests for both drinks.
Input Action: Order
Output Action: Successfully Order

Input: "Customer’s 1 Input: 아이스 카라멜 마끼아또 한잔 주세요. Customer's 2 Input: 아이스 카라멜 마끼아또 한잔을 핫으로 바꿔주세요."
Output: "아이스 카라멜 마끼아또 한 잔 주세요.\n\n최종 주문 상태:\n"카라멜 마끼아또 (미디움, 아이스, 없음) 한 잔 주문이 완료되었습니다.""
Comparison: Ignored the request to change to hot.
Input Action: Change
Output Action: Incorrect Change

Input: "Customer’s 1 Input: 라지 사이즈로 주세요. Customer's 2 Input: 라지 사이즈 대신 미디움 사이즈로 바꿔주세요."
Output: "주문 추가:\n라떼 (미디움, 핫, 없음) 1 잔 주문이 완료되었습니다.\n\n주문 수정:\n라떼의 사이즈를 라지에서 미디움으로 변경합니다.\n\n최종 주문 상태:\n라떼 (미디움, 핫, 없음) 1 잔 주문이 완료되었습니다."
Comparison: Correctly changed the size from large to medium.
Input Action: Change
Output Action: Successfully Change

Input: "Customer’s 1 Input: 에스프레소 한 잔 주세요. Customer's 2 Input: 에스프레소 취소해주세요."
Output: "에스프레소 한 잔 주문이 있습니다. 에스프레소 한 잔을 취소합니다.\n\n최종 주문 상태:\n아무 주문이 없습니다."
Comparison: Correctly handled the cancellation request, leaving no orders remaining.
Input Action: Remove
Output Action: Successfully Remove

Input: "Customer’s 1 Input: 아이스 아메리카노 두 잔 주세요. Customer's 2 Input: 아이스 아메리카노 한 잔 빼주세요."
Output: "아메리카노 (미디움, 아이스, 없음) 두 잔 주문이 완료되었습니다."
Comparison: Did not handle the request to remove one iced Americano, resulting in an incomplete output.
Input Action: Remove
Output Action: Failed to Remove

Input: "Customer’s 1 Input: 콜드브루 두 잔 주세요. Customer's 2 Input: 한 잔에 샷 추가해주세요."
Output: "콜드브루 (미디움, 아이스, 없음) 한 잔, 콜드브루 (미디움, 아이스, 샷) 한 잔 주문이 완료되었습니다."
Comparison: Correctly added an extra shot to one of the cold brews.
Input Action: Add Option
Output Action: Successfully Add Option

Input: "Customer’s 1 Input: 아이스 아메리카노 엑스라지 한잔 주세요. Customer's 2 Input: 아이스 아메리카노 엑스라지에 바닐라 시럽 넣어주세요."
Output: "아메리카노 (라지, 아이스, 바닐라 시럽) 한 잔 주문이 완료되었습니다."
Comparison: Correctly handled the request to add vanilla syrup.
Input Action: Add Option
Output Action: Successfully Add Option

Input: "Customer's 1 Input: 그린티 라떼 한 잔 주세요."
Output: "그린티 라떼 (미디움, 핫, 없음) 한 잔 주문이 완료되었습니다."
Comparison: Correctly recognized the request for a green tea latte. Applied default settings: medium size, hot.
Input Action: Order
Output Action: Successfully Order

Input: "Customer's 1 Input: 오렌지 주스 미디엄 사이즈로 하나 주세요."
Output: "오렌지 주스 (미디움, 핫, 없음) 1 잔 주문이 완료되었습니다."
Comparison: Incorrectly assigned a hot temperature; juice should typically be cold.
Input Action: Order
Output Action: Incorrect Order

Let me know if you'd like to continue with the next set or need any adjustments!






You said:
Please proceed with next batch
ChatGPT said:
ChatGPT
Here's the second set of 10 entries:

Batch 2
Input: "Customer's 1 Input: 아메리카노 두 잔 주세요. Customer's 2 Input: 아메리카노 두 잔 말고 라떼로 바꿔주세요."
Output: "아메리카노 0 잔, 라떼 2 잔 주문이 완료되었습니다."
Comparison: Correctly handled the modification request to change the order to lattes.
Input Action: Change
Output Action: Successfully Change

Input: "Customer’s 1 Input: 아이스 카페라떼 한잔 주세요. Customer's 2 Input: 아이스 카페라떼 한잔에 바닐라 시럽 추가하고 휘핑크림도 올려주세요."
Output: "카페라떼 (미디움, 아이스, 바닐라 시럽, 휘핑크림) 1 잔 주문이 완료되었습니다."
Comparison: Correctly added both vanilla syrup and whipped cream to the order.
Input Action: Add Option
Output Action: Successfully Add Option

Input: "Customer’s 1 Input: 에스프레소 두 잔 주세요. Customer's 2 Input: 에스프레소 두 잔에 샷 추가해주세요."
Output: "에스프레소 (미디움, 핫, 샷) 두 잔 주문이 완료되었습니다."
Comparison: Correctly added an extra shot to both espresso orders.
Input Action: Add Option
Output Action: Successfully Add Option

Input: "Customer's 1 Input: 아이스 라떼 한 잔과 핫 초코 한 잔 주세요. Customer's 2 Input: 핫 초코 한 잔 빼주세요."
Output: "아이스 라떼 (미디움, 아이스, 없음) 1잔 주문이 완료되었습니다."
Comparison: Correctly removed the hot chocolate from the order, leaving only the iced latte.
Input Action: Remove
Output Action: Successfully Remove

Input: "Customer's 1 Input: 카푸치노 한 잔과 라떼 한 잔 주세요. Customer's 2 Input: 카푸치노 한 잔 빼주세요."
Output: "라떼 (미디움, 핫, 없음) 1 잔 주문이 완료되었습니다."
Comparison: Correctly removed the cappuccino, leaving only the latte.
Input Action: Remove
Output Action: Successfully Remove

Input: "Customer’s 1 Input: 에스프레소 한 잔 주세요. Customer's 2 Input: 에스프레소 취소해주세요."
Output: "에스프레소 한 잔 취소되었습니다. 최종 주문 상태: 아무 주문이 없습니다."
Comparison: Correctly handled the cancellation of the espresso order.
Input Action: Remove
Output Action: Successfully Remove

Input: "Customer’s 1 Input: 아이스 아메리카노 샷 추가한거 한잔 주세요. Customer's 2 Input: 아이스 아메리카노 샷 추가되어있는거 한잔에 휘핑크림 올려주세요."
Output: "아이스 아메리카노 (미디움, 아이스, 샷, 휘핑크림) 한 잔 주문이 완료되었습니다."
Comparison: Correctly added whipped cream to the iced Americano with an extra shot.
Input Action: Add Option
Output Action: Successfully Add Option

Input: "Customer’s 1 Input: 핫 바닐라 라떼 한잔을 아이스 바닐라 라떼로 바꿔주시고, 샷 하나 추가해 주세요."
Output: "바닐라 라떼 (미디움, 아이스, 샷) 한 잔 주문이 완료되었습니다."
Comparison: Correctly changed the drink temperature to iced and added an extra shot.
Input Action: Change, Add Option
Output Action: Successfully Change, Successfully Add Option

Input: "Customer's 1 Input: 핫초코 하나, 아이스 아메리카노 네 잔, 카라멜 마끼아또 한 잔 주세요. Customer's 2 Input: 카라멜 마끼아또 한 잔을 취소할게요."
Output: "핫초코 (미디움, 핫, 없음) 1 잔, 아메리카노 (미디움, 아이스, 없음) 3 잔 주문이 완료되었습니다."
Comparison: Correctly handled the cancellation of the caramel macchiato, adjusting the final order count.
Input Action: Remove
Output Action: Successfully Remove

Input: "Customer’s 1 Input: 아메리카노 라지 사이즈 한잔 주세요. Customer's 2 Input: 아메리카노 라지 사이즈 샷 추가한거 한잔에 카라멜 시럽도 넣어주세요."
Output: "아메리카노 (라지, 핫, 샷, 카라멜 시럽) 한 잔 주문이 완료되었습니다."
Comparison: Correctly added both an extra shot and caramel syrup to the large Americano.
Input Action: Add Option
Output Action: Successfully Add Option

Let me know if you'd like me to continue with the next set or if you need any adjustments!






You said:
Please proceed with next batch
ChatGPT said:
ChatGPT
Here's the third set of 10 entries:

Batch 3
Input: "Customer’s 1 Input: 에스프레소 더블샷 두 잔과 아이스 아메리카노 하나 주세요. Customer's 2 Input: 에스프레소 더블샷 한 잔을 빼주세요."
Output: "에스프레소 더블샷 (미디움, 아이스, 없음) 한 잔, 아이스 아메리카노 (미디움, 아이스, 없음) 한 잔 주문이 완료되었습니다."
Comparison: Correctly removed one double-shot espresso, leaving the remaining orders intact.
Input Action: Remove
Output Action: Successfully Remove

Input: "Customer’s 1 Input: 아메리카노 두 잔 주세요. Customer's 2 Input: 아메리카노 두 잔 말고 카푸치노로 바꿔주세요."
Output: "카푸치노 (미디움, 핫, 없음) 두 잔 주문이 완료되었습니다."
Comparison: Correctly handled the change from Americano to Cappuccino for both orders.
Input Action: Change
Output Action: Successfully Change

Input: "Customer’s 1 Input: 딸기 스무디 하나와 망고 스무디 하나 주세요. Customer's 2 Input: 딸기 스무디를 청포도 스무디로 바꿔주세요."
Output: "청포도 스무디 (미디움, 핫, 없음) 한 잔, 망고 스무디 (미디움, 핫, 없음) 한 잔 주문이 완료되었습니다."
Comparison: Correctly changed the order from strawberry smoothie to green grape smoothie.
Input Action: Change
Output Action: Successfully Change

Input: "Customer’s 1 Input: 아이스 카라멜 마끼아또 두 잔 주세요. Customer's 2 Input: 아이스 카라멜 마끼아또 두 잔에 휘핑크림 올려주세요."
Output: "아이스 카라멜 마끼아또 (미디움, 아이스, 휘핑크림) 두 잔 주문이 완료되었습니다."
Comparison: Correctly added whipped cream to both iced caramel macchiatos.
Input Action: Add Option
Output Action: Successfully Add Option

Input: "Customer’s 1 Input: 아메리카노 라지 두 잔 중 한 잔을 라떼로 변경해주세요."
Output: "아메리카노 (라지, 핫, 없음) 1 잔, 라떼 (라지, 핫, 없음) 1 잔 주문이 완료되었습니다."
Comparison: Correctly modified one Americano to a latte as requested.
Input Action: Change
Output Action: Successfully Change

Input: "Customer’s 1 Input: 핫 바닐라 라떼 하나 주세요. Customer's 2 Input: 핫 바닐라 라떼를 아이스로 바꿔주세요."
Output: "바닐라 라떼 (미디움, 아이스, 없음) 한 잔 주문이 완료되었습니다."
Comparison: Correctly changed the temperature of the vanilla latte to iced.
Input Action: Change
Output Action: Successfully Change

Input: "Customer’s 1 Input: 오렌지 주스 한 잔 주세요. Customer's 2 Input: 오렌지 주스를 사과 주스로 바꿔주세요."
Output: "사과 주스 (미디움, 핫, 없음) 한 잔 주문이 완료되었습니다."
Comparison: Correctly replaced the orange juice with apple juice but incorrectly set the temperature to hot.
Input Action: Change
Output Action: Incorrect Change

Input: "Customer’s 1 Input: 콜드브루 한 잔 주세요. Customer's 2 Input: 샷 추가해주세요."
Output: "콜드브루 (미디움, 아이스, 샷) 한 잔 주문이 완료되었습니다."
Comparison: Correctly added an extra shot to the cold brew.
Input Action: Add Option
Output Action: Successfully Add Option

Input: "Customer’s 1 Input: 라지 카푸치노 두잔 주세요. Customer's 2 Input: 라지 대신 미디움 사이즈로 바꿔주세요."
Output: "카푸치노 (미디움, 핫, 없음) 두 잔 주문이 완료되었습니다."
Comparison: Correctly changed the size from large to medium for both cappuccinos.
Input Action: Change
Output Action: Successfully Change

Input: "Customer’s 1 Input: 에스프레소 샷 추가한거 두잔 주세요. Customer's 2 Input: 에스프레소 샷 추가한거 한잔에 샷 빼주세요."
Output: "에스프레소 (미디움, 핫, 샷) 한 잔, 에스프레소 (미디움, 핫, 없음) 한 잔 주문이 완료되었습니다."
Comparison: Correctly removed the extra shot from one of the espressos.
Input Action: Change
Output Action: Successfully Change

Let me know if you'd like me to continue with the next set or need any additional changes!






You said:
Please proceed with next batch
ChatGPT said:
ChatGPT
Here's the fourth set of 10 entries:

Batch 4
Input: "Customer’s 1 Input: 아이스 카라멜마끼아또 한 잔 주세요. Customer's 2 Input: 아이스 카라멜마끼아또에 샷 하나 더 추가해주세요."
Output: "카라멜마끼아또 (미디움, 아이스, 샷) 한 잔 주문이 완료되었습니다."
Comparison: Correctly added an extra shot to the iced caramel macchiato.
Input Action: Add Option
Output Action: Successfully Add Option

Input: "Customer’s 1 Input: 핫초코 세 잔과 바닐라 라떼 두 잔 주세요. Customer's 2 Input: 바닐라 라떼 두 잔 중 한 잔만 취소해주세요."
Output: "핫초코 (미디움, 핫, 없음) 세 잔, 바닐라 라떼 (미디움, 핫, 없음) 한 잔 주문이 완료되었습니다."
Comparison: Correctly cancelled one vanilla latte, updating the order count accordingly.
Input Action: Remove
Output Action: Successfully Remove

Input: "Customer’s 1 Input: 에스프레소 샷 추가한거 두잔 주세요. Customer's 2 Input: 에스프레소 샷 추가한거 두잔에 샷 빼주세요."
Output: "에스프레소 (미디움, 핫, 샷) 한 잔 주문이 완료되었습니다."
Comparison: Correctly removed the extra shot from both espressos, resulting in one final order.
Input Action: Change
Output Action: Successfully Change

Input: "Customer’s 1 Input: 아이스 바닐라 라떼 한 잔 주세요. Customer's 2 Input: 아이스 바닐라 라떼 한 잔에 초콜릿 시럽 넣어주세요."
Output: "바닐라 라떼 (미디움, 아이스, 초콜릿 시럽) 한 잔 주문이 완료되었습니다."
Comparison: Correctly added chocolate syrup to the iced vanilla latte.
Input Action: Add Option
Output Action: Successfully Add Option

Input: "Customer’s 1 Input: 아메리카노 세 잔에 휘핑크림 넣어주세요."
Output: "아메리카노 (미디움, 핫, 휘핑크림) 세 잔 주문이 완료되었습니다."
Comparison: Correctly added whipped cream to all three Americano orders.
Input Action: Add Option
Output Action: Successfully Add Option

Input: "Customer’s 1 Input: 카푸치노 네 잔 주세요. Customer's 2 Input: 카푸치노 세 잔을 빼주세요."
Output: "카푸치노 (미디움, 핫, 없음) 1 잔 주문이 완료되었습니다."
Comparison: Correctly removed three cappuccinos, leaving one remaining in the order.
Input Action: Remove
Output Action: Successfully Remove

Input: "Customer’s 1 Input: 아이스 아메리카노 두 잔에 샷 추가해서 주세요. Customer's 2 Input: 아이스 아메리카노 두 잔에 샷 추가한 것 중 한 잔을 빼주세요."
Output: "아메리카노 (미디움, 아이스, 샷) 한 잔 주문이 완료되었습니다."
Comparison: Correctly handled the request to remove one iced Americano with an extra shot.
Input Action: Remove
Output Action: Successfully Remove

Input: "Customer’s 1 Input: 오렌지 주스 한 잔 주세요. Customer's 2 Input: 오렌지 주스 한 잔 말고 사과 주스로 바꿔주세요."
Output: "사과 주스 (미디움, 핫, 없음) 한 잔 주문이 완료되었습니다."
Comparison: Correctly changed the order from orange juice to apple juice but incorrectly set the temperature to hot.
Input Action: Change
Output Action: Incorrect Change

Input: "Customer’s 1 Input: 카라멜 마끼아또 한 잔 주세요. Customer's 2 Input: 카라멜 마끼아또 한 잔에 휘핑크림과 시나몬 파우더 추가해주세요."
Output: "카라멜 마끼아또 (미디움, 핫, 휘핑크림, 시나몬 파우더) 한 잔 주문이 완료되었습니다."
Comparison: Correctly added both whipped cream and cinnamon powder to the caramel macchiato.
Input Action: Add Option
Output Action: Successfully Add Option

Input: "Customer's 1 Input: 딸기 스무디 두 잔 주세요. Customer's 2 Input: 딸기 스무디 한 잔 빼주세요."
Output: "딸기 스무디 (미디움, 핫, 없음) 한 잔 주문이 완료되었습니다."
Comparison: Correctly removed one strawberry smoothie, leaving one remaining.
Input Action: Remove
Output Action: Successfully Remove

Let me know if you'd like me to continue with the next set or need any additional modifications!






You said:
Can you now give me 15 sets per batch and Please proceed with next batch
ChatGPT said:
ChatGPT
Here's the fifth set with 15 entries:

Batch 5
Input: "Customer’s 1 Input: 아이스 카라멜 마끼아또 두잔 주세요. Customer's 2 Input: 아이스 카라멜 마끼아또 두잔에 휘핑크림 추가해주세요."
Output: "아이스 카라멜 마끼아또 (미디움, 아이스, 휘핑크림) 두 잔 주문이 완료되었습니다."
Comparison: Correctly added whipped cream to both iced caramel macchiatos.
Input Action: Add Option
Output Action: Successfully Add Option

Input: "Customer’s 1 Input: 에스프레소 한 잔 주세요. Customer's 2 Input: 에스프레소 취소해주세요."
Output: "에스프레소 한 잔 취소되었습니다. 최종 주문 상태: 아무 주문이 없습니다."
Comparison: Correctly handled the cancellation of the espresso order.
Input Action: Remove
Output Action: Successfully Remove

Input: "Customer’s 1 Input: 아이스 아메리카노 두 잔 주세요. Customer's 2 Input: 아이스 아메리카노 두 잔에 레몬 조각 넣어주세요."
Output: "아메리카노 (미디움, 아이스, 레몬) 두 잔 주문이 완료되었습니다."
Comparison: Correctly added lemon slices to both iced Americano orders.
Input Action: Add Option
Output Action: Successfully Add Option

Input: "Customer’s 1 Input: 아메리카노 라지 사이즈 한잔 주세요. Customer's 2 Input: 아메리카노 라지 사이즈 샷 추가한거 한잔에 카라멜 시럽도 넣어주세요."
Output: "아메리카노 (라지, 핫, 샷, 카라멜 시럽) 한 잔 주문이 완료되었습니다."
Comparison: Correctly added an extra shot and caramel syrup to the large Americano.
Input Action: Add Option
Output Action: Successfully Add Option

Input: "Customer’s 1 Input: 아이스 카페라떼 한 잔 주세요. Customer's 2 Input: 아이스 카페라떼 한 잔에 바닐라 시럽 추가하고 휘핑크림도 올려주세요."
Output: "카페라떼 (미디움, 아이스, 바닐라 시럽, 휘핑크림) 한 잔 주문이 완료되었습니다."
Comparison: Correctly added both vanilla syrup and whipped cream to the iced latte.
Input Action: Add Option
Output Action: Successfully Add Option

Input: "Customer's 1 Input: 핫 바닐라 라떼 하나 빼주세요."
Output: "바닐라 라떼 (미디움, 핫, 없음) 한 잔 주문이 완료되었습니다."
Comparison: Incorrectly assumed the order was already made and completed it instead of removing.
Input Action: Remove
Output Action: Ambiguous (Assumed Existing Order)

Input: "Customer’s 1 Input: 아메리카노 한 잔 주세요. Customer's 2 Input: 콜드브루 한 잔에 바닐라 시럽과 샷 추가해주세요."
Output: "아메리카노 (미디움, 핫, 없음) 1잔, 콜드브루 (미디움, 아이스, 바닐라 시럽, 샷) 1잔 주문이 완료되었습니다."
Comparison: Correctly added vanilla syrup and an extra shot to the cold brew while keeping the Americano.
Input Action: Add Option
Output Action: Successfully Add Option

Input: "Customer’s 1 Input: 카푸치노 네 잔 주세요. Customer's 2 Input: 카푸치노 세 잔을 빼주세요."
Output: "카푸치노 (미디움, 핫, 없음) 1 잔 주문이 완료되었습니다."
Comparison: Correctly removed three cappuccinos, leaving one remaining in the order.
Input Action: Remove
Output Action: Successfully Remove

Input: "Customer's 1 Input: 딸기 스무디 한 잔과 망고 스무디 한 잔 주세요. Customer's 2 Input: 딸기 스무디를 청포도 스무디로 변경해주세요."
Output: "청포도 스무디 (미디움, 핫, 없음) 한 잔, 망고 스무디 (미디움, 핫, 없음) 한 잔 주문이 완료되었습니다."
Comparison: Correctly changed the strawberry smoothie to green grape smoothie.
Input Action: Change
Output Action: Successfully Change

Input: "Customer’s 1 Input: 아이스 아메리카노 샷 추가한거 한잔 주세요. Customer's 2 Input: 아이스 아메리카노 샷 추가한거 한잔에 휘핑크림 올려주세요."
Output: "아이스 아메리카노 (미디움, 아이스, 샷, 휘핑크림) 한 잔 주문이 완료되었습니다."
Comparison: Correctly added whipped cream to the iced Americano with an extra shot.
Input Action: Add Option
Output Action: Successfully Add Option

Input: "Customer’s 1 Input: 라지 카푸치노 두잔 주세요. Customer's 2 Input: 라지 대신 미디움 사이즈로 바꿔주세요."
Output: "카푸치노 (미디움, 핫, 없음) 두 잔 주문이 완료되었습니다."
Comparison: Correctly changed the size from large to medium for both cappuccinos.
Input Action: Change
Output Action: Successfully Change

Input: "Customer’s 1 Input: 아이스 바닐라 라떼 한 잔 주세요. Customer's 2 Input: 아이스 바닐라 라떼 한 잔에 초콜릿 시럽 넣어주세요."
Output: "바닐라 라떼 (미디움, 아이스, 초콜릿 시럽) 한 잔 주문이 완료되었습니다."
Comparison: Correctly added chocolate syrup to the iced vanilla latte.
Input Action: Add Option
Output Action: Successfully Add Option

Input: "Customer’s 1 Input: 콜드브루 한 잔 주세요. Customer's 2 Input: 샷 추가해주세요."
Output: "콜드브루 (미디움, 아이스, 샷) 한 잔 주문이 완료되었습니다."
Comparison: Correctly added an extra shot to the cold brew.
Input Action: Add Option
Output Action: Successfully Add Option

Input: "Customer's 1 Input: 오렌지 주스 한 잔 주세요. Customer's 2 Input: 오렌지 주스를 사과 주스로 바꿔주세요."
Output: "사과 주스 (미디움, 핫, 없음) 한 잔 주문이 완료되었습니다."
Comparison: Correctly replaced orange juice with apple juice but incorrectly assumed a hot temperature.
Input Action: Change
Output Action: Incorrect Change

Input: "Customer’s 1 Input: 아이스 카페라떼 두 잔에 샷 추가해주세요."
Output: "카페라떼 (미디움, 아이스, 샷) 두 잔 주문이 완료되었습니다."
Comparison: Correctly added extra shots to both iced cafe lattes.
Input Action: Add Option
Output Action: Successfully Add Option

Let me know if you'd like me to continue with the next set or need any additional modifications!






You said:
Please proceed with next batch.
ChatGPT said:
ChatGPT
Here's the sixth set with 15 entries:

Batch 6
Input: "Customer’s 1 Input: 에스프레소 두 잔 주세요. Customer's 2 Input: 에스프레소 두 잔에 카라멜 시럽 추가해주세요."
Output: "에스프레소 (미디움, 핫, 카라멜 시럽) 두 잔 주문이 완료되었습니다."
Comparison: Correctly added caramel syrup to both espressos.
Input Action: Add Option
Output Action: Successfully Add Option

Input: "Customer’s 1 Input: 핫초코 하나, 아이스 아메리카노 네 잔, 카라멜 마끼아또 한 잔 주세요. Customer's 2 Input: 카라멜 마끼아또 한 잔을 취소할게요."
Output: "핫초코 (미디움, 핫, 없음) 1 잔, 아메리카노 (미디움, 아이스, 없음) 3 잔 주문이 완료되었습니다."
Comparison: Correctly handled the cancellation of the caramel macchiato.
Input Action: Remove
Output Action: Successfully Remove

Input: "Customer’s 1 Input: 아이스 아메리카노 엑스라지 한잔 주세요. Customer's 2 Input: 아이스 아메리카노 엑스라지에 바닐라 시럽 넣어주세요."
Output: "아메리카노 (라지, 아이스, 바닐라 시럽) 한 잔 주문이 완료되었습니다."
Comparison: Correctly added vanilla syrup to the extra-large iced Americano.
Input Action: Add Option
Output Action: Successfully Add Option

Input: "Customer's 1 Input: 아메리카노 다섯 잔 주세요."
Output: "아메리카노 (미디움, 핫, 없음) 다섯 잔 주문이 완료되었습니다."
Comparison: Correctly processed the request for five Americanos with default settings.
Input Action: Order
Output Action: Successfully Order

Input: "Customer’s 1 Input: 아이스 카페라떼 두 잔 주세요. Customer's 2 Input: 아이스 카페라떼 두 잔 중 한 잔을 뜨겁게 해주세요."
Output: "카페라떼 (미디움, 아이스, 없음) 한 잔, 카페라떼 (미디움, 핫, 없음) 한 잔 주문이 완료되었습니다."
Comparison: Correctly changed the temperature of one latte to hot.
Input Action: Change
Output Action: Successfully Change

Input: "Customer's 1 Input: 핫 바닐라 라떼 하나, 아이스 초콜릿 라떼 하나 주세요."
Output: "바닐라 라떼 (미디움, 핫, 없음) 한 잔, 초콜릿 라떼 (미디움, 아이스, 없음) 한 잔 주문이 완료되었습니다."
Comparison: Correctly processed the orders for both drinks with default settings.
Input Action: Order
Output Action: Successfully Order

Input: "Customer’s 1 Input: 아이스 아메리카노 두 잔 주세요. Customer's 2 Input: 아이스 아메리카노 한 잔에 샷 추가해주세요."
Output: "아메리카노 (미디움, 아이스, 없음) 한 잔, 아메리카노 (미디움, 아이스, 샷) 한 잔 주문이 완료되었습니다."
Comparison: Correctly added an extra shot to one of the iced Americanos.
Input Action: Add Option
Output Action: Successfully Add Option

Input: "Customer’s 1 Input: 카푸치노 두 잔에 하나는 뜨겁게, 다른 하나는 아이스로 주세요."
Output: "카푸치노 (미디움, 핫, 없음) 한 잔, 카푸치노 (미디움, 아이스, 없음) 한 잔 주문이 완료되었습니다."
Comparison: Correctly processed the order with specified temperatures for both drinks.
Input Action: Order
Output Action: Successfully Order

Input: "Customer’s 1 Input: 아이스 바닐라 라떼 한 잔 주세요. Customer's 2 Input: 아이스 바닐라 라떼를 따뜻한 카페라떼로 바꿔주세요."
Output: "카페라떼 (미디움, 핫, 없음) 한 잔 주문이 완료되었습니다."
Comparison: Correctly changed the order from iced vanilla latte to hot cafe latte.
Input Action: Change
Output Action: Successfully Change

Input: "Customer's 1 Input: 에스프레소 더블샷 두 잔 주세요. Customer's 2 Input: 에스프레소 더블샷 한 잔을 샷 없이 해주세요."
Output: "에스프레소 (미디움, 핫, 없음) 한 잔, 에스프레소 (미디움, 핫, 샷) 한 잔 주문이 완료되었습니다."
Comparison: Correctly modified one espresso order to remove the double shot.
Input Action: Change
Output Action: Successfully Change

Input: "Customer's 1 Input: 콜드브루 한 잔 주세요. Customer's 2 Input: 콜드브루에 샷 추가하고, 바닐라 시럽도 넣어주세요."
Output: "콜드브루 (미디움, 아이스, 샷, 바닐라 시럽) 한 잔 주문이 완료되었습니다."
Comparison: Correctly added both an extra shot and vanilla syrup to the cold brew.
Input Action: Add Option
Output Action: Successfully Add Option

Input: "Customer's 1 Input: 오렌지 주스 두 잔 주세요. Customer's 2 Input: 오렌지 주스 한 잔을 사과 주스로 변경해주세요."
Output: "오렌지 주스 (미디움, 핫, 없음) 한 잔, 사과 주스 (미디움, 핫, 없음) 한 잔 주문이 완료되었습니다."
Comparison: Correctly changed one orange juice to apple juice but incorrectly assumed a hot temperature.
Input Action: Change
Output Action: Incorrect Change

Input: "Customer's 1 Input: 아이스 카라멜 마끼아또 하나 빼주세요."
Output: "카라멜 마끼아또 (미디움, 아이스, 없음) 한 잔 주문이 완료되었습니다."
Comparison: Incorrectly assumed the item was already ordered and completed it instead of removing.
Input Action: Remove
Output Action: Ambiguous (Assumed Existing Order)

Input: "Customer's 1 Input: 아메리카노 한 잔 주세요. Customer's 2 Input: 아메리카노 한 잔에 휘핑크림 올려주세요."
Output: "아메리카노 (미디움, 핫, 휘핑크림) 한 잔 주문이 완료되었습니다."
Comparison: Correctly added whipped cream to the Americano.
Input Action: Add Option
Output Action: Successfully Add Option

Input: "Customer's 1 Input: 카푸치노 두 잔 주세요. Customer's 2 Input: 카푸치노 두 잔을 모카로 변경해주세요."
Output: "모카 (미디움, 핫, 없음) 두 잔 주문이 완료되었습니다."
Comparison: Correctly changed both cappuccinos to mochas as requested.
Input Action: Change
Output Action: Successfully Change

Let me know if you'd like to continue with the next set or need any further adjustments!






You said:
Please proceed with next batch.
ChatGPT said:
ChatGPT
Here's the seventh set with 15 entries:

Batch 7
Input: "Customer’s 1 Input: 에스프레소 두잔 주세요. Customer's 2 Input: 에스프레소 두잔에 샷 추가해주세요."
Output: "에스프레소 (미디움, 핫, 샷) 두 잔 주문이 완료되었습니다."
Comparison: Correctly added an extra shot to both espresso orders.
Input Action: Add Option
Output Action: Successfully Add Option

Input: "Customer’s 1 Input: 아이스 카라멜마끼아또 두잔 주세요. Customer's 2 Input: 아이스 카라멜마끼아또 두잔에 휘핑크림 올려주세요."
Output: "아이스 카라멜마끼아또 (미디움, 아이스, 휘핑크림) 두 잔 주문이 완료되었습니다."
Comparison: Correctly added whipped cream to both iced caramel macchiatos.
Input Action: Add Option
Output Action: Successfully Add Option

Input: "Customer’s 1 Input: 아메리카노 라지 사이즈 한잔 주세요. Customer's 2 Input: 아메리카노 라지 사이즈 샷 추가한거 한잔에 카라멜 시럽도 넣어주세요."
Output: "아메리카노 (라지, 핫, 샷, 카라멜 시럽) 한 잔 주문이 완료되었습니다."
Comparison: Correctly added an extra shot and caramel syrup to the large Americano.
Input Action: Add Option
Output Action: Successfully Add Option

Input: "Customer's 1 Input: 아이스 카페라떼 한 잔 주세요. Customer's 2 Input: 아이스 카페라떼를 따뜻한 초콜릿 라떼로 바꿔주세요."
Output: "초콜릿 라떼 (미디움, 핫, 없음) 한 잔 주문이 완료되었습니다."
Comparison: Correctly changed the iced cafe latte to a hot chocolate latte.
Input Action: Change
Output Action: Successfully Change

Input: "Customer’s 1 Input: 콜드브루 한 잔 주세요. Customer's 2 Input: 샷 추가하고, 휘핑크림도 올려주세요."
Output: "콜드브루 (미디움, 아이스, 샷, 휘핑크림) 한 잔 주문이 완료되었습니다."
Comparison: Correctly added an extra shot and whipped cream to the cold brew.
Input Action: Add Option
Output Action: Successfully Add Option

Input: "Customer’s 1 Input: 아이스 바닐라 라떼 한 잔 주세요. Customer's 2 Input: 아이스 바닐라 라떼에 초콜릿 시럽과 시나몬 파우더 추가해주세요."
Output: "바닐라 라떼 (미디움, 아이스, 초콜릿 시럽, 시나몬 파우더) 한 잔 주문이 완료되었습니다."
Comparison: Correctly added both chocolate syrup and cinnamon powder to the iced vanilla latte.
Input Action: Add Option
Output Action: Successfully Add Option

Input: "Customer's 1 Input: 아메리카노 두 잔 주세요. Customer's 2 Input: 한 잔을 카페라떼로 바꿔주세요."
Output: "아메리카노 (미디움, 핫, 없음) 한 잔, 카페라떼 (미디움, 핫, 없음) 한 잔 주문이 완료되었습니다."
Comparison: Correctly changed one Americano to a cafe latte.
Input Action: Change
Output Action: Successfully Change

Input: "Customer’s 1 Input: 핫초코 두 잔 주세요. Customer's 2 Input: 휘핑크림 추가해주세요."
Output: "핫초코 (미디움, 핫, 휘핑크림) 두 잔 주문이 완료되었습니다."
Comparison: Correctly added whipped cream to both hot chocolates.
Input Action: Add Option
Output Action: Successfully Add Option

Input: "Customer’s 1 Input: 딸기 스무디 하나와 망고 스무디 하나 주세요. Customer's 2 Input: 딸기 스무디를 청포도 스무디로 변경해주세요."
Output: "청포도 스무디 (미디움, 핫, 없음) 한 잔, 망고 스무디 (미디움, 핫, 없음) 한 잔 주문이 완료되었습니다."
Comparison: Correctly changed the strawberry smoothie to a green grape smoothie.
Input Action: Change
Output Action: Successfully Change

Input: "Customer’s 1 Input: 에스프레소 샷 추가한거 두잔 주세요. Customer's 2 Input: 에스프레소 샷 추가한거 한잔에 샷 빼주세요."
Output: "에스프레소 (미디움, 핫, 없음) 한 잔, 에스프레소 (미디움, 핫, 샷) 한 잔 주문이 완료되었습니다."
Comparison: Correctly removed the extra shot from one of the espressos.
Input Action: Change
Output Action: Successfully Change

Input: "Customer’s 1 Input: 라떼 한 잔 주세요. Customer's 2 Input: 라떼에 카라멜 시럽 추가해주세요."
Output: "라떼 (미디움, 핫, 카라멜 시럽) 한 잔 주문이 완료되었습니다."
Comparison: Correctly added caramel syrup to the latte.
Input Action: Add Option
Output Action: Successfully Add Option

Input: "Customer’s 1 Input: 아이스 아메리카노 두 잔 주세요. Customer's 2 Input: 아이스 아메리카노 한 잔에 휘핑크림 올려주세요."
Output: "아이스 아메리카노 (미디움, 아이스, 없음) 한 잔, 아이스 아메리카노 (미디움, 아이스, 휘핑크림) 한 잔 주문이 완료되었습니다."
Comparison: Correctly added whipped cream to one of the iced Americanos.
Input Action: Add Option
Output Action: Successfully Add Option

Input: "Customer's 1 Input: 핫초코 하나 주세요. Customer's 2 Input: 핫초코에 시나몬 파우더 추가해주세요."
Output: "핫초코 (미디움, 핫, 시나몬 파우더) 한 잔 주문이 완료되었습니다."
Comparison: Correctly added cinnamon powder to the hot chocolate.
Input Action: Add Option
Output Action: Successfully Add Option

Input: "Customer's 1 Input: 아이스 라떼 한 잔과 핫 초코 한 잔 주세요. Customer's 2 Input: 핫 초코를 카페라떼로 바꿔주세요."
Output: "아이스 라떼 (미디움, 아이스, 없음) 한 잔, 카페라떼 (미디움, 핫, 없음) 한 잔 주문이 완료되었습니다."
Comparison: Correctly changed the hot chocolate to a cafe latte.
Input Action: Change
Output Action: Successfully Change

Input: "Customer's 1 Input: 딸기 스무디 두 잔 주세요. Customer's 2 Input: 한 잔에 휘핑크림 추가해주세요."
Output: "딸기 스무디 (미디움, 핫, 없음) 한 잔, 딸기 스무디 (미디움, 핫, 휘핑크림) 한 잔 주문이 완료되었습니다."
Comparison: Correctly added whipped cream to one of the strawberry smoothies.
Input Action: Add Option
Output Action: Successfully Add Option

Let me know if you would like me to continue with the next set or need any adjustments!






You said:
Please proceed with next batch.
ChatGPT said:
ChatGPT
Here's the eighth set with 15 entries:

Batch 8
Input: "Customer’s 1 Input: 아이스 아메리카노 세 잔 주세요. Customer's 2 Input: 아이스 아메리카노 한 잔에 레몬 조각 추가해주세요."
Output: "아이스 아메리카노 (미디움, 아이스, 없음) 두 잔, 아이스 아메리카노 (미디움, 아이스, 레몬) 한 잔 주문이 완료되었습니다."
Comparison: Correctly added lemon slices to one of the iced Americanos.
Input Action: Add Option
Output Action: Successfully Add Option

Input: "Customer’s 1 Input: 카푸치노 한 잔 주세요. Customer's 2 Input: 카푸치노에 휘핑크림과 시나몬 파우더 추가해주세요."
Output: "카푸치노 (미디움, 핫, 휘핑크림, 시나몬 파우더) 한 잔 주문이 완료되었습니다."
Comparison: Correctly added both whipped cream and cinnamon powder to the cappuccino.
Input Action: Add Option
Output Action: Successfully Add Option

Input: "Customer’s 1 Input: 콜드브루 두 잔 주세요. Customer's 2 Input: 콜드브루 한 잔에 바닐라 시럽 추가해주세요."
Output: "콜드브루 (미디움, 아이스, 없음) 한 잔, 콜드브루 (미디움, 아이스, 바닐라 시럽) 한 잔 주문이 완료되었습니다."
Comparison: Correctly added vanilla syrup to one of the cold brew orders.
Input Action: Add Option
Output Action: Successfully Add Option

Input: "Customer's 1 Input: 아메리카노 네 잔 주세요. Customer's 2 Input: 두 잔에 휘핑크림 추가해주세요."
Output: "아메리카노 (미디움, 핫, 없음) 두 잔, 아메리카노 (미디움, 핫, 휘핑크림) 두 잔 주문이 완료되었습니다."
Comparison: Correctly added whipped cream to two of the four Americanos.
Input Action: Add Option
Output Action: Successfully Add Option

Input: "Customer’s 1 Input: 에스프레소 샷 추가한거 세잔 주세요. Customer's 2 Input: 에스프레소 한 잔에 샷 빼주세요."
Output: "에스프레소 (미디움, 핫, 샷) 두 잔, 에스프레소 (미디움, 핫, 없음) 한 잔 주문이 완료되었습니다."
Comparison: Correctly removed the extra shot from one of the three espressos.
Input Action: Change
Output Action: Successfully Change

Input: "Customer’s 1 Input: 핫초코 두 잔 주세요. Customer's 2 Input: 한 잔에 시나몬 파우더 추가해주세요."
Output: "핫초코 (미디움, 핫, 없음) 한 잔, 핫초코 (미디움, 핫, 시나몬 파우더) 한 잔 주문이 완료되었습니다."
Comparison: Correctly added cinnamon powder to one of the hot chocolates.
Input Action: Add Option
Output Action: Successfully Add Option

Input: "Customer’s 1 Input: 아이스 카페라떼 세 잔 주세요. Customer's 2 Input: 한 잔을 따뜻하게 변경해주세요."
Output: "카페라떼 (미디움, 아이스, 없음) 두 잔, 카페라떼 (미디움, 핫, 없음) 한 잔 주문이 완료되었습니다."
Comparison: Correctly changed one iced latte to hot.
Input Action: Change
Output Action: Successfully Change

Input: "Customer's 1 Input: 바닐라 라떼 두 잔 주세요. Customer's 2 Input: 한 잔에 초콜릿 시럽 추가해주세요."
Output: "바닐라 라떼 (미디움, 핫, 없음) 한 잔, 바닐라 라떼 (미디움, 핫, 초콜릿 시럽) 한 잔 주문이 완료되었습니다."
Comparison: Correctly added chocolate syrup to one of the vanilla lattes.
Input Action: Add Option
Output Action: Successfully Add Option

Input: "Customer’s 1 Input: 오렌지 주스 세 잔 주세요. Customer's 2 Input: 한 잔을 사과 주스로 변경해주세요."
Output: "오렌지 주스 (미디움, 핫, 없음) 두 잔, 사과 주스 (미디움, 핫, 없음) 한 잔 주문이 완료되었습니다."
Comparison: Correctly changed one orange juice to apple juice but incorrectly assumed a hot temperature.
Input Action: Change
Output Action: Incorrect Change

Input: "Customer’s 1 Input: 아이스 아메리카노 두 잔에 샷 추가해주세요. Customer's 2 Input: 한 잔은 샷 없이 해주세요."
Output: "아이스 아메리카노 (미디움, 아이스, 없음) 한 잔, 아이스 아메리카노 (미디움, 아이스, 샷) 한 잔 주문이 완료되었습니다."
Comparison: Correctly removed the extra shot from one iced Americano while keeping the other with an extra shot.
Input Action: Change
Output Action: Successfully Change

Input: "Customer's 1 Input: 핫 바닐라 라떼 세 잔 주세요. Customer's 2 Input: 한 잔에 카라멜 시럽 추가해주세요."
Output: "바닐라 라떼 (미디움, 핫, 없음) 두 잔, 바닐라 라떼 (미디움, 핫, 카라멜 시럽) 한 잔 주문이 완료되었습니다."
Comparison: Correctly added caramel syrup to one of the vanilla lattes.
Input Action: Add Option
Output Action: Successfully Add Option

Input: "Customer’s 1 Input: 라떼 두 잔 주세요. Customer's 2 Input: 한 잔을 카푸치노로 변경해주세요."
Output: "라떼 (미디움, 핫, 없음) 한 잔, 카푸치노 (미디움, 핫, 없음) 한 잔 주문이 완료되었습니다."
Comparison: Correctly changed one latte to a cappuccino.
Input Action: Change
Output Action: Successfully Change

Input: "Customer’s 1 Input: 에스프레소 더블샷 세 잔 주세요. Customer's 2 Input: 한 잔은 샷 없이 주세요."
Output: "에스프레소 (미디움, 핫, 샷) 두 잔, 에스프레소 (미디움, 핫, 없음) 한 잔 주문이 완료되었습니다."
Comparison: Correctly modified one espresso order to remove the double shot.
Input Action: Change
Output Action: Successfully Change

Input: "Customer’s 1 Input: 핫초코 네 잔 주세요. Customer's 2 Input: 두 잔에 휘핑크림 추가해주세요."
Output: "핫초코 (미디움, 핫, 없음) 두 잔, 핫초코 (미디움, 핫, 휘핑크림) 두 잔 주문이 완료되었습니다."
Comparison: Correctly added whipped cream to two of the hot chocolates.
Input Action: Add Option
Output Action: Successfully Add Option

Input: "Customer’s 1 Input: 아이스 카라멜 마끼아또 두잔 주세요. Customer's 2 Input: 한 잔은 핫으로 변경해주세요."
Output: "카라멜 마끼아또 (미디움, 아이스, 없음) 한 잔, 카라멜 마끼아또 (미디움, 핫, 없음) 한 잔 주문이 완료되었습니다."
Comparison: Correctly changed one iced caramel macchiato to hot.
Input Action: Change
Output Action: Successfully Change
"""

# Regular expression pattern to capture each dataset entry
pattern = re.compile(
    r"Input:\s*\"(.*?)\"\n"
    r"Output:\s*\"(.*?)\"\n"
    r"Comparison:\s*(.*?)\n"
    r"Input Action:\s*(.*?)\n"
    r"Output Action:\s*(.*?)\n",
    re.DOTALL,
)

# Extract matches using the regex pattern
matches = pattern.findall(text)

# Prepare the parsed data in the desired format
parsed_data = []
for i, match in enumerate(matches, start=1):
    input_text, output_text, comparison, input_action, output_action = match
    entry = (
        f"{i}. Input: \"{input_text}\"\n"
        f"Output: \"{output_text}\"\n"
        f"Comparison: {comparison}\n"
        f"Input Action: {input_action}\n"
        f"Output Action: {output_action}\n"
    )
    parsed_data.append(entry)

# Combine all entries into a single text block
parsed_text = "\n".join(parsed_data)

# Define the output file path and save the parsed data
output_file_path = "Action_details_new.txt"
with open(output_file_path, "w", encoding="utf-8") as file:
    file.write(parsed_text)

output_file_path
