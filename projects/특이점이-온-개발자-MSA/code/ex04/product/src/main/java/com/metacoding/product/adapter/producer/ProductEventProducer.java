package com.metacoding.product.adapter.producer;

import com.metacoding.product.adapter.message.*;
import lombok.RequiredArgsConstructor;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.stereotype.Component;

@Component
@RequiredArgsConstructor
public class ProductEventProducer {
    private final KafkaTemplate<String, Object> kafkaTemplate;

    public void publishProductDecreased(ProductDecreasedEvent event) {
        kafkaTemplate.send("product-decreased", event);
    }
}
