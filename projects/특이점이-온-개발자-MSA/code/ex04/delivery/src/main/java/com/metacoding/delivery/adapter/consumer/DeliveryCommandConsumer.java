package com.metacoding.delivery.adapter.consumer;

import com.metacoding.delivery.adapter.message.*;
import com.metacoding.delivery.adapter.producer.DeliveryEventProducer;
import com.metacoding.delivery.usecase.DeliveryService;
import lombok.RequiredArgsConstructor;
import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.stereotype.Component;

@Component
@RequiredArgsConstructor
public class DeliveryCommandConsumer {

    private final DeliveryService deliveryService;
    private final DeliveryEventProducer deliveryEventProducer;

    @KafkaListener(topics = "create-delivery-command", groupId = "delivery-service")
    public void createDeliveryCommand(CreateDeliveryCommand command) {
        boolean isSuccess = false;
        int deliveryId = 0;
        try {
            var response = deliveryService.createDelivery(command.orderId(), command.address());
            isSuccess = true;
            deliveryId = response.id();
        } catch (Exception e) {
            // 실패는 isSuccess=false로 이벤트 발행
        }
        deliveryEventProducer.publishDeliveryCreated(
                new DeliveryCreatedEvent(command.orderId(), deliveryId, isSuccess));
    }
}
