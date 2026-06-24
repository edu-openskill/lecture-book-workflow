package com.metacoding.product.adapter.consumer;

import com.metacoding.product.adapter.message.*;
import com.metacoding.product.adapter.producer.ProductEventProducer;
import com.metacoding.product.usecase.ProductService;
import lombok.RequiredArgsConstructor;
import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.stereotype.Component;

@Component
@RequiredArgsConstructor
public class ProductCommandConsumer {

    private final ProductService productService;
    private final ProductEventProducer productEventProducer;

    @KafkaListener(topics = "decrease-product-command", groupId = "product-service")
    public void decreaseProductCommand(DecreaseProductCommand command) {
        boolean isSuccess = false;
        try {
            productService.decreaseQuantity(command.productId(), command.quantity(), command.price());
            isSuccess = true;
        } catch (Exception e) {
            // 실패는 isSuccess=false로 이벤트 발행
        }
        productEventProducer.publishProductDecreased(
                new ProductDecreasedEvent(command.orderId(), command.productId(), command.quantity(), isSuccess));
    }

    @KafkaListener(topics = "increase-product-command", groupId = "product-service")
    public void increaseProductCommand(IncreaseProductCommand command) {
        productService.increaseQuantity(command.productId(), command.quantity(), command.price());
    }
}
