package com.metacoding.orchestrator.handler;

import com.metacoding.orchestrator.message.*;
import lombok.*;
import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.stereotype.Component;

import java.util.*;
import java.util.concurrent.ConcurrentHashMap;

@Component
@RequiredArgsConstructor
public class OrderOrchestrator {

    private final KafkaTemplate<String, Object> kafkaTemplate;
    private final Map<Integer, WorkflowState> states = new ConcurrentHashMap<>();

    // 주문 생성 이벤트 수신 → 재고 차감 명령 발행
    @KafkaListener(topics = "order-created", groupId = "orchestrator")
    public void orderCreated(OrderCreatedEvent event) {
        int orderId = event.orderId();
        // 주문 상태 저장
        states.put(orderId, new WorkflowState(orderId, event.address(),
                event.productId(), event.quantity(), event.price()));

        // 재고 차감 명령 발행
        kafkaTemplate.send(
                "decrease-product-command",
                String.valueOf(orderId),
                new DecreaseProductCommand(orderId, event.productId(), event.quantity(), event.price())
        );
    }

    // 재고 차감 결과 수신 → 성공 시 배달 생성
    @KafkaListener(topics = "product-decreased", groupId = "orchestrator")
    public void productDecreased(ProductDecreasedEvent event) {
        int orderId = event.orderId();
        // 주문 상태 조회
        WorkflowState state = states.get(orderId);
        // 주문 상태 없으면 종료
        if (state == null) return;

        // 실패 시: 주문 취소
        if (!event.isSuccess()) {
            kafkaTemplate.send(
                    "cancel-order-command",
                    String.valueOf(orderId),
                    new CancelOrderCommand(orderId)
            );
            states.remove(orderId);
            return;
        }

        // 성공 시: 배달 생성
        kafkaTemplate.send(
                "create-delivery-command",
                String.valueOf(orderId),
                new CreateDeliveryCommand(orderId, state.getAddress())
        );
    }

    // 배달 생성 결과 수신 → 성공 시 주문 완료
    @KafkaListener(topics = "delivery-created", groupId = "orchestrator")
    public void deliveryCreated(DeliveryCreatedEvent event) {
        int orderId = event.orderId();
        WorkflowState state = states.get(orderId);
        if (state == null) return;

        // 배달 생성 실패 시 재고 복구
        if (!event.isSuccess()) {
            kafkaTemplate.send(
                    "increase-product-command",
                    String.valueOf(orderId),
                    new IncreaseProductCommand(orderId, state.getProductId(), state.getQuantity(), state.getPrice())
            );
            // 실패 시 주문 취소
            kafkaTemplate.send(
                    "cancel-order-command",
                    String.valueOf(orderId),
                    new CancelOrderCommand(orderId)
            );
            states.remove(orderId);
            return;
        }
        // 주문 완료 명령 발행
        kafkaTemplate.send(
                "complete-order-command",
                String.valueOf(orderId),
                new CompleteOrderCommand(orderId)
        );
        states.remove(orderId);
    }

    @Data
    private static class WorkflowState {
        private final int orderId;
        private final String address;
        private final int productId;
        private final int quantity;
        private final Long price;
    }
}
